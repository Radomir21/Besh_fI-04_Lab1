def compute_cell(i: int, j: int, p: int) -> str:
    if (2 ** i + 2 ** j) % p == 1:
        return '1'
    elif (2 ** i - 2 ** j) % p == 1:
        return '1'
    elif (-2 ** i + 2 ** j) % p == 1:
        return '1'
    elif (-2 ** i - 2 ** j) % p == 1:
        return '1'
    else:
        return '0'


def get_matrix(m: int) -> tuple[tuple[str]]:
    p = 2 * m + 1
    matrix = [[0] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            matrix[i][j] = compute_cell(i, j, p)
    matrix = [tuple(row) for row in matrix]
    matrix = tuple(matrix)
    return matrix
