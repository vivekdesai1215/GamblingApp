from services.bet_service import place_bet
from repositories.gambler_repo import get_gambler_by_id


def run_session_with_strategy(gambler_id, strategy, session_id):
    while True:
        # always fetch latest stake
        gambler = get_gambler_by_id(gambler_id)
        current_stake = float(gambler["current_stake"])

        amount = strategy.get_bet_amount(current_stake)

        try:
            status = place_bet(gambler_id, amount)
        except ValueError as e:
            print("⛔ Strategy stopped:", e)
            break

        result = status["result"]

        strategy.update_after_result(result)

        if status["stop"]:
            break