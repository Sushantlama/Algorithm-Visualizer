from tkinter import *
import astar
class cell:
    def __init__(self,i,j) -> None:
        self.x = i
        self.y = j
        self.f = -1
        self.g = -1
        self.h = -1
        self.obstacle = 0
        self.prevNode = None
        self.rectangle = None

class Application(Tk):
    def __init__(self):
        super().__init__()
        self.title('visualiser')
        self.geometry('900x650')
        self.resizable(False,False)
        self.root_height = 650
        self.root_width = 900
        # print(self.root_height,self.root_width)
        # print(str(self.root_height)+" "+str(self.root_width))
        self.frame()
        self.create_grid()

    def frame(self):
        self.canvas1 = Canvas(self,height=45,width=self.root_width,bg='steel blue')
        self.canvas1.pack()
        self.menu()
        self.canvas2 = Canvas(self,height=self.root_height-50,width=self.root_width,bg="white",highlightbackground="black",highlightthickness=2)
        self.canvas2.pack()
        self.val = 1
        self.canvas2.bind('<Button-1>',self.motion)
    
    def menu(self):
        Font_tuple = ("Segeo print", 14, "bold")
        self.canvas1.create_text((100,20),text=" by sushant lama",fill="white",font=Font_tuple)
        self.btn1 = Button(self.canvas1,text="add Source",width=12,height=1,command=self.add_source)
        self.btn1.place(x=300,y=10)
        self.btn2 = Button(self.canvas1,text="add Obstacles",width=12,height=1,command=self.add_obstacle)
        self.btn2.place(x=400,y=10)
        self.btn3 = Button(self.canvas1,text="add Goal",width=12,height=1,command=self.add_goal)
        self.btn3.place(x=500,y=10)
        self.btn3 = Button(self.canvas1,text="start",width=12,height=1,command=self.start)
        self.btn3.place(x=600,y=10)
        self.btn4 = Button(self.canvas1,text="reset",width=12,height=1,command=self.reset)
        self.btn4.place(x=700,y=10)


    def create_grid(self):
        self.size = 20
        self.rows = int((self.root_height-50)/self.size)
        self.cols = int(self.root_width/self.size)
        for i in range(self.rows):
            self.canvas2.create_line(0,i*self.size,self.root_width,i*self.size,fill="black")
        for j in range(self.cols):
            self.canvas2.create_line(j*self.size,0,j*self.size,self.root_height-50,fill="black")
        self.grid = []
        for i in range(self.cols):
            column = []
            for j in range(self.rows):
                column.append(cell(i,j))
            self.grid.append(column)
        self.start_node = self.grid[0][0]
        self.goal_node = self.grid[self.cols-1][self.rows-1]
        self.start_node.rectangle = self.canvas2.create_rectangle(self.start_node.x * self.size , self.start_node.y * self.size,
                                                                    self.start_node.x * self.size + self.size , self.start_node.y * self.size + self.size,
                                                                        fill="blue")
        self.goal_node.rectangle = self.canvas2.create_rectangle(self.goal_node.x * self.size , self.goal_node.y * self.size,
                                                                    self.goal_node.x * self.size + self.size , self.goal_node.y * self.size + self.size,
                                                                        fill="red")



    def motion(self,event):
        x = int(event.x/self.size)
        y = int(event.y/self.size)

        if self.val == 1:
            self.canvas2.delete(self.start_node.rectangle)
            self.start_node.rectangle = None
            self.start_node = self.grid[x][y]
            self.start_node.rectangle = self.canvas2.create_rectangle(self.start_node.x * self.size , self.start_node.y * self.size,
                                                                    self.start_node.x * self.size + self.size , self.start_node.y * self.size + self.size,
                                                                        fill="blue")
        if self.val == 2:
            self.canvas2.delete(self.goal_node.rectangle)
            self.goal_node.rectangle = None
            self.goal_node = self.grid[x][y]
            self.goal_node.rectangle = self.canvas2.create_rectangle(self.goal_node.x * self.size , self.goal_node.y * self.size,
                                                                    self.goal_node.x * self.size + self.size , self.goal_node.y * self.size + self.size,
                                                                        fill="red")
        if self.val == 3:
            node = self.grid[x][y]
            if node.obstacle == 0:
                node.obstacle = 1
                node.rectangle = self.canvas2.create_rectangle(node.x * self.size , node.y * self.size,
                                                                    node.x * self.size + self.size , node.y * self.size + self.size,
                                                                        fill="black")
            else:
                node.obstacle = 0
                self.canvas2.delete(node.rectangle)
                node.rectangle = None
            return
        if self.val == 0:
            return
        

    def add_source(self):
        if self.val != 0:
            self.val = 1

    def add_goal(self):
        if self.val != 0:
            self.val = 2

    def add_obstacle(self):
        if self.val != 0:
            self.val = 3

    def start(self):
        if self.val != 0:
            self.val = 0
            astar.astar(self,self.canvas2,self.start_node,self.goal_node,self.grid,self.size)
            self.val = 4
    
    def reset(self):
        if self.val != 0:
            self.val = 0
            self.canvas2.delete(self.start_node.rectangle)
            self.canvas2.delete(self.goal_node.rectangle)
            
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    node = self.grid[i][j]
                    if node.rectangle != None:
                        self.canvas2.delete(node.rectangle)
                    node.f = -1
                    node.g = -1
                    node.h = -1
                    node.obstacle = 0
                    node.prevNode = None
                    node.rectangle = None
            self.start_node = self.grid[0][0]
            self.goal_node = self.grid[self.cols-1][self.rows-1]
            self.start_node.rectangle = self.canvas2.create_rectangle(self.start_node.x * self.size , self.start_node.y * self.size,
                                                                        self.start_node.x * self.size + self.size , self.start_node.y * self.size + self.size,
                                                                            fill="blue")
            self.goal_node.rectangle = self.canvas2.create_rectangle(self.goal_node.x * self.size , self.goal_node.y * self.size,
                                                                        self.goal_node.x * self.size + self.size , self.goal_node.y * self.size + self.size,
                                                                        fill="red")
            self.val = 1




app = Application()
app.mainloop()