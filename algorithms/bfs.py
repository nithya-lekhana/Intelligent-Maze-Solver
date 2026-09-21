from collections import deque


def bfs(start, goal, maze, get_neighbors):

    queue = deque([start])

    visited = {start}

    parent = {
        start: None
    }

    explored = []

    while queue:

        current = queue.popleft()

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

                queue.append(neighbor)

    # --------------------------------------------------------
    # Reconstruct path
    # --------------------------------------------------------

    path = []

    if goal in parent:

        current = goal

        while current is not None:

            path.append(current)

            current = parent[current]

        path.reverse()

    return path, explored