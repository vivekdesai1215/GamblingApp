class BettingPreferences:
    def __init__(
        self,
        gambler_id,
        min_bet,
        max_bet,
        preferred_game_type,
        auto_play_enabled=False,
        auto_play_max_games=None,
        session_loss_limit=None,
        session_win_target=None
    ):
        self.gambler_id = gambler_id
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.preferred_game_type = preferred_game_type

        self.auto_play_enabled = auto_play_enabled
        self.auto_play_max_games = auto_play_max_games

        self.session_loss_limit = session_loss_limit
        self.session_win_target = session_win_target