class BettingStrategy:
    def get_bet_amount(self, current_stake):
        raise NotImplementedError

    def update_after_result(self, result):
        pass  # optional