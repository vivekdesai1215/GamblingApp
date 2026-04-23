from services.bet_service import place_bet


def run_session_with_strategy(gambler_id, strategy):
    while True:
        amount = strategy.get_bet_amount(1000)  # or fetch current stake

        try:
            status = place_bet(gambler_id, amount)
        except ValueError as e:
            print("⛔ Strategy stopped:", e)
            break
        # You need result → small change in place_bet()
        result = status["result"]

        strategy.update_after_result(result)

        if status["stop"]:
            break
