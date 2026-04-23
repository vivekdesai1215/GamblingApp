from services.gambler_service import create_gambler, get_gambler_profile
from services.betting_preferences_service import create_preferences
from services.session_service import start_session
from services.bet_service import place_bet
from strategies.fixed_strategy import FixedAmountStrategy
from utils.stake_history import print_stake_history

# NEW
from services.run_session_with_strategy import run_session_with_strategy

# from strategies. import FixedAmountStrategy
from strategies.percentage_strategy import PercentageStrategy
from strategies.martingale_strategy import MartingaleStrategy
from strategies.reverse_martingale_strategy import ReverseMartingaleStrategy
from strategies.fibonacci_strategy import FibonacciStrategy
from strategies.dalembert_strategy import DAlembertStrategy


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
    mode = input("\nChoose mode (1 = manual, 2 = strategy): ")

    # =============================
    # MANUAL MODE
    # =============================
    if mode == "1":
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

            except Exception as e:
                print("Error:", e)
                break

        # ✅ print once
        print_stake_history(session_id)

    # =============================
    # STRATEGY MODE
    # =============================
    else:
        print("\nChoose Strategy:")
        print("1. Fixed")
        print("2. Percentage")
        print("3. Martingale")
        print("4. Reverse Martingale")
        print("5. Fibonacci")
        print("6. D'Alembert")

        choice = input("Enter choice: ")

        if choice == "1":
            amt = float(input("Enter fixed amount: "))
            strategy = FixedAmountStrategy(amt)

        elif choice == "2":
            percent = float(input("Enter percentage: "))
            strategy = PercentageStrategy(percent)

        elif choice == "3":
            base = float(input("Enter base amount: "))
            strategy = MartingaleStrategy(base)

        elif choice == "4":
            base = float(input("Enter base amount: "))
            strategy = ReverseMartingaleStrategy(base)

        elif choice == "5":
            base = float(input("Enter base amount: "))
            strategy = FibonacciStrategy(base)

        elif choice == "6":
            base = float(input("Enter base amount: "))
            strategy = DAlembertStrategy(base)

        else:
            print("Invalid choice")
            return

        # run strategy session
        run_session_with_strategy(gambler_id, strategy)

        # print history after session
        print_stake_history(session_id)


if __name__ == "__main__":
    main()