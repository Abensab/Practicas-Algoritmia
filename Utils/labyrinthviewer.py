'''
2016-09-28: Versión 1.2
2015-10-05: Versión 1.1
2012-10-03: Version 1
@author: David Llorens dllorens@uji.es

Dibuja un laberinto a partir de un grafo no dirigido con las siguientes características:
- Los vértices son tuplas de enteros (fila, columna) que se corresponden con las celdas 
  del laberinto. El vértice (0,0) se corresponde en el dibujo con la celda superior 
  izquierda del laberinto.
- Sólo puede haber una arista entre dos vértices si se corresponden a celdas vecinas en 
  el laberinto: La existencia de una arista significa que entre dichas celdas del laberinto 
  NO hay muro.
'''

from easycanvas import EasyCanvas
from algoritmia.datastructures.digraphs import UndirectedGraph

class LabyrinthViewer(EasyCanvas):
    def __init__(self, lab, canvas_width=400, canvas_height=400, margin=10):
        EasyCanvas.__init__(self)
        
        # check 'lab' type
        if not isinstance(lab, UndirectedGraph) or \
           any([type(p)!=type((1,1)) or len(p)!=2 or type(p[0])!=type(1) or type(p[1])!=type(1) for p in lab.V]):
            raise TypeError("The labyrinth must be an UnirectedGraph of two integer tuples")
        
        self.lab = lab
        self.paths=[]
        self.marked_cells=[]
        self.margin = margin
        self.max_col = max(p[1] for p in self.lab.V)
        self.max_row = max(p[0] for p in self.lab.V)
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.cell_size = min (float((canvas_width-margin)/(self.max_col+1)), float((canvas_height-margin)/(self.max_row+1)))
        self.mw = self.canvas_width - self.cell_size*(self.max_col+1)
        self.mh = self.canvas_height - self.cell_size*(self.max_row+1)
        self.ip = self.op = None
        
      
    def set_input_point(self, pos):
        self.ip = pos
        
    def set_output_point(self, pos):
        self.op = pos
        
    def add_marked_cell(self, cell, color='red', ): 
        self.marked_cells.append((cell, color))
    
 
    def add_path(self, path, color='red', offset=0): 
        self.paths.append((path, color, offset))
        
    def _draw_path(self,path,color,offset):
        u = path[0]
        m = self.cell_size/2+offset
        mw2 = self.mw/2+self.cell_size/2+offset
        mh2 = self.mh/2+self.cell_size/2+offset
        for v in path[1:]:
            self.create_line(mw2+u[1]*self.cell_size, mh2+u[0]*self.cell_size, mw2+v[1]*self.cell_size, mh2+v[0]*self.cell_size, color)
            u = v
                   
    def main(self):
        mw = self.mw
        mh = self.mh
        
        self.easycanvas_configure(title = 'Labyrinth',
                                  background = 'white',
                                  size = (self.canvas_width, self.canvas_height), 
                                  coordinates = (0, self.canvas_height, self.canvas_width, 0))

        # Draw borders
        self.create_rectangle(mw/2, mh/2, self.canvas_width-mw/2, self.canvas_height-mh/2)

        # Draw I and O on input and output cells
        if self.ip != None:
            self.create_text(mw/2+(self.ip[1]+0.5)*self.cell_size, mh/2+(self.ip[0]+0.5)*self.cell_size, "I", self.cell_size/1.5, "CENTER", "black")
        if self.op != None:
            self.create_text(mw/2+(self.op[1]+0.5)*self.cell_size, mh/2+(self.op[0]+0.5)*self.cell_size, "O", self.cell_size/1.5, "CENTER", "black")
            
        # Draw marked cells    
        for cell, color in self.marked_cells:
            self.create_filled_circle(mw/2+cell[1]*self.cell_size+self.cell_size/2, mh/2+cell[0]*self.cell_size+self.cell_size/2, self.cell_size/2.5-1, 'black', color)

        # Draw internal walls
        for r in range(self.max_row+1):
            for c in range(self.max_col+1):
                u = r, c
                x = c*self.cell_size
                y = r*self.cell_size
                
                if u not in self.lab.V or (r+1,c) not in self.lab.succs(u):
                    self.create_line(mw/2+x, mh/2+y+self.cell_size, mw/2+x+self.cell_size, mh/2+y+self.cell_size)
        
                if u not in self.lab.V or (r,c+1) not in self.lab.succs(u):
                    self.create_line(mw/2+x+self.cell_size, mh/2+y, mw/2+x+self.cell_size, mh/2+y+self.cell_size)
         
        for path, color, offset in self.paths:
            self._draw_path(path, color, offset)
        
        # Wait for a key   
        self.readkey(True)
        