import itertools
import re


def delete_duplicats(sequence: list[str]):
    """
    Delete duplicates of nested lists.
    """
    items = [i.split() for i in sequence]
    res = []
    items = [list(i.split(' + ')) for i in sequence]
    for i in items:
        i.sort()
        if i not in res:
            res.append(i)

    return res


def equal_tables(mdnf: str, expression: str) -> bool:
    """Returns bool variable 'are expressions equal?' using truth tables."""
    return get_truth_table(to_expression(mdnf)) == get_truth_table(expression)


def get_implicants_expressions(implicants: list[str]) -> list[str]:
    """
    Get all implicants expressions. Returns list of expressions, for example:
    ['!y*!z + x*!z', '!y*!z', 'x*!z + x*y + !x*!y + !y*!z', ...]
    """
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
    """
    Returns all mdnf from given expression as list of lists of terms.
    To get them, list of all expressions is checking for equal truth table, and
    then duplicates are removing.
    For example, returns [['!x*!y', 'x*!z', 'x*y'], ['!x*!y', '!y*!z', 'x*y']].
    """
    res = []
    for i in expressions:
        if equal_tables(i.replace('*', ''), expression):
            res.append(i)

    potencial_mdnfs = delete_duplicats(res)
    shortest_mdnf_len = get_min_length(potencial_mdnfs)

    return [i for i in potencial_mdnfs if len(i) == shortest_mdnf_len]


def get_min_length(sequence: list[list[str]]):
    """Returns the lowest length of nested lists."""
    min_length = len(sequence[0])
    for i in sequence:
        if (new_length := len(i)) < min_length:
            min_length = new_length

    return min_length


def get_permutations(count: int = 3) -> list[str]:
    """
    Get permutations of 1 and 0 with given count of digits:
      000
      001
      010
      ...
    Returns list of permutations.
    """
    res = ['0' * count]
    for i in range(1, 2**count):
        value = numeral_sys_sum(res[i - 1], '1')
        res.append(value)

    return res


def get_terms(expresion: str) -> list[str]:
    """
    Get terms of expression.
    Returns list of terms, for example: ['XYz', 'Xyz', 'xYZ', 'xYz', 'xyz']
    where upper means negative form: X is equal to !x.
    """
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


def get_truth_table(expression: str) -> list[list[int]]:
    """
    Create expression's truth table. Returns list of rows, for example:
    [
        [0, 0, 0, 0],
        [0, 0, 1, 1],
        [0, 1, 0, 1],
        ...
    ]
    Last row element is a function value.
    """
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


def get_truth(table: list[int]) -> list[list[int]]:
    """Returns only truth rows from truth table as list of lists(rows)."""
    return [row[0:3] for row in table if row[-1]]


def get_variables(expression: str) -> list[str]:
    variables = [i for i in set(re.findall(r'[a-z]', expression))]
    variables.sort()

    return variables


def glue_together_2(terms: list[str]) -> tuple[bool, list[str]]:
    """
    Glue implicants with length 2 via Quine's algorithm.
    Returns bool varibale 'all absobed?' and list of implicants with length 1
    or 2 (if it wasn't absorbed), for example: (False, ['x!y', 'z']).
    """
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
    """
    Glue implicants with length 3 via Quine's algorithm.
    Returns list of implicants with length 2
    For example: ['Xz', 'Yz', 'yz', 'xY', 'xz'].
    """
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
    """
    Input expression as str variable. Symbols: x, y, z, !, *, +.
    Returns given str.
    """
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
    # expression = 'x*!y + x*z + !x*!y*!z' --> !y!z + xz

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
            print('МДНФ:', ' + '.join(mdnf).replace('*', ''))


def numeral_sys_sum(a: str, b: str, base: int = 2) -> str:
    """
    Get sum of 2 digits with given numeral base (<=10). Returns str result.
    """
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
    """
    Get PDNF of given truth table's expression.
    Return str variable, for example '!x!y!z + !x!yz + !xy!z + x!yz + xyz'.
    """
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
    """
    Get expression could be eval. Returns str.
    """
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
    """Returns bool variable 'is expression valid?'."""
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
