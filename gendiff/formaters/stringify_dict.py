def stringify_not_dict(data):
    if data is None:
        return 'null'
    elif type(data) == bool:
        return str(data).lower()
    else:
        return data


def stringify_dict(dictionary, depth=1):
    """
    stringify_dict(dictionary, depth=1)
    Принимает словарь и возвращает строку с удобным визуальным
    отображением исходного словаря.
    Значения приводятся к стандарту json (None -> null, True -> true и т.д.)
    """
    dictionary = stringify_not_dict(dictionary)
    if type(dictionary) != dict:
        return dictionary
    result = ''
    keys = list(dictionary.keys())
    keys.sort()
    for key in keys:
        item = dictionary[key]
        if type(item) == dict:
            result += (f'{depth * "    "}{key}: '
                       f'{stringify_dict(item, depth + 1)}\n')
        else:
            if type(item) == bool:
                item = str(item).lower()
            result += f'{depth * "    "}{key}: {item}\n'
    return '{\n' + result + f'{(depth - 1) * "    "}' + '}'
