class Gambler:
    def __init__(
        self,
        username,
        email,
        initial_stake,
        full_name=None,
        win_threshold=None,
        loss_threshold=None,
        min_required_stake=0
    ):
        self.username = username
        self.email = email
        self.full_name = full_name
        self.is_active = True

        self.initial_stake = initial_stake
        self.current_stake = initial_stake

        self.win_threshold = win_threshold
        self.loss_threshold = loss_threshold
        self.min_required_stake = min_required_stake