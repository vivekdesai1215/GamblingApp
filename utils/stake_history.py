from repositories.stake_transaction_repo import get_stake_transactions_by_session


def print_stake_history(session_id):
    transactions = get_stake_transactions_by_session(session_id)

    print("\n📊 STAKE HISTORY")
    print("---------------------------")

    for t in transactions:
        print(
            t["transaction_type"],
            "| Amount:", t["amount"],
            "| Balance:", t["balance_after"]
        )