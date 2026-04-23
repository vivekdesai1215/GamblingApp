from config.db_config import get_connection

def insert_preferences(p):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO betting_preferences
    (gambler_id, min_bet, max_bet, preferred_game_type,
     auto_play_enabled, auto_play_max_games,
     session_loss_limit, session_win_target)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        p.gambler_id,
        p.min_bet,
        p.max_bet,
        p.preferred_game_type,
        p.auto_play_enabled,
        p.auto_play_max_games,
        p.session_loss_limit,
        p.session_win_target
    )

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()


def get_preferences_by_gambler_id(gambler_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM betting_preferences WHERE gambler_id = %s"
    cursor.execute(query, (gambler_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result