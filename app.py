from services.gambler_service import create_gambler, get_gambler_profile
from services.betting_preferences_service import create_preferences
from services.session_service import start_session
from services.session_runner import run_session
from services.bet_service import place_bet
from utils.stake_history import print_stake_history


def main():
    print("🎰 Welcome to Gambling App\n")

    # -----------------------------
    # USER INPUT
    # -----------------------------
    username = input("Enter username: ")
    email = input("Enter email: ")
    full_name = input("Enter full name: ")
    initial_stake = float(input("Enter initial stake: "))

    min_bet = float(input("Min bet: "))
    max_bet = float(input("Max bet: "))
    max_games = int(input("Max games: "))
    loss_limit = float(input("Session loss limit: "))
    win_target = float(input("Session win target: "))

    # -----------------------------
    # CREATE GAMBLER
    # -----------------------------
    gambler_data = {
        "username": username,
        "email": email,
        "full_name": full_name,
        "initial_stake": initial_stake,
        "win_threshold": initial_stake * 2,
        "loss_threshold": initial_stake / 2,
        "min_required_stake": min_bet
    }

    create_gambler(gambler_data)

    gambler = get_gambler_profile(username)
    gambler_id = gambler["gambler_id"]

    # -----------------------------
    # CREATE PREFERENCES
    # -----------------------------
    preferences_data = {
        "gambler_id": gambler_id,
        "min_bet": min_bet,
        "max_bet": max_bet,
        "preferred_game_type": "roulette",
        "auto_play_enabled": True,
        "auto_play_max_games": max_games,
        "session_loss_limit": loss_limit,
        "session_win_target": win_target
    }

    create_preferences(preferences_data)

    # -----------------------------
    # START SESSION
    # -----------------------------
    session_id = start_session(
        gambler_id=gambler_id,
        current_stake=gambler["current_stake"],
        max_games=max_games
    )

    # -----------------------------
    # MODE SELECTION
    # -----------------------------
    mode = input("\nChoose mode (1 = manual, 2 = auto): ")

    if mode == "1":
        # Manual mode
        while True:
            try:
                bet = float(input("Enter bet amount (or 0 to exit): "))

                if bet == 0:
                    print("Exiting manual mode")
                    break

                status = place_bet(gambler_id, bet)

                if status == "STOP":
                    print("Session ended")
                    break
                print_stake_history(session_id)
            except Exception as e:
                print("Error:", e)
                break
        print_stake_history(session_id)
            
    else:
        # Auto-play
        bet_amount = float(input("Enter fixed bet amount: "))
        run_session(gambler_id, bet_amount)


if __name__ == "__main__":
    main()