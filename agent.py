from collections import deque
import heapq
import math

class SearchAgent:
    """Agent that uses BFS, DFS, or UCS to find food."""

    def __init__(self):
        self.plan = []
        self.active_algo = "UCS"
        

    # -------------------------------------------------
    # Get valid neighbouring cells
    # -------------------------------------------------
    def get_neighbors(self, position, grid_size, walls):
        x, y = position
        width, height = grid_size

        possible_moves = [
            ("Right", (x + 1, y)),
            ("Left", (x - 1, y)),
            ("Up", (x, y + 1)),
            ("Down", (x, y - 1)),
        ]

        neighbors = []

        for action, new_position in possible_moves:
            nx, ny = new_position

            # Check whether the position is inside the grid
            if not (0 <= nx < width and 0 <= ny < height):
                continue

            # Check whether the position is a wall
            if new_position in walls:
                continue

            neighbors.append((new_position, action))

        return neighbors

    # -------------------------------------------------
    # Manhattan Distance
    # -------------------------------------------------
    def manhattan_distance(self, pos, goal):
        x1, y1 = pos
        x2, y2 = goal

        return abs(x1 - x2) + abs(y1 - y2)

    def manhattan_distance(self, pos, goal):
        x1, y1 = pos
        x2, y2 = goal

        return abs(x1 - x2) + abs(y1 - y2)

    def euclidean_distance(self, pos, goal):
        x1, y1 = pos
        x2, y2 = goal

        return math.sqrt(
            (x1 - x2) ** 2 +
            (y1 - y2) ** 2
        )
    # -------------------------------------------------
    # BFS
    # -------------------------------------------------
    def bfs_search(self, start, goal, grid_size, walls):

        frontier = deque()
        frontier.append((start, []))

        reached = set()
        reached.add(start)

        while frontier:

            current, path = frontier.popleft()

            if current == goal:
                return path

            for next_position, action in self.get_neighbors(
                current, grid_size, walls
            ):

                if next_position not in reached:
                    reached.add(next_position)

                    new_path = path + [action]

                    frontier.append(
                        (next_position, new_path)
                    )

        return []

    # -------------------------------------------------
    # DFS
    # -------------------------------------------------
    def dfs_search(self, start, goal, grid_size, walls):

        frontier = []
        frontier.append((start, []))

        reached = set()
        reached.add(start)

        while frontier:

            current, path = frontier.pop()

            if current == goal:
                return path

            for next_position, action in self.get_neighbors(
                current, grid_size, walls
            ):

                if next_position not in reached:
                    reached.add(next_position)

                    new_path = path + [action]

                    frontier.append(
                        (next_position, new_path)
                    )

        return []

    # -------------------------------------------------
    # UCS
    # -------------------------------------------------
    def ucs_search(self, start, goal, grid_size, walls):

        frontier = []

        # (total_cost, position, path)
        heapq.heappush(
            frontier,
            (0, start, [])
        )

        reached = {}

        reached[start] = 0

        while frontier:

            cost, current, path = heapq.heappop(frontier)

            if current == goal:
                return path

            for next_position, action in self.get_neighbors(
                current, grid_size, walls
            ):

                new_cost = cost + 1

                if (
                    next_position not in reached
                    or new_cost < reached[next_position]
                ):

                    reached[next_position] = new_cost

                    new_path = path + [action]

                    heapq.heappush(
                        frontier,
                        (
                            new_cost,
                            next_position,
                            new_path
                        )
                    )

        return []

        # -------------------------------------------------
    # A* Search
    # -------------------------------------------------
    def astar_search(
        self,
        start_pos,
        goal_pos,
        walls,
        grid_size,
        heuristic_type="manhattan"
    ):

        # Priority queue
        frontier = []

        # States that have already been explored
        reached_states = set()

        # Starting node
        g_cost = 0

        # Calculate h(n)
        if heuristic_type == "manhattan":
            h_cost = self.manhattan_distance(
                start_pos,
                goal_pos
            )
        else:
            h_cost = self.euclidean_distance(
                start_pos,
                goal_pos
            )

        # f(n) = g(n) + h(n)
        f_cost = g_cost + h_cost

        # (f_cost, g_cost, current_pos, path_taken)
        heapq.heappush(
            frontier,
            (
                f_cost,
                g_cost,
                start_pos,
                []
            )
        )

        # Process nodes
        while frontier:

            f_cost, g_cost, current_pos, path_taken = (
                heapq.heappop(frontier)
            )

            # Goal reached
            if current_pos == goal_pos:
                return path_taken

            # Mark current node as reached
            if current_pos in reached_states:
                continue

            reached_states.add(current_pos)

            # Expand neighbours
            for next_position, action in self.get_neighbors(
                current_pos,
                grid_size,
                walls
            ):

                # Ignore already reached states
                if next_position in reached_states:
                    continue

                # g(new) = g(current) + 1
                new_g_cost = g_cost + 1

                # Calculate h(new)
                if heuristic_type == "manhattan":
                    new_h_cost = self.manhattan_distance(
                        next_position,
                        goal_pos
                    )
                else:
                    new_h_cost = self.euclidean_distance(
                        next_position,
                        goal_pos
                    )

                # f(new) = g(new) + h(new)
                new_f_cost = new_g_cost + new_h_cost

                # Add action to the path
                new_path = path_taken + [action]

                # Add new node to priority queue
                heapq.heappush(
                    frontier,
                    (
                        new_f_cost,
                        new_g_cost,
                        next_position,
                        new_path
                    )
                )

        return []
    
    # -------------------------------------------------
    # Convert search direction into environment actions
    # -------------------------------------------------
    def convert_direction_to_actions(
        self, target_direction, current_direction
    ):
        directions = ["Up", "Right", "Down", "Left"]

        current_index = directions.index(current_direction)
        target_index = directions.index(target_direction)

        difference = (target_index - current_index) % 4

        actions = []

        if difference == 0:
            actions.append("move_forward")

        elif difference == 1:
            actions.append("turn_right")
            actions.append("move_forward")

        elif difference == 2:
            actions.append("turn_right")
            actions.append("turn_right")
            actions.append("move_forward")

        elif difference == 3:
            actions.append("turn_left")
            actions.append("move_forward")

        return actions


    # -------------------------------------------------
    # Main agent function
    # -------------------------------------------------
    def sense_and_act(self, percept: dict) -> str:

        # If standing on food, collect it first
        if percept["food_here"]:
            self.plan = []
            self.action_plan = []
            return "suck"

        # Create a new search plan if there is no plan
        if not self.plan:

            start = percept["agent_pos"]
            all_food = percept["all_food"]

            grid_size = percept["grid_size"]
            walls = set(percept["walls"])

            if not all_food:
                return "suck"

            # Find closest food
            goal = min(
                all_food,
                key=lambda food:
                abs(start[0] - food[0])
                + abs(start[1] - food[1])
            )

            # Select search algorithm
            if self.active_algo == "BFS":
                self.plan = self.bfs_search(
                    start, goal, grid_size, walls
                )

            elif self.active_algo == "DFS":
                self.plan = self.dfs_search(
                    start, goal, grid_size, walls
                )

            elif self.active_algo == "UCS":
                self.plan = self.ucs_search(
                    start, goal, grid_size, walls
                )

        # If no path was found
        if not self.plan:
            return "suck"

        # Get the next required movement direction
        target_direction = self.plan[0]
        current_direction = percept["agent_direction"]

        directions = ["Up", "Right", "Down", "Left"]

        current_index = directions.index(current_direction)
        target_index = directions.index(target_direction)

        difference = (target_index - current_index) % 4

        # Already facing the correct direction
        if difference == 0:
            self.plan.pop(0)
            return "move_forward"

        # One step clockwise
        elif difference == 1:
            return "turn_right"

        # Opposite direction
        elif difference == 2:
            return "turn_right"

        # One step counter-clockwise
        else:
            return "turn_left"
        
if __name__ == "__main__":

    agent = SearchAgent()

    start = (0, 0)
    goal = (3, 3)

    grid_size = (5, 5)
    walls = set()

    path = agent.astar_search(
        start,
        goal,
        walls,
        grid_size,
        heuristic_type="manhattan"
    )

    print("A* path:", path)