from tkinter import *

import random
random.seed(98)

main_colors = ["#FE6A6A","#ED91B6","#FFD7FC","#DF93FF","#BEE1E3","#B0CFFE","#BA96FF","#A7FCDB","#A6E8AA","#CCFCA6","#F9FF91","#997D65","#F1956E","#FCB96B","#EAD376"]
dark_colors20 = ["#FE2222","#e24f8a","#ff79f5","#c743ff","#84c6ca","#5b9bfd","#8545ff","#56f9ba","#67d86e","#9ef955","#e3f000","#7a6451","#eb662e","#fb9825","#e1bf39"]# 40 for yellow F9FF91
nb_colors = 15
BORDERWIDTH = 4
#C3C2E2,CCCCCC

WIDTH = 1000


class Ribbon:
    def __init__(self):
        self.elements = []
        self.is_top_left = True

    def append(self, value):
        self.elements.append(value)

    def __getitem__(self, i):
        return self.elements[i]

    def invert(self):
        self.elements = self.elements[::-1]
        self.is_top_left = not self.is_top_left

    def generate_positions(self):
        initial_direction = self.is_top_left
        elements_sizes = [1/2]
        for elt in self.elements:
            if elt.isTurn:
                elements_sizes[-2] -= 1/12
                elements_sizes[-1] = -1/12
            else:
                elements_sizes[-1]+= 1
                elements_sizes.append(0)
        elements_sizes[-1]+= 1/2
        total=sum(elements_sizes)
        y_positions = [0]
        sub_total = 0
        for size in elements_sizes:
            sub_total += size
            y_positions.append(sub_total/total)
        x_positions = [0]
        direction = 1 if self.is_top_left else -1
        i = 0
        for elt in self.elements:
            if elt.isTurn:
                direction = -direction
            else:
                x_positions.append(elements_sizes[i]*direction+x_positions[-1])
                i += 1
        x_positions[-1]+= direction/2
        return x_positions, y_positions

    def fold_start(self, grid, is_vertical, pos, update_function):
        def aux(evt):
            print("fold_start", is_vertical, pos)
            update_function()
        return aux

    def fold_end(self, grid, is_vertical, pos, update_function):
        def aux(evt):
            
            if not is_vertical:# is_horizontal
                i = pos
                if grid.contains(pos,len(grid[0])-1,self.elements[-1]):
                    j = len(grid.grid[0])-1
                    diff = -1
                elif grid.contains(pos, 0, self.elements[-1]):
                    j = 0
                    diff = 1
                else:
                    raise ValueError("end not on the end ???")
                print(grid.height(pos, j, self.elements[-1]))
                height = grid.height(pos, j, self.elements[-1])
                if height == 0:
                    is_on_top = False
                elif height == len(grid[pos][j])-1:
                    is_on_top = True
                else:
                    raise ValueError("Not possible to turn, should raise error later")
                while self.elements and not self.elements[-1].isTurn and grid.height(pos, j, self.elements[-1]) == (len(grid[pos][j])-1 if is_on_top else 0):
                    grid[pos][j].remove(self.elements[-1])
                    self.elements.pop()
                    j += diff
                print(j)
                if self.elements:
                    if self.elements[-1].isTurn:
                        self.elements.pop()
                    else:
                        self.elements.append(RibbonElement(True))
                while 0 <= j < len(grid[pos]):
                    self.elements.append(RibbonElement())
                    if is_on_top:
                        grid[pos][j].append(self.elements[-1])
                    else:
                        grid[pos][j].insert(0, self.elements[-1])
                    j += diff
                print(j,diff, is_on_top)
                                  
            print("fold_end", is_vertical, pos)
            update_function()
        return aux

    def __repr__(self):
        return "Ribbon("+",".join(map(str, self.elements))+")"
        

class RibbonElement:
    def __init__(self, isTurn = False):
        self.isTurn = isTurn

class Grid:
    def __init__(self,grid):
        self.grid=grid

    def __len__(self):
        return len(self.grid)

    def height(self, i, j, value):
        return self.grid[i][j].index(value)

    def __getitem__(self, i):
        return self.grid[i]

    def contains(self, i, j, value):
        return value in self.grid[i][j]

                                  

class State:
    def __init__(self, grid, horizontal_ribbons, vertical_ribbons):
        self.grid=grid
        self.horizontal = horizontal_ribbons
        self.vertical = vertical_ribbons

    def plot(self):
        empty_line = "  "+" ".join("|" for i in range(len(self.grid[0])))+"  "
        print(empty_line)
        for i in range(len(self.grid)):
            line = "−−"+"−".join("−" if self.grid.height(i,j,self.horizontal[i][j])==1 else "|" for j in range(len(self.grid[i])))+"−−"
            print(line)
            print(empty_line)

    def generate_intersection_coordinates(self):
        N=len(self.grid)
        cell_size = WIDTH/(N+1)
        intersections = [[[None]*len(inters) for inters in line] for line in self.grid]
        for i in range(len(self.grid)):
            xposs, yposs = self.horizontal[i].generate_positions()
            xpos = 0 if self.horizontal[i].is_top_left else WIDTH
            j = 0 if self.horizontal[i].is_top_left else N
            direction = 1 if self.horizontal[i].is_top_left else -1
            start_ypos = (5/6+i)*cell_size
            cpt = 0
            for elt_id in range(len(self.horizontal[i].elements)):
                elt = self.horizontal[i].elements[elt_id]
                if elt.isTurn:
                    direction = -direction
                    j += direction
                else:
                    height = self.grid.height(i,j,elt)
                    intersections[i][j][height] = ((BORDERWIDTH+(xpos+xposs[cpt])*cell_size-direction*7, BORDERWIDTH+start_ypos+yposs[cpt]*cell_size/3, BORDERWIDTH+(xpos+xposs[cpt+1])*cell_size+direction*7, BORDERWIDTH+start_ypos+yposs[cpt+1]*cell_size/3),
                                                   (main_colors[i%8], dark_colors20[i%8]),
                                                   f"horizontal-start-{i}" if elt_id == 0 else f"horizontal-end-{i}" if elt_id == len(self.horizontal[i].elements)-1 else "nothing",
                                                   (BORDERWIDTH+(xpos+xposs[cpt])*cell_size, BORDERWIDTH+start_ypos+yposs[cpt]*cell_size/3, BORDERWIDTH+(xpos+xposs[cpt+1])*cell_size, BORDERWIDTH+start_ypos+yposs[cpt+1]*cell_size/3))# todo for tag add test if not surrounded
                    cpt += 1
                    j += direction
        for j in range(len(self.vertical)):
            xposs, yposs = self.vertical[j].generate_positions()
            xpos = 0 if self.vertical[j].is_top_left else WIDTH
            i = 0 if self.vertical[j].is_top_left else N
            direction = 1 if self.vertical[j].is_top_left else -1
            start_ypos = (5/6+j)*cell_size
            cpt = 0
            for elt_id in range(len(self.vertical[j].elements)):
                elt = self.vertical[j].elements[elt_id]
                if elt.isTurn:
                    direction = -direction
                    i += direction
                else:
                    height = self.grid.height(i,j,elt)
                    intersections[i][j][height] = ((BORDERWIDTH+start_ypos+yposs[cpt]*cell_size/3, BORDERWIDTH+(xpos+xposs[cpt])*cell_size-direction*3, BORDERWIDTH+start_ypos+yposs[cpt+1]*cell_size/3, BORDERWIDTH+(xpos+xposs[cpt+1])*cell_size+direction*3),
                                                   (main_colors[j%7+8], dark_colors20[j%7+8]),
                                                   f"vertical-start-{j}" if elt_id == 0 else f"vertical-end-{j}" if elt_id == len(self.vertical[j].elements)-1 else "nothing",
                                                   (BORDERWIDTH+start_ypos+yposs[cpt]*cell_size/3, BORDERWIDTH+(xpos+xposs[cpt])*cell_size-direction, BORDERWIDTH+start_ypos+yposs[cpt+1]*cell_size/3, BORDERWIDTH+(xpos+xposs[cpt+1])*cell_size+direction))
                    cpt += 1
                    i += direction
        return intersections        

def generate_random_state(n):
    grid=[[[RibbonElement(),RibbonElement()] for i in range(n)] for j in range(n)]
    horizontal_on_top = [[random.randrange(0,2) for i in range(n)] for j in range(n)]
    horizontal_ribbons = [Ribbon() for i in range(n)]
    vertical_ribbons = [Ribbon() for j in range(n)]
    for i in range(n):
        for j in range(n):
            horizontal_ribbons[i].append(grid[i][j][horizontal_on_top[i][j]])
            vertical_ribbons[j].append(grid[i][j][1-horizontal_on_top[i][j]])
    return State(Grid(grid), horizontal_ribbons, vertical_ribbons)







class Application(Frame):

    def __init__(self, nb_ribbons = 10, size=WIDTH, master = None):
        """Initialization of all the data"""
        Frame.__init__(self, master)
        self.grid()
        self.bind_all("<Escape>", lambda x:self.quit())
        self.canv = Canvas(self, height = size, width = size, relief="ridge", borderwidth = BORDERWIDTH,bg="white")#,bg="#404040")
        self.canv.grid(column = 1, columnspan = 2*nb_ribbons+3, row = 1, rowspan = 2*nb_ribbons+3)
        #self.canv.bind("<Button-1>", self._click)

        self.state = generate_random_state(nb_ribbons)
        self.state.plot()
        #self.state.vertical[2].invert()
        self.update_canvas()

    def update_canvas(self):
        self.canv.delete("all")
        coordinates = self.state.generate_intersection_coordinates()
        line_width = WIDTH/(len(self.state.grid)+1)/3
        for i in range(len(coordinates)):
            for j in range(len(coordinates[i])):
                for k in range(len(coordinates[i][j])):
                    elt,col,tag,back_elt = coordinates[i][j][k]
                    self.canv.create_line(back_elt, width=line_width+10, fill="#000000")
                    self.canv.create_line(elt, width=line_width, fill=col[0], activefill=col[1] if tag!="nothing" else col[0], tags=tag)#, activestipple="gray75", tags=tag)
        for is_vertical in [True, False]:
            for i in range(len(self.state.grid)):
                self.canv.tag_bind(f"{'vertical' if is_vertical else 'horizontal'}-start-{i}","<Button-1>", (self.state.vertical if is_vertical else self.state.horizontal)[i].fold_start(self.state.grid, is_vertical, i, self.update_canvas))
                self.canv.tag_bind(f"{'vertical' if is_vertical else 'horizontal'}-end-{i}","<Button-1>", (self.state.vertical if is_vertical else self.state.horizontal)[i].fold_end(self.state.grid, is_vertical, i, self.update_canvas))
        

    def _click(self, event):
        x, y = event.x-BORDERWIDTH, event.y-BORDERWIDTH
        print(x,y)

                    

if __name__ == "__main__":
    app = Application(5)
    app.mainloop()
