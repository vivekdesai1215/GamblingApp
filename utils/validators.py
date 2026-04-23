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