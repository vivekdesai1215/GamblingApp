from config.db_config import get_connection

def print_session_summary(session_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # session data
    cursor.execute("SELECT * FROM sessions WHERE session_id = %s", (session_id,))
    session = cursor.fetchone()

    # bet stats
    cursor.execute("""
        SELECT 
            COUNT(*) as total_bets,
            SUM(CASE WHEN result='WIN' THEN 1 ELSE 0 END) as wins,
            SUM(CASE WHEN result='LOSS' THEN 1 ELSE 0 END) as losses
        FROM bets
        WHERE session_id = %s
    """, (session_id,))

    stats = cursor.fetchone()

    profit = float(session["ending_stake"] or 0) - float(session["starting_stake"])

    print("\n📊 SESSION SUMMARY")
    print("-------------------------")
    print("Games Played:", session["games_played"])
    print("Wins:", stats["wins"])
    print("Losses:", stats["losses"])
    print("Profit/Loss:", profit)
    print("Peak Stake:", session["peak_stake"])
    print("Lowest Stake:", session["lowest_stake"])

    cursor.close()
    conn.close()