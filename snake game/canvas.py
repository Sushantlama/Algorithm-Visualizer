from tkinter import *
import time
class node:
    def __init__(self,i,j) -> None:
        self.x = i
        self.y = j
        self.f = -1
        self.g = -1
        self.h = -1
        self.obstacle = 0
        self.prevNode = None



def motion(event):
    global goal_node,source_node
    x = int(event.x/50)
    y = int(event.y/50)
    # print("Mouse position: "+str(x) + " " +str(y))
    # print("Mouse position: "+str(int(x/50)) + " " +str(int(y/50)))
    canvas.create_rectangle(x*width,y*width,x*width+width,y*width+width,fill=color)
    if color == "red":
        goal_node = grid[x][y]
    if color == "black":
        grid[x][y].obstacle = 1
    if color == "blue":
        source_node = grid[x][y]

def create_goal():
    global color,goal_set
    if goal_set == 0:
        color = "red"
        goal_set = 1

def create_obstacle():
    global color,obstacle_set
    color = "black"
    obstacle_set = 1

def create_source():
    global color,source_set
    if source_set == 0:
        color = "blue"
        source_set = 1

def start():
    # if obstacle_set == 1 and source_set == 1 and goal_set == 1:
    algo()


def algo():
    openset.append(source_node)
    # print_openset()
    # print_grid()
    while(len(openset)!=0):
        openset.sort(key=lambda node: node.f)

        current_node = openset[0]
        
        if current_node != source_node and current_node != goal_node:
            current_rec = canvas.create_rectangle(current_node.x*width,current_node.y*width,current_node.x*width+width,current_node.y*width+width,fill="brown")
        # print("current : (" + str(current_node.x) +","+ str(current_node.y)+") ---> " + str(current_node.f)+"=" + str(current_node.g) + "+" + str(current_node.h))
        if current_node == goal_node :
            path(current_node)
            return 
        openset.remove(current_node)
        myneighbours = neighbours(current_node)

        for neighbour in myneighbours:
            # print("neighbour :" + str(neighbour.x) + " " + str(neighbour.y))
            
            tentative_gscore = current_node.g +cost
            if neighbour.g == -1 or tentative_gscore <neighbour.g:
                neighbour.prevNode = current_node
                neighbour.g = tentative_gscore
                neighbour.h = find_h(neighbour)
                neighbour.f = tentative_gscore + neighbour.h

                if neighbour not in openset:
                    openset.append(neighbour)
                    if(neighbour!=goal_node and neighbour != source_node):
                        canvas.create_rectangle(neighbour.x*width,neighbour.y*width,neighbour.x*width+width,neighbour.y*width+width,fill="green")
        root.update()
        time.sleep(0.3)
        # print_openset()
        # return

def neighbours(node):
    # return list of neighbours of current from the grid
    x = node.x
    y = node.y
    n = []
    # print("\n indexes "+str(x)+"  "+str(y))
    if x < row-1:
        if(grid[x+1][y].obstacle == 0):
            n.append(grid[x+1][y])
    if y < col-1:
        if(grid[x][y+1].obstacle == 0):
            n.append(grid[x][y+1])
    if x > 0:
        if(grid[x-1][y].obstacle == 0):
            n.append(grid[x-1][y])
    if y > 0:
        if(grid[x][y-1].obstacle == 0):
            n.append(grid[x][y-1])
    return n

def find_h(node):
    x = node.x
    y = node.y
    return abs(goal_node.x-x)+abs(goal_node.y-y)

def path(current_node):
    Result.append(current_node)
    canvas.create_rectangle(current_node.x*width,current_node.y*width,current_node.x*width+width,current_node.y*width+width,fill="blue")
    while current_node.prevNode != None:
        current_node = current_node.prevNode
        canvas.create_rectangle(current_node.x*width,current_node.y*width,current_node.x*width+width,current_node.y*width+width,fill="blue")
        canvas.update()
        time.sleep(0.2)
        Result.append(current_node)
    # print_Result()






root = Tk()
root.resizable(False,False)
width = 50
row = 10
col = 10
canvas = Canvas(root,width=500,height=500,background="white")
canvas.pack()
color = "black"

grid = []
for i in range(col):
    column = []
    for j in range(row):
        column.append(node(i,j))
    grid.append(column)

goal_node = grid[row-1][col-1]
source_node = grid[0][0]

cost = 1
openset=[]
Result=[]
obstacle_set = 0
goal_set = 0
source_set = 0

for i in range(row):
    canvas.create_line(0,i*width,500,i*width,fill="black")
for j in range(col):
    canvas.create_line(j*width,0,j*width,500,fill="black")


obstacle_btn = Button(root,text="Set Obstacle",width=40,height=2,command=create_obstacle)
obstacle_btn.pack()
source_btn = Button(root,text="Set Source",width=40,height=2,command=create_source)
source_btn.pack()
goal_btn = Button(root,text="Set Goal",width=40,height=2,command=create_goal)
goal_btn.pack()
start_btn = Button(root,text="Start Path",width=40,height=2,command=start)
start_btn.pack()

canvas.bind('<Button-1>',motion)

root.mainloop()
