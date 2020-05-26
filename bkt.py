import pygame

# GLOBAL VARIABLES

done = False
sol = []
columns = 5
rows = 5
rectwidth = 25
array = [[0 for j in range(columns)] for i in range(rows)]
start = []
end = []
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)
black = (0, 0, 0)
yellow = (255,255,0)
screen = pygame.display.set_mode((columns*rectwidth, rows*rectwidth))
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]


def isOK(i : int, j : int)->bool:
	# CHECKS MISTAKES
	if i > rows - 1 or i < 0:
		return False
	if j > columns - 1 or j < 0:
		return False
	if array[i][j] == 1 or [i, j] == end:
		return True
	if array[i][j] == 0 or array[i][j]:
		return False

def solve(i, j, step):
	global array
	if [i, j] == end:
		# IF A PATH HAS BEEN FOUND SHOW IT
		update()
		pygame.time.delay(1000)
	else:
		# CHECKS ALL 4 DIRECTIONS TOP BOT LEFT AND RIGHT
		for k in range(4):
			next_i = i + di[k]
			next_j = j + dj[k]
			if isOK(next_i, next_j):
				array[next_i][next_j] = step
				solve(next_i, next_j, step + 1)
				array[next_i][next_j] = -1


def checkevents():
	global done, array, start, end
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		# ALLOWS CONTINOUS MOVE AND INCONTINOUS
		elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
			# ADD WALL ONLY IF START AND END ARE PLACED
			if start and end:
				# IF LEFT CLICK IS PRESSED GET THE POS AND ADD WALL
				if pygame.mouse.get_pressed()[0]:
					pos = pygame.mouse.get_pos()
					# CHECK TO NOT PLACE WALLS ON THE START AND END POINT
					if [pos[1] // rectwidth, pos[0] // rectwidth] != start and [pos[1] // rectwidth, pos[0] // rectwidth] != end:
						array[pos[1] // rectwidth][pos[0] // rectwidth] = 1
				# IF RIGHT CLICK IS PRESSED GET THE POS AND DELETE WALL
				if pygame.mouse.get_pressed()[2]:
					pos = pygame.mouse.get_pos()
					# CHECKS TO ONLY DELETE WALL
					if array[pos[1] // rectwidth][pos[0] // rectwidth] == 1:
						array[pos[1] // rectwidth][pos[0] // rectwidth] = 0
			# PLACE A START POINT IF IT'S NOT GIVEN
			elif not start:
				if pygame.mouse.get_pressed()[0]:
					pos = pygame.mouse.get_pos()
					start.append(pos[1] // rectwidth)
					start.append(pos[0] // rectwidth)
			# PLACE AN END POINT IF IT'S NOT GIVEN
			elif not end:
				if pygame.mouse.get_pressed()[0]:
					pos = pygame.mouse.get_pos()
					# CHECKS IF END POINT IT'S NOT AT THE SAME PLACE AS START POINT
					if [pos[1] // rectwidth, pos[0] // rectwidth] != start:
						end.append(pos[1] // rectwidth)
						end.append(pos[0] // rectwidth)
		# CHECKS FOR ENTER PRESS TO FIND PATHS ONLY IF THE START AND END POINT WERE GIVEN
		elif event.type == pygame.KEYDOWN and start and end:
			if event.key == pygame.K_RETURN:
				solve(start[0], start[1], 2)
				pygame.time.delay(1000)
				done = True


def update():
	# TRAVERSING THE ARRAY FOR DRAWING RECTS
	for i in range(rows):
		# DRAW ORIZONTAL LINES
		pygame.draw.line(screen, white, (0, i * rectwidth), (columns * rectwidth, i * rectwidth))
		for j in range(columns):
			# IF IT'S A WALL DRAW A WHITE RECT
			if array[i][j] == 1 or array[i][j] == -1:
				pygame.draw.rect(screen, white, (j * rectwidth, i * rectwidth, rectwidth, rectwidth))
			# IF IT'S NOT A WALL IN CANSE YOU DELETE IT DRAW A BLACK SPOT
			if array[i][j] == 0:
				pygame.draw.rect(screen, black, (j * rectwidth + 1, i * rectwidth + 1, rectwidth - 1, rectwidth - 1))
			if array[i][j] >= 2:
				pygame.draw.rect(screen, yellow, (j * rectwidth + 1, i * rectwidth + 1, rectwidth - 1, rectwidth - 1))
	# DRAW VERTICAL LINES 
	for j in range(columns):
		pygame.draw.line(screen, white, (j * rectwidth, 0), (j * rectwidth, rows * rectwidth))

	# DRAW START AND END POSITION
	if start:
		pygame.draw.rect(screen, green, (start[1] * rectwidth, start[0] * rectwidth, rectwidth, rectwidth))
	if end:
		pygame.draw.rect(screen, red, (end[1] * rectwidth, end[0] * rectwidth, rectwidth, rectwidth))
	pygame.display.update()

while not done:
	checkevents()
	update()
