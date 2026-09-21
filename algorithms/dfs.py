# ============================================================
# DEPTH-FIRST SEARCH (DFS)
# ============================================================

def dfs(start, goal, maze, get_neighbors):

    # Stack for DFS
    stack = [start]

    # Keep track of visited cells
    visited = {start}

    # Store parent of each cell
    parent = {
        start: None
    }

    # Store exploration order
    explored = []

    # --------------------------------------------------------
    # DFS LOOP
    # --------------------------------------------------------

    while stack:

        # LIFO: remove the last element
        current = stack.pop()

        explored.append(current)

        # Goal test
        if current == goal:
            break

        # Get valid neighboring cells
        neighbors = get_neighbors(
            current,
            maze
        )

        # Add neighbors to stack
        for neighbor in neighbors:

            if neighbor not in visited:

                visited.add(neighbor)

                parent[neighbor] = current

                stack.append(neighbor)

    # --------------------------------------------------------
    # RECONSTRUCT PATH
    # --------------------------------------------------------

    path = []

    if goal in parent:

        current = goal

        while current is not None:

            path.append(current)

            current = parent[current]

        path.reverse()

    return path, explored