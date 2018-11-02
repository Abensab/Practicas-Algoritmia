import sys


def test(nomfich_folletos: str, nomfich_solucion: str):
    error = False
    try:
        aux = open(nomfich_folletos, "r").read().strip().split('\n')
        page_size = int(aux[0])
        folletos = [tuple(int(num) for num in a.split()) for a in aux[1:]]
        df = {}
        for f in folletos:
            df[f[0]] = f
        ss = set([f[0] for f in folletos])
    except Exception:
        print("Error leyendo el fichero '{0}".format(nomfich_folletos))
        sys.exit()

    try:
        aux = open(nomfich_solucion, "r").read().strip().split('\n')
    except Exception:
        print("Error leyendo el fichero '{0}".format(nomfich_solucion))
        sys.exit()
    try:
        solucion = [tuple(int(num) for num in a.split()) for a in aux]
        for t in solucion:
            if len(t) != 4:
                raise Exception("formato erróneo")
    except Exception:
        print(
            "El formato del fichero '{0}' no es correcto. Deben ser 4 enteros separados por blancos en cada línea.".format(
                nomfich_folletos))
        sys.exit()

    papers_list = [s[1] for s in solucion]
    papers_set = set(papers_list)
    last_paper_id = max(papers_list)
    if min(papers_list) < 1:
        print("ERROR: la primera hoja de imprenta que puede utilizarse es la 1", file=sys.stderr)
        sys.exit()

    for s in solucion:
        if s[0] not in ss:
            print("ERROR: el folleto {0} no existe.".format(s[0]), file=sys.stderr)
            sys.exit()

    pages = [None]
    for i in range(1, last_paper_id + 1):
        if i not in papers_set:
            error = True
            print("ERROR: la hoja {} no se utiliza".format(i), file=sys.stderr)
        pages.append([[0] * page_size for _ in range(page_size)])

    # comprueba que la solucion tiene todos los folletos
    ss = set([f[0] for f in solucion])
    for f in folletos:
        if f[0] not in ss:
            error = True
            print("ERROR: La solución no contiene el folleto", f, file=sys.stderr)

    # comprueba que no se solapen los folletos ni se salgan de la hoja de imprenta
    solapes = set()
    fuera_hoja = set()
    for s in solucion:
        iden, p_id, px, py = s
        sx, sy = df[iden][1], df[iden][2]
        for r in range(sy):
            rpy = r + py
            for c in range(sx):
                cpx = c + px
                if rpy >= page_size or cpx >= page_size:
                    error = True
                    if iden not in fuera_hoja:
                        fuera_hoja.add(iden)
                        print("ERROR: El folleto {} se sale de la hoja {}".format(iden, p_id), file=sys.stderr)
                    continue
                f1 = pages[p_id][rpy][cpx]
                f2 = iden
                if pages[p_id][r + py][cpx] != 0:
                    error = True
                    if (f1, f2) not in solapes:
                        solapes.add((f1, f2))
                        solapes.add((f2, f1))
                        print("ERROR: Se solapan los folletos {} y {} en la hoja {}".format(f1, f2, p_id),
                              file=sys.stderr)
                else:
                    pages[p_id][r + py][c + px] = iden

    last = pages[-1]
    libres = sum([row.count(0) for row in last])
    total = page_size ** 2
    ocupado = total - libres
    if not error:
        print("SOLUCIÓN VÁLIDA")
        print("\t-Hojas de imprenta utilizadas: {0}".format(last_paper_id))
        print("\t-Porcentaje utilizado de la última hoja: {0:0.1f}%".format(100 * ocupado / page_size ** 2))
    else:
        print("SOLUCIÓN NO VÁLIDA")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("USO:\n\tpython3 comprueba_solucion_imprenta.py <ficheroImprenta.txt> <ficheroSolucion.txt>")
    else:
        test(sys.argv[1], sys.argv[2])
