from config.db_config import get_connection


def insert_stake_transaction(
    gambler_id,
    session_id,
    bet_id,
    transaction_type,
    amount,
    balance_before,
    balance_after,
    conn=None
):
    close_conn = False

    if conn is None:
        conn = get_connection()
        close_conn = True

    cursor = conn.cursor()

    query = """
        INSERT INTO stake_transactions (
            gambler_id,
            session_id,
            bet_id,
            transaction_type,
            amount,
            balance_before,
            balance_after
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        gambler_id,
        session_id,
        bet_id,
        transaction_type,
        amount,
        balance_before,
        balance_after
    )

    cursor.execute(query, values)

    if close_conn:
        conn.commit()
        cursor.close()
        conn.close()

def get_stake_transactions_by_session(session_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT * FROM stake_transactions
        WHERE session_id = %s
        ORDER BY created_at
    """

    cursor.execute(query, (session_id,))
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result