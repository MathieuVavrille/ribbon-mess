from tkinter import *

import random

colors = ["#FE6A6A","#ED91B6","#FFD7FC","#DF93FF","#BEE1E3","#B0CFFE","#BA96FF","#A7FCDB","#A6E8AA","#CCFCA6","#F9FF91","#997D65","#F1956E","#FCB96B","#EAD376"]
#C3C2E2,CCCCCC

class Ribbon:
    def __init__(self):
        self.elements = []

    def append(self, value):
        self.elements.append(value)

    def __getitem__(self, i):
        return self.elements[i]

class RibbonElement:
    def __init__(self):
        self.isTurn = False

class Grid:
    def __init__(self,grid):
        self.grid=grid

    def __len__(self):
        return len(self.grid)

    def height(self, value, i, j):
        return self.grid[i][j].index(value)

    def __getitem__(self, i):
        return self.grid[i]

class State:
    def __init__(self, grid, horizontal_ribbons, vertical_ribbons):
        self.grid=grid
        self.horizontal = horizontal_ribbons
        self.vertical = vertical_ribbons

    def plot(self):
        empty_line = "  "+" ".join("|" for i in range(len(self.grid[0])))+"  "
        print(empty_line)
        for i in range(len(self.grid)):
            line = "−−"+"−".join("−" if self.grid.height(self.horizontal[i][j],i,j)==1 else "|" for j in range(len(self.grid[i])))+"−−"
            print(line)
            print(empty_line)

    def generate_intersection_coordinates(self):
        intersections = [[[None]*len(inters) for inters in line] for line in self.grid]
        for i in range(len(self.grid)):
            pass
        

def generate_random_state(n):
    grid=[[[RibbonElement(),RibbonElement] for i in range(n)] for j in range(n)]
    horizontal_on_top = [[random.randrange(0,2) for i in range(n)] for j in range(n)]
    print(horizontal_on_top)
    horizontal_ribbons = [Ribbon() for i in range(n)]
    vertical_ribbons = [Ribbon() for j in range(n)]
    for i in range(n):
        for j in range(n):
            horizontal_ribbons[i].append(grid[i][j][horizontal_on_top[i][j]])
            vertical_ribbons[j].append(grid[i][j][1-horizontal_on_top[i][j]])
    return State(Grid(grid), horizontal_ribbons, vertical_ribbons)







class Application(Frame):

    def __init__(self, master = None):
        """Initialization of all the data"""
        Frame.__init__(self, master)
        self.grid()
        self.bind_all("<Escape>", lambda x:self.quit())
        self.canv = Canvas(self, height = 500, width = 500, relief="ridge",borderwidth=20)
        self.canv.grid(column = 0, columnspan = 5, row = 0, rowspan = 5)
        self.canv.create_line(22,100,350,100,width=20,fill=colors[0])
        #self.canv.bind("<Button-1>", self._click)

    def plot_state(self, state):
        pass
                    
    def _exit(self, event):
        """Exit event function"""
        self.quit()


if __name__ == "__main__":
    state = generate_random_state(10)
    state.plot()
    app = Application()
    app.mainloop()
