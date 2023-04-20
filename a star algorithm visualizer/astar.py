import time

class astar:
    def __init__(self,root : None, canvas : None,start_node : None,end_node : None,grid : None,size : 0):
        self.root = root
        self.canvas = canvas
        self.start_node = start_node
        self.end_node = end_node
        self.grid = grid
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.size = size
        self.algo()

    
    def algo(self):
        openset = []
        openset.append(self.start_node)
        while(len(openset)!=0):
            current_node = self.get_min(openset)
            # if current_node != self.start_node and current_node != self.end_node:
            #     current_node.rectangle = self.canvas.create_rectangle(current_node.x * self.size , current_node.y * self.size 
            #                                 ,current_node.x * self.size + self.size , current_node.y * self.size + self.size,fill="brown")
            if current_node == self.end_node :
                self.path(current_node)
                return 
            openset.remove(current_node)
            myneighbours = self.neighbours(current_node)

            for neighbour in myneighbours:     
                if neighbour == self.start_node:
                    continue
                tentative_gscore = current_node.g + 1
                if neighbour.g == -1 or  tentative_gscore <neighbour.g:
                    neighbour.prevNode = current_node
                    neighbour.g = tentative_gscore
                    neighbour.h = self.find_h(neighbour)
                    neighbour.f = tentative_gscore + neighbour.h

                    if neighbour not in openset:
                        openset.append(neighbour)
            self.canvas.update()
            # time.sleep(0.1)
        print("empty")

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

    def get_min(self,set):
        set.sort(key=lambda node: node.f)
        key = set[0]
        new_list = []
        for element in set:
            if element.f == key.f:
                new_list.append(element)
            else:
                break
        new_list.sort(key=lambda node: node.h)
        return new_list[0]

    def find_h(self,node):
        x = node.x
        y = node.y
        return abs(self.end_node.x-x)+abs(self.end_node.y-y)
    
    def path(self,current_node):
        Result = []
        Result.append(current_node)
        self.canvas.delete(current_node.rectangle)
        current_node.rectangle = self.canvas.create_rectangle(current_node.x*self.size,current_node.y*self.size,
                                        current_node.x*self.size+self.size,current_node.y*self.size+self.size,fill="light green")
        while current_node.prevNode != None:
            current_node = current_node.prevNode
            self.canvas.delete(current_node.rectangle)
            current_node.rectangle=self.canvas.create_rectangle(current_node.x*self.size,current_node.y*self.size,
                                            current_node.x*self.size+self.size,current_node.y*self.size+self.size,fill="light green")
            self.canvas.update()
            time.sleep(0.1)
            Result.append(current_node)
        return







