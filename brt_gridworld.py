"""Problem 3: inevitable backward-reachable tube (BRT) in a 10x10 grid world.

Standalone version of the course Colab notebook. It contains the two functions
that the problem asks for (`get_successors` and `calculate_inevitable_brt`),
the notebook's driver and visualisation code (saving figures to ./figures
instead of calling plt.show()), and the file-export cell that writes each
submitted function to its own .py file for inclusion in the LaTeX write-up.

Run:  python3 brt_gridworld.py
"""
import inspect
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(HERE, "figures")


# ----------------------------------------------------------------------------
# Functions asked for by the problem (exported to their own .py files below).
# ----------------------------------------------------------------------------
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


# ----------------------------------------------------------------------------
# Visualisation (from the notebook; plt.show() replaced by savefig).
# ----------------------------------------------------------------------------
def _setup_axes(ax, grid_size, title):
    ax.set_title(title)
    ax.set_xticks(range(grid_size + 1))
    ax.set_yticks(range(grid_size + 1))
    ax.grid(True)
    ax.set_xlim(0, grid_size)
    ax.set_ylim(0, grid_size)
    ax.set_aspect("equal")


def visualize_world(grid_size, obstacle_1, obstacle_2, fname):
    """Generates and displays the grid world with only the obstacles."""
    fig, ax = plt.subplots(figsize=(6, 6))
    _setup_axes(ax, grid_size, "Grid World with Obstacles")
    for i, obs in enumerate(obstacle_1):
        ax.add_patch(patches.Rectangle(obs, 1, 1, facecolor="lightblue",
                                       label="Obstacle 1" if i == 0 else ""))
    for i, obs in enumerate(obstacle_2):
        ax.add_patch(patches.Rectangle(obs, 1, 1, facecolor="lightgreen",
                                       label="Obstacle 2" if i == 0 else ""))
    ax.legend()
    fig.savefig(fname, dpi=200, bbox_inches="tight")
    plt.close(fig)


def visualize_single_set(title, grid_size, obstacles, inevitable_set, fname):
    """Visualizes a single inevitable set on its own plot."""
    fig, ax = plt.subplots(figsize=(6, 6))
    _setup_axes(ax, grid_size, title)
    for cell in (inevitable_set - obstacles):
        ax.add_patch(patches.Rectangle(cell, 1, 1, facecolor="#ffcccb"))
    for obs in obstacles:
        ax.add_patch(patches.Rectangle(obs, 1, 1, facecolor="red"))
    legend_patches = [
        patches.Patch(color="red", label="Obstacle(s)"),
        patches.Patch(color="#ffcccb", label="Inevitable BRT"),
    ]
    ax.legend(handles=legend_patches)
    fig.savefig(fname, dpi=200, bbox_inches="tight")
    plt.close(fig)


def visualize_union_vs_combined(grid_size, obstacles, union_set, combined_set, fname):
    """Combined-obstacle BRT, highlighting cells absent from the union of the
    two single-obstacle BRTs."""
    fig, ax = plt.subplots(figsize=(6, 6))
    _setup_axes(ax, grid_size, "Combined BRT vs. union of individual BRTs")
    for cell in (union_set - obstacles):
        ax.add_patch(patches.Rectangle(cell, 1, 1, facecolor="#ffcccb"))
    for cell in (combined_set - union_set):
        ax.add_patch(patches.Rectangle(cell, 1, 1, facecolor="#ff8c00"))
    for obs in obstacles:
        ax.add_patch(patches.Rectangle(obs, 1, 1, facecolor="red"))
    legend_patches = [
        patches.Patch(color="red", label="Obstacle(s)"),
        patches.Patch(color="#ffcccb", label="In union of individual BRTs"),
        patches.Patch(color="#ff8c00", label="Only in combined BRT"),
    ]
    ax.legend(handles=legend_patches)
    fig.savefig(fname, dpi=200, bbox_inches="tight")
    plt.close(fig)


# ----------------------------------------------------------------------------
# Main execution (mirrors the notebook's driver).
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    os.makedirs(FIG_DIR, exist_ok=True)
    GRID_SIZE = 10
    OBSTACLE_1 = {(x, 5) for x in range(2, 5)}  # 3-unit obstacle
    OBSTACLE_2 = {(x, 5) for x in range(5, 7)}  # 2-unit obstacle

    visualize_world(GRID_SIZE, OBSTACLE_1, OBSTACLE_2,
                    os.path.join(FIG_DIR, "world.png"))

    set_1 = calculate_inevitable_brt(OBSTACLE_1, GRID_SIZE)
    visualize_single_set("Inevitable BRT for Obstacle 1 Only", GRID_SIZE,
                         OBSTACLE_1, set_1, os.path.join(FIG_DIR, "brt_obstacle1.png"))

    set_2 = calculate_inevitable_brt(OBSTACLE_2, GRID_SIZE)
    visualize_single_set("Inevitable BRT for Obstacle 2 Only", GRID_SIZE,
                         OBSTACLE_2, set_2, os.path.join(FIG_DIR, "brt_obstacle2.png"))

    all_obs = OBSTACLE_1.union(OBSTACLE_2)
    combined_set = calculate_inevitable_brt(all_obs, GRID_SIZE)
    visualize_single_set("Inevitable BRT for Combined Obstacles", GRID_SIZE,
                         all_obs, combined_set, os.path.join(FIG_DIR, "brt_combined.png"))

    union_set = set_1 | set_2
    visualize_union_vs_combined(GRID_SIZE, all_obs, union_set, combined_set,
                                os.path.join(FIG_DIR, "brt_union_vs_combined.png"))

    print("BRT(obstacle 1) \\ obstacle 1 :", sorted(set_1 - OBSTACLE_1))
    print("BRT(obstacle 2) \\ obstacle 2 :", sorted(set_2 - OBSTACLE_2))
    print("BRT(combined)   \\ obstacles  :", sorted(combined_set - all_obs))
    print("union of individual BRTs \\ obstacles:", sorted(union_set - all_obs))
    print("combined minus union:", sorted(combined_set - union_set))
    assert union_set <= combined_set

    # ---- Export the requested functions to their own .py files. ----
    SUBMIT = ["get_successors", "calculate_inevitable_brt"]
    for name in SUBMIT:
        fn = globals().get(name)
        if fn is not None:
            with open(os.path.join(HERE, f"{name}.py"), "w") as f:
                f.write(inspect.getsource(fn))
    print("wrote", ", ".join(f"{n}.py" for n in SUBMIT))
