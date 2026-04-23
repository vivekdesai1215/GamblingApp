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