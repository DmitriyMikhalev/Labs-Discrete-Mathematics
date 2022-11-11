from __future__ import annotations

from random import randint
from typing import Optional


def choose_set_number(sets: list, max_option: int) -> Optional[int]:
    """Args: sets - список, max_option - число. Возвращает число, выбранное в
    диапазоне [1, max_option]. Если введено max_option + 1, возвращается None.
    """
    EXIT_VALUE = 6
    option = None
    message = [f"\n{i}. Множество {chr(64 + i)}: {sets[i - 1] if len(sets[i - 1]) != 0 else '{}'}" for i in range(1, 6)]

    while option not in range(1, max_option + 1):
        option = handle_menu(
            "".join(message) + "\n\nВыберите множество: ",
            max_option
        )

        if option in (EXIT_VALUE, None):
            break

    return option


def contains(sets: list) -> None:
    """Функция, выводящая сообщение о содержании введенного числа в выбранном
    множестве. Аргументы: sets - кортеж множеств. Возвращает None.
    """
    value = input_int("\nВведите проверяемое число: ")
    alias_set = choose_set_number(sets, 5)

    print(f"Число {value}", end="")
    if value not in sets[alias_set - 1]:
        print(" не", end="")
    print(f" содержится во множестве {chr(64 + alias_set)}")


def difference(sets: list) -> None:
    """Функция, выводящая результат вычитания множеств.
    Аргументы: sets - список множеств. Возвращает None.
    """
    set_1_num, set_2_num = get_sets_numbers(sets, 5)
    if any(i is None for i in (set_1_num, set_2_num)):
        return

    print(
        f"\nРезультат вычитания из множества {chr(set_1_num + 64)} множества "
        + f"{chr(set_2_num + 64)}:", end=" "
    )

    res = list(i for i in sets[set_1_num - 1] if i not in sets[set_2_num - 1])
    print("{}") if len(res) == 0 else print(f"{set(res)}")


def fill_set(sets: list, values_range: range) -> None:
    """Функция заполнения множества. Аргументы: sets - список множеств,
    values_range - диапазон значений для заполнения. Позволяет как вводить
    значения вручную, так и генерировать сразу все множества. Возвращает None.
    """
    set_number = choose_set_number(sets, 6)

    if set_number is None:
        return

    if set_number == 6:
        for i, _ in enumerate(sets):
            sets[i] = generate_set(values_range=values_range)

        return

    option = None
    while option not in (1, 2):
        option = handle_menu(
            "\n1. Ввести вручную.\n2. Сгенерировать\n\nВыберите действие: ", 5
        )

        if option is None:
            return

    if option == 1:
        sets[set_number - 1] = input_set(values_range=values_range)
    elif option == 2:
        sets[set_number - 1] = generate_set(values_range=values_range)

    print('\nМножество создано.')


def generate_set(values_range: range) -> None:
    """Функция для генерации множества из случайных значений в диапазоне
    values_range. Возвращает полученное множество типа set."""
    res = []
    for _ in range(randint(1, 8)):
        random_value = randint(values_range[0], values_range[-1])
        if random_value not in res:
            res.append(random_value)

    return set(res)


def get_sets_numbers(sets: list, max_option: int = 5) -> tuple:
    """Функция для взятия 2-х чисел для определения номеров множеств.
    Аргументы: sets - список множеств, max_option - верхняя граница диапазона,
    по умолчанию 5. Число принадлежит отрезку [1, max_option]. Возвращает
    кортеж, состоящий из выбранных чисел.
    """
    set_1 = choose_set_number(sets, max_option)
    set_2 = choose_set_number(sets, max_option)

    return set_1, set_2


def handle_menu(message: str, max_option: int) -> Optional[int]:
    """Функция обработки меню. Аргументы: message - строка, сообщение при
    запросе ввода, max_option - верхняя граница диапазона. Возвращает выбранное
    число из отрезка [1, max_option]. Если введено ключевое слово 'стоп', будет
    возвращен None.
    """
    option = input_int(message=message)
    if option is None:
        return None

    if option:
        while (option < 1 or option > max_option):
            if option < 1 or option > max_option:
                print('\nНеверное значение, повторите ввод.')

            option = input_int(message=message)

            if option is None:
                break

    return option


def input_int(message: str) -> Optional[int]:
    """Функция ввода целого числа. Аргументы: message - сообщение, выводимое
    при запросе числа у пользователя. Возвращает введенное число или None, если
    введено некорректное значение.
    """
    line = input(message).strip()
    if line.isdigit() or line[1:].isdigit() and line[0] in ("+", "-",):
        return int(line)
    elif line == "стоп":
        return None
    elif any(i in (".", ",",) for i in line):
        print("Допустимы только целые числа.")
    else:
        print("Введено не число.")

    return None


def input_section() -> tuple[int, int]:
    """Функция ввода отрезка. Запрашивает у пользователя 2 числа до тех пор,
    пока они не будут введены корректно. В случае, если границы отрезка
    расположены не по возрастанию, повторно запрашивается верхняя граница.
    Возвращает кортеж вида (min, max).
    """
    first_value = second_value = None
    while first_value is None:
        first_value = input_int("Введите нижнюю границу области значений: ")

    while second_value is None or second_value <= first_value:
        second_value = input_int("Введите верхнюю границу области значений: ")
        if second_value <= first_value:
            print('Верхняя граница должна быть как минимум не меньше нижней.')

    return first_value, second_value


def input_set(values_range: range) -> set:
    """Функция для ввода элементов множества из диапазона values_range.
    Возвращает множество типа set.
    """
    res = []
    print("\nДля выхода напишите 'стоп'.")
    while True:
        value = input_int("Введите элемент множества: ")

        if value is None:
            break

        if value not in values_range:
            print('Значение не из универсума. Не будет добавлено.')
        elif value not in res:
            res.append(value)

    return set(res)


def intersection(sets: list) -> None:
    """Функция пересечения множеств. Аргументы: sets - список множеств.
    Возвращает None.
    """
    set_1_num, set_2_num = get_sets_numbers(sets, 5)
    if any(i is None for i in (set_1_num, set_2_num)):
        return

    print(
        f"\nРезультат пересечения множества {chr(64 + set_1_num)} с множеством"
        + f" {chr(64 + set_2_num)}:", end=" "
    )

    set_1 = sets[set_1_num - 1]
    set_2 = sets[set_2_num - 1]

    if len(set_2) > len(set_1):
        set_1, set_2 = set_2, set_1

    res = list(i for i in set_2 if i in set_1)

    print("{}") if len(res) == 0 else print(f"{set(res)}")


def main() -> None:
    """Главная функция, хранит значения всех множеств, список множеств sets,
    диапазон значений values_range, и так далее. В этой функции вызываются
    остальные функции в зависимости от выбранного действия. Возвращает None.
    """
    set_a = set()
    set_b = set()
    set_c = set()
    set_d = set()
    set_e = set()
    sets = [set_a, set_b, set_c, set_d, set_e,]

    min_value, max_value = input_section()
    values_range = range(min_value, max_value + 1)
    set_universum = {i for i in values_range}
    print('\nУниверсум создан.')

    options: dict[int, tuple] = {
        1: (fill_set, (sets, values_range,),),
        2: (show_sets, (sets,),),
        3: (union, (sets,),),
        4: (difference, (sets,),),
        5: (intersection, (sets,),),
        6: (symmetric_difference, (sets,),),
        7: (show_addition, (sets, set_universum,),),
        8: (show_universum, (set_universum,),),
        9: (contains, (sets,),),
    }

    while True:
        option = handle_menu(
            "\n1. Создать множество\n2. Показать множества\n3. Объединение\n"
            + "4. Разность\n5. Пересечение\n6. Симметрическая разность\n"
            + "7. Дополнение\n8. Показать универсум\n9. Проверка вхождения\n"
            + "10. Выход\n\nВыберите действие: ",
            10
        )

        if option == 10:
            return

        func, args = options.get(option)

        if callable(func) and isinstance(args, tuple):
            func(*args)
        else:
            raise Exception("Некорректное взаимодействие. Повторите попытку.")


def show_addition(sets: list, universum: set) -> None:
    """Функция вывода дополнения множества. Аргументы: sets - список множеств,
    universum - множество всех значений. Возвращает None.
    """
    set_num = choose_set_number(sets, 5)

    if set_num is None:
        return

    sequence = sets[set_num - 1]
    res = [i for i in universum if i not in sequence]

    print(
        f"\nДополнение множества {chr(set_num + 64)}: "
        + f"{set(res)}"
    )


def show_sets(sets: list) -> None:
    """Функция вывода множеств. Аргументы: sets - список множеств. Возвращает
    None.
    """
    print(
        "\n" + "\n".join((
            f"Множество {chr(65 + i)}: {val if len(val) != 0 else '{}'}" for i, val in enumerate(sets))
        )
    )


def show_universum(set_universum: set) -> None:
    """Функция вывода множества значений. Аргументы: set_universum - множество
    значений. Возвращает None.
    """
    print(f"\nУниверсум: {set_universum}")


def symmetric_difference(sets: list) -> None:
    """Функция вывода симметрической разности множеств. Аргументы: sets -
    список множеств. Возвращает None.
    """
    set_1_num, set_2_num = get_sets_numbers(sets, 5)
    if any(i is None for i in (set_1_num, set_2_num)):
        return

    print(
        f"\nРезультат симметрической разности множеств {chr(64 + set_1_num)}"
        + f" и {chr(64 + set_2_num)}: ", end=""
    )

    set_1 = sets[set_1_num - 1]
    set_2 = sets[set_2_num - 1]

    part_1 = [i for i in set_1 if i not in set_2]
    part_2 = [i for i in set_2 if i not in set_1]
    res = [*part_1, *part_2]

    print("{}") if len(res) == 0 else print(f"{set(res)}")


def union(sets: list) -> None:
    """Функция печати объединения множеств. Аргументы: sets - список множеств.
    Возвращает None.
    """
    set_1_num, set_2_num = get_sets_numbers(sets, 5)
    if any(i is None for i in (set_1_num, set_2_num)):
        return

    print(
        f"\nОбъединение множеств {chr(64 + set_1_num)} и {chr(64 + set_2_num)}:",
        end=" "
    )

    set_1 = sets[set_1_num - 1]
    set_2 = sets[set_2_num - 1]

    if len(set_2) > len(set_1):
        set_1, set_2 = set_2, set_1

    add = list(i for i in set_2 if i not in set_1)
    res = [*set_1, *add]

    print("{}") if len(res) == 0 else print(f"{set(res)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Ошибка! {str(e)}")
