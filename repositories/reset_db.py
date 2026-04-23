from config.db_config import get_connection

def reset_db(session_id, preference_id, username):
    conn = get_connection()
    cursor = conn.cursor()

    print("🔄 Resetting DB...")

    try:
        # 1. Delete sessions
        cursor.execute(
            "DELETE FROM sessions WHERE session_id = %s",
            (session_id,)
        )
        print("✅ Deleted session")

        # 2. Delete preferences
        cursor.execute(
            "DELETE FROM betting_preferences WHERE preference_id = %s",
            (preference_id,)
        )
        print("✅ Deleted preferences")

        # 3. Delete gambler
        cursor.execute(
            "DELETE FROM gamblers WHERE username = %s",
            (username,)
        )
        print("✅ Deleted gambler")

        conn.commit()

    except Exception as e:
        print("❌ Reset failed:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()