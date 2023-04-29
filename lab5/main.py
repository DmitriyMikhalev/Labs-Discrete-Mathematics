"""
Проверка принадлежности слова грамматике
G = ({0, 1, ~, !}, {I, J, K, N, M}, I, П),
где П:
    I --> J0 | K1 | M0
    J --> K~ | M0
    K --> M~ | J0 | N0
    N --> K1 | !
    M --> I0 | I1 | !
"""


def is_correct(string: str, allowed_symbols: tuple[str, ...]) -> bool:
    for symbol in string:
        if symbol not in allowed_symbols:
            return False

    return True


def main() -> None:
    transformings = {
        'J0': ('I', 'K'),
        'K1': ('I', 'M'),
        'M0': ('I', 'J'),
        'M~': ('K',),
        'I0': ('N',),
        'I1': ('N',),
        '!': ('N', 'M'),
        'N0': ('K',),
        'K~': ('J',)
    }
    terminals = ('0', '1', '~', '!')
    symbols = ('I', 'J', 'K', 'N', 'M')
    start_symbol = 'I'

    to_recognize = input('Введите слово для проверки: ')
    if not is_correct(to_recognize, symbols + terminals):
        print('Слово содержит символы, не входящие в грамматику.')
    else:
        if recognize(to_recognize, start_symbol, rules=transformings):
            print('Слово принадлежит грамматике.')
        else:
            print('Слово не принадлежит грамматике.')


def recognize(word: str, target: str,
              rules: dict[str, tuple[str, ...]]) -> bool:
    if word == target:
        return True

    for replacement in rules.keys():
        if replacement in word:
            options: tuple[str, ...] = rules[replacement]
            for option in options:
                if recognize(word.replace(replacement, option), target, rules):
                    return True

    return False


if __name__ == '__main__':
    main()
