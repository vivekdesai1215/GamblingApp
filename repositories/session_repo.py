from config.db_config import get_connection


def create_session(session):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO sessions (
        gambler_id, status, starting_stake,
        peak_stake, lowest_stake,
        max_games, games_played,
        total_pause_seconds, started_at
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        session.gambler_id,
        session.status,
        session.starting_stake,
        session.peak_stake,
        session.lowest_stake,
        session.max_games,
        session.games_played,
        session.total_pause_seconds,
        session.started_at
    )

    cursor.execute(query, values)
    conn.commit()

    session_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return session_id

def get_active_session(gambler_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT * FROM sessions
    WHERE gambler_id = %s AND status = 'ACTIVE'
    LIMIT 1
    """

    cursor.execute(query, (gambler_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result

def update_session(session_id, current_stake, peak_stake, lowest_stake):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE sessions
    SET games_played = games_played + 1,
        peak_stake = %s,
        lowest_stake = %s
    WHERE session_id = %s
    """

    cursor.execute(query, (peak_stake, lowest_stake, session_id))
    conn.commit()

    cursor.close()
    conn.close()

def end_session(session_id, ending_stake, end_reason):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE sessions
    SET status = 'COMPLETED',
        ending_stake = %s,
        end_reason = %s,
        ended_at = NOW()
    WHERE session_id = %s
    """

    cursor.execute(query, (ending_stake, end_reason, session_id))
    conn.commit()

    cursor.close()
    conn.close()