#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
##############################################################################
#
# comprueba.py 0.99: a simple program checker
#
# Copyright (C) 2008 Juan Miguel Vilar
#                    Universitat Jaume I
#                    Castelló (Spain)
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#  Any questions regarding this software should be directed to:
#
#   Juan Miguel Vilar
#   Departament de Llenguatges i Sistemes Informàtics
#   Universitat Jaume I
#   E12071 Castellón (SPAIN)
#
#   email: jvilar@lsi.uji.es
#
##############################################################################
#
# comprueba.py
#

from optparse import OptionParser
import os
from subprocess import Popen
import sys
from tempfile import TemporaryFile

################################################################################
#
# Colores:
#

AMARILLO = 33
AZUL = 34
MAGENTA = 35
NEGRO = 30
ROJO = 31
VERDE = 32

FONDOROJO = 41

BRILLANTE = 1

noColores = False


def colorea(color, cadena, color_salida=0):
    if noColores:
        return cadena
    if isinstance(color, int):
        r = "\x1b[%dm" % color
    else:
        r = ""
        for i in color:
            r += "\x1b[%dm" % i
    if cadena[-1] != "\n":
        r += cadena
    else:
        r += cadena[:-1]
    if isinstance(color_salida, int):
        r += "\x1b[%dm" % color_salida
    else:
        for i in color_salida:
            r += "\x1b[%dm" % i
    if cadena[-1] == "\n":
        r += "\n"
    return r


################################################################################
#
# Errores:
#

def error(m):
    sys.stderr.write(colorea(ROJO, "Error: %s\n" % m))
    sys.exit(1)


def aviso(m):
    sys.stderr.write(colorea(AMARILLO, "Aviso: %s\n" % m))


################################################################################
#
# Ficheros:
#

def abre(n):
    try:
        return open(n)
    except:
        error("No he podido abrir %s para lectura" % n)


def abre_o_none(n):
    if n is None:
        return None
    return abre(n)


################################################################################
#
# Redirección:
#

class RedirigeSalida:
    def __init__(self, original=sys.stdout):
        self.original = original
        self._acumulado = ""

    def write(self, l):
        self._acumulado += l

    def flush(self):
        pass

    def acumulado(self):
        return self._acumulado

    def limpia(self):
        self._acumulado = ""

    def escribe_original(self, l):
        self.original.write(l)

    def __del__(self):
        if self._acumulado:
            self.original.write(self._acumulado)
            self._acumulado = ""


class RedirigeEntrada:
    def __init__(self, fentrada, salida, error, procesador):
        self.fentrada = fentrada  # fichero de entrada
        self.salida = salida
        self.error = error
        self.procesador = procesador

        self.eof = False
        self.entrada = ""
        self.nlinea = 0
        self.pos = 0

    def leelinea(self):
        if self.eof:
            return ""
        if self.nlinea:
            salida_encontrada = self.salida.acumulado()
            self.salida.limpia()
            error_encontrado = self.error.acumulado()
            self.error.limpia()
            self.procesador.presenta_salida(salida_encontrada, error_encontrado)
        l = self.fentrada.readline()
        if not l:
            self.eof = True
            self.procesador.trata_EOF()
            return
        self.nlinea = self.nlinea + 1
        self.entrada = self.procesador.trata_linea(l, self.nlinea)

    def read(self, n):
        if self.eof:
            return ""
        if n != 1:
            l = ""
            for i in range(n):
                l = l + self.read(1)
            return l
        if self.pos == len(self.entrada):
            self.leelinea()
        if self.eof:
            return ""
        c = self.entrada[self.pos]
        self.pos = self.pos + 1
        return c

    def readline(self):
        if self.eof:
            return ""
        self.leelinea()
        if self.eof:
            return ""
        return self.entrada

    def isatty(self):
        return 0

    def close(self):
        pass

    def flush(self):
        pass

    def __del__(self):
        if not self.eof:
            salida_encontrada = self.salida.acumulado()
            self.salida.limpia()
            error_encontrado = self.error.acumulado()
            self.error.limpia()
            self.procesador.presenta_salida(salida_encontrada, error_encontrado)
            self.procesador.trata_EOF()

    def __iter__(self):
        while 1:
            line = self.readline()
            if not line:
                break
            yield line


################################################################################
#
# Procesadores (actuan sobre la entrada y la salida):
#

class Procesador:
    def trata_linea(self, l, nlinea):
        """Recibe la línea leída y el número de línea"""
        return l

    def presenta_salida(self, salida_encontrada, error_encontrado):
        """Recibe la salida y el error correspondiente a la última línea leída"""
        pass

    def trata_EOF(self):
        """Se invoca cuando se ha terminado de procesar el fichero"""
        pass


class Comprobador(Procesador):
    """Procesador que comprueba que lo encontrado coincide con lo esperado"""

    def __init__(self, salida, mostrar_todas, separa_campos, separa_error, nombre):
        self.salida = salida
        self.mostrarTodas = mostrar_todas
        self.separaCampos = separa_campos
        self.separaError = separa_error
        self.salida.write(self.barra(" " + nombre + " "))
        self.vistaEntrada = False
        self.nerrores = 0
        self.nlinea = 0

    def trata_linea(self, l, nlinea):
        self.vistaEntrada = True
        hay_fin_l = l[-1] == "\n"
        if hay_fin_l:
            l = l[:-1]
        campos = l.split(self.separaCampos)
        campos_error = campos[-1].split(self.separaError)
        campos[-1] = campos_error[0]
        campos_error = campos_error[1:]

        self.entrada = campos[0].rstrip()
        if hay_fin_l:
            self.entrada = self.entrada + "\n"

        self.salidaEsperada = [s.strip() for s in campos[1:]]
        self.errorEsperado = [s.strip() for s in campos_error]
        self.nlinea = nlinea
        return self.entrada

    def error_en_salida(self, esperado, encontrado):
        if len(esperado) == 0 and encontrado == "":
            return False
        fin_ok = (encontrado == "" or encontrado[-1] == "\n")
        if len(esperado) != 0 and fin_ok:
            s = [c.strip() for c in encontrado.split("\n")]
            s = s[:-1]  # La última línea tiene \n por fin_ok
            if s == esperado:
                return False
        return True

    def muestra_salida(self, esperado, encontrado, titulo_esperado, titulo_encontrado):
        self.salida.write("---------------------------------------\n")
        self.salida.write(titulo_esperado + "\n")
        if len(esperado) == 0:
            self.salida.write(colorea(ROJO, "Ninguna") + "\n")
        else:
            for l in esperado:
                self.salida.write("  %s\n" % l)
        self.salida.write("--\n")
        self.salida.write(titulo_encontrado + "\n")
        if encontrado == "":
            self.salida.write(colorea(ROJO, "Ninguna") + "\n")
        else:
            s = encontrado.split("\n")
            if encontrado[-1] == "\n":
                s = s[:-1]
            for l in s:
                self.salida.write("  %s\n" % l)

    def presenta_salida(self, salida_encontrada, error_encontrado):
        if not self.vistaEntrada:
            esalida = self.error_en_salida("", salida_encontrada)
            eerror = self.error_en_salida("", error_encontrado)
        else:
            esalida = self.error_en_salida(self.salidaEsperada, salida_encontrada)
            eerror = self.error_en_salida(self.errorEsperado, error_encontrado)
        if esalida or eerror:
            self.nerrores += 1
        if not self.mostrarTodas and not esalida and not eerror:
            return
        if not self.vistaEntrada:
            self.salida.write(colorea(ROJO, "Antes de la primera entrada\n"))
            if esalida:
                self.muestra_salida("", salida_encontrada, "Salida esperada:", "Salida encontrada:")
            if eerror:
                self.muestra_salida("", error_encontrado, "Salida de error esperada:", "Salida de error encontrada:")
        else:
            self.salida.write("Línea: %s\n" % colorea(VERDE, str(self.nlinea)))
            self.salida.write("Entrada: %s\n" % self.entrada.rstrip())
            if esalida or self.mostrarTodas:
                self.muestra_salida(self.salidaEsperada, salida_encontrada,
                                    "Salida esperada:", "Salida encontrada:")
            else:
                self.salida.write("Salida estándar: " + colorea(VERDE, "correcta\n"))
            if eerror or self.mostrarTodas:
                self.muestra_salida(self.errorEsperado, error_encontrado,
                                    "Salida de error esperada:", "Salida de error encontrada:")
            else:
                self.salida.write("---------------------------------------\n")
                self.salida.write("Salida de error: " + colorea(VERDE, "correcta\n"))
        self.salida.write(self.barra(""))

    def trata_EOF(self):
        if self.nerrores == 0:
            m = colorea(VERDE, "No ha habido errores")
        else:
            m = colorea(ROJO, "Ha habido %d errores" % self.nerrores)
        self.salida.write(m + "\n")
        self.salida.write(self.barra(" FIN "))

    def barra(self, m):
        return colorea(MAGENTA, "==%s%s\n" % (m, max(1, 40 - len(m) - 2) * "="))


class Generador(Procesador):
    """Genera la salida en el formato adecuado para ser utilizado con -e"""

    def __init__(self, salida, separa_campos, separa_error):
        self.salida = salida
        self.separaCampos = separa_campos
        self.separaError = separa_error

    def trata_linea(self, l, nlinea):
        self.entrada = l
        return l

    def presenta_salida(self, salida_encontrada, error_encontrado):
        fin = ""
        if len(self.entrada) != "" and self.entrada[-1] == "\n":
            self.entrada = self.entrada[:-1]
            fin = "\n"
        self.salida.write(self.entrada)
        if salida_encontrada != "":
            self.salida.write(" " + self.separaCampos + " ")
            if salida_encontrada != "" and salida_encontrada[-1] == "\n":
                salida_encontrada = salida_encontrada[:-1]
            self.salida.write((" " + self.separaCampos + " ").join(salida_encontrada.split("\n")))
        if error_encontrado != "":
            self.salida.write(" " + self.separaError + " ")
            if error_encontrado != "" and error_encontrado[-1] == "\n":
                error_encontrado = error_encontrado[:-1]
            self.salida.write((" " + self.separaError + " ").join(error_encontrado.split("\n")))
        self.salida.write(fin)

    def trata_EOF(self):
        pass


################################################################################
#
# Pruebas simples:
#

def prueba_simple(options, args):
    if len(args) == 0:
        error("Necesito al menos el nombre del programa")
    programa = args[0]
    entrada = None
    salida_esperada = None
    error_esperado = None
    es_directorio = False
    if len(args) == 1:
        pass
    elif os.path.isdir(args[1]):
        es_directorio = True
    else:
        if len(args) == 2:
            salida_esperada = args[1]
        elif len(args) == 3:
            entrada = args[1]
            salida_esperada = args[2]
        elif len(args) == 4:
            entrada = args[1]
            salida_esperada = args[2]
            error_esperado = args[3]
        else:
            error("Demasiados argumentos")
    if es_directorio:
        bien = 0
        mal = 0
        for directorio in args[1:]:
            d = {}
            for nfichero in sorted(os.listdir(directorio)):
                (nombre, sufijo) = os.path.splitext(nfichero)
                if sufijo != "":
                    sufijo = sufijo[1:]
                fichero = os.path.join(directorio, nfichero)
                t = d.get(nombre, (None, None, None))
                if sufijo == options.sufijoEntrada:
                    d[nombre] = (fichero, t[1], t[2])
                elif sufijo == options.sufijoSalida:
                    d[nombre] = (t[0], fichero, t[2])
                elif sufijo == options.sufijoError:
                    d[nombre] = (t[0], t[1], fichero)
            for (entrada, salida_esperada, error_esperado) in sorted(d.values()):
                if len(options.argumentos) > 0:
                    linea = programa + " " + " ".join(options.argumentos)
                else:
                    linea = programa
                if options.argumento and entrada is not None:
                    r = ejecuta_programa(linea + " " + entrada, None, salida_esperada, error_esperado)
                else:
                    r = ejecuta_programa(linea, entrada, salida_esperada, error_esperado)
                if r:
                    bien += 1
                else:
                    mal += 1
        print(colorea(MAGENTA, "===========================\n"))
        print(colorea(AZUL, "Probados %d ficheros" % (bien + mal)))
        if mal == 0:
            print(colorea(VERDE, "Todos correctos"))
        else:
            print(colorea(VERDE, "Correctos: %d" % bien))
            print(colorea(ROJO, "Erróneos: %d" % mal))
    else:
        if options.argumento and entrada is not None:
            ejecuta_programa(programa + " " + entrada, None, salida_esperada, error_esperado)
        else:
            ejecuta_programa(programa, entrada, salida_esperada, error_esperado)


def ejecuta_programa(nombre, entrada, salida_esperada, error_esperado):
    print(colorea((AZUL, BRILLANTE), "Ejecutando %s" % nombre))
    if entrada is not None:
        print("- Fichero de entrada: %s" % entrada)
    if salida_esperada is not None:
        print("- Salida esperada: %s" % salida_esperada)
    if error_esperado is not None:
        print("- Error esperado: %s" % error_esperado)

    fentrada = abre_o_none(entrada)
    fsalida_esperada = abre_o_none(salida_esperada)
    ferror_esperado = abre_o_none(error_esperado)

    fsalida = TemporaryFile(mode="w+")
    ferror = TemporaryFile(mode="w+")

    try:
        programa = Popen(nombre.split(), shell=False, stdin=fentrada, stdout=fsalida, stderr=ferror)
    except OSError as e:
        error("No he podido ejecutar %s, (%s)" % (nombre, e))

    codigo = programa.wait()
    fsalida.seek(0)
    ferror.seek(0)

    print(colorea((AZUL, BRILLANTE), "Resultado:"))
    va_bien = True
    if codigo != 0:
        print(colorea(AMARILLO, "Código de error %d" % codigo))
        # va_bien= False
    r = compara_ficheros("- Salida estándar:", fsalida_esperada, fsalida)
    va_bien = va_bien and r
    r = compara_ficheros("- Salida de error:", ferror_esperado, ferror)
    va_bien = va_bien and r
    return va_bien


################################################################################
#
# Pruebas entrelazadas:
#

def prueba_entrelazado(options, args):
    salida = sys.stdout
    if len(args) == 0:
        error("Necesito al menos un parámetro, el nombre del programa")
    elif len(args) == 1:
        ejecuta_entrelazado(args[0], sys.stdin, salida, options, "stdin")
    else:
        for e in args[1:]:
            if not os.path.isdir(e):
                entrada = abre(e)
                ejecuta_entrelazado(args[0], entrada, salida, options, e)
            else:  # Es un directorio
                for nfichero in sorted(os.listdir(e)):
                    (nombre, sufijo) = os.path.splitext(nfichero)
                    if sufijo != "":
                        sufijo = sufijo[1:]
                    if sufijo == options.sufijoEntrelazado:
                        fichero = os.path.join(e, nfichero)
                        entrada = abre(fichero)
                        ejecuta_entrelazado(args[0], entrada, salida, options, fichero)


def ejecuta_entrelazado(programa, entrada, salida, options, nombre):
    # Nos guardamos los ficheros originales
    stdout = sys.stdout
    stdin = sys.stdin
    stderr = sys.stderr

    # Preparamos las redirecciones
    sys.stdout = RedirigeSalida(salida)
    sys.stderr = RedirigeSalida(salida)
    if options.genera:
        procesador = Generador(stdout, options.separaCampos, options.marcaError)
    else:
        procesador = Comprobador(stdout, options.todas, options.separaCampos, options.marcaError, nombre)
    sys.stdin = RedirigeEntrada(entrada, sys.stdout, sys.stderr, procesador)

    # Guardamos sys.argv y construimos el del programa
    argv = sys.argv[:]
    sys.argv = [programa] + options.argumentos
    path = os.path.dirname(programa)
    if path not in sys.path:
        sys.path.append(path)

    # Anotamos qué modulos había antes de la ejecución
    modules = list(sys.modules.keys())

    # Prepara el entorno de ejecución
    # Fuerza la ejecución de programas guardados con if __name__=="__main__"
    globales = {"__name__": "__main__"}
    try:
        exec(compile(open(programa).read(), programa, 'exec'), globales)
    except SystemExit:
        pass
    except:
        import traceback
        sei = sys.exc_info()
        traceback.print_exception(sei[0], sei[1], sei[2])

    # Limpiamos los restos que pudieran quedar de la ejecucion
    for i in list(sys.modules.keys()):
        if i not in modules:
            del sys.modules[i]
    sys.stdout = stdout
    sys.stdin = stdin
    sys.stderr = stderr
    sys.argv = argv


################################################################################
#
# Comparaciones
#

class Comparacion:
    """Guarda los resultados de una comparación"""

    def __init__(self, _iguales, _diferencias):
        self._iguales = _iguales
        self._diferencias = _diferencias

    def iguales(self):
        """Cierto si ambos ficheros son iguales"""
        return self._iguales

    def diferencias(self):
        """Diferencias entre los ficheros"""
        return self._diferencias

    def __str__(self):
        if self._iguales:
            return "Iguales"
        else:
            return "".join([str(d) for d in self._diferencias])

    def pretty(self, lin_ref, lin_obtenido):
        if self._iguales:
            return "Iguales"
        else:
            return "".join([d.pretty(lin_ref, lin_obtenido) for d in self._diferencias])


def nlineas(n):
    """Escribe n líneas o línea según el valor de n"""
    if n == 0:
        return "cero líneas"
    elif n == 1:
        return "una línea"
    elif n == 2:
        return "dos líneas"
    else:
        return "%d líneas" % n


def plural(n):
    """Devuelve s si n!= 1"""
    if n != 1:
        return "s"
    else:
        return ""


class Diferencia:
    """Una diferencia"""

    def __init__(self, pos_ref, talla_ref, pos_obtenido, talla_obtenido):
        """Guarda la posición y líneas de los ficheros"""
        self.posRef = pos_ref
        self.tallaRef = talla_ref
        self.posObtenido = pos_obtenido
        self.tallaObtenido = talla_obtenido

    def es_vacia(self):
        return self.tallaRef == 0 and self.tallaObtenido == 0

    def __add__(self, other):
        if (self.posRef + self.tallaRef != other.posRef
                or self.posObtenido + self.tallaObtenido != other.posObtenido):
            return self, other
        return Diferencia(self.posRef, self.tallaRef + other.tallaRef,
                          self.posObtenido, self.tallaObtenido + other.tallaObtenido)

    def pretty(self, lin_ref, lin_obtenido):
        sr = plural(self.tallaRef)
        nr = nlineas(self.tallaRef)
        so = plural(self.tallaObtenido)
        no = nlineas(self.tallaObtenido)
        lineas_ref = "".join([" - " + l for l in lin_ref[self.posRef - 1:self.posRef - 1 + self.tallaRef]])
        lineas_obt = "".join(
            [" + " + l for l in lin_obtenido[self.posObtenido - 1:self.posObtenido - 1 + self.tallaObtenido]])
        if self.tallaRef != 0:
            if self.tallaObtenido != 0:
                r = "** %s cambiada%s; en la posición %d de la referencia pone:\n" % (nr, sr, self.posRef)
                r += lineas_ref
                r += "*  y en la posición %d de la salida pone:\n" % self.posObtenido
                r += lineas_obt
            else:
                r = ("** borrada%s %s en la posición %d de la referencia:\n" % (sr, nr, self.posRef))
                r += lineas_ref
        else:
            if self.tallaObtenido != 0:
                r = ("** %s inesperada%s en la posición %d de la salida:\n" %
                     (no, so, self.posObtenido))
                r += lineas_obt
            else:
                r = "** diferencia vacía en %d y %d" % (self.posRef, self.posObtenido)
        return r

    def __str__(self):
        return "Diferencia"


class ListaDiferencias:
    """Almacena una lista de diferencias de manera persistente"""

    def __init__(self, c=None, a=None):
        self.contenido = c
        self.anterior = a

    def es_vacia(self):
        return self.contenido is None and self.anterior is None

    def append(self, d):
        """Añade d, que es una diferencia, al final de la lista"""
        if d.es_vacia():
            return self
        if self.es_vacia():
            return ListaDiferencias(d, None)
        d2 = self.contenido + d
        if type(d2) == type(d):
            return ListaDiferencias(d2, self.anterior)
        else:
            return ListaDiferencias(d, self)

    def __iter__(self):
        if self.anterior is not None:
            for d in self.anterior:
                yield d
        if self.contenido is not None:
            yield self.contenido


def muestra(l):
    for puntos, difs in l:
        print("  ", puntos, [str(d) for d in difs])


def compara_ficheros(titulo, f_ref, f_obtenido):
    if f_ref is not None:
        l_ref = f_ref.readlines()
    else:
        l_ref = []
    if f_obtenido is not None:
        l_obtenidas = f_obtenido.readlines()
    else:
        l_obtenidas = []
    comparacion = compara_lineas(l_ref, l_obtenidas)
    print(titulo, end=' ')
    if comparacion.iguales():
        print(colorea(VERDE, "correcta"))
    else:
        print(colorea(ROJO, "errores"))
        print(comparacion.pretty(l_ref, l_obtenidas))
    return comparacion.iguales()


def compara_lineas(l_referencia, l_obtenidas):
    actual = [(0, ListaDiferencias())]
    for pos_ref in range(len(l_referencia)):
        pos_ref += 1
        ld = actual[-1][1].append(Diferencia(pos_ref, 1, 1, 0))
        actual.append((actual[-1][0] + 1, ld))
    pos_obtenida = 0
    for lObtenida in l_obtenidas:
        anterior = actual
        pos_obtenida += 1
        ld = ListaDiferencias()
        ld = ld.append(Diferencia(1, 0, 1, pos_obtenida))
        actual = [(anterior[0][0] + 1, ld)]
        pos_ref = 0
        for lRef in l_referencia:
            pos_ref += 1
            ins = anterior[pos_ref][0] + 1
            if lRef == lObtenida:
                sust = anterior[pos_ref - 1][0]
            else:
                sust = anterior[pos_ref - 1][0] + 1
            borr = actual[-1][0] + 1
            puntos = min(ins, sust, borr)
            if puntos == sust:
                ld = anterior[pos_ref - 1][1]
                if lRef == lObtenida:
                    diferencia = Diferencia(pos_ref, 0, pos_obtenida, 0)
                else:
                    diferencia = Diferencia(pos_ref, 1, pos_obtenida, 1)
            elif puntos == borr:
                ld = actual[-1][1]
                diferencia = Diferencia(pos_ref, 1, pos_obtenida, 0)
            elif puntos == ins:
                ld = anterior[pos_ref][1]
                diferencia = Diferencia(pos_ref, 0, pos_obtenida, 1)
            actual.append((puntos, ld.append(diferencia)))
    if actual[-1][0] == 0:
        return Comparacion(True, [])
    else:
        return Comparacion(False, actual[-1][1])


################################################################################
#
# Principal:
#

def analiza_sufijos(options):
    c = options.sufijos.split(",")
    if len(c) != 3:
        error("La cadena pasada a --sufijos tiene que tener tres componentes separados por comas")
    options.sufijoEntrada = c[0]
    options.sufijoSalida = c[1]
    options.sufijoError = c[2]


def main():
    parser = OptionParser(usage="%prog [<opciones>] <programa> [ [<entrada>] <salida> [<error>] ] | {<directorio>} ]")
    parser.add_option("-a", "--argumento", action="store_true", default=False,
                      help="el fichero de entrada se pasa como argumento al programa, sin efecto en el modo entrelazado. Si se usa con -A, el fichero de entrada es el último argumento.")
    parser.add_option("-A", "--argumentos", type="string", default=None,
                      help="lista de argumentos que se pasan al programa, separados por blancos. Por defecto no se le pasa ninguno")
    parser.add_option("-E", "--marcaError", type="string", default="@*",
                      help="separador de las líneas de error en modo entrelazado, por defecto: %default.")
    parser.add_option("-e", "--entrelazado", action="store_true", default=False,
                      help="utilizar el modo entrelazado.")
    parser.add_option("-g", "--genera", action="store_true", default=False,
                      help="generar la salida en el formato adecuado para entrelazado (implica -e).")
    parser.add_option("-n", "--noColores", action="store_true", default=False,
                      help="no utilizar colores en la salida.")
    parser.add_option("-S", "--separaCampos", type="string", default="@@",
                      help="separador de los campos en modo entrelazado, por defecto: %default.")
    parser.add_option("-s", "--sufijos", type="string", default="i,o,e",
                      help="sufijos de los ficheros de entrada, salida y error, por defecto: %default.")
    parser.add_option("-t", "--todas", action="store_true", default=False,
                      help="en modo entrelazado, muestra todas las líneas incluso si no hay diferencias respecto a lo esperado.")
    parser.add_option("-x", "--sufijoEntrelazado", type="string", default="pr",
                      help="sufijo de los ficheros con pruebas entrelazadas, por defecto: %default.")

    (options, args) = parser.parse_args()
    if options.genera:
        options.entrelazado = True
    global noColores
    noColores = options.noColores

    if options.argumentos is None:
        options.argumentos = []
    else:
        options.argumentos = options.argumentos.split()

    analiza_sufijos(options)
    if options.entrelazado:
        prueba_entrelazado(options, args)
    else:
        prueba_simple(options, args)


if __name__ == "__main__":
    main()
