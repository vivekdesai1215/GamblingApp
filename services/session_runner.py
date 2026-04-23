from services.bet_service import place_bet
from repositories.gambler_repo import get_gambler_by_id
from repositories.session_repo import get_active_session


def run_session(gambler_id, bet_amount):
    print("\n🎮 Starting Auto-Play Session\n")

    while True:
        try:
            status = place_bet(gambler_id, bet_amount)

            if status == "STOP":
                print("\n🛑 Session Ended\n")
                break

        except Exception as e:
            print("⚠️ Error during session:", e)
            break

    # Print summary
    print_summary(gambler_id)

def print_summary(gambler_id):
    gambler = get_gambler_by_id(gambler_id)
    session = get_active_session(gambler_id)

    print("📊 SESSION SUMMARY")
    print("----------------------")
    print("Final Stake:", gambler["current_stake"])

    if session:
        print("Status:", session["status"])