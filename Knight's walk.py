import numpy
import matplotlip.pyplot as plt


def generate_board(n):
	if n < 1:
		return None
	
	board = np.zeros((n, n), dtype=int)
	num = n*n
	
	x, y = 0, 0
	dx, dy = 0, 1
	
	for i in range(num, 0, -1):
		board[x][y] = i
		if (
			x + dx < 0
			or x + dx >= n
			or y + dy < 0
			or y + dy >= n
			or board[x + dx][y + dy] != 0
		):
			dx, dy = dy, -dx
		x += dx
		y += dy
	
	return np.flip(board)


board = generate_board(7)
# print(*board, sep='\n')


visited_cells = []
visited_cells_set = set()
current_position = tuple(c.item() for c in np.where(board == 1))  # Starting at cell 1 (the center)


def find_next_move(position):
	knight_moves = [
		(-2, 1), (-1, 2), (1, 2), (2, 1),
		(2, -1), (1, -2), (-1, -2), (-2, -1)
	]
	min_value = float('inf')
	next_move = None
	
	for move in knight_moves:
		new_position = (position[0] + move[0], position[1] + move[1])
		if 0 <= new_position[0] < board.shape[0] and 0 <= new_position[1] < board.shape[0] and new_position not in visited_cells_set:
			value = board[new_position]
			if value < min_value:
				min_value = value
				next_move = new_position
	return next_move


while current_position is not None:
	visited_cells.append(board[current_position])
	visited_cells_set.add(current_position)
	current_position = find_next_move(current_position)

# print(*visited_cells)


visited_cells_positions = [tuple(c.item() for c in np.where(board == i)) for i in visited_cells]
# print(*visited_cells_positions)


x = [point[0] for point in visited_cells_positions]
y = [point[1] for point in visited_cells_positions]

plt.plot(x, y, marker='o', linestyle='-')

plt.xlabel('X')
plt.ylabel('Y')
plt.title("Knight's walk")

plt.grid(True)
plt.show()
