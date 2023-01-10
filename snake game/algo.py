class node:
    def __init__(self,i,j) -> None:
        self.x = i
        self.y = j
        self.f = -1
        self.g = -1
        self.h = -1
        self.prevNode = None
        pass


def find_h(node):
    x = node.x
    y = node.y
    return abs(goal_node.x-x)+abs(goal_node.y-y)

def print_grid():
    for i in range(rows):
        for j in range(cols):
            node  = grid[i][j]
            print("(" + str(node.x) + "," + str(node.y) + ") ----> "+str(node.f)+" = "+str(node.g)+" + "+str(node.h))

def neighbours(node):
    # return list of neighbours of current from the grid
    x = node.x
    y = node.y
    n = []
    # print("\n indexes "+str(x)+"  "+str(y))

    if x < rows-1:
        n.append(grid[x+1][y])
    if y < cols-1:
        n.append(grid[x][y+1])
    if x > 0:
        n.append(grid[x-1][y])
    if y > 0:
        n.append(grid[x][y-1])
    return n

def print_openset():
    print("[",end=" ")
    for node in openset:
        print("("+str(node.x)+","+str(node.y)+",f "+str(node.f)+")",end=" , ")
    print("]\n")

def print_Result():
    print("Result")
    print("[",end=" ")
    for node in Result:
        print("("+str(node.x)+","+str(node.y)+")",end=" , ")
    print("]")


def path(current_node):
    Result.append(current_node)
    while current_node.prevNode != None:
        current_node = current_node.prevNode
        Result.append(current_node)
    print_Result()


def algo():
    openset.append(start_node)
    # print_openset()
    # print_grid()
    while(len(openset)!=0):
        openset.sort(key=lambda node: node.f)
        current_node = openset[0]
        print("current : (" + str(current_node.x) +","+ str(current_node.y)+") ---> " + str(current_node.f)+"=" + str(current_node.g) + "+" + str(current_node.h))
        if current_node == goal_node :
            path(current_node)
            return 
        openset.remove(current_node)
        myneighbours = neighbours(current_node)

        for neighbour in myneighbours:
            print("neighbour :" + str(neighbour.x) + " " + str(neighbour.y))
            
            tentative_gscore = current_node.g +cost
            if neighbour.g == -1 or tentative_gscore <neighbour.g:
                neighbour.prevNode = current_node
                neighbour.g = tentative_gscore
                neighbour.h = find_h(neighbour)
                neighbour.f = tentative_gscore + neighbour.h

                if neighbour not in openset:
                    openset.append(neighbour)
        print_openset()
        # return



grid=[]
rows = 4
cols = 4
for i in range(cols):
    column = []
    for j in range(rows):
        column.append(node(i,j))
    grid.append(column)
start_node = grid[0][0]
start_node.f = 0
start_node.g = 0
start_node.h = 0
goal_node = grid[0][2]
cost = 1
openset=[]
Result=[]
algo()
