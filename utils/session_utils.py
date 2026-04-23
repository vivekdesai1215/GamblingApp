def get_session_duration(session):
    if not session["ended_at"]:
        return None

    duration = session["ended_at"] - session["started_at"]
    return duration.total_seconds()


from config.db_config import get_connection

def get_total_pause_time(session_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(TIMESTAMPDIFF(SECOND, paused_at, resumed_at))
        FROM pause_records
        WHERE session_id = %s AND resumed_at IS NOT NULL
    """, (session_id,))

    result = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return result or 0