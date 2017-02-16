from operator import *
from pykeyboard import PyKeyboard
class AI:
	def __init__(self, canvasSize):
		#Common Inoformation:
		self.canvasSize = canvasSize
		#Game Data
		self.snakePs = []
		self.foodPs = []
		#Every Step Simulation Information:
		self.path = []
		self.obstacle = []
		self.posbMove = []
		self.snakePsCurrent = []
		#AI virtual Device:
		self.keyboard = PyKeyboard()


	def FindPath(self, snakePs, foodPs):
		#Remember snake and food positions in real game:
		self.snakePs = [] + snakePs
		self.foodPs = [] + foodPs
		#Initialize:
		self.ResetSnakePsInfo()
		while (len(self.path) == 0) or (self.path[len(self.path)-1] != foodPs):
			self.FindNextStep(self.foodPs)
		self.ClearObstacle()

	def FindNextStep(self, foodPs):

		def CalPotentialMove():
			snakeHead = self.snakePsCurrent[len(self.snakePsCurrent) - 1]
			snakeBody = self.snakePsCurrent[0:len(self.snakePsCurrent) - 1]
			self.posbMove = [map(add, snakeHead, [1,0])  , \
							 map(add, snakeHead, [-1,0]) , \
							 map(add, snakeHead, [0,-1]) , \
							 map(add, snakeHead, [0,1])]

		def FiltPotentialMove():
			snakeHead = self.snakePsCurrent[len(self.snakePsCurrent) - 1]
			snakeBody = self.snakePsCurrent[0:len(self.snakePsCurrent) - 1]
			#Judge if inside canvas:
			def InsideCanvas(coordinate):
				if (coordinate[0] in range(0, self.canvasSize['width']/self.canvasSize['block'])) \
				and (coordinate[1] in range(0, self.canvasSize['height']/self.canvasSize['block'])):
					return True
				else:
					return False
			#---------------------#
			memoryMove = []
			for step in self.posbMove:
				if (step not in snakeBody) and InsideCanvas(step) and (step not in self.obstacle):
					memoryMove.append(step)
			self.posbMove += memoryMove
			#Closing
			memoryMove = []
			del self.posbMove[0:4]

		def ChooseNextMove(foodPs):
			#Choose the next step
			posbMoveNums = len(self.posbMove)
			if posbMoveNums == 0:
				#Add to obsticle
				print 'Cannot Find Path'
				print ''
				#Add obstacle:
				self.obstacle.append( self.snakePsCurrent[len(self.snakePsCurrent)-1] )
				self.ResetSnakePsInfo()
				self.ClearPath()
				print 'Obstacle: ' + str(self.obstacle)
				print ''


			elif posbMoveNums == 1:
				self.path.append(self.posbMove[0])
				self.snakePsCurrent.append(self.path[len(self.path)-1])
				del self.snakePsCurrent[0]

			else :
				#compare
				stepNums = []
				for step in self.posbMove:
					stepNums.append(abs(foodPs[0] - step[0]) + abs(foodPs[1] - step[1]))
				self.path.append(self.posbMove[stepNums.index(min(stepNums))])
				self.snakePsCurrent.append(self.path[len(self.path)-1])
				del self.snakePsCurrent[0]

		CalPotentialMove()
		FiltPotentialMove()
		ChooseNextMove(foodPs)

	def ResetSnakePsInfo(self):
		self.snakePsCurrent = [] + self.snakePs

	def ChangeSnakeDir(self):
		snakeHead = self.snakePs[len(self.snakePs) - 1]
		if map(sub, self.path[0], snakeHead) == [1,0]:
			#right
			self.keyboard.tap_key(self.keyboard.right_key)
		elif map(sub, self.path[0], snakeHead) == [-1,0]:
			#left
			self.keyboard.tap_key(self.keyboard.left_key)
		elif map(sub, self.path[0], snakeHead) == [0,1]:
			#Down
			self.keyboard.tap_key(self.keyboard.down_key)
		elif map(sub, self.path[0], snakeHead) == [0,-1]:
			#Up
			self.keyboard.tap_key(self.keyboard.up_key)


	def PrintPath(self):
		print '--------PATH--------'
		print self.path
		print ''

	def ClearObstacle(self):
		self.obstacle = []

	def ClearPath(self):
		self.path = []
