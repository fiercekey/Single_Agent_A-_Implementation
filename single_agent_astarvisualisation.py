import pygame
import math
from queue import PriorityQueue
#queues will be used for open and closed in implementing a*

#defining the winndow size where we want the code to run
width = 500
window = pygame.display.set_mode((width, width))
pygame.display.set_caption("A* Path finding Algorithm")

#setting colours as constt variables so that we dont have to put (r, g, b) values again and again
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURUOISE = (64, 224, 288)

#node is the same as spot
class Spot:
	"""
		Defining a class for spots that is squares in the grid
		just like a structure in c
		__init__ function is necessary to define
	"""
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = width*row
		self.y = width*col
		self.color = WHITE
		self.neighbour = []
		self.width = width
		self.total_rows = total_rows
	
	#location status of a spot
	def get_pos(self):
		return self.row, self.col
	"""
	Colour coding 
	The follwing codes are asking the question from the spots whether the spots are inthe open, closed, start or end
	red--closed, white--not looked at, green--in open
	colour status which tells whether the block has been occupied or not
	as we can see this will return a boolean value 
	"""
	def is_closed(self):
		return self.color == RED
	def is_open(self):
		return self.color == GREEN
	def is_barrier(self):
		return self.color == BLACK
	def is_start(self):
		return self.color == ORANGE
	def is_end(self):
		return self.color == PURPLE
	
	def reset(self):
		self.color = WHITE
	def make_closed(self):
		self.color = RED
	def make_open(self):
		self.color = GREEN
	def make_barrier(self):
		self.color = BLACK
	def make_start(self):
		self.color = ORANGE
	def make_end(self):
		self.color = PURPLE
	def make_path(self):
		self.color = BLUE
	
	def draw(self, window):
		#(where , colour of the box, (x, y for the star, length, breadth) or breadth length)
		pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))
	
	def update_neigbour(self, grid, total_rows):
		#self.neighbour = []
		if self.row < self.total_rows-1 and not grid[self.row + 1][self.col].is_barrier():
			self.neighbour.append(grid[self.row+ 1][self.col])

		if self.row >0 and not grid[self.row - 1][self.col].is_barrier():
			self.neighbour.append(grid[self.row- 1][self.col])

		if self.col< total_rows -1 and not grid[self.row][self.col + 1].is_barrier():
			self.neighbour.append(grid[self.row][self.col + 1])

		if self.col>0 and not grid[self.row][self.col - 1].is_barrier():
			self.neighbour.append(grid[self.row][self.col - 1])


	
#heuristic iis going to be the manhatten distance between two spots
def h_score(p1, p2):
	# we expect p1, p2 to bbe points, the python command x1, y1 = 3, 5 assign the value 3 to x1 and 5 to y1
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2)+abs(y1 - y2)

def final_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw(draw)

def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	#((f-score, count, start))
	open_set.put((0, count, start))
	came_from = {}					#keeps track of where we came from
	g_score = {spot: float("inf") for row in grid for spot in row}#distance from where we came start
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h_score(start.get_pos(), end.get_pos()) 	#f-score = the net cost

	open_set_hash = {start}
	while open_set.empty() == False:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]        	#get()[2] refers to the second parameter in the open_set.get(0 = f-score, 1 = counnt, 2 = start which is the node)
		if current in open_set_hash:
			open_set_hash.remove(current)

		if current == end:
			final_path(came_from, end, draw)
			end.make_end()
			return True  #draw the final path
		
		for neighbour in current.neighbour:
			temp_g_score = g_score[current] + 1

			if temp_g_score< g_score[neighbour]:
				came_from[neighbour] = current
				g_score[neighbour] = temp_g_score
				f_score[neighbour] = temp_g_score +h_score(neighbour.get_pos(), end.get_pos())
				if neighbour not in open_set_hash:
					count +=1
					open_set.put((f_score[neighbour], count, neighbour))
					neighbour.make_open()

		draw(draw)

		if current != start:
			current.make_closed()

	return False

def make_grid(rows, width):
#we're going to make a 2d list that will represent the grid initialing it to an emply list
	grid = []
# gap is going to be the dimensions of each square as it is equal to the nearest integer to the total width/the rows
	gap = width//rows

	for i in range(rows):
		# add an empty list in each row to make a 2d array
		grid.append([])

		for j in range(rows):
			#using the class Spot now
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)
	return grid

def draw_grid(window, rows, width):
	gap = width//rows
	for i in range(rows):
		pygame.draw.line(window, GREY, (0, i*gap), (width, i*gap))
	for j in range(rows):
		pygame.draw.line(window, GREY, (j*gap, 0), (j*gap, width))

#drawing everything
def Draw(window, grid, rows, width):
	window.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(window)
	draw_grid(window, rows, width)
	pygame.display.update()

# the mouse is going to hover on the screen so he have to sprt of get the particular position of the mouse wrt our grid and nto the ppixels on the screer
def get_clicked_pos(pos, rows, width):
	gap = width//rows
	y, x = pos

	row = y//gap
	col = x//gap

	return row, col

def main(window, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	#just defining some variables
	start = None
	end= None


	run = True 
	started = False

	while run:
		Draw(window, grid, ROWS, width)
		for event in pygame.event.get():
			#if the user clicks on the cross button 
			if event.type == pygame.QUIT:
				run = False
			#if the program is already running, (mouse clicks will not be considered except for thhe quit button)then no change should be made and the program should keep running
			if started:
				continue

			#if the user clicks the left mouse button
			if pygame.mouse.get_pressed()[0]:    #()[0]-- left ()[1]-- middle  ()[2]-- right
				pos = pygame.mouse.get_pos()     # get the position of the mouse using this function
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				#if it is the first click
				if not start:
					start = spot
					start.make_start()
				elif not end and spot!=start:
					end = spot
					end.make_end()
				elif spot!=end and spot!=start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]:
				pos = pygame.mouse.get_pos()     # get the position of the mouse using this function
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if spot == start:
					start = None
				if spot == end:
					end = None
				spot.reset()
			#if a key is pressed
			if event.type == pygame.KEYDOWN:
				#checking whether the spaecbar is clicked before the event has started
				if event.key == pygame.K_SPACE and not started:
					for row in grid:
						for spot in row:
							spot.update_neigbour(grid, ROWS)

					algorithm(lambda draw: Draw(window, grid, ROWS, width), grid, start, end)


				


	pygame.quit()



main(window, width)

