MAX_GRAPH_VERTEX = 10
MIN_GRAPH_VERTEX = 1


class ArrayLengthError(Exception):
    pass


def check_row(array: list[int], size: int) -> None:
    for i in array:
        if i not in (0, 1):
            raise ValueError('Некорректное значение в матрице смежности.')
        if len(array) != size:
            raise ArrayLengthError('Некорректное количество связей.')


def clear_loops(matrix: list[list[int]]) -> None:
    for i in range(len(matrix)):
        matrix[i][i] = 0


def create_unit_matrix(size: int) -> list[list[int]]:
    matr = [[0] * size for _ in range(size)]
    for i in range(size):
        matr[i][i] = 1

    return matr


def get_components(matrix: list[list[int]]) -> list[list[int]]:
    components = []
    for row in matrix:
        indexes = get_relevant_indexes(row)
        if len(indexes):
            components.append([i + 1 for i in indexes])
        for index in indexes:
            mark_row_col(matrix, index)

    return components


def get_matrix() -> list[list[int]]:
    vertex_count = read_int(
        message='Введите число вершин графа: ',
        error_message='Неверное значение, повторите ввод: ',
        min_value=MIN_GRAPH_VERTEX,
        max_value=MAX_GRAPH_VERTEX
    )
    matrix = read_matrix(vertex_count)
    clear_loops(matrix)

    return matrix


def get_reachability_matrix(matrix: list[list[int]]) -> list[list[int]]:
    degree = len(matrix)
    res = [[0] * degree for _ in range(degree)]
    for i in range(0, degree + 1):
        res = sum_matrix(res, pow_matrix(matrix, i))

    replace_nums(res)
    return res


def get_relevant_indexes(array: list[int]) -> list[int]:
    return [i for i in range(len(array)) if array[i] == 1]


def get_strong_matrix(matrix: list[list[int]]) -> list[list[int]]:
    return matrix_mul_element(matrix, get_transpone_matrix(matrix))


def get_transpone_matrix(matrix: list[list[int]]) -> list[list[int]]:
    return [list(i) for i in zip(*matrix)]


def main() -> None:
    # matrix = get_matrix()
    # int_matrix(matrix)
    matrix = [
        [0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [1, 0, 1, 1, 0]
    ]
    reachability_matrix = get_reachability_matrix(matrix)
    strong_matrix = get_strong_matrix(reachability_matrix)
    print_matrix(strong_matrix)
    components = get_components(strong_matrix)
    for i, val in enumerate(components):
        print(f'Компонента {i + 1}:', *val)


def make_matrix(size: int) -> list[list[int]]:
    return [[0] * size for _ in range(size)]


def mark_row_col(matrix: list[list[int]], index: int) -> None:
    matrix[index] = [2 for i in matrix[index]]
    matrix[index][index] = 2
    for i in range(len(matrix)):
        matrix[i][index] = 2


def matrix_mul(x: list[list[int]], y: list[list[int]]) -> list[list[int]]:
    zip_y = [i for i in zip(*y)]
    return [
        [sum(
            i * j for i, j in zip(row_i, col_j)
        ) for col_j in zip_y] for row_i in x
    ]


def matrix_mul_element(
    x: list[list[int]],
    y: list[list[int]]
) -> list[list[int]]:
    res = [[0] * len(x) for _ in range(len(x))]
    for i in range(len(x)):
        for j in range(len(x)):
            res[i][j] = x[i][j] * y[i][j]

    return res


def pow_matrix(matrix: list[list[int]], pow: int) -> list[list[int]]:
    if pow == 0:
        return create_unit_matrix(len(matrix))
    elif pow == 1:
        return matrix
    else:
        res = matrix
        for _ in range(2, pow + 1):
            res = matrix_mul(matrix, res)
        return res


def print_matrix(matrix: list[list[int]]) -> None:
    for row in matrix:
        for item in row:
            print(item, end=' ')
        print()


def read_matrix(size: int) -> list[list[int]]:
    return [read_row('Введите строку матрицы: ', size) for _ in range(size)]


def read_row(message: str, size: int) -> list[int]:
    print(message, end='')
    row = [int(i) for i in input().split(' ')]
    check_row(row, size)

    return row


def read_int(
    message: str,
    error_message: str,
    min_value: int = 0,
    max_value: int = 0
) -> int:
    print(message, end='')
    while True:
        val = input()
        if val.isdigit() and min_value <= (res := int(val)) <= max_value:
            return res
        print(error_message, end='')


def replace_nums(matrix: list[list[int]]) -> None:
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j]:
                matrix[i][j] = 1


def sum_matrix(
    matrix_1: list[list[int]],
    matrix_2: list[list[int]]
) -> list[list[int]]:
    res = [[0] * len(matrix_1) for _ in range(len(matrix_1))]
    for i in range(len(matrix_1)):
        for j in range(len(matrix_1)):
            res[i][j] = matrix_1[i][j] + matrix_2[i][j]

    return res


if __name__ == '__main__':
    main()
