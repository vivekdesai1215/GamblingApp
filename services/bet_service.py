import random
from config.db_config import get_connection

from repositories.stake_transaction_repo import insert_stake_transaction
from utils.transation_type import TransactionType


def place_bet(gambler_id, amount,outcome_strategy,odds_strategy):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        conn.start_transaction()

        # 1. Fetch gambler
        cursor.execute(
            "SELECT * FROM gamblers WHERE gambler_id = %s FOR UPDATE",
            (gambler_id,)
        )
        gambler = cursor.fetchone()
        if not gambler:
            raise ValueError("Gambler not found")

        current_stake = float(gambler["current_stake"])

        # 2. Fetch session
        cursor.execute(
            "SELECT * FROM sessions WHERE gambler_id = %s AND status = 'ACTIVE' FOR UPDATE",
            (gambler_id,)
        )
        session = cursor.fetchone()
        if not session:
            raise ValueError("No active session")

        # 3. Fetch preferences
        cursor.execute(
            "SELECT * FROM betting_preferences WHERE gambler_id = %s",
            (gambler_id,)
        )
        prefs = cursor.fetchone()

        # 4. Validation
        if amount > current_stake:
            raise ValueError("Insufficient balance")

        if amount < float(prefs["min_bet"]) or amount > float(prefs["max_bet"]):
            raise ValueError("Invalid bet amount")

        #Outcome
        result = outcome_strategy.determine_outcome()

        if result=="WIN":
            payout = odds_strategy.calculate_payout(amount)
            new_stake = current_stake + payout
            transaction_type = TransactionType.BET_WIN
            result = "WIN"
        else:
            payout = -amount
            new_stake = current_stake + payout
            result = "LOSS"
            transaction_type = TransactionType.BET_LOSS

        balance_before = current_stake
        balance_after = new_stake

        # 6. Update gambler
        cursor.execute(
            "UPDATE gamblers SET current_stake = %s WHERE gambler_id = %s",
            (new_stake, gambler_id)
        )

        # 7. Insert bet
        cursor.execute("""
            INSERT INTO bets (session_id, gambler_id, bet_amount, result, payout)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            session["session_id"], gambler_id, amount, result, payout
        ))

        bet_id = cursor.lastrowid  # ✅ IMPORTANT

        # 8. Insert stake transaction (NEW)
        insert_stake_transaction(
            gambler_id=gambler_id,
            session_id=session["session_id"],
            bet_id=bet_id,
            transaction_type=transaction_type,
            amount=amount,
            balance_before=balance_before,
            balance_after=balance_after,
            conn=conn  # use same transaction
        )

        # 9. Update session
        peak = max(float(session["peak_stake"]), new_stake)
        lowest = min(float(session["lowest_stake"]), new_stake)
        games_played = session["games_played"] + 1

        cursor.execute("""
            UPDATE sessions
            SET games_played = %s,
                peak_stake = %s,
                lowest_stake = %s
            WHERE session_id = %s
        """, (games_played, peak, lowest, session["session_id"]))

        # 10. Stop conditions
        starting_stake = float(session["starting_stake"])
        profit = new_stake - starting_stake
        loss = starting_stake - new_stake

        stop_reason = None

        if session["max_games"] and games_played >= session["max_games"]:
            stop_reason = "MAX_GAMES"

        elif prefs["session_loss_limit"] and loss >= float(prefs["session_loss_limit"]):
            stop_reason = "LOSS_LIMIT"

        elif prefs["session_win_target"] and profit >= float(prefs["session_win_target"]):
            stop_reason = "WIN_TARGET"

        # 11. End session if needed
        if stop_reason:
            cursor.execute("""
                UPDATE sessions
                SET status = 'COMPLETED',
                    ending_stake = %s,
                    end_reason = %s,
                    ended_at = NOW()
                WHERE session_id = %s
            """, (new_stake, stop_reason, session["session_id"]))

        conn.commit()

        print(f"🎲 {result} | Stake: {new_stake}")

        return {
            "result": result,
            "payout": payout,
            "new_stake": new_stake,
            "stop": bool(stop_reason)
        }

    except Exception as e:
        conn.rollback()
        print("❌ Bet failed:", e)
        raise

    finally:
        cursor.close()
        conn.close()