from tkinter import *
import random

class Snake:
	def __init__(self, master = None):
		self.master = master
		self.canvas = Canvas(master,bg = "black",width=500,height=500)
		sideframe = Frame(master,bg="white")
		
		scoreframe = Frame(sideframe,bg="white")
		scoroetext = Label(scoreframe,bg="white",text="score")
		self.valtext = Label(scoreframe,bg="white",text="0")

		scoroetext.grid(row=0,column=0,sticky="n",padx=10,pady=10)
		self.valtext.grid(row=0,column=1,sticky="n",padx=10,pady=10)

		buttonframe = Frame(sideframe,bg="white")

	
		self.btn1 = Button(buttonframe,text="god mode",width=12,height=1,command=self.god_mode)
		self.btn1.grid(row=0,column=0,sticky="ns",padx=10,pady=10) 

		self.btn2 = Button(buttonframe,text="normal mode",width=12,height=1,command=self.normal_mode)
		self.btn2.grid(row=1,column=0,sticky="ns",padx=10,pady=10) 

		self.btn3 = Button(buttonframe,text="pause",width=12,height=1,command=self.pause)
		self.btn3.grid(row=2,column=0,sticky="ns",padx=10,pady=10) 

		self.btn4 = Button(buttonframe,text="restart",width=12,height=1,command=self.restart)
		self.btn4.grid(row=3,column=0,sticky="ns",padx=10,pady=10) 
		self.text=Label(buttonframe,text="welcome ,\n you are in god mode",width=20)
		self.text.grid(row=4,column=0,sticky="ns",padx=10,pady=10)


		self.canvas.grid(row=0,column=0,sticky="nsew")
		sideframe.grid(row=0,column=1,sticky="ns")
		scoreframe.grid(row=0,column=0,sticky="ns")
		buttonframe.grid(row=1,column=0,sticky="ns")
		self.init = 0
		
		# if self.init == 1:
		# 	self.canvas.delete("all")
		self.start()
		self.movement()

	def start(self):
		self.mode = 0
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
		x = len(self.snake)-1
		if self.mode != 0:
			for i in range(3,x):
						if(self.canvas.coords(self.snake[0])==self.canvas.coords(self.snake[i])):
							self.died()
		if self.mode != 2:
		
			if(self.canvas.coords(self.food)==self.canvas.coords(self.snake[x])):
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
			else:
				if self.mode == 1:
					self.died()

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

	def god_mode(self):
		self.mode = 0
		self.text["text"]="you are in god mode"
	def normal_mode(self):
		self.text["text"]="you are in normal mode"
		self.mode = 1
	def pause(self):
		self.text["text"]="game is paused"
		self.mode = 2
	def died(self):
		self.text["text"]="oops,\n your snake died"
		self.mode = 2
	def restart(self):
		self.canvas.delete("all")
		self.start()
		self.valtext["text"]="0"
		self.text["text"]="you are in god mode"
