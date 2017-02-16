
from Tkinter import *
from tkFont import *
from random import *
from snake_ai import *
from SnakeStyle import *

class Food:
	def __init__(self,canvasSize):
		self.canvasSize = canvasSize
		self.ps = []
	def GenerateFood(self,snakePs):
		#print 'New food'
		canvasSize = self.canvasSize
		self.ps = [	randint(0,canvasSize['width']/canvasSize['block'] - 1),\
					randint(0,canvasSize['height']/canvasSize['block'] - 1)	]
		if self.ps in snakePs:
			self.GenerateFood(snakePs)

class Snake:
	def __init__(self):
		self.ps = [[0,0],[1,0],[2,0],[3,0],[4,0]]	#Body lenth = 5
		self.dir = 'R'								#Initial direction = Right
		self.dirForbid = False
		self.tail = [0,0]

	def Move(self):
		#Head moves to the next block
		head = self.ps[len(self.ps) - 1]	#Head Coordinate Index
		if self.dir == 'R':
			newHead = [head[0]+1, head[1]]
		elif self.dir == 'L':
			newHead = [head[0]-1, head[1]]
		elif self.dir == 'U':
			newHead = [head[0], head[1]-1]
		elif self.dir == 'D':
			newHead = [head[0], head[1]+1]
		self.ps.append(newHead)
		#Tail moves to the next block
		#Remember tail info for growing
		self.tail = self.ps[0]
		del self.ps[0]

	def AllowDirChange(self):
		self.dirForbid = False

	def Grow(self):
		self.ps.insert(0, self.tail)

class Game:
	def __init__(self,canvasSize):
		#gameStatus
		self.gameStatus = {'Start':False, 'Pause':False, 'Over':False}
		#Create food and snake instance
		self.snake = Snake()
		self.food = Food(canvasSize)
		self.food.GenerateFood(self.snake.ps)

		self.canvasSize = canvasSize

		#Speed and time
		self.gameSpeed = 50
		self.minSpeed = 30
		self.unitSpeed = 10

		#Score:
		self.playScore = 0
		self.scoreIncrement = 10
		########################
		########################
		self.aiPlayer = AI(self.canvasSize)

		#Effect:
		self.showGetScore = False
		self.timeCounter = 200 #ms

	#Game is running
	def Update(self):
		if (self.gameStatus['Pause'] == False) and (self.gameStatus['Over'] == False) and (self.gameStatus['Start'] == True):
			#Move
			self.snake.Move()
			self.snake.AllowDirChange()
			snakeHead = self.snake.ps[len(self.snake.ps)-1]
			snakeBody = self.snake.ps[0:len(self.snake.ps)-1]
			snakePs = self.snake.ps
			foodPs = self.food.ps
			canvasSize = self.canvasSize
			#Die
			if (snakeHead in snakeBody) or \
			(snakeHead[0]*canvasSize['block'] >= canvasSize['width']) or \
			(snakeHead[0]*canvasSize['block'] < 0) or \
			(snakeHead[1]*canvasSize['block'] >= canvasSize['height']) or \
			(snakeHead[1]*canvasSize['block'] < 0):
				self.gameStatus['Over'] = True
			#GetScore
			elif snakeHead == foodPs:
				self.GetScore()
				self.Indicate_GetScore()
				self.snake.Grow()
				self.food.GenerateFood(snakePs)
				self.IncreaseSpeed()

			#AI Player Action:
			
			self.aiPlayer.FindPath(self.snake.ps,self.food.ps)
			self.aiPlayer.ChangeSnakeDir()
			self.aiPlayer.PrintPath()
			self.aiPlayer.ClearPath()
			


	def IncreaseSpeed(self):
		if self.gameSpeed > self.minSpeed:
			self.gameSpeed -= self.unitSpeed

	def GetScore(self):
		"""
		if 	(self.gameSpeed == self.minSpeed) and \
			(self.scoreIncrement != 20):
			self.scoreIncrement = 20
		"""
		self.playScore += self.scoreIncrement

	def Indicate_GetScore(self):
		#ShowScore:
		self.showGetScore = True

	def DoneIndicate_GetScore(self):
		self.showGetScore = False
		self.timeCounter = 200

class Frame:
	def __init__(self):
		#Root:
		self.root = Tk()
		self.root.wm_title("Burning's Snake Game")
		self.root.bind("<Key>", self.KeyPressed)
		#Canvas:
		self.canvasSize = {'height':480,'width':640,'block':20}
		self.canvas = Canvas(self.root, height = self.canvasSize['height'], width = self.canvasSize['width'], bg = '#272822')
		self.canvas.pack()
		#Create Game:
		self.myGame = Game(self.canvasSize)
		#Snake Style Manager:
		self.styler = StyleManager()

	def DrawGame(self):
		#Save Canvas Information
		canvasSize = self.canvasSize
		pixelSize = self.canvasSize['block']
		#Function Definition:
		def DrawMainMenu():
			self.canvas.create_text(canvasSize['width']/2, canvasSize['height']*0.38, text = "Welcome to Snake world!", font = self.styler.headFont, fill = '#FD971F')
			self.canvas.create_text(canvasSize['width']/2, canvasSize['height']*0.45, text = "Designed by Burning", font = self.styler.hintFont, fill = '#75715E')
			self.canvas.create_text(canvasSize['width']/2, canvasSize['height']*0.55, text = "Press SPACE to begin", font = self.styler.hintFont, fill = '#66D9EF')
		def DrawPauseMenu():
			self.canvas.create_text(canvasSize['width']/2, canvasSize['height']*0.38, text = "Pasue", font = self.styler.headFont, fill = '#FD971F')
			self.canvas.create_text(canvasSize['width']/2, canvasSize['height']*0.55, text = "Press SPACE to continue", font = self.styler.hintFont, fill = '#66D9EF')
		def DrawHUD():
			#Display PlayerScore
			self.canvas.create_text(15,15, text = "Scores: " + str(self.myGame.playScore), anchor = NW, fill = '#FD971F', font = self.styler.scoreFont)
		def DrawSnake():
			#Display Snake Position
			snakeColor = self.styler.initSnakeColor
			for block in self.myGame.snake.ps[0:len(self.myGame.snake.ps)-1]:
				self.canvas.create_rectangle(block[0]*pixelSize,block[1]*pixelSize, block[0]*pixelSize + pixelSize, block[1]*pixelSize + pixelSize, fill = snakeColor)
				snakeColor = self.styler.DimColor(snakeColor)
		def DrawFood():
			#Display Food Position
			foodPs = self.myGame.food.ps
			self.canvas.create_rectangle(foodPs[0]*pixelSize, foodPs[1]*pixelSize, foodPs[0]*pixelSize + pixelSize, foodPs[1]*pixelSize + pixelSize, fill = '#FF0000')
		def DrawGameOver():
			#Draw Game Over Menu
			self.canvas.create_text(canvasSize['width']/2, canvasSize['height']*0.38, text = "Game Over", font = self.styler.headFont, fill = '#F92672')
			self.canvas.create_text(canvasSize['width']/2, canvasSize['height']*0.5, text = "Your score is: " + str(self.myGame.playScore), font = self.styler.hintFont, fill = '#F92672')
			self.canvas.create_text(canvasSize['width']/2, canvasSize['height']*0.6, text = "Press SPACE to restart", font = self.styler.hintFont, fill = '#66D9EF')
		#Not Determined Function
		def DrawGetScore():
			if self.myGame.showGetScore == True:
				self.canvas.create_text(canvasSize['width']/2, canvasSize['height']*0.14, text = '+'+ str(self.myGame.scoreIncrement), fill = '#F92672', font = self.styler.getScoreFont)
				self.myGame.timeCounter -= 10
				if self.myGame.timeCounter <= 0:
					self.myGame.DoneIndicate_GetScore()

		#Begin to Draw:
		gameStatus = self.myGame.gameStatus
		if gameStatus['Start'] == False:
			DrawMainMenu()
		elif gameStatus['Pause'] == True:
			DrawPauseMenu()
		elif gameStatus['Over'] == True:
			DrawGameOver()
		else:
			DrawFood()
			DrawSnake()
			DrawHUD()
			DrawGetScore()

	def Refresh(self):
		self.canvas.delete('all')
		self.myGame.Update()
		self.DrawGame()
		self.root.after(self.myGame.gameSpeed, self.Refresh)

	def CreateNewGame(self):
		self.myGame = Game(self.canvasSize)
		self.myGame.gameStatus['Start'] = True

	def KeyPressed(self, event):
		#Initialize:
		keySym = event.keysym
		keyChar = event.char
		gameStatus = self.myGame.gameStatus
		#Change Direction Event:
		snakeDir = self.myGame.snake.dir
		if ( snakeDir !=  'U') and (keySym == 'Down') and (self.myGame.snake.dirForbid == False):
			self.myGame.snake.dir = 'D'
			self.myGame.snake.dirForbid = True
		elif ( snakeDir !=  'R') and (keySym == 'Left') and (self.myGame.snake.dirForbid == False):
			self.myGame.snake.dir = 'L'
			self.myGame.snake.dirForbid = True
		elif ( snakeDir !=  'L') and (keySym == 'Right') and (self.myGame.snake.dirForbid == False):
			self.myGame.snake.dir = 'R'
			self.myGame.snake.dirForbid = True
		elif ( snakeDir !=  'D') and (keySym == 'Up') and (self.myGame.snake.dirForbid == False):
			self.myGame.snake.dir = 'U'
			self.myGame.snake.dirForbid = True
		#Space Event Begin / Pause:
		elif keyChar == ' ':
			if gameStatus['Start'] == False:
				self.CreateNewGame()
			elif gameStatus['Over'] == True:
				self.CreateNewGame()
			elif gameStatus['Pause'] == False:
				self.myGame.gameStatus['Pause'] = True
			else:
				self.myGame.gameStatus['Pause'] = False
		#Return to Main:
		elif keySym == 'Escape':
			if gameStatus['Start'] == True:
				self.myGame.gameStatus['Start'] = False

mainFrame = Frame()
mainFrame.Refresh()
mainFrame.root.mainloop()
