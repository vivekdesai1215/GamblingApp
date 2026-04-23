from strategies.base_strategy import BettingStrategy


class DAlembertStrategy(BettingStrategy):
    def __init__(self, base_amount, step=1):
        self.base_amount = base_amount
        self.current_units = 1
        self.step = step

    def get_bet_amount(self, current_stake):
        return self.base_amount * self.current_units

    def update_after_result(self, result):
        if result == "LOSS":
            self.current_units += self.step
        else:
            self.current_units = max(1, self.current_units - self.step)