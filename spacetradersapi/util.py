def yes_no(flag: bool, true_good: bool = True) -> str:
    true_color = '[green]'
    false_color = '[red]'
    if not true_good:
        true_color = '[red]'
        false_color = '[green]'
    return true_color + 'Yes' if flag else false_color + 'No'


def shade_percentage(current: int, capacity: int, full_good: bool = True) -> str:
    if capacity == 0:
        return '[grey54]0/0'

    first = '[green]'
    second = '[yellow]'
    third = '[dark_orange3]'
    fourth = '[red]'
    if not full_good:
        first = '[red]'
        second = '[dark_orange3]'
        third = '[yellow]'
        fourth = '[green]'

    fullness = 100 * float(current)/float(capacity)

    if fullness >= 75:
        color = first
    elif fullness >= 50:
        color = second
    elif fullness >= 25:
        color = third
    else:
        color = fourth

    return color + str(current) + '/' + str(capacity)
