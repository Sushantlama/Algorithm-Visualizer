from tkinter import *
import astar
import bfs
import dfs
import random
import time

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
        self.blocked = 1
        self.ConNode = None

class Application(Tk):
    def __init__(self):
        super().__init__()
        self.title('Search Algo visualiser')
        self.geometry('1000x650')
        self.resizable(False,False)
        self.root_height = 650
        self.root_width = 1000
        # print(self.root_height,self.root_width)
        # print(str(self.root_height)+" "+str(self.root_width))
        self.frame()
        self.create_grid()

    # creates the whole
    def frame(self):
        self.canvas1 = Canvas(self,height=45,width=self.root_width,bg='navy')
        self.canvas1.pack()
        self.menu()
        self.canvas2 = Canvas(self,height=self.root_height-50,width=self.root_width,bg="white",highlightbackground="black",highlightthickness=2)
        self.canvas2.pack()
        self.val = 1
        self.canvas2.bind('<Button-1>',self.motion)
    
    # creates the menu
    def menu(self):
        Font_tuple = ("Segeo print", 14, "bold")
        self.canvas1.create_text((80,20),text=" by sushant lama",fill="white",font=Font_tuple)
        self.btn5 = Button(self.canvas1,text="maze",width=12,height=1,command=self.create_maze)
        self.btn5.place(x=170,y=10)
        self.btn1 = Button(self.canvas1,text="add Source",width=12,height=1,command=self.add_source)
        self.btn1.place(x=270,y=10)
        self.btn2 = Button(self.canvas1,text="add Obstacles",width=12,height=1,command=self.add_obstacle)
        self.btn2.place(x=370,y=10)
        self.btn3 = Button(self.canvas1,text="add Goal",width=12,height=1,command=self.add_goal)
        self.btn3.place(x=470,y=10)
        self.btn3 = Button(self.canvas1,text="start",width=12,height=1,command=self.start)
        self.btn3.place(x=570,y=10)
        self.btn4 = Button(self.canvas1,text="clear",width=12,height=1,command=self.reset)
        self.btn4.place(x=670,y=10)
        
        
        self.options1 = [
            "BFS",
            "DFS",
            "A*"
        ]
        self.clicked1 = StringVar()
        self.clicked1.set("BFS")
        self.drop1 = OptionMenu(self.canvas1, self.clicked1 , *self.options1 )
        self.drop1.place(x=770,y=10)
        
        self.options2 = [
                    "Clear All",
                    "Clear ALL except Maze"
                    ]
        self.clicked2 = StringVar()
        self.clicked2.set("Clear All")
        self.drop2 = OptionMenu(self.canvas1, self.clicked2 , *self.options2 )
        self.drop2.place(x=840,y=10)


    # creates the grid
    def create_grid(self):
        self.size = 20
        self.rows = int((self.root_height-50)/self.size)
        self.cols = int(self.root_width/self.size)
        
        self.grid_lines=[]
        for i in range(self.rows):
            self.grid_lines.append(self.canvas2.create_line(0,i*self.size,self.root_width,i*self.size,fill="black"))
        for j in range(self.cols):
            self.grid_lines.append(self.canvas2.create_line(j*self.size,0,j*self.size,self.root_height-50,fill="black"))
        self.grid = []
        for i in range(self.cols):
            column = []
            for j in range(self.rows):
                column.append(cell(i,j))
            self.grid.append(column)
        self.start_node = self.grid[0][0]
        self.goal_node = self.grid[0][4]
        self.start_node.rectangle = self.canvas2.create_rectangle(self.start_node.x * self.size , self.start_node.y * self.size,
                                                                    self.start_node.x * self.size + self.size , self.start_node.y * self.size + self.size,
                                                                        fill="limegreen")
        self.goal_node.rectangle = self.canvas2.create_rectangle(self.goal_node.x * self.size , self.goal_node.y * self.size,
                                                                    self.goal_node.x * self.size + self.size , self.goal_node.y * self.size + self.size,
                                                                        fill="red")
        self.frontier = []
        self.mode = 0
        print(self.rows,self.cols)


    # detects the motion of the mouse and sets selected node as (sourcenode,goalnode,obstaclenode)
    def motion(self,event):
        x = int(event.x/self.size)
        y = int(event.y/self.size)
        
        # sets selected node as source node
        if self.val == 1:
            if self.goal_node != None:
                if self.goal_node.x == x and self.goal_node.y == y:
                    return
            
            if self.grid[x][y].obstacle == 1:
                return
            if  self.start_node != None:
                self.canvas2.delete(self.start_node.rectangle)
                self.start_node.rectangle = None
            
            self.start_node = self.grid[x][y]
            self.start_node.rectangle = self.canvas2.create_rectangle(self.start_node.x * self.size , self.start_node.y * self.size,
                                                                    self.start_node.x * self.size + self.size , self.start_node.y * self.size + self.size,
                                                                        fill="limegreen")
        if self.val == 2:
            if self.start_node != None:
                if self.start_node.x == x and self.start_node.y == y:
                    return
            if self.goal_node != None:
                if self.goal_node.x == x and self.goal_node.y == y:
                    return
            if self.grid[x][y].obstacle == 1:
                return
            if self.goal_node != None:
                self.canvas2.delete(self.goal_node.rectangle)
                self.goal_node.rectangle = None
            
            self.goal_node = self.grid[x][y]
            self.goal_node.rectangle = self.canvas2.create_rectangle(self.goal_node.x * self.size , self.goal_node.y * self.size,
                                                                    self.goal_node.x * self.size + self.size , self.goal_node.y * self.size + self.size,
                                                                        fill="red")
        
        #sets selected node as obstacle(can be multiple)
        if self.val == 3:
            if self.start_node != None:
                if self.start_node.x == x and self.start_node.y == y:
                    return
            if self.goal_node != None:
                if self.goal_node.x == x and self.goal_node.y == y:
                    return
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
        

    # sets a node as a source node
    def add_source(self):
        if self.val != 0:
            self.val = 1

    # sets a node as goal node
    def add_goal(self):
        if self.val != 0:
            self.val = 2

    # sets a node as an obstacle
    def add_obstacle(self):
        if self.val != 0:
            self.val = 3

    # starts the Chosen Algorithm
    def start(self):
        if self.val != 0:
            self.val = 0
            if self.start_node and self.goal_node:
                if self.clicked1.get() == "BFS":
                    bfs.bfs(self,self.canvas2,self.start_node,self.goal_node,self.grid,self.size)
                if self.clicked1.get() == "DFS":
                    dfs.dfs(self,self.canvas2,self.start_node,self.goal_node,self.grid,self.size)
                if self.clicked1.get() == "A*":
                    astar.astar(self,self.canvas2,self.start_node,self.goal_node,self.grid,self.size)
                
                
            else:
                print("either start node or end node is not set")
            self.val = 4
    
    def resetNode(self,node):
        if node.rectangle != None:
            self.canvas2.delete(node.rectangle)
        node.f = -1
        node.g = -1
        node.h = -1
        node.obstacle = 0
        node.prevNode = None
        node.rectangle = None
        
    # Resets the board
    def reset(self):
        
        if self.val != 0:
            if self.clicked2.get() == "Clear All":
                if self.goal_node != None:
                    self.resetNode(self.goal_node)
                    self.goal_node = None
                if self.start_node != None:
                    self.resetNode(self.start_node)
                    self.start_node = None
                for i in range(len(self.grid)):
                    for j in range(len(self.grid[i])):
                        self.resetNode(self.grid[i][j])
                self.mode = 0
                self.val = 1
                
            if self.clicked2.get() == "Clear ALL except Maze":
                self.val = 0
                if self.goal_node != None:
                    self.resetNode(self.goal_node)
                    self.goal_node = None
                if self.start_node != None:
                    self.resetNode(self.start_node)
                    self.start_node = None
                for i in range(len(self.grid)):
                    for j in range(len(self.grid[i])):
                        node = self.grid[i][j]
                        if node.obstacle == 1:
                            continue
                        self.resetNode(self.grid[i][j])
                self.mode = 1
                self.val = 1
    
    

    # Mage Generating Function
    def create_maze(self):
        if self.goal_node and self.start_node:
            
            self.canvas2.delete(self.goal_node.rectangle)
            self.canvas2.delete(self.start_node.rectangle)
            self.goal_node = None
            self.start_node = None
        for i in range(self.cols):
                for j in range(self.rows):
                    node = self.grid[i][j]
                    if node.obstacle == 1:
                        node.obstacle = 0
                        self.canvas2.delete(node.rectangle)
                        node.rectangle = None
        self.prims()
        
        
        for i in range(self.cols):
                for j in range(self.rows):
                    node = self.grid[i][j]
                    if node.obstacle == 1:
                        node.rectangle = self.canvas2.create_rectangle(node.x * self.size , node.y * self.size,
                                                                node.x * self.size + self.size , node.y * self.size + self.size,
                                                                fill="black")
                    self.canvas2.update()
    
    # finds a random node for Prims Algorithm
    def random_node(self,choice):
        if choice == 0:
            x = random.randint(0,44)
            y = random.randint(0,29)
            return self.grid[x][y]
        else:
            if self.frontier:
                return random.choice(self.frontier)
            else :
                return
    # using Prims Algorithm for Mage Generation
    def prims(self):
        if self.mode == 0:
            for i in range(self.cols):
                for j in range(self.rows):
                    self.grid[i][j].obstacle = 1
        
            current_node = self.random_node(0)
            current_node.obstacale = 0
            self.cal_frontier_node(current_node)
            print(current_node.x,current_node.y)
            self.mode =1
        
        if len(self.frontier) == 0 :
            return
            
        current_node = self.random_node(1)
        self.frontier.remove(current_node)
        current_node.obstacle = 0
        connection_node = current_node.ConNode
        
        a = connection_node.x - current_node.x
        if a > 0:
            node = self.grid[connection_node.x-1][connection_node.y]
            node.obstacle = 0
        elif a < 0:
            node = self.grid[connection_node.x+1][connection_node.y]
            node.obstacle = 0
        else:
            b = connection_node.y - current_node.y
            if b > 0:
                node = self.grid[connection_node.x][connection_node.y-1]
                node.obstacle = 0
            elif b < 0:
                node = self.grid[connection_node.x][connection_node.y+1]
                node.obstacle = 0
        self.cal_frontier_node(current_node)
        self.canvas2.update()
        self.prims()


        
    def cal_frontier_node(self,node):
        x = node.x
        y = node.y
        if x-2 >=  0:
            if self.grid[x-2][y] not in self.frontier and self.grid[x-2][y].obstacle == 1:
                self.grid[x-2][y].ConNode = node
                self.frontier.append(self.grid[x-2][y])
            
        if x+2 < self.cols :
            if self.grid[x+2][y] not in self.frontier and self.grid[x+2][y].obstacle == 1:
                self.grid[x+2][y].ConNode = node
                self.frontier.append(self.grid[x+2][y])
        if y-2 >= 0:
            if self.grid[x][y-2] not in self.frontier and self.grid[x][y-2].obstacle == 1:
                self.grid[x][y-2].ConNode = node
                self.frontier.append(self.grid[x][y-2])
        if y+2 < self.rows:
            if self.grid[x][y+2] not in self.frontier and self.grid[x][y+2].obstacle == 1:
                self.grid[x][y+2].ConNode = node
                self.frontier.append(self.grid[x][y+2])


app = Application()
app.mainloop()