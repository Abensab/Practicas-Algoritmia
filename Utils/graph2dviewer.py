'''
Created on 02/10/2013

@author: david
'''
from easycanvas import EasyCanvas
from algoritmia.datastructures.digraphs import UndirectedGraph

class Graph2dViewer(EasyCanvas):
    X_Y = 0
    ROW_COL = 1

    def __init__(self, g, window_size=(400,400), vertexmode=X_Y):
        EasyCanvas.__init__(self)

        if not isinstance(g, UndirectedGraph) or \
                any([type(p) != type((1,1)) or
                     len(p) != 2 or
                     type(p[0]) != type(p[1]) for p in g.V]) or \
                any([type(p[0])!=type(1) and type(p[0])!=type(1.0) for p in g.V]):
            raise TypeError("The graph must be an UnirectedGraph. Vertices must be tuples of two integers or floats")

        if vertexmode==Graph2dViewer.ROW_COL:
            if any([type(p[0])!=type(1) for p in g.V]):
                raise TypeError("In this mode, vertices must be tuples of two integers")
            g = UndirectedGraph(V = [(-v[1],v[0]) for v in g.V], E=[((-u[1],u[0]),(-v[1],v[0])) for (u,v) in g.E])
        
        self.g = g
        self.max_y = max(p[1] for p in self.g.V)
        self.max_x = max(p[0] for p in self.g.V)
        self.min_y = min(p[1] for p in self.g.V)
        self.min_x = min(p[0] for p in self.g.V)
        self.window_size = window_size

    def main(self):
        sizex = self.max_x - self.min_x + 1
        sizey = self.max_y - self.min_y + 1
        self.cell_size = min(self.window_size[0]/sizex, self.window_size[1]/sizey)
        m = ((self.window_size[0]-self.cell_size*sizex) / 2 - self.min_x * self.cell_size,
             (self.window_size[1]-self.cell_size*sizey) / 2 - self.min_y * self.cell_size)
        self.easycanvas_configure(title = '2D Graph Viewer',
                                  background = 'white',
                                  size = self.window_size, 
                                  coordinates = (0, 0, self.window_size[0]-1,self.window_size[1]-1))
                
        for u,v in self.g.E:
            self.create_line((u[0]+0.5)*self.cell_size+m[0], (u[1]+0.5)*self.cell_size+m[1], (v[0]+0.5)*self.cell_size+m[0], (v[1]+0.5)*self.cell_size+m[1])
         
        for u in self.g.V:
            self.create_filled_circle((u[0]+0.5)*self.cell_size+m[0], (u[1]+0.5)*self.cell_size+m[1], self.cell_size/8, relleno='palegreen')
        # Wait for a key   
        self.readkey(True)
        
if __name__ == '__main__':
    viewer = Graph2dViewer(UndirectedGraph(E=[((-5,-1), (0,0)), ((0,0),(1,1))]), window_size=(400, 200))
    viewer.run()
