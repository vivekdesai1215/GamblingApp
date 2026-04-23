from config.db_config import get_connection

def insert_bet(session_id, gambler_id, amount, result, payout):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO bets (session_id, gambler_id, bet_amount, result, payout)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, (session_id, gambler_id, amount, result, payout))
    conn.commit()

    cursor.close()
    conn.close()