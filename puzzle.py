import heapq

def getInvCount(arr):
    inv_count = 0
    empty_value = 0
    for i in range(0, 9):
        for j in range(i + 1, 9):
            if arr[j] != empty_value and arr[i] != empty_value and arr[i] > arr[j]:
                inv_count += 1
    return inv_count

def isSolvable(puzzle):
    inv_count = getInvCount([j for sub in puzzle for j in sub])
    print(f"Inversion Count: {inv_count}")  # Debug print
    return (inv_count % 2 == 0)

class PuzzleState:
    def __init__(self, board, goal, moves=0, previous=None):
        self.board = board
        self.goal = goal
        self.moves = moves
        self.previous = previous

    def __lt__(self, other):
        return self.f() < other.f()

    def f(self):
        return self.moves + self.h()

    def h(self):
        goal_positions = {self.goal[i][j]: (i, j) for i in range(3) for j in range(3)}
        return sum(abs(i - goal_positions[val][0]) + abs(j - goal_positions[val][1]) 
                   for i, row in enumerate(self.board) for j, val in enumerate(row) if val != 0)

    def get_neighbors(self):
        def swap(board, i1, j1, i2, j2):
            new_board = [row[:] for row in board]
            new_board[i1][j1], new_board[i2][j2] = new_board[i2][j2], new_board[i1][j1]
            return new_board

        neighbors = []
        zero_pos = next((i, j) for i, row in enumerate(self.board) for j, val in enumerate(row) if val == 0)
        i, j = zero_pos

        if i > 0:
            neighbors.append(PuzzleState(swap(self.board, i, j, i - 1, j), self.goal, self.moves + 1, self))
        if i < 2:
            neighbors.append(PuzzleState(swap(self.board, i, j, i + 1, j), self.goal, self.moves + 1, self))
        if j > 0:
            neighbors.append(PuzzleState(swap(self.board, i, j, i, j - 1), self.goal, self.moves + 1, self))
        if j < 2:
            neighbors.append(PuzzleState(swap(self.board, i, j, i, j + 1), self.goal, self.moves + 1, self))

        return neighbors

    def is_goal(self):
        return self.board == self.goal

def solve_puzzle(start_board, goal_board):
    start_state = PuzzleState(start_board, goal_board)
    open_set = []
    heapq.heappush(open_set, start_state)
    closed_set = set()

    while open_set:
        current_state = heapq.heappop(open_set)
        
        if current_state.is_goal():
            return reconstruct_path(current_state)
        
        closed_set.add(tuple(map(tuple, current_state.board)))

        for neighbor in current_state.get_neighbors():
            if tuple(map(tuple, neighbor.board)) not in closed_set:
                heapq.heappush(open_set, neighbor)
    
    return None

def reconstruct_path(state):
    path = []
    while state:
        path.append(state.board)
        state = state.previous
    return path[::-1]

def print_board(board):
    for row in board:
        print(' '.join(str(x) if x != 0 else ' ' for x in row))
    print()

def input_board(prompt):
    print(prompt)
    board = []
    for _ in range(3):
        row = list(map(int, input().split()))
        board.append(row)
    return board

if __name__ == "__main__":
    start_board = input_board("Enter the initial state (3x3 grid, use 0 for empty space):")
    goal_board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    if isSolvable(start_board):
        solution = solve_puzzle(start_board, goal_board)
        
        if solution:
            for step in solution:
                print_board(step)
                print()
        else:
            print("No solution found")
    else:
        print("The puzzle is not solvable")
