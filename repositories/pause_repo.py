from config.db_config import get_connection


def create_pause_record(session_id, reason="USER"):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pause_records (session_id, paused_at, reason)
        VALUES (%s, NOW(), %s)
    """, (session_id, reason))

    conn.commit()
    cursor.close()
    conn.close()


def close_pause_record(session_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE pause_records
        SET resumed_at = NOW()
        WHERE session_id = %s AND resumed_at IS NULL
    """, (session_id,))

    conn.commit()
    cursor.close()
    conn.close()