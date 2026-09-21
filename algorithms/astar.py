import heapq


def heuristic(position, goal):
    """
    Manhattan distance heuristic.
    """
    row1, col1 = position
    row2, col2 = goal

    return abs(row1 - row2) + abs(col1 - col2)


def astar(start, goal, maze, get_neighbors):

    # Priority queue
    # Stores: (f_score, g_score, position)
    priority_queue = []

    # Cost from start to start
    g_score = {
        start: 0
    }

    # f(n) = g(n) + h(n)
    f_score = {
        start: heuristic(start, goal)
    }

    heapq.heappush(
        priority_queue,
        (f_score[start], g_score[start], start)
    )

    # Store the parent of every cell
    parent = {
        start: None
    }

    # Keep track of explored cells
    explored = []

    # Keep track of cells already processed
    visited = set()

    while priority_queue:

        _, current_g, current = heapq.heappop(priority_queue)

        # Ignore outdated queue entries
        if current in visited:
            continue

        visited.add(current)
        explored.append(current)

        # Goal test
        if current == goal:
            break

        # Get neighboring cells
        neighbors = get_neighbors(
            current,
            maze
        )

        for neighbor in neighbors:

            # Every move has cost 1
            tentative_g = current_g + 1

            # If this is a better path to the neighbor
            if (
                neighbor not in g_score
                or tentative_g < g_score[neighbor]
            ):

                g_score[neighbor] = tentative_g

                h_score = heuristic(
                    neighbor,
                    goal
                )

                f_score[neighbor] = tentative_g + h_score

                parent[neighbor] = current

                heapq.heappush(
                    priority_queue,
                    (
                        f_score[neighbor],
                        tentative_g,
                        neighbor
                    )
                )

    # --------------------------------------------------
    # Reconstruct path
    # --------------------------------------------------

    path = []

    if goal in parent:

        current = goal

        while current is not None:

            path.append(current)

            current = parent[current]

        path.reverse()

    return path, explored