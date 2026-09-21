# ============================================================
# ITERATIVE DEEPENING SEARCH (IDS)
# ============================================================

def depth_limited_search(
    current,
    goal,
    maze,
    get_neighbors,
    depth,
    path,
    explored
):
    """
    Depth-Limited DFS used by IDS.
    """

    explored.append(current)

    # Goal test
    if current == goal:
        return True

    # Depth limit reached
    if depth == 0:
        return False

    # Explore neighbors
    for neighbor in get_neighbors(current, maze):

        # Avoid cycles in the current path
        if neighbor not in path:

            path.append(neighbor)

            found = depth_limited_search(
                neighbor,
                goal,
                maze,
                get_neighbors,
                depth - 1,
                path,
                explored
            )

            if found:
                return True

            # Backtrack
            path.pop()

    return False


def ids(start, goal, maze, get_neighbors):

    explored = []

    # Start with depth limit 0
    depth_limit = 0

    while True:

        path = [start]

        print(
            "IDS searching with depth limit:",
            depth_limit
        )

        found = depth_limited_search(
            start,
            goal,
            maze,
            get_neighbors,
            depth_limit,
            path,
            explored
        )

        if found:
            return path, explored, depth_limit

        depth_limit += 1