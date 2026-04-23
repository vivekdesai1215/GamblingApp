from models.gambler import Gambler
from repositories.gambler_repo import insert_gambler, get_gambler_by_username
from utils.validators import validate_gambler_data


def create_gambler(data):
    # Step 1: Convert dict → object
    gambler = Gambler(
        username=data["username"],
        email=data["email"],
        full_name=data.get("full_name"),
        initial_stake=data["initial_stake"],
        win_threshold=data.get("win_threshold"),
        loss_threshold=data.get("loss_threshold"),
        min_required_stake=data.get("min_required_stake", 0)
    )
    print("Reached Service Layer")
    # Step 2: Validate
    validate_gambler_data(gambler)

    # Step 3: Check duplicates
    existing = get_gambler_by_username(gambler.username)
    if existing:
        raise ValueError("Username already exists")

    # Step 4: Save
    insert_gambler(gambler)

    print("✅ Gambler created successfully")



def get_gambler_profile(username):
    gambler = get_gambler_by_username(username)

    if not gambler:
        print("❌ Gambler not found")
        return None

    return gambler