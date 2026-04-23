from strategies.base_strategy import BettingStrategy


class ReverseMartingaleStrategy(BettingStrategy):
    def __init__(self, base_amount):
        self.base_amount = base_amount
        self.current_bet = base_amount

    def get_bet_amount(self, current_stake):
        return self.current_bet

    def update_after_result(self, result):
        if result == "WIN":
            self.current_bet *= 2
        else:
            self.current_bet = self.base_amount