# ============================================================
# MAZE CONFIGURATION
# ============================================================

CELL_SIZE = 40


# ============================================================
# MAZE
# ============================================================

maze = [
    "###############",
    "#S....#.......#",
    "#.#.#.#.#####.#",
    "#.#.#.........#",
    "#.#.#########.#",
    "#.............#",
    "#######.#######",
    "#............G#",
    "###############"
]


# ============================================================
# FIND START AND GOAL
# ============================================================

def find_positions(maze):

    start = None
    goal = None

    for row in range(len(maze)):

        for col in range(len(maze[row])):

            if maze[row][col] == "S":
                start = (row, col)

            elif maze[row][col] == "G":
                goal = (row, col)

    return start, goal


# ============================================================
# GET VALID NEIGHBORS
# ============================================================

def get_neighbors(position, maze):

    row, col = position

    directions = [
        (-1, 0),   # Up
        (1, 0),    # Down
        (0, -1),   # Left
        (0, 1)     # Right
    ]

    neighbors = []

    for dr, dc in directions:

        new_row = row + dr
        new_col = col + dc

        if (
            0 <= new_row < len(maze)
            and 0 <= new_col < len(maze[0])
        ):

            if maze[new_row][new_col] != "#":

                neighbors.append(
                    (new_row, new_col)
                )

    return neighbors