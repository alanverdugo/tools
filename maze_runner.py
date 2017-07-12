#!/usr/bin/env python
'''
	This program solves mazes using code from https://github.com/laurentluce/python-algorithms/tree/master/algorithms
	Refer to http://www.laurentluce.com/posts/solving-mazes-using-python-simple-recursivity-and-a-search/

	This puzzle involves the creation of a maze, this maze will be represented on the format: 10111;1110x 
	In which: 1 = allowed path 0 = not allowed path/wall x = point that you need to find 
	; = separation for next row of the maze 
	The maze will be solved if you can find the shortest path that needs to be followed in order to get to the point! 
	For example, for the maze: 
	1100001;
	0100111;
	1111101;
	1000111;
	1110100;
	1011110;
	111001x
	ALL the mazes will start from position 0,0.
	You can only move to left, right, down and up, not in diagonal. 
	Only the shortest path will be valid, on this case it will be: 
	0.0, 0.1, 1.1, 2.1, 2.2, 2.3, 2.4, 3.4, 4.4, 5.4, 5.5, 6.5, 6.6 
'''
import heapq

maze_string = "1100001;0100111;1111101;1000111;1110100;1011110;111001x"

current_maze_row = 0

current_maze_column = 0

wall_list = []

# Read the maze and figure out the size
## Split the maze_string into rows
total_rows = len(maze_string.split(";"))
total_columns = len(maze_string.split(";")[0])
print "This maze's size is", total_rows, "x", total_columns, "\r"


# Create a matrix.
matrix = [[0 for x in range(total_columns)] for y in range(total_rows)]

# Fill the matrix with the maze's data.
for index_x, row in enumerate(maze_string.split(";")):
	for index_y, box in enumerate(list(row)):
		matrix[index_x][index_y] = box
		# Since we are already reading the maze data, 
		# let's find the goal and save its position.
		if box == "x":
			goal_position_x = index_x
			goal_position_y = index_y
		if box == "0":
			# Add position to the list of "walls"
			wall_list.append((index_x,index_y))

# Print the goal's position:
print "The goal is at position X=", goal_position_x, "Y=", goal_position_y, "\r"


class Cell(object):
    def __init__(self, x, y, reachable):
        """Initialize new cell.

        @param reachable is cell reachable? not a wall?
        @param x cell x coordinate
        @param y cell y coordinate
        @param g cost to move from the starting cell to this cell.
        @param h estimation of the cost to move from this cell
                 to the ending cell.
        @param f f = g + h
        """
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0


class AStar(object):
    def __init__(self):
        # open list
        self.opened = []
        heapq.heapify(self.opened)
        # visited cells list
        self.closed = set()
        # grid cells
        self.cells = []
        self.grid_height = None
        self.grid_width = None

    def init_grid(self, width, height, walls, start, end):
        """Prepare grid cells, walls.

        @param width grid's width.
        @param height grid's height.
        @param walls list of wall x,y tuples.
        @param start grid starting point x,y tuple.
        @param end grid ending point x,y tuple.
        """
        self.grid_height = height
        self.grid_width = width
        walls = wall_list
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in walls:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable))
        self.start = self.get_cell(*start)
        self.end = self.get_cell(*end)

    def get_heuristic(self, cell):
        """Compute the heuristic value H for a cell.

        Distance between this cell and the ending cell multiply by 10.

        @returns heuristic value H
        """
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def get_cell(self, x, y):
        """Returns a cell from the cells list.

        @param x cell x coordinate
        @param y cell y coordinate
        @returns cell
        """
        return self.cells[x * self.grid_height + y]

    def get_adjacent_cells(self, cell):
        """Returns adjacent cells to a cell.

        Clockwise starting from the one on the right.

        @param cell get adjacent cells for this cell
        @returns adjacent cells list.
        """
        cells = []
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells

    def get_path(self):
        cell = self.end
        path = [(cell.x, cell.y)]
        while cell.parent is not self.start:
            cell = cell.parent
            path.append((cell.x, cell.y))

        path.append((self.start.x, self.start.y))
        path.reverse()
        return path

    def update_cell(self, adj, cell):
        """Update adjacent cell.

        @param adj adjacent cell to current cell
        @param cell current cell being processed
        """
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def solve(self):
        """Solve maze, find path to ending cell.

        @returns path or None if not found.
        """
        # add starting cell to open heap queue
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # pop cell from heap queue
            f, cell = heapq.heappop(self.opened)
            # add cell to closed list so we don't process it twice
            self.closed.add(cell)
            # if ending cell, return found path
            if cell is self.end:
                return self.get_path()
            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found
                        # for this adj cell.
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))


a = AStar()
walls = wall_list
a.init_grid(1000, 1000, walls, (0, 0), (goal_position_x, goal_position_y))
path = a.solve()

print "Solution path:", path
