from config.db_config import get_connection


def insert_gambler(g):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO gamblers
    (username, full_name, email, is_active,
     initial_stake, current_stake,
     win_threshold, loss_threshold, min_required_stake)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        g.username,
        g.full_name,
        g.email,
        g.is_active,
        g.initial_stake,
        g.current_stake,
        g.win_threshold,
        g.loss_threshold,
        g.min_required_stake
    )

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()


def get_gambler_by_username(username):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM gamblers WHERE username = %s"
    cursor.execute(query, (username,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


def get_gambler_by_username(username):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM gamblers WHERE username = %s"
    cursor.execute(query, (username,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


def update_gambler_stake(gambler_id, new_stake):
    conn = get_connection()
    cursor = conn.cursor()

    query = "UPDATE gamblers SET current_stake = %s WHERE gambler_id = %s"
    cursor.execute(query, (new_stake, gambler_id))
    conn.commit()

    cursor.close()
    conn.close()

def get_gambler_by_id(gambler_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM gamblers WHERE gambler_id = %s"
    cursor.execute(query, (gambler_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return result