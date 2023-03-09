"""
Kruskal's algorithm to find minimum base of the graph.

Algorithm:
    1. Sort edges by weight in ASC order.
    2. Iterate over sorted edges:
      * Concatenate single vertex with another single vertex or group of
        vertices
      * Results of concatenating are components, return it
    3. Iterate over sorted edges again and glue all components if edge is
       chaining vertices from different components
"""

from pprint import pprint

MIN_GRAPH_VERTEX = 1
MAX_GRAPH_VERTEX = 10


class ArrayLengthError(Exception):
    pass


def check_row(array: list[int], size: int) -> None:
    for i in array:
        if i < 0:
            raise ValueError('Некорректное значение в матрице.')
        if len(array) != size:
            raise ArrayLengthError('Некорректное количество связей.')


def clear_loops(matrix: list[list[int]]) -> None:
    for i in range(len(matrix)):
        matrix[i][i] = 0


def find_components(edges: list[tuple[int]]) -> list[list[tuple[int]]]:
    components = []
    used = []
    for edge in edges:
        if edge[0] not in used or edge[1] not in used:
            if edge[0] not in used and edge[1] not in used:
                components.append([edge])
                used.append(edge[0])
                used.append(edge[1])
            else:
                if edge[0] in used:
                    index = get_component_index(components, vertex_ind=edge[0])
                    used.append(edge[1])
                else:
                    index = get_component_index(components, vertex_ind=edge[1])
                    used.append(edge[0])

                components[index].append(edge)

    return components


def get_base(matrix: list[list[int]]) -> list[list[int]]:
    edges: list[tuple[int]] = sorted(
        get_edges_list(matrix=matrix),
        key=lambda x: x[2]
    )
    components: list[list[tuple[int]]] = find_components(edges=edges)

    return glue_components(components=components, edges=edges)



def get_component_index(components: list[list[list[int]]],
                        vertex_ind: int) -> int:
    for index, component in enumerate(components):
        for vertexes in component:
            if vertex_ind in vertexes[:2]:
                return index


def get_edges_list(matrix: list[list[int]]) -> list[tuple[int]]:
    """[from, to, weight]"""
    edges = []
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j]:
                edges.append((i, j, matrix[i][j]))

    return edges


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


def glue_components(components: list[list[tuple[int]]],
                    edges: list[tuple[int]]) -> list[tuple[int]]:
    for edge in edges:
        from_index = get_component_index(
            components=components,
            vertex_ind=edge[0]
        )
        to_index = get_component_index(
            components=components,
            vertex_ind=edge[1]
        )
        if from_index != to_index:
            components[from_index].extend(components[to_index])
            components[from_index].append(edge)
            components.pop(to_index)

    return components[0]


def main() -> None:
    # matrix = get_matrix()
    #matrix = [
    #    [0, 1, 3],
    #    [9, 0, 4],
    #    [3, 0, 0]
    #]
    matrix = [
        [0, 13, 18, 17, 14, 22],
        [13, 0, 26, 0, 22, 0],
        [18, 26, 0, 3, 0, 0],
        [17, 0, 3, 0, 0, 19],
        [14, 22, 0, 0, 0, 0],
        [22, 0, 0, 19, 0, 0]
    ]
    base_edges = get_base(matrix=matrix)
    print_res(base_edges)


def print_res(edges: list[tuple[int]]) -> None:
    res_matrix = [
        [0 for _ in range(len(edges) + 1)] for _ in range(len(edges) + 1)
    ]
    print('Остов графа состоит из ребер:')
    for i, j, val in edges:
        res_matrix[i][j] = val
        print(f' * {i + 1} -> {j + 1} длиной {val}')

    print('\nМатрица остова имеет вид:')
    pprint(res_matrix)


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
