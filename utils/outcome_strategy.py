import random

class RandomOutcomeStrategy:
    def determine_outcome(self):
        return "WIN" if random.random() < 0.5 else "LOSS"


class WeightedOutcomeStrategy:
    def __init__(self, win_probability=0.5):
        self.win_probability = win_probability

    def determine_outcome(self):
        return "WIN" if random.random() < self.win_probability else "LOSS"