def steer(pos_goal, pos_now, d_max):
    """Moves towards pos_goal up to maximum distance d_max."""

    # Compute distance between pos_now and pos_goal.
    distance = ...  # *YOUR CODE HERE*
    if distance > d_max:
        # Compute x_new.
        x_new = ...  # *YOUR CODE HERE*
    else:
        x_new = pos_goal
    return x_new
