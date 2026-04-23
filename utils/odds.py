class FixedOdds:
    def __init__(self, multiplier=2.0):
        self.multiplier = multiplier

    def calculate_payout(self, amount):
        return amount * self.multiplier


class ProbabilityBasedOdds:
    def __init__(self, win_probability):
        if win_probability <= 0 or win_probability >= 1:
            raise ValueError("Probability must be between 0 and 1")
        self.win_probability = win_probability

    def calculate_payout(self, amount):
        odds = 1 / self.win_probability
        return amount * odds