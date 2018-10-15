def format_matrix(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('[{{:{}}}]'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    return '\n'.join(table)
