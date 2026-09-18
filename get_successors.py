def get_successors(cell, grid_size):
    """Calculates the three successor states based on the forward dynamics."""
    x, y = cell
    successors = []
    # Dynamics: y_{t+1} = y_t + 1 and x_{t+1} = x_t + u_t with u_t in {-1, 0, 1}.
    # A move that would leave the grid is not admissible, so a cell on the
    # left/right border has only two successors (this never matters for the
    # obstacle layout in this problem, since the BRT stays away from the walls).
    for u in (-1, 0, 1):
        x_next, y_next = x + u, y + 1
        if 0 <= x_next < grid_size and 0 <= y_next < grid_size:
            successors.append((x_next, y_next))
    # successors is a list of tuples. each tuple is a (x,y) coordinate pair.
    return successors
