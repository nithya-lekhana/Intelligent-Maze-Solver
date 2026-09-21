import heapq


def heuristic(position, goal):
    """
    Manhattan distance heuristic.
    """
    row1, col1 = position
    row2, col2 = goal

    return abs(row1 - row2) + abs(col1 - col2)


def best_first(start, goal, maze, get_neighbors):

    # Priority queue
    # Stores: (heuristic value, position)
    priority_queue = []

    heapq.heappush(
        priority_queue,
        (heuristic(start, goal), start)
    )

    visited = {start}

    parent = {
        start: None
    }

    explored = []

    while priority_queue:

        # Get the position with the smallest heuristic
        _, current = heapq.heappop(priority_queue)

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

            if neighbor not in visited:

                visited.add(neighbor)

                parent[neighbor] = current

                priority = heuristic(
                    neighbor,
                    goal
                )

                heapq.heappush(
                    priority_queue,
                    (priority, neighbor)
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