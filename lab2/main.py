import re


def get_permutations(count: int = 3) -> list[str]:
    res = ['0' * count]
    for i in range(1, 2**count):
        value = numeral_sys_sum(res[i - 1], '1')
        res.append(value)

    return res


def get_terms(exp: str) -> list[str]:
    return exp.replace(
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


def get_truth(expression: str):
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
            res.append([x, y, z])

    return res


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

    if all(i for i in status):
        return True, res

    for i in status:
        if not i:
            res.append(terms[i])

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


def main() -> None:
    expression = 'x*y + !y*x + x*y'
    if not validate_expression(expression):
        raise ValueError('Incorrect expression!')
    pdnf = perfect_disjunctive_normal_form(expression)
    print('СДНФ:', pdnf)
    terms = glue_together_3(get_terms(pdnf))
    success, glue = glue_together_2(terms)
    if success:
        print('МДНФ:', ' + '.join(glue))
    else:
        # TODO: implicant matrix
        pass


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


def perfect_disjunctive_normal_form(expression: str) -> str:
    truth = get_truth(expression)
    res = ''
    for term in truth:
        x, y, z = term
        res += 'x' if x else '!x'
        res += 'y' if y else '!y'
        res += 'z' if z else '!z'
        res += ' + '
    return res.removesuffix(' + ')


def validate_expression(expression: str) -> bool:
    correct = 'xyz!+* '
    if expression[-1] not in 'xyz':
        return False
    for i in expression:
        if i not in correct:
            return False

    return True


if __name__ == '__main__':
    main()
