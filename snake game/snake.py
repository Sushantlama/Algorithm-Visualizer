from tkinter import *
import random

class Snake:
	def __init__(self, master = None):
		self.master = master
		self.canvas = Canvas(master,bg = "black",width=500,height=500)
		scoref = Frame(master,bg="white")
		scoroetext = Label(scoref,bg="white",text="score")
		self.valtext = Label(scoref,bg="white",text="0")

		scoroetext.grid(row=0,column=0,sticky="n",padx=10,pady=10)
		self.valtext.grid(row=0,column=1,sticky="n",padx=10,pady=10)
		
		self.canvas.grid(row=0,column=0,sticky="nsew")
		scoref.grid(row=0,column=1,sticky="ns")
		self.init = 0
		
		if self.init == 1:
			self.canvas.delete("all")
		
		self.init = 1
		self.x1 = 0
		self.x2 = 10
		self.y1 = 0
		self.y2 = 10
		self.dir = 1
		self.snake = []

		self.snake.append(self.create_rec(self.x1,self.y1,self.y1,self.y2))
		self.length = 0
		self.food = self.get_food()
		self.movement()

	# creates a rectangle in canvas
	def create_rec(self,x1,y1,x2,y2):
		colors = ["red", "orange", "yellow", "green", "blue", "violet"]
		color=random.choice(colors)
		rec = self.canvas.create_rectangle(x1,y1,x2,y2,fill=color)
		return rec

	# creates a food in canvas
	def get_food(self):
		x1 = random.randint(0,49)*10
		y1 = random.randint(0,49)*10
		x2 = x1+10
		y2 = y1+10
		return self.create_rec(x1,y1,x2,y2)

	#for movement checks the direction and increment the direction by 10
	def addcord(self):
		fac = 10
		if(self.dir == 1):
			if(self.x2 != 500):
				self.x1=self.x1+fac
				self.x2=self.x2+fac
			else:
				return False
		elif(self.dir == 2):
			if(self.y1 != 0):
				self.y1 = self.y1-fac
				self.y2 = self.y2-fac
			else:
				return False
		elif(self.dir == 3):
			if(self.x1 != 0):
				self.x1=self.x1-fac
				self.x2=self.x2-fac
			else:
				return False
			
		elif(self.dir == 4):
			if(self.y2 != 500):
				self.y1 = self.y1+fac
				self.y2 = self.y2+fac
			else:
				return False
		return True

	#moves the snake
	def movement(self):
		if(self.canvas.coords(self.food)==self.canvas.coords(self.snake[0])):
			# self.canvas.delete(self.food)
			# last_coords=self.canvas.coords(self.snake[self.length])
			self.snake.append(self.food)
			self.food = self.get_food()
			# self.snake.append(self.create_rec(last_coords[0],last_coords[1],last_coords[2],last_coords[3]))
			self.length = self.length+1
			self.valtext["text"]=str(self.length)

		new_coords=self.canvas.coords(self.snake[0])
		if self.addcord() == True:
			self.canvas.coords(self.snake[0],self.x1,self.y1,self.x2,self.y2)
			for i in range(1,self.length+1):
				prev_coords=self.canvas.coords(self.snake[i])
				self.canvas.coords(self.snake[i],new_coords[0],new_coords[1],new_coords[2],new_coords[3])
				new_coords=prev_coords
		self.canvas.after(50, self.movement)

	
	# for motion in positive x direction //1
	def right(self, event):
		if self.dir != 3:
			self.dir=1


	
	# for motion in positive y direction//2
	def up(self,event):
		if self.dir != 4:
			self.dir = 2	

	# for motion in negative x direction//3
	def left(self, event):
		if self.dir != 1:
			self.dir=3

	# for motion in negative y direction//4
	def down(self, event):
		if self.dir != 2:
			self.dir=4
