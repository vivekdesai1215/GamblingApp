from models.betting_preferences import BettingPreferences
from repositories.betting_preferences_repo import insert_preferences


def create_preferences(data):
    preferences = BettingPreferences(
        gambler_id=data["gambler_id"],
        min_bet=data["min_bet"],
        max_bet=data["max_bet"],
        preferred_game_type=data["preferred_game_type"],
        auto_play_enabled=data.get("auto_play_enabled", False),
        auto_play_max_games=data.get("auto_play_max_games"),
        session_loss_limit=data.get("session_loss_limit"),
        session_win_target=data.get("session_win_target")
    )

    # Basic validation
    if preferences.min_bet <= 0:
        raise ValueError("Min bet must be positive")

    if preferences.max_bet < preferences.min_bet:
        raise ValueError("Max bet must be >= min bet")

    insert_preferences(preferences)

    print("✅ Preferences created")