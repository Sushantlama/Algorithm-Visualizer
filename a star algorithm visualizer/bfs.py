import time

class bfs:
    def __init__(self,root : None, canvas : None,start_node : None,end_node : None,grid : None,size : 0):
        self.root = root
        self.canvas = canvas
        self.start_node = start_node
        self.end_node = end_node
        self.grid = grid
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.visited = [[0 for i in range(self.cols)] for j in range(self.rows)]
        self.queue = []
        self.queue.append(self.start_node)
        self.size = size
        self.algo()

    
    def algo(self):
        while(len(self.queue)):
            current_node = self.queue.pop(0)
            if(current_node.rectangle != None):
                self.canvas.delete(current_node.rectangle)    
                current_node.rectangle = self.canvas.create_rectangle(current_node.x * self.size , current_node.y * self.size 
                                                ,current_node.x * self.size + self.size , current_node.y * self.size + self.size,fill="navy")
            self.canvas.update()
            time.sleep(0.1)
            myneighbours = self.neighbours(current_node)

            for neighbour in myneighbours:     
                if(not self.visited[neighbour.x][neighbour.y] ):
                    count = self.queue.count(neighbour)
                    if(count==0):
                        neighbour.prevNode = current_node
                        self.queue.append(neighbour)
                        if(neighbour == self.end_node):
                            self.path(neighbour)
                            print("Found")
                            return
                        neighbour.rectangle = self.canvas.create_rectangle(neighbour.x * self.size , neighbour.y * self.size 
                                                ,neighbour.x * self.size + self.size , neighbour.y * self.size + self.size,fill="deepskyblue")
            self.visited[current_node.x][current_node.y] = True
            self.canvas.update()
            time.sleep(0.1)
            self.canvas.delete(current_node.rectangle)
            if current_node != self.start_node:
                current_node.rectangle = self.canvas.create_rectangle(current_node.x * self.size , current_node.y * self.size 
                                                ,current_node.x * self.size + self.size , current_node.y * self.size + self.size,fill="lightsteelblue")
            else:
                current_node.rectangle = self.canvas.create_rectangle(current_node.x * self.size , current_node.y * self.size 
                                                ,current_node.x * self.size + self.size , current_node.y * self.size + self.size,fill="limegreen")
            self.canvas.update()
            time.sleep(0.1)
            
        print("Not Found")

    def neighbours(self,node):
        # return list of neighbours of current from the grid
        x = node.x
        y = node.y
        n = []

        if x < self.rows - 1:
            if(self.grid[x+1][y].obstacle == 0):
                n.append(self.grid[x+1][y])
        if y < self.cols - 1:
            if(self.grid[x][y+1].obstacle == 0):
                n.append(self.grid[x][y+1])
        if x > 0:
            if(self.grid[x-1][y].obstacle == 0):
                n.append(self.grid[x-1][y])
        if y > 0:
            if(self.grid[x][y-1].obstacle == 0):
                n.append(self.grid[x][y-1])
        return n

    
    def path(self,current_node):
        Result = []
        Result.append(current_node)
        self.canvas.delete(current_node.rectangle)
        current_node.rectangle = self.canvas.create_rectangle(current_node.x*self.size,current_node.y*self.size,
                                        current_node.x*self.size+self.size,current_node.y*self.size+self.size,fill="greenyellow")
        while current_node.prevNode != None:
            current_node = current_node.prevNode
            self.canvas.delete(current_node.rectangle)
            current_node.rectangle=self.canvas.create_rectangle(current_node.x*self.size,current_node.y*self.size,
                                            current_node.x*self.size+self.size,current_node.y*self.size+self.size,fill="greenyellow")
            self.canvas.update()
            time.sleep(0.1)
            Result.append(current_node)
        return







