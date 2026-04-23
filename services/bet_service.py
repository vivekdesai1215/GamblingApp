import random
from config.db_config import get_connection

from repositories.gambler_repo import get_gambler_by_id
from repositories.session_repo import get_active_session
from repositories.betting_preferences_repo import get_preferences_by_gambler_id


def place_bet(gambler_id, amount):
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

        # 5. Outcome
        is_win = random.choice([True, False])

        if is_win:
            payout = amount
            new_stake = current_stake + payout
            result = "WIN"
        else:
            payout = -amount
            new_stake = current_stake + payout
            result = "LOSS"

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

        # 8. Update session
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

        # 9. Stop conditions
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

        # 10. End session if needed
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

        return "STOP" if stop_reason else "CONTINUE"

    except Exception as e:
        conn.rollback()
        print("❌ Bet failed:", e)
        raise

    finally:
        cursor.close()
        conn.close()