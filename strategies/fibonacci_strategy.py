from strategies.base_strategy import BettingStrategy


class FibonacciStrategy(BettingStrategy):
    def __init__(self, base_amount):
        self.base_amount = base_amount
        self.sequence = [1, 1]
        self.index = 0

    def get_bet_amount(self, current_stake):
        return self.base_amount * self.sequence[self.index]

    def update_after_result(self, result):
        if result == "LOSS":
            self.index += 1
            if self.index >= len(self.sequence):
                self.sequence.append(
                    self.sequence[-1] + self.sequence[-2]
                )
        else:
            self.index = max(0, self.index - 2)