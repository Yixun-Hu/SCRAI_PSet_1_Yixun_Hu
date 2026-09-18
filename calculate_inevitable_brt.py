def calculate_inevitable_brt(obstacles, grid_size):
    """Calculates the set of states from which eventual collision is unavoidable."""
    inevitable_brt = set(obstacles)
    while True:
        newly_added_states = set()
        max_obs_y = max(y for x, y in obstacles) if obstacles else -1
        # check all cells below this y-level
        # ensure that for any given cell that you check, all successors must
        # hit the obstacles (otherwise there is an escape route and a collision
        # is not inevitable)
        for y in range(max_obs_y):          # rows y = 0, ..., max_obs_y - 1
            for x in range(grid_size):
                cell = (x, y)
                if cell in inevitable_brt:
                    continue
                successors = get_successors(cell, grid_size)
                # Every admissible control leads into the current tube, i.e.
                # there is no escape route, so collision is inevitable.
                if successors and all(s in inevitable_brt for s in successors):
                    newly_added_states.add(cell)
        if not newly_added_states:
            break                           # fixed point reached
        inevitable_brt |= newly_added_states

    # Your brt should be a set of tuples. Each tuple is a (x,y) coordinate pair.
    return inevitable_brt
