from services.bet_service import place_bet
from repositories.gambler_repo import get_gambler_by_id
from repositories.session_repo import get_active_session
from utils.stake_history import print_stake_history


def run_session(gambler_id, bet_amount):
    print("\n🎮 Starting Auto-Play Session\n")

    session = get_active_session(gambler_id)
    session_id = session["session_id"]

    while True:
        try:
            status = place_bet(gambler_id, bet_amount)

            if status == "STOP":
                print("\n🛑 Session Ended\n")
                break

        except Exception as e:
            print("⚠️ Error during session:", e)
            break

    # ✅ ADD HERE
    print_stake_history(session_id)

def print_summary(gambler_id):
    gambler = get_gambler_by_id(gambler_id)
    session = get_active_session(gambler_id)

    print("📊 SESSION SUMMARY")
    print("----------------------")
    print("Final Stake:", gambler["current_stake"])

    if session:
        print("Status:", session["status"])