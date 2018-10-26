from easycanvas import EasyCanvas
import sys
from typing import *

Folleto = Tuple[int, int, int]
PosicionFolleto = Tuple[int, int, int, int]


class ImprentaViewer(EasyCanvas):
    def __init__(self, nom_fich_trabajos: str, nom_fich_solucion: str):
        EasyCanvas.__init__(self)
        try:
            self.pageSize, self.foil_dict = ImprentaViewer.dict_imprenta(nom_fich_trabajos)
        except Exception:
            print("ERROR leyendo fichero '{0}".format(nom_fich_trabajos))
            sys.exit()
        try:
            self.sol = ImprentaViewer.lee_fichero_solucion(nom_fich_solucion)
        except Exception:
            print("ERROR leyendo fichero '{0}".format(nom_fich_solucion))
            sys.exit()
        self.num_pages = max(s[1] for s in self.sol)

    @staticmethod
    def dict_imprenta(nom_fich: str) -> Tuple[int, Dict[int, Tuple[int, int]]]:
        f = open(nom_fich)
        paper_size = int(f.readline())
        foil_dict = {}
        for lin in f:
            t = lin.strip().split()
            foil_dict[int(t[0])] = (int(t[1]), int(t[2]))
        return paper_size, foil_dict

    @staticmethod
    def lee_fichero_solucion(nom_fich: str) -> List[PosicionFolleto]:
        f = open(nom_fich)
        sol = []
        for lin in f:
            a, b, c, d = lin.split()
            sol.append((int(a), int(b), int(c), int(d)))
        return sol

    def show_page(self, page_id: int):
        self.erase()
        for f_id, x, y in ((s[0], s[-2], s[-1]) for s in self.sol if s[1] == page_id):
            sx, sy = self.foil_dict[f_id]
            self.create_filled_rectangle(x, y, x + sx, y + sy, "black", "red")

    def main(self):
        self.easycanvas_configure(title='ImprentaViewer',
                                  background='white',
                                  size=(800, 800),
                                  coordinates=(0, 0, self.pageSize, self.pageSize))

        print("*" * 30)
        print("IMPORTANTE:")
        print(
            "   Pon el foco en la ventana gráfica y muévete por las hojas con las fechas del cursor 'izquierda' y 'derecha'.")
        print("*" * 30)
        page = 1
        while True:
            self.show_page(page)
            self.create_text(50, 0, "{0}".format(page), 20, anchor="S")
            key = self.readkey(True)
            if key == 'Right':
                page = page + 1 if page < self.num_pages else 1
            elif key == 'Left':
                page = page - 1 if page > 1 else self.num_pages
            elif key == 'Escape':
                break


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("USO:\n\tpython3 visualizador_solucion_imprenta.py <ficheroImprenta.txt> <ficheroSolucion.txt>")
    else:
        ImprentaViewer(sys.argv[1], sys.argv[2]).run()
