import pygame
import random
import heapq
import time
from collections import deque
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.ids import ids
from algorithms.best_first import best_first
from algorithms.astar import astar

# ============================================================
# INITIALIZATION
# ============================================================

pygame.init()

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption(
    "Intelligent Maze Solver"
)

clock = pygame.time.Clock()


# ============================================================
# MAZE SETTINGS
# ============================================================

CELL_SIZE = 45

MAZE_ROWS = 13
MAZE_COLS = 19

MAZE_WIDTH = MAZE_COLS * CELL_SIZE
MAZE_HEIGHT = MAZE_ROWS * CELL_SIZE

PANEL_X = MAZE_WIDTH
PANEL_WIDTH = SCREEN_WIDTH - PANEL_X


# ============================================================
# COLORS
# ============================================================

BLACK = (30, 30, 30)
WHITE = (245, 245, 245)
GRID = (190, 190, 190)

GREEN = (0, 210, 0)
RED = (220, 0, 0)

BLUE = (70, 150, 240)
YELLOW = (255, 215, 70)

PANEL = (38, 62, 91)

BUTTON = (78, 110, 150)
BUTTON_SELECTED = (80, 145, 205)

RUN_GREEN = (0, 210, 0)
RESET_RED = (220, 0, 0)

LIGHT_TEXT = (245, 245, 245)
GRAY_TEXT = (205, 215, 225)


# ============================================================
# FONTS
# ============================================================

FONT_TITLE = pygame.font.SysFont(
    "arial",
    32,
    bold=True
)

FONT_SUBTITLE = pygame.font.SysFont(
    "arial",
    20
)

FONT_BUTTON = pygame.font.SysFont(
    "arial",
    21,
    bold=True
)

FONT_SECTION = pygame.font.SysFont(
    "arial",
    20,
    bold=True
)

FONT_SMALL = pygame.font.SysFont(
    "arial",
    16
)

FONT_TINY = pygame.font.SysFont(
    "arial",
    14
)


# ============================================================
# ALGORITHMS
# ============================================================

ALGORITHMS = [
    "BFS",
    "DFS",
    "IDS",
    "Best-First",
    "A*"
]


# ============================================================
# GLOBAL VARIABLES
# ============================================================

maze = []

start = None
goal = None

selected_algorithm = "BFS"

current_path = []
current_visited = []

show_comparison = False

last_status = "Ready"


# ============================================================
# RESULTS
# ============================================================

results = {}

for algorithm in ALGORITHMS:

    results[algorithm] = {
        "path_length": 0,
        "nodes_explored": 0,
        "time": 0.0
    }


# ============================================================
# ANIMATION VARIABLES
# ============================================================

animation_active = False

animation_algorithm = None

animation_visited = []
animation_path = []

animation_visited_index = 0
animation_path_index = 0

animation_phase = "visited"

last_animation_time = 0

ANIMATION_DELAY = 45


# ============================================================
# BUTTON POSITIONS
# ============================================================

button_x = PANEL_X + 40

button_width = PANEL_WIDTH - 80

button_height = 50

button_y = 155

button_gap = 54


algorithm_buttons = {}

for i, algorithm in enumerate(ALGORITHMS):

    algorithm_buttons[algorithm] = pygame.Rect(
        button_x,
        button_y + i * button_gap,
        button_width,
        button_height
    )


# ============================================================
# CONTROL BUTTONS
# ============================================================

RUN_BUTTON = pygame.Rect(
    PANEL_X + 40,
    445,
    150,
    52
)

RESET_BUTTON = pygame.Rect(
    PANEL_X + 205,
    445,
    150,
    52
)

COMPARE_BUTTON = pygame.Rect(
    PANEL_X + 370,
    445,
    155,
    52
)

NEW_MAZE_BUTTON = pygame.Rect(
    PANEL_X + 40,
    510,
    PANEL_WIDTH - 80,
    52
)


# ============================================================
# TEXT DRAWING
# ============================================================

def draw_text(
    text,
    x,
    y,
    font,
    color=LIGHT_TEXT
):

    surface = font.render(
        str(text),
        True,
        color
    )

    screen.blit(
        surface,
        (x, y)
    )


# ============================================================
# MAZE GENERATOR
# ============================================================

def generate_maze(rows, cols):

    grid = [
        ["#" for _ in range(cols)]
        for _ in range(rows)
    ]

    start_cell = (1, 1)

    grid[1][1] = "."

    stack = [start_cell]

    directions = [
        (-2, 0),
        (2, 0),
        (0, -2),
        (0, 2)
    ]

    while stack:

        row, col = stack[-1]

        possible = []

        shuffled = directions[:]

        random.shuffle(shuffled)

        for dr, dc in shuffled:

            nr = row + dr
            nc = col + dc

            if (
                1 <= nr < rows - 1
                and
                1 <= nc < cols - 1
                and
                grid[nr][nc] == "#"
            ):

                possible.append(
                    (nr, nc, dr, dc)
                )

        if possible:

            nr, nc, dr, dc = random.choice(
                possible
            )

            grid[
                row + dr // 2
            ][
                col + dc // 2
            ] = "."

            grid[nr][nc] = "."

            stack.append(
                (nr, nc)
            )

        else:

            stack.pop()

    grid[1][1] = "S"

    grid[rows - 2][cols - 2] = "G"

    return [
        "".join(row)
        for row in grid
    ]


# ============================================================
# INITIALIZE MAZE
# ============================================================

def initialize_maze():

    global maze
    global start
    global goal

    maze = generate_maze(
        MAZE_ROWS,
        MAZE_COLS
    )

    start, goal = find_positions(
        maze
    )


# ============================================================
# FIND START AND GOAL
# ============================================================

def find_positions(grid):

    start_position = None
    goal_position = None

    for row in range(len(grid)):

        for col in range(len(grid[0])):

            if grid[row][col] == "S":

                start_position = (
                    row,
                    col
                )

            elif grid[row][col] == "G":

                goal_position = (
                    row,
                    col
                )

    return (
        start_position,
        goal_position
    )


    return neighbors



# ============================================================
# ALGORITHMS REMOVED
# Algorithms are now imported from the algorithms/ module.
# ============================================================


# ============================================================
# SOLVE SELECTED ALGORITHM
# ============================================================

def solve_algorithm(
    algorithm
):

    start_time = time.perf_counter()
    
    # We define a helper that the algorithms can use to get neighbors
    def get_neighbors_wrapper(position, grid):
        row, col = position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != "#":
                neighbors.append((nr, nc))
        return neighbors

    if algorithm == "BFS":
        path, exploration = bfs(start, goal, maze, get_neighbors_wrapper)

    elif algorithm == "DFS":
        path, exploration = dfs(start, goal, maze, get_neighbors_wrapper)

    elif algorithm == "IDS":
        path, exploration, _ = ids(start, goal, maze, get_neighbors_wrapper)

    elif algorithm == "Best-First":
        path, exploration = best_first(start, goal, maze, get_neighbors_wrapper)

    elif algorithm == "A*":
        path, exploration = astar(start, goal, maze, get_neighbors_wrapper)

    else:
        path = []
        exploration = []

    execution_time = (
        time.perf_counter()
        -
        start_time
    )

    path_length = max(
        0,
        len(path) - 1
    )

    nodes_explored = len(
        exploration
    )

    return {
        "path": path,
        "exploration": exploration,
        "path_length": path_length,
        "nodes_explored": nodes_explored,
        "time": execution_time
    }


# ============================================================
# RUN
# ============================================================

def start_run():

    global animation_active
    global animation_algorithm
    global animation_visited
    global animation_path
    global animation_visited_index
    global animation_path_index
    global animation_phase
    global current_path
    global current_visited
    global last_status
    global show_comparison
    global last_animation_time

    show_comparison = False

    data = solve_algorithm(
        selected_algorithm
    )

    current_path = data["path"]

    current_visited = data[
        "exploration"
    ]

    results[selected_algorithm] = {
        "path_length": data[
            "path_length"
        ],

        "nodes_explored": data[
            "nodes_explored"
        ],

        "time": data[
            "time"
        ]
    }

    animation_algorithm = (
        selected_algorithm
    )

    animation_visited = data[
        "exploration"
    ]

    animation_path = data[
        "path"
    ]

    animation_visited_index = 0

    animation_path_index = 0

    animation_phase = "visited"

    animation_active = True

    last_animation_time = (
        pygame.time.get_ticks()
    )

    last_status = "Searching..."


# ============================================================
# COMPARE
# ============================================================

def compare_algorithms():

    global results
    global current_path
    global current_visited
    global show_comparison
    global animation_active
    global last_status

    animation_active = False

    for algorithm in ALGORITHMS:

        data = solve_algorithm(
            algorithm
        )

        results[algorithm] = {
            "path_length": data[
                "path_length"
            ],

            "nodes_explored": data[
                "nodes_explored"
            ],

            "time": data[
                "time"
            ]
        }

    # Use A* for the displayed comparison path
    astar_data = solve_algorithm(
        "A*"
    )

    current_path = astar_data[
        "path"
    ]

    current_visited = astar_data[
        "exploration"
    ]

    show_comparison = True

    last_status = "Comparison complete"


# ============================================================
# RESET
# ============================================================

def reset_solver():

    global current_path
    global current_visited
    global animation_active
    global animation_visited
    global animation_path
    global show_comparison
    global last_status
    global animation_visited_index
    global animation_path_index

    current_path = []

    current_visited = []

    animation_active = False

    animation_visited = []

    animation_path = []

    animation_visited_index = 0

    animation_path_index = 0

    show_comparison = False

    for algorithm in ALGORITHMS:

        results[algorithm] = {
            "path_length": 0,
            "nodes_explored": 0,
            "time": 0.0
        }

    last_status = "Ready"


# ============================================================
# NEW MAZE
# ============================================================

def new_maze():

    global current_path
    global current_visited
    global animation_active
    global animation_visited
    global animation_path
    global show_comparison
    global selected_algorithm
    global last_status
    global animation_visited_index
    global animation_path_index

    initialize_maze()

    current_path = []

    current_visited = []

    animation_active = False

    animation_visited = []

    animation_path = []

    animation_visited_index = 0

    animation_path_index = 0

    show_comparison = False

    selected_algorithm = "BFS"

    for algorithm in ALGORITHMS:

        results[algorithm] = {
            "path_length": 0,
            "nodes_explored": 0,
            "time": 0.0
        }

    last_status = "New maze generated"


# ============================================================
# DRAW MAZE
# ============================================================

def draw_maze():

    if animation_active:

        visited_to_draw = set(
            animation_visited[
                :animation_visited_index
            ]
        )

        if animation_phase == "path":

            path_to_draw = set(
                animation_path[
                    :animation_path_index
                ]
            )

        else:

            path_to_draw = set()

    else:

        visited_to_draw = set(
            current_visited
        )

        path_to_draw = set(
            current_path
        )

    for row in range(
        MAZE_ROWS
    ):

        for col in range(
            MAZE_COLS
        ):

            x = col * CELL_SIZE
            y = row * CELL_SIZE

            cell = maze[row][col]

            position = (
                row,
                col
            )

            if cell == "#":

                color = BLACK

            else:

                color = WHITE

                if position in visited_to_draw:

                    color = YELLOW

                if position in path_to_draw:

                    color = BLUE

                if position == start:

                    color = GREEN

                if position == goal:

                    color = RED

            pygame.draw.rect(
                screen,
                color,
                (
                    x,
                    y,
                    CELL_SIZE,
                    CELL_SIZE
                )
            )

            pygame.draw.rect(
                screen,
                GRID,
                (
                    x,
                    y,
                    CELL_SIZE,
                    CELL_SIZE
                ),
                2
            )


# ============================================================
# DRAW PANEL
# ============================================================

def draw_panel():

    pygame.draw.rect(
        screen,
        PANEL,
        (
            PANEL_X,
            0,
            PANEL_WIDTH,
            SCREEN_HEIGHT
        )
    )

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    draw_text(
        "MAZE SOLVER",
        PANEL_X + 40,
        35,
        FONT_TITLE
    )

    draw_text(
        "Select Algorithm",
        PANEL_X + 40,
        115,
        FONT_SUBTITLE,
        GRAY_TEXT
    )

    # --------------------------------------------------------
    # ALGORITHM BUTTONS
    # --------------------------------------------------------

    for algorithm in ALGORITHMS:

        rect = algorithm_buttons[
            algorithm
        ]

        if algorithm == selected_algorithm:

            color = BUTTON_SELECTED

        else:

            color = BUTTON

        pygame.draw.rect(
            screen,
            color,
            rect,
            border_radius=10
        )

        text_surface = FONT_BUTTON.render(
            algorithm,
            True,
            LIGHT_TEXT
        )

        text_rect = text_surface.get_rect(
            center=rect.center
        )

        screen.blit(
            text_surface,
            text_rect
        )

    # --------------------------------------------------------
    # RUN
    # --------------------------------------------------------

    pygame.draw.rect(
        screen,
        RUN_GREEN,
        RUN_BUTTON,
        border_radius=10
    )

    run_text = FONT_BUTTON.render(
        "RUN",
        True,
        WHITE
    )

    screen.blit(
        run_text,
        run_text.get_rect(
            center=RUN_BUTTON.center
        )
    )

    # --------------------------------------------------------
    # RESET
    # --------------------------------------------------------

    pygame.draw.rect(
        screen,
        RESET_RED,
        RESET_BUTTON,
        border_radius=10
    )

    reset_text = FONT_BUTTON.render(
        "RESET",
        True,
        WHITE
    )

    screen.blit(
        reset_text,
        reset_text.get_rect(
            center=RESET_BUTTON.center
        )
    )

    # --------------------------------------------------------
    # COMPARE
    # --------------------------------------------------------

    pygame.draw.rect(
        screen,
        BUTTON_SELECTED,
        COMPARE_BUTTON,
        border_radius=10
    )

    compare_text = FONT_BUTTON.render(
        "COMPARE",
        True,
        WHITE
    )

    screen.blit(
        compare_text,
        compare_text.get_rect(
            center=COMPARE_BUTTON.center
        )
    )

    # --------------------------------------------------------
    # NEW MAZE
    # --------------------------------------------------------

    pygame.draw.rect(
        screen,
        BUTTON_SELECTED,
        NEW_MAZE_BUTTON,
        border_radius=10
    )

    new_text = FONT_BUTTON.render(
        "NEW MAZE",
        True,
        WHITE
    )

    screen.blit(
        new_text,
        new_text.get_rect(
            center=NEW_MAZE_BUTTON.center
        )
    )

    # --------------------------------------------------------
    # RESULTS / COMPARISON
    # --------------------------------------------------------

    if show_comparison:

        draw_comparison()

    else:

        draw_results()


# ============================================================
# RESULTS
# ============================================================

def draw_results():

    x = PANEL_X + 40

    y = 610

    draw_text(
        "RESULTS",
        x,
        y,
        FONT_SECTION
    )

    y += 32

    data = results[
        selected_algorithm
    ]

    draw_text(
        f"Algorithm: {selected_algorithm}",
        x,
        y,
        FONT_SMALL,
        GRAY_TEXT
    )

    y += 25

    draw_text(
        f"Path Length: {data['path_length']}",
        x,
        y,
        FONT_SMALL,
        GRAY_TEXT
    )

    y += 25

    draw_text(
        f"Nodes Explored: {data['nodes_explored']}",
        x,
        y,
        FONT_SMALL,
        GRAY_TEXT
    )

    y += 25

    draw_text(
        f"Time: {data['time']:.6f} s",
        x,
        y,
        FONT_SMALL,
        GRAY_TEXT
    )

    y += 25

    draw_text(
        f"Status: {last_status}",
        x,
        y,
        FONT_SMALL,
        GRAY_TEXT
    )


# ============================================================
# COMPARISON TABLE
# ============================================================

def draw_comparison():

    x = PANEL_X + 40

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    draw_text(
        "ALGORITHM COMPARISON",
        x,
        600,
        FONT_SECTION
    )

    # --------------------------------------------------------
    # HEADERS
    # --------------------------------------------------------

    header_y = 635

    draw_text(
        "Algorithm",
        x,
        header_y,
        FONT_TINY,
        GRAY_TEXT
    )

    draw_text(
        "Path",
        x + 155,
        header_y,
        FONT_TINY,
        GRAY_TEXT
    )

    draw_text(
        "Nodes",
        x + 235,
        header_y,
        FONT_TINY,
        GRAY_TEXT
    )

    draw_text(
        "Time",
        x + 335,
        header_y,
        FONT_TINY,
        GRAY_TEXT
    )

    # --------------------------------------------------------
    # ROWS
    # --------------------------------------------------------

    row_y = 660

    row_gap = 27

    for algorithm in ALGORITHMS:

        data = results[
            algorithm
        ]

        draw_text(
            algorithm,
            x,
            row_y,
            FONT_TINY,
            LIGHT_TEXT
        )

        draw_text(
            str(data["path_length"]),
            x + 155,
            row_y,
            FONT_TINY,
            LIGHT_TEXT
        )

        draw_text(
            str(data["nodes_explored"]),
            x + 235,
            row_y,
            FONT_TINY,
            LIGHT_TEXT
        )

        draw_text(
            f"{data['time']:.6f}",
            x + 335,
            row_y,
            FONT_TINY,
            LIGHT_TEXT
        )

        row_y += row_gap

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    draw_text(
        "A* path displayed",
        x,
        row_y + 5,
        FONT_TINY,
        GRAY_TEXT
    )


# ============================================================
# UPDATE ANIMATION
# ============================================================

def update_animation():

    global animation_active
    global animation_visited_index
    global animation_path_index
    global animation_phase
    global last_status
    global last_animation_time

    if not animation_active:

        return

    current_time = (
        pygame.time.get_ticks()
    )

    if (
        current_time
        -
        last_animation_time
        <
        ANIMATION_DELAY
    ):

        return

    # Update timer properly
    last_animation_time = current_time

    # --------------------------------------------------------
    # VISITED NODE ANIMATION
    # --------------------------------------------------------

    if animation_phase == "visited":

        if (
            animation_visited_index
            <
            len(animation_visited)
        ):

            animation_visited_index += 1

        else:

            animation_phase = "path"

            animation_path_index = 0

    # --------------------------------------------------------
    # PATH ANIMATION
    # --------------------------------------------------------

    elif animation_phase == "path":

        if (
            animation_path_index
            <
            len(animation_path)
        ):

            animation_path_index += 1

        else:

            animation_active = False

            last_status = "Completed"


# ============================================================
# HANDLE CLICK
# ============================================================

def handle_click(position):

    global selected_algorithm
    global show_comparison
    global current_path
    global current_visited
    global last_status

    # --------------------------------------------------------
    # ALGORITHM BUTTONS
    # --------------------------------------------------------

    for algorithm, rect in (
        algorithm_buttons.items()
    ):

        if rect.collidepoint(
            position
        ):

            if not animation_active:

                selected_algorithm = algorithm

                show_comparison = False

                current_path = []

                current_visited = []

                last_status = "Ready"

            return

    # --------------------------------------------------------
    # RUN
    # --------------------------------------------------------

    if RUN_BUTTON.collidepoint(
        position
    ):

        if not animation_active:

            start_run()

        return

    # --------------------------------------------------------
    # RESET
    # --------------------------------------------------------

    if RESET_BUTTON.collidepoint(
        position
    ):

        reset_solver()

        return

    # --------------------------------------------------------
    # COMPARE
    # --------------------------------------------------------

    if COMPARE_BUTTON.collidepoint(
        position
    ):

        if not animation_active:

            compare_algorithms()

        return

    # --------------------------------------------------------
    # NEW MAZE
    # --------------------------------------------------------

    if NEW_MAZE_BUTTON.collidepoint(
        position
    ):

        new_maze()

        return


# ============================================================
# MAIN LOOP
# ============================================================

initialize_maze()

running = True

while running:

    # --------------------------------------------------------
    # EVENTS
    # --------------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        elif (
            event.type
            ==
            pygame.MOUSEBUTTONDOWN
        ):

            if event.button == 1:

                handle_click(
                    event.pos
                )

    # --------------------------------------------------------
    # UPDATE ANIMATION
    # --------------------------------------------------------

    if animation_active:

        update_animation()

    # --------------------------------------------------------
    # DRAW EVERYTHING
    # --------------------------------------------------------

    screen.fill(
        WHITE
    )

    draw_maze()

    draw_panel()

    pygame.display.flip()

    clock.tick(60)


# ============================================================
# EXIT
# ============================================================

pygame.quit()