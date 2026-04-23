from datetime import datetime

class Session:
    def __init__(self, gambler_id, starting_stake, max_games=None):
        self.gambler_id = gambler_id
        self.status = "ACTIVE"
        self.end_reason = None

        self.starting_stake = starting_stake
        self.ending_stake = None

        self.peak_stake = starting_stake
        self.lowest_stake = starting_stake

        self.max_games = max_games
        self.games_played = 0
        self.total_pause_seconds = 0

        self.started_at = datetime.now()
        self.ended_at = None