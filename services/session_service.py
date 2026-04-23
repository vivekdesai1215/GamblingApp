# from models.session import Session
from models.sessions import Session
from repositories.session_repo import create_session, get_active_session


def start_session(gambler_id, current_stake, max_games=None):
    # Check if already active
    existing = get_active_session(gambler_id)
    if existing:
        raise ValueError("Active session already exists")

    session = Session(
        gambler_id=gambler_id,
        starting_stake=current_stake,
        max_games=max_games
    )

    session_id = create_session(session)

    print(f"✅ Session started: {session_id}")
    return session_id

from repositories.session_repo import update_session


def update_session_after_bet(session, current_stake):
    peak = session["peak_stake"]
    lowest = session["lowest_stake"]

    if current_stake > peak:
        peak = current_stake

    if current_stake < lowest:
        lowest = current_stake

    update_session(
        session["session_id"],
        current_stake,
        peak,
        lowest
    )

from repositories.session_repo import end_session as end_session_repo


def close_session(session_id, ending_stake, reason):
    end_session_repo(session_id, ending_stake, reason)
    print("✅ Session closed")