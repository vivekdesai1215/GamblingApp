from strategies.base_strategy import BettingStrategy


class PercentageStrategy(BettingStrategy):
    def __init__(self, percent):
        self.percent = percent

    def get_bet_amount(self, current_stake):
        return (self.percent / 100) * current_stake