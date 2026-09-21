import random


# ============================================================
# MAZE GENERATOR
# ============================================================

def generate_maze(rows, cols):
    """
    Generate a random maze using
    Recursive Backtracking / DFS.

    Returns:
        List of strings representing the maze.
    """

    # --------------------------------------------------------
    # Make dimensions odd
    # --------------------------------------------------------

    if rows % 2 == 0:
        rows -= 1

    if cols % 2 == 0:
        cols -= 1

    # Minimum valid maze size
    if rows < 5:
        rows = 5

    if cols < 5:
        cols = 5

    # --------------------------------------------------------
    # Create grid filled with walls
    # --------------------------------------------------------

    grid = [
        ["#" for _ in range(cols)]
        for _ in range(rows)
    ]

    # --------------------------------------------------------
    # Start position
    # --------------------------------------------------------

    start = (1, 1)

    grid[start[0]][start[1]] = "."

    # --------------------------------------------------------
    # DFS stack
    # --------------------------------------------------------

    stack = [start]

    # --------------------------------------------------------
    # Directions
    #
    # We move two cells at a time so that the
    # cell between them can become a passage.
    # --------------------------------------------------------

    directions = [
        (-2, 0),   # Up
        (2, 0),    # Down
        (0, -2),   # Left
        (0, 2)     # Right
    ]

    # --------------------------------------------------------
    # Maze generation
    # --------------------------------------------------------

    while stack:

        current_row, current_col = stack[-1]

        # Find unvisited neighbors
        neighbors = []

        for dr, dc in directions:

            new_row = current_row + dr
            new_col = current_col + dc

            if (
                1 <= new_row < rows - 1
                and
                1 <= new_col < cols - 1
                and
                grid[new_row][new_col] == "#"
            ):
                neighbors.append(
                    (new_row, new_col, dr, dc)
                )

        # ----------------------------------------------------
        # If there are available neighbors
        # ----------------------------------------------------

        if neighbors:

            new_row, new_col, dr, dc = random.choice(
                neighbors
            )

            # Open wall between current cell
            # and selected neighbor

            wall_row = current_row + dr // 2
            wall_col = current_col + dc // 2

            grid[wall_row][wall_col] = "."

            # Open selected cell

            grid[new_row][new_col] = "."

            # Push new cell onto stack

            stack.append(
                (new_row, new_col)
            )

        # ----------------------------------------------------
        # No neighbors -> backtrack
        # ----------------------------------------------------

        else:

            stack.pop()

    # --------------------------------------------------------
    # Start and Goal
    # --------------------------------------------------------

    start = (1, 1)

    goal = (
        rows - 2,
        cols - 2
    )

    grid[start[0]][start[1]] = "S"

    grid[goal[0]][goal[1]] = "G"

    # --------------------------------------------------------
    # Convert grid to list of strings
    # --------------------------------------------------------

    maze_result = [
        "".join(row)
        for row in grid
    ]

    return maze_result


# ============================================================
# TEST GENERATOR
# ============================================================

if __name__ == "__main__":

    test_maze = generate_maze(
        9,
        15
    )

    print()

    for row in test_maze:
        print(row)

    print()