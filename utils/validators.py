def validate_gambler_data(g):
    if not g.username:
        raise ValueError("Username is required")

    if not g.email or "@" not in g.email:
        raise ValueError("Invalid email")

    if g.initial_stake < 100:
        raise ValueError("Initial stake must be at least 100")

    if g.win_threshold and g.win_threshold <= g.initial_stake:
        raise ValueError("Win threshold must be greater than initial stake")

    if g.loss_threshold and g.loss_threshold >= g.initial_stake:
        raise ValueError("Loss threshold must be less than initial stake")

    if g.min_required_stake < 0:
        raise ValueError("Minimum stake cannot be negative")


def validate_bet_amount(amount, current_stake, min_bet, max_bet):
    if amount <= 0:
        raise ValueError("Bet amount must be greater than 0")

    if amount > current_stake:
        raise ValueError("Bet amount cannot exceed current stake")

    if amount < min_bet:
        raise ValueError(f"Bet amount must be at least {min_bet}")

    if amount > max_bet:
        raise ValueError(f"Bet amount cannot exceed max bet limit {max_bet}")


def validate_probability(probability):
    if probability <= 0 or probability >= 1:
        raise ValueError("Probability must be between 0 and 1")


def validate_limits(lower_limit, upper_limit):
    if lower_limit <= 0:
        raise ValueError("Lower limit must be greater than 0")

    if upper_limit <= 0:
        raise ValueError("Upper limit must be greater than 0")

    if upper_limit <= lower_limit:
        raise ValueError("Upper limit must be greater than lower limit")


def validate_positive_number(value, field_name):
    if value <= 0:
        raise ValueError(f"{field_name} must be greater than 0")