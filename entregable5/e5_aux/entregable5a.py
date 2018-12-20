#####################################################################################################
#  IMPORTANTE:                                                                                      #
#  Sólo tienes que modificar la función find_lower_energy_seam que se encuentra al final del código #
#####################################################################################################

import sys
import tkinter
from copy import deepcopy
from typing import *
from algoritmia.utils import argmin, infinity

MatrixGrayImage = List[List[int]]


class PixelColor:
    def __init__(self, r: int, g: int, b: int):
        self.r, self.g, self.b = r, g, b


MatrixColorImage = List[List[PixelColor]]


class GrayImage:
    def __init__(self, m: MatrixGrayImage):
        if isinstance(m, List) and isinstance(m[0], List) and isinstance(m[0][0], int):
            self.rows: int = len(m)
            self.cols: int = len(m[0])
            self.m: MatrixGrayImage = deepcopy(m)
        else:
            raise Exception("BAD PARAMETER")

    def get_tkinter_image(self, veta=None) -> tkinter.PhotoImage:
        new_image_sc = tkinter.PhotoImage(width=self.cols, height=self.rows)
        for r in range(self.rows):
            im_row = self.m[r]
            for c in range(self.cols):
                v = im_row[c]
                new_image_sc.put("#%02x%02x%02x" % (v, v, v), (c, r))
            if veta is not None:
                new_image_sc.put("#%02x%02x%02x" % (0, 255, 0), (veta[r], r))
        return new_image_sc

    def get_energy_as_grayimage(self) -> "GrayImage":
        min_v = 10e100
        max_v = -10e100
        mat_float = [[0.0] * self.cols for _ in range(self.rows)]
        m = self.m  # para escribir menos
        for r in range(1, self.rows - 1):
            for c in range(1, self.cols - 1):
                sx = m[r - 1][c - 1] + 2 * m[r - 1][c] + m[r - 1][c + 1] - m[r + 1][c - 1] - 2 * m[r + 1][c] - m[r + 1][
                    c + 1]
                sy = m[r - 1][c - 1] + 2 * m[r][c - 1] + m[r + 1][c - 1] - m[r - 1][c + 1] - 2 * m[r][c + 1] - m[r + 1][
                    c + 1]
                v = (sx * sx + sy * sy) ** 0.5
                if v < min_v:
                    min_v = v
                if v > max_v:
                    max_v = v
                mat_float[r][c] = v
            mat_float[r][0] = mat_float[r][2]
            mat_float[r][self.cols - 1] = mat_float[r][self.cols - 3]

        for c in range(self.cols):
            mat_float[0][c] = mat_float[2][c]
            mat_float[self.rows - 1][c] = mat_float[self.rows - 3][c]

        mat: MatrixGrayImage = [[0] * self.cols for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                mat[r][c] = int(255 * (mat_float[r][c] - min_v) / max_v)
        return GrayImage(mat)

    def remove_seam(self, seam: List[int]):
        if self.cols > 1:
            for r in range(self.rows):
                del self.m[r][seam[r]]
            self.cols -= 1


class ColorImage:
    def __init__(self, obj: Union[str, MatrixColorImage]):
        if isinstance(obj, str):  # carga de fichero
            filename = obj
            self.imageOrig = tkinter.PhotoImage(file=filename)
            self.cols = self.imageOrig.width()
            self.rows = self.imageOrig.height()
            self.m: MatrixColorImage = [[PixelColor(0, 0, 0)] * self.cols for _ in range(self.rows)]
            for r in range(self.rows):
                for c in range(self.cols):
                    cr, cg, cb = [int(v) for v in self.imageOrig.get(c, r)]
                    self.m[r][c] = PixelColor(cr, cg, cb)
        elif isinstance(obj, List) and isinstance(obj[0], List) and isinstance(obj[0][0], PixelColor):
            # carga a partir de una matriz de pixels (p.e. colorImage.m)
            m = obj
            self.rows = len(m)
            self.cols = len(m[0])
            self.m = deepcopy(m)
        else:
            raise Exception("BAD PARAMETER")

    def get_tkinter_image(self) -> tkinter.PhotoImage:
        new_tkinter_image = tkinter.PhotoImage(width=self.cols, height=self.rows)
        for r in range(self.rows):
            im_row = self.m[r]
            for c in range(self.cols):
                pc = im_row[c]
                new_tkinter_image.put("#%02x%02x%02x" % (pc.r, pc.g, pc.b), (c, r))
        return new_tkinter_image

    def to_grayimage(self) -> GrayImage:
        mat: MatrixGrayImage = [[0] * self.cols for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                p = self.m[r][c]
                mat[r][c] = int(p.r * 0.3 + p.g * 0.56 + p.b * 0.11)
        return GrayImage(mat)

    def remove_seam(self, seam: List[int]):
        if self.cols > 1:
            for r in range(self.rows):
                del self.m[r][seam[r]]
            self.cols -= 1


def reduce_image_width(image: ColorImage, energy_image: GrayImage, new_width: int) -> ColorImage:
    res_image = ColorImage(image.m)
    width = res_image.cols
    n = width - new_width
    for i in range(n):
        seam = find_lower_energy_seam(energy_image.m)
        res_image.remove_seam(seam)
        energy_image.remove_seam(seam)
        print("Removed seam {}/{}".format(i + 1, n))
    print("Done: {0} pixels width -> {1} pixels width.".format(width, res_image.cols))
    return res_image


def main():
    if len(sys.argv) != 3:
        print()
        print("Uso:")
        print("  python3 entregrable5.py <nombre_fichero> <factor_reducción>")
        print("donde ")
        print("  'nombre_fichero' es el nombre de un fichero de imagen en formato GIF")
        print("  'factor_reducción' es un entero entre 1 y 99. P. ej.: 15 indica una reducción de anchura del 15%")
        print()
        sys.exit(1)

    # LEER PARÁMETROS DE LA LÍNEA DE ÓRDENES
    image_filename = sys.argv[1]  # Por ejemplo: Castillo400x271.gif
    scale_width = (100 - max(1, min(99, int(sys.argv[2])))) / 100.0  # Por ejemplo: 15

    # Crea la ventana gráfica
    root = tkinter.Tk()
    root.title("Seam Carving - Algoritmia - UJI 2018")
    root.resizable(width=False, height=False)

    # Lee la imagen original
    color_image = ColorImage(image_filename)

    # Ajusta el tamaño de la ventana gráfica según el tamalo de la imagen original
    canvas = tkinter.Canvas(root, borderwidth=0, highlightthickness=0,
                            width=color_image.cols * 2, height=color_image.rows * 2,
                            background="WHITE")
    canvas.pack(padx=0, pady=0)

    # --------------- Seam Carving ---------------

    # Calcula la energia de la imagen
    im_energy_original = color_image.to_grayimage().get_energy_as_grayimage()
    im_energy = deepcopy(im_energy_original)

    # Crea la imagen final resescalada a la nueva anchura
    final_width = int(color_image.cols * scale_width)
    reduced_image = reduce_image_width(color_image, im_energy, final_width)

    # --------------- Muestra las tres imágenes ---------------

    # Muestra la imagen original
    tki_color_image = color_image.get_tkinter_image()
    canvas.create_image(0, 0, image=tki_color_image, anchor="nw")

    # Muestra la imagen de la energía (y, en verde, la primera veta eliminada)
    # print(primeraveta)
    tki_im_energy_original = im_energy_original.get_tkinter_image()
    canvas.create_image(color_image.cols, 0,
                        image=tki_im_energy_original, anchor="nw")

    # Muestra la nueva imagen reescalada
    tki_reduced_image = reduced_image.get_tkinter_image()
    tki_reduced_image.write("Castillo_reduced.gif")
    canvas.create_image((color_image.cols - final_width) / 2, color_image.rows,
                        image=tki_reduced_image, anchor="nw")

    # --------------- lanza el mainloop ---------------
    root.mainloop()


####################################################################################
# No es necesario modificar el código que hay ENCIMA de esta línea
####################################################################################

def find_lower_energy_seam(m: MatrixGrayImage) -> List[int]:  #
    rows = len(m)
    cols = len(m[0])

    def rec(r, c):
        if (r, c) not in mem:
            if r == 0:
                mem[r, c] = (m[r][c], c)
            elif r > 0 and c == 0 and c == cols-1:
                mem[r, c] = (rec(r - 1, c) + m[r][c], c)
            elif r > 0 and c == 0 and c < cols - 1:
                mem[r, c] = min((rec(r - 1, c) + m[r][c], c), (rec(r - 1, c + 1) + m[r][c], c + 1))
            elif r > 0 and c > 0 and c == cols - 1:
                mem[r, c] = min((rec(r - 1, c - 1) + m[r][c], c - 1), (rec(r - 1, c) + m[r][c], c))
            elif r > 0 and c > 0 and c < cols - 1:
                mem[r, c] = min((rec(r - 1, c - 1) + m[r][c], c - 1), (rec(r - 1, c) + + m[r][c], c),
                                (rec(r - 1, c + 1) + m[r][c], c + 1))
        return mem[r, c][0]

    mem = {}
    minimum_seam = infinity
    minimum_col = -1
    for c in range(cols):
        actual = rec(rows - 1, c)
        if actual < minimum_seam:
            minimum_seam = actual
            minimum_col = c

    seam = [minimum_col]
    q = rows
    while q > 0:
        q -= 1
        _, minimum_col = mem[q, minimum_col]
        seam.append(minimum_col)

    seam.reverse()
    seam.pop(0)

    print("Energy: {0}".format(minimum_seam))
    print("Seam: {0}".format(seam))

    return seam

####################################################################################
# No es necesario modificar el código que hay DEBAJO de esta línea
####################################################################################

if __name__ == "__main__":
    main()
