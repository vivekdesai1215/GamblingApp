class WinLossStats:
    def __init__(self):
        self.wins = 0
        self.losses = 0

        self.total_win_amount = 0
        self.total_loss_amount = 0

        self.current_win_streak = 0
        self.current_loss_streak = 0

        self.max_win_streak = 0
        self.max_loss_streak = 0

    def update(self, result, payout):
        if result == "WIN":
            self.wins += 1
            self.total_win_amount += payout

            self.current_win_streak += 1
            self.current_loss_streak = 0

            self.max_win_streak = max(self.max_win_streak, self.current_win_streak)

        else:
            self.losses += 1
            self.total_loss_amount += abs(payout)

            self.current_loss_streak += 1
            self.current_win_streak = 0

            self.max_loss_streak = max(self.max_loss_streak, self.current_loss_streak)

    def get_summary(self):
        total_games = self.wins + self.losses
        win_rate = (self.wins / total_games * 100) if total_games > 0 else 0

        net_profit = self.total_win_amount - self.total_loss_amount

        return {
            "games": total_games,
            "wins": self.wins,
            "losses": self.losses,
            "win_rate": round(win_rate, 2),
            "net_profit": net_profit,
            "max_win_streak": self.max_win_streak,
            "max_loss_streak": self.max_loss_streak
        }