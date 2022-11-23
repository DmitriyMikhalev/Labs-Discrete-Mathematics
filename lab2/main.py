import itertools
import re


def delete_duplicats(sequence: list[str]):
    items = [i.split() for i in sequence]
    res = []
    items = [list(i.split(' + ')) for i in sequence]
    for i in items:
        i.sort()
        if i not in res:
            res.append(i)

    return res


def equal_tables(mdnf: str, expression: str) -> bool:
    """"""
    return get_truth_table(to_expression(mdnf)) == get_truth_table(expression)


def get_implicants_expressions(implicants: list[str]) -> list[list[str]]:
    for i in range(0, len(implicants)):
        implicants[i] = implicants[i].replace(
            'X', '!x'
            ).replace(
                'Y', '!y'
            ).replace(
                'Z', '!z'
            )
    combs = [list(i) for i in itertools.permutations(implicants)]
    res = []
    count = len(implicants)
    for perm in combs:
        for j in range(count, 0, -1):
            res.append(perm[0:j])

    res = [tuple(i) for i in res]
    res = [list(i) for i in [*set(res)]]

    for i in range(0, len(res)):
        res[i] = to_expression(' + '.join(res[i]))
    return res


def get_mdnf(expressions: list[str], expression):
    res = []
    for i in expressions:
        if equal_tables(i.replace('*', ''), expression):
            res.append(i)

    potencial_mdnfs = delete_duplicats(res)
    shortest_mdnf_len = get_min_length(potencial_mdnfs)

    return [i for i in potencial_mdnfs if len(i) == shortest_mdnf_len]


def get_min_length(sequence: list[list[str]]):
    min_length = len(sequence[0])
    for i in sequence:
        if (new_length := len(i)) < min_length:
            min_length = new_length

    return min_length


def get_permutations(count: int = 3) -> list[str]:
    res = ['0' * count]
    for i in range(1, 2**count):
        value = numeral_sys_sum(res[i - 1], '1')
        res.append(value)

    return res


def get_terms(expresion: str) -> list[str]:
    return expresion.replace(
        ' ', ''
        ).replace(
            '*', ''
        ).replace(
            '!x', 'X'
        ).replace(
            '!y', 'Y'
        ).replace(
            '!z', 'Z'
        ).split('+')


def get_truth_table(expression: str):
    res = []
    permutations = get_permutations()
    for permutation in permutations:
        x, y, z = [int(i) for i in permutation]
        result = expression.replace(
            'x', str(x)
        ).replace(
            'y', str(y)
        ).replace(
            'z', str(z)
        ).replace(
            '!0', '1'
        ).replace(
            '!1', '0'
        )
        if eval(result):
            res.append([x, y, z, 1])
        else:
            res.append([x, y, z, 0])

    return res


def get_truth(table: list[int]):
    return [row[0:3] for row in table if row[-1]]


def get_variables(expression: str) -> list[str]:
    variables = [i for i in set(re.findall(r'[a-z]', expression))]
    variables.sort()

    return variables


def glue_together_2(terms: list[str]) -> tuple[bool, list[str]]:
    status = [0] * len(terms)
    res = []
    for i, term in enumerate(terms, 1):
        s1 = term[0]
        s2 = term[1]
        for j, nxt_term in enumerate(terms[i:]):
            if s1.isupper() and s2 in nxt_term and s1.lower() in nxt_term:
                res.append(s2)
                status[i - 1] = status[j + i] = 1
            if s2.isupper() and s1 in nxt_term and s2.lower() in nxt_term:
                res.append(s1)
                status[i - 1] = status[j + i] = 1

    res = [*set(res)]
    res.sort()
    for i in range(0, len(res)):
        res[i] = res[i].replace(
            'X', '!x'
            ).replace(
                'Y', '!y'
            ).replace(
                'Z', '!z'
            )

    if all(i for i in status):
        return True, res

    # print(f'{res=}')
    # print(f'{status=}')
    # print(f'{terms=}')
    for i in range(0, len(status)):
        if not status[i]:
            res.append(terms[i])
    res.sort()
    for i in range(0, len(res)):
        res[i] = res[i].replace(
            'X', '!x'
            ).replace(
                'Y', '!y'
            ).replace(
                'Z', '!z'
            )

    return False, res


def glue_together_3(terms: list[str]) -> list[str]:
    res = []
    for i, term in enumerate(terms, 1):
        comb_1 = [term[0], term[1]]
        comb_2 = [term[0], term[2]]
        comb_3 = [term[1], term[2]]

        for nxt_term in terms[i:]:
            if all(i in nxt_term for i in comb_1):
                res.append(''.join(comb_1))
            if all(i in nxt_term for i in comb_2):
                res.append(''.join(comb_2))
            if all(i in nxt_term for i in comb_3):
                res.append(''.join(comb_3))

    return res


def input_expression() -> str:
    while True:
        expression = input(
            'Valid symbols: x, y, z, !, *, +\n'
            + 'For example, x*z + !x*z + x*!y\n'
            + 'Input your expression: '
        )
        print()
        if validate_expression(expression):
            break
    return expression


def main() -> None:
    # expression = 'x*z + !x*z + x*!y' --> x!y + z
    # expression = 'x*y*z + x*z' --> xz
    # expression = 'x*y*!z + x*z' --> xy + xz

    expression = input_expression()
    truth_table = get_truth_table(expression)
    pdnf = perfect_disjunctive_normal_form(truth_table)
    print('СДНФ:', pdnf)

    implicants = glue_together_3(get_terms(pdnf))
    success, glue = glue_together_2(implicants)
    if success:
        print('МДНФ:', ' + '.join(glue))
    else:
        expressions = get_implicants_expressions(glue)
        results_mdnf = get_mdnf(expressions, expression)
        for mdnf in results_mdnf:
            print('МДНФ:', ' + '.join(mdnf))


def numeral_sys_sum(a: str, b: str, base: int = 2) -> list[int]:
    res = []
    max_len = max(len(a), len(b))
    a = [int(i) for i in a.zfill(max_len)]
    b = [int(i) for i in b.zfill(max_len)]

    if any(i >= base for i in a) or any(i >= base for i in b):
        raise ValueError('Incorrect base: number has digit >= base!')

    overflow = 0
    for i in range(max_len - 1, -1, -1):
        digits_sum = overflow + a[i] + b[i]
        overflow = digits_sum // base
        res.append(digits_sum % base)

    if overflow:
        res.append(overflow)

    return ''.join(str(i) for i in res[::-1])


def perfect_disjunctive_normal_form(truth_table: list[int]) -> str:
    truth = get_truth(truth_table)
    res = ''
    for term in truth:
        x, y, z = term
        res += 'x' if x else '!x'
        res += 'y' if y else '!y'
        res += 'z' if z else '!z'
        res += ' + '
    return res.removesuffix(' + ')


def to_expression(expression: str) -> str:
    """"""
    # !x!y + !y!z + x!z + xy
    expression = expression.replace(
        '!x', 'X'
        ).replace(
            '!y', 'Y'
        ).replace(
            '!z', 'Z'
        ).split(' + ')

    for i, group in enumerate(expression):
        if len(group) > 1:
            expression[i] = '*'.join([i for i in group])
        expression[i] = expression[i].replace(
            'X', '!x'
            ).replace(
                'Y', '!y'
            ).replace(
                'Z', '!z'
            )

    return ' + '.join(expression)


def validate_expression(expression: str) -> bool:
    correct = 'xyz!+* '
    if expression[-1] not in 'xyz':
        return False
    for i in expression:
        if i not in correct:
            return False

    return True


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Something went wrong!', e)
