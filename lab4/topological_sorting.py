"""
Topological graph sorting.

Algorithm:
    While not all verices are used:
      * Find zero columns
      * Delete zero columns and chained rows
      * Set deleted columns to one layer
      * Switch layer
"""
MIN_GRAPH_VERTEX = 1
MAX_GRAPH_VERTEX = 10


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


def delete_layer(
    matrix: list[list[int]],
    indexes: list[int]
) -> None:
    if len(indexes) == 0:
        return

    for index in indexes:
        delete_row_col(matrix=matrix, index=index)


def delete_row_col(matrix, index):
    matrix[index] = [-1] * len(matrix)
    for row in matrix:
        row[index] = -1


def get_empty_columns(matrix) -> list[int]:
    res = []
    for i, col in enumerate(matrix):
        if col.count(-1) != len(matrix) and col.count(1) == 0:
            res.append(i)

    return res


def get_height_weight(layers: list[list[int]]) -> tuple[int, int]:
    return len(max(layers, key=len)), len(layers)


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


def get_sorted_graph(matrix: list[list[int]]) -> list[list[int]]:
    layers = []
    columns = [list(i) for i in zip(*matrix)]
    used = []
    while len(used) != len(matrix):
        if len(layer := get_empty_columns(matrix=columns)) != 0:
            delete_layer(matrix=columns, indexes=layer)
        else:
            layer = [i for i in range(len(matrix)) if i not in used]

        layers.append(layer)
        used.extend(layer)

    return layers


def main() -> None:
    matrix = get_matrix()
    # matrix = [
    #     [0, 1, 0, 0, 0, 1, 1, 0]
    #     [0, 0, 0, 0, 0, 0, 0, 0]
    #     [0, 0, 0, 1, 1, 0, 0, 0]
    #     [1, 0, 0, 0, 0, 0, 0, 0]
    #     [0, 0, 0, 0, 0, 0, 1, 0]
    #     [0, 0, 0, 0, 0, 0, 0, 0]
    #     [0, 0, 0, 0, 0, 0, 0, 0]
    #     [0, 1, 0, 0, 1, 0, 0, 0]
    # ]
    # [[3, 8], [4, 5], [1], [2, 6, 7]] --> correct
    sorted_graph = get_sorted_graph(matrix=matrix)
    height, weight = get_height_weight(layers=sorted_graph)
    for i, layer in enumerate(iterable=sorted_graph, start=1):
        print(f'Ярус #{i}:', ', '.join([str(i + 1) for i in layer]))
    print(f'Высота: {height}, ширина: {weight}')


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


def read_row(message: str, size: int) -> list[int]:
    print(message, end='')
    row = [int(i) for i in input().split(' ')]
    check_row(row, size)

    return row


def read_matrix(size: int) -> list[list[int]]:
    return [read_row('Введите строку матрицы: ', size) for _ in range(size)]


if __name__ == '__main__':
    main()
