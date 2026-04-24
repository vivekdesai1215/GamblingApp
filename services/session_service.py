from models.sessions import Session
from repositories.session_repo import create_session, get_active_session
from repositories.stake_transaction_repo import insert_stake_transaction
from utils.transation_type import TransactionType
from config.db_config import get_connection


def start_session(gambler_id, current_stake, max_games=None):

    # 1. Check active session
    existing = get_active_session(gambler_id)
    if existing:
        raise ValueError("Active session already exists")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        conn.start_transaction()

        # 2. Create session
        session = Session(
            gambler_id=gambler_id,
            starting_stake=current_stake,
            max_games=max_games
        )

        session_id = create_session(session, conn=conn)  # pass conn


        # 3. Insert INITIAL stake transaction
        insert_stake_transaction(
            gambler_id=gambler_id,
            session_id=session_id,
            bet_id=None,
            transaction_type=TransactionType.INITIAL,
            amount=current_stake,
            balance_before=0,
            balance_after=current_stake,
            conn=conn
        )

        conn.commit()

        print(f"✅ Session started: {session_id}")
        return session_id

    except Exception as e:
        conn.rollback()
        print("❌ Session start failed:", e)
        raise

    finally:
        cursor.close()
        conn.close()


from repositories.pause_repo import create_pause_record
from config.db_config import get_connection


def pause_session(session_id, reason="USER"):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT status FROM sessions WHERE session_id = %s", (session_id,))
    session = cursor.fetchone()

    if not session:
        print("Session not found")
        return

    if session["status"] == "PAUSED":
        print("Already paused")
        return

    cursor.execute("""
        UPDATE sessions
        SET status = 'PAUSED'
        WHERE session_id = %s
    """, (session_id,))

    conn.commit()
    cursor.close()
    conn.close()

    create_pause_record(session_id, reason)

    print("⏸ Session paused")



from repositories.pause_repo import close_pause_record
from config.db_config import get_connection

def resume_session(session_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT status FROM sessions WHERE session_id = %s", (session_id,))
    session = cursor.fetchone()

    if not session:
        print("Session not found")
        return

    if session["status"] != "PAUSED":
        print("Session is not paused")
        return

    cursor.execute("""
        UPDATE sessions
        SET status = 'ACTIVE'
        WHERE session_id = %s
    """, (session_id,))

    conn.commit()
    cursor.close()
    conn.close()
    close_pause_record(session_id)
    print("▶️ Session resumed")


from repositories.session_repo import end_session as end_session_repo
from repositories.gambler_repo import get_gambler_by_id


def close_session(session_id, gambler_id=None):

    ending_stake = None

    if gambler_id:
        gambler = get_gambler_by_id(gambler_id)
        if gambler:
            ending_stake = float(gambler["current_stake"])

    end_session_repo(session_id, ending_stake, "MANUAL")

    print("🛑 Session closed manually")