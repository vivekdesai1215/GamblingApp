from config.db_config import get_connection


def create_session(session, conn=None):
    close_conn = False

    if not conn:
        conn = get_connection()
        close_conn = True

    cursor = conn.cursor()

    query = """
    INSERT INTO sessions (
        gambler_id,
        starting_stake,
        peak_stake,
        lowest_stake,
        games_played,
        max_games,
        status,
        created_at,
        started_at
    )
    VALUES (%s, %s, %s, %s, %s, %s, 'ACTIVE', NOW(), NOW())
    """

    values = (
        session.gambler_id,
        session.starting_stake,
        session.starting_stake,  # initial peak
        session.starting_stake,  # initial lowest
        0,
        session.max_games
    )

    cursor.execute(query, values)

    session_id = cursor.lastrowid

    if close_conn:
        conn.commit()
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