MAX_GRAPH_VERTEX = 10
MIN_GRAPH_VERTEX = 1
INPUT_ROW_MESSAGE = ''


class ArrayLengthError(Exception):
    pass


def main():
    # matr = get_matrix()
    # print_matrix(matr)
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
    print(components)


def get_relevant_indexes(array):
    return [i for i in range(len(array)) if array[i] == 1]


def mark_row_col(matrix, index):
    matrix[index] = [2 for i in matrix[index]]
    matrix[index][index] = 2
    for i in range(len(matrix)):
        matrix[i][index] = 2


def get_components(matrix):
    components = []
    for row in matrix:
        indexes = get_relevant_indexes(row)
        if len(indexes):
            components.append([i + 1 for i in indexes])
        for index in indexes:
            mark_row_col(matrix, index)

    return components


def get_strong_matrix(matrix):
    return matrix_mul_element(matrix, get_transpone_matrix(matrix))


def get_transpone_matrix(matrix):
    return [list(i) for i in zip(*matrix)]


def replace_nums(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j]:
                matrix[i][j] = 1


def get_matrix():
    vertex_count = read_int(
        message='Введите число вершин графа: ',
        error_message='Неверное значение, повторите ввод: ',
        min_value=MIN_GRAPH_VERTEX,
        max_value=MAX_GRAPH_VERTEX
    )
    matrix = read_matrix(vertex_count)
    clear_loops(matrix)

    return matrix


def matrix_mul(x, y):
    zip_y = [i for i in zip(*y)]
    return [
        [sum(
            i * j for i, j in zip(row_i, col_j)
        ) for col_j in zip_y] for row_i in x
    ]


def matrix_mul_element(x, y):
    res = [[0] * len(x) for _ in range(len(x))]
    for i in range(len(x)):
        for j in range(len(x)):
            res[i][j] = x[i][j] * y[i][j]

    return res


def pow_matrix(matrix, pow):
    if pow == 0:
        return create_unit_matrix(len(matrix))
    elif pow == 1:
        return matrix
    else:
        res = matrix
        for _ in range(2, pow + 1):
            res = matrix_mul(matrix, res)
        return res


def get_reachability_matrix(matrix):
    degree = len(matrix)
    res = [[0] * degree for _ in range(degree)]
    for i in range(0, degree + 1):
        res = sum_matrix(res, pow_matrix(matrix, i))

    replace_nums(res)
    return res


def sum_matrix(matrix_1, matrix_2):
    res = [[0] * len(matrix_1) for _ in range(len(matrix_1))]
    for i in range(len(matrix_1)):
        for j in range(len(matrix_1)):
            res[i][j] = matrix_1[i][j] + matrix_2[i][j]

    return res


def clear_loops(matrix):
    for i in range(len(matrix)):
        matrix[i][i] = 0


def create_unit_matrix(size):
    matr = [[0] * size for _ in range(size)]
    for i in range(size):
        matr[i][i] = 1

    return matr


def read_matrix(size):
    return [read_row('Введите строку матрицы: ', size) for _ in range(size)]


def check_row(array, size):
    for i in array:
        if i not in (0, 1):
            raise ValueError('Некорректное значение в матрице смежности.')
        if len(array) != size:
            raise ArrayLengthError('Некорректное количество связей.')


def read_row(message, size):
    print(message, end='')
    row = [int(i) for i in input().split(' ')]
    check_row(row, size)

    return row


def print_matrix(matrix):
    for row in matrix:
        for item in row:
            print(item, end=' ')
        print()


def make_matrix(size):
    return [[0] * size for _ in range(size)]


def read_int(message, error_message, min_value=0, max_value=0):
    print(message, end='')
    while True:
        val = input()
        if val.isdigit() and min_value <= (res := int(val)) <= max_value:
            return res
        print(error_message, end='')


if __name__ == '__main__':
    main()
