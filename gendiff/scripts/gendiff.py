import argparse
import json
import yaml
from yaml.loader import SafeLoader


def arguments():
    """
    arguments
    Принимает и парсит аргументы командной строки.
    """
    my_parser = argparse.ArgumentParser(prog='gendiff',
                                        description=('Compares two'
                                                     ' configuration '
                                                     'files and shows'
                                                     ' a difference.'))
    my_parser.add_argument('first_file')
    my_parser.add_argument('second_file')
    my_parser.add_argument('-f', '--output_format',
                           help='set format of output')
    args = my_parser.parse_args()
    return args


def stringify_dict(dictionary, depth=1):
    """
    stringify_dict(dictionary, depth=1)
    Принимает словарь и возвращает строку с удобным визуальным
    отображением исходного словаря.
    Значения приводятся к стандарту json (None -> null, True -> true и т.д.)
    """
    if dictionary is None:
        return 'null'
    if type(dictionary) == bool:
        return str(dictionary).lower()
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


def gen_base_diff(dict1, dict2):
    """
    gen_base_diff(dict1, dict2)
    Принимает два словаря (любой вложенности). Возвращает словарь
    с описанием различий:
        unchanged: содержит пары ключ/значение, которые не были изменены
        removed: содержит пары ключ/значение отсутствующие во 2-ом словаре
        added: содержит пары ключ/значение, добавленные во 2-ой словарь
        changed: содержит пары ключ/кортеж или ключ/словарь для измененных
            значений. Элементами кортежа будут значения ключа в 1-ом и 2-ом
            словарях соответственно. Значением ключа будет словарь в случае,
            если исходные словари по этому ключу сами содержали словари,
            и те были изменены. Такой словарь будет иметь описаную здесь
            структуру.
        keys: список, содержит отсортированый набор неповторяющихся ключей
            обоих переданых словарей.

    Возвращаемый словарь предполагается для передачи в любой из декораторов.
    """
    diff = {
        'unchanged': {},
        'removed': {},
        'added': {},
        'changed': {},
        'keys': []
    }
    keys = list(set(dict1.keys()).union(set(dict2.keys())))
    diff['keys'].extend(keys)
    for key in keys:
        if dict1.get(key) == dict2.get(key):
            diff['unchanged'][key] = dict1.get(key)
        else:
            if key in dict1.keys() and key not in dict2.keys():
                diff['removed'][key] = dict1.get(key)
            elif key not in dict1.keys() and key in dict2.keys():
                diff['added'][key] = dict2.get(key)
            elif key in dict1.keys() and key in dict2.keys():
                if type(dict1[key]) == dict and type(dict2[key]) == dict:
                    diff['changed'][key] = gen_base_diff(dict1[key], dict2[key])
                else:
                    diff['changed'][key] = (dict1[key], dict2[key])
    diff['keys'].sort()
    return diff


def gen_text_diff_tree(diff, depth=1):
    """
    gen_text_diff_tree(diff, depth=1)
    Принимает словарь, созданный gen_base_diff. Возвращает строку с
    представлением изменений в формате дерева. Например:
        file1.json
        {
          "host": "hexlet.io",
          "timeout": 50,
          "proxy": "123.234.53.22",
          "follow": false
        }

        file2.json
        {
          "host": "hexlet.io",
          "timeout": 50,
          "proxy": "123.234.53.22",
          "follow": false
        }

        gen_text_diff_tree(gen_base_diff(file1.json, file2.json))
        {
          - follow: false
            host: hexlet.io
          - proxy: 123.234.53.22
          - timeout: 50
          + timeout: 20
          + verbose: true
        }

        Отсутствие плюса или минуса говорит о том, что ключ есть в обоих
        файлах, и его значения совпадают. Во всех остальных ситуациях значение
        по ключу либо отличается, либо ключ есть только в одном файле.
        В примере выше ключ timeout есть в обоих файлах, но имеет разные
        значения, proxy находится только в file1.json, а verbose только
        в file2.json.
    """
    result = ''
    for key in diff['keys']:
        if key in diff['unchanged'].keys():
            item = stringify_dict(diff["unchanged"][key], depth + 1)
            result += f'{depth * "    "}{key}: {item}\n'
        else:
            if key in diff['removed'].keys():
                item = stringify_dict(diff["removed"][key],
                                      depth + 1)
                result += f'{(depth - 1) * "    "}  - {key}: {item}\n'
            elif key in diff['added'].keys():
                item = stringify_dict(diff["added"][key],
                                      depth + 1)
                result += f'{(depth - 1) * "    "}  + {key}: {item}\n'
            elif key in diff['changed'].keys():
                item = diff['changed'][key]
                if type(item) == dict:
                    result += (f'{depth * "    "}{key}: '
                               f'{gen_text_diff_tree(item, depth + 1)}\n')
                else:
                    item1 = stringify_dict(diff['changed'][key][0], depth + 1)
                    item2 = stringify_dict(diff['changed'][key][1], depth + 1)
                    result += f'{(depth - 1) * "    "}  - {key}: {item1}\n'
                    result += f'{(depth - 1) * "    "}  + {key}: {item2}\n'
    result = '{\n' + result + f'{(depth - 1) * "    "}' + '}'
    return result


def get_value_plain(value):
    """
    get_value_plain(value)
    Возвращает значение, приведенное к формату для представления в
    формате plain (gen_text_diff_plain).
    """
    if type(value) == dict:
        return '[complex value]'
    elif type(value) == str:
        return f"'{value}'"
    else:
        return stringify_dict(value)


def get_path_plain(previous_path, new_part):
    """
    get_path_plain(previous_path, new_part)
    Принимает путь для обрабатываемого объекта и имя следующего,
    возвращает путь для конечного описываемого объекта для формата plain
    (gen_text_diff_plain).
    """
    new_path = f'{previous_path}.{new_part}'[1:]
    return new_path


def gen_text_diff_plain_real(diff, path=''):
    """
    gen_text_diff_plain_real(diff, path='')
    Принимает словарь, созданный gen_base_diff. Возвращает строку с
    представлением изменений в формате plain:

    Property 'common.follow' was added with value: false
    Property 'common.setting2' was removed
    Property 'common.setting3' was updated. From true to null
    Property 'common.setting4' was added with value: 'blah blah'
    Property 'common.setting5' was added with value: [complex value]
    Property 'common.setting6.doge.wow' was updated. From '' to 'so much'
    Property 'common.setting6.ops' was added with value: 'vops'
    Property 'group1.baz' was updated. From 'bas' to 'bars'
    Property 'group1.nest' was updated. From [complex value] to 'str'
    Property 'group2' was removed
    Property 'group3' was added with value: [complex value]


    Если новое значение свойства является составным, то пишется [complex value].
    Если свойство вложенное, то отображается весь путь до корня, а не только с
    учетом родителя, например выше это: common.setting6.ops
    """
    result = ''
    for key in diff['keys']:
        if key in diff['removed'].keys():
            result += f"Property '{get_path_plain(path, key)}' was removed\n"
        elif key in diff['added'].keys():
            item = diff['added'][key]
            result += (f"Property '{get_path_plain(path, key)}' was added with"
                       f" value: {get_value_plain(item)}\n")
        elif key in diff['changed'].keys():
            if type(diff['changed'][key]) == dict:
                result += gen_text_diff_plain_real(diff['changed'][key],
                                              path + f'.{key}')
            else:
                was = get_value_plain(diff['changed'][key][0])
                now = get_value_plain(diff['changed'][key][1])
                result += (f"Property '{get_path_plain(path, key)}' was "
                           f"updated. From {was} to {now}\n")
    return result


def gen_text_diff_plain(diff):
    plain_diff = gen_text_diff_plain_real(diff)
    return plain_diff[:len(plain_diff) - 1]


def gen_text_diff_json(diff):
    """
    gen_text_diff_json(diff)
    Принимает словарь, созданный gen_base_diff. Возвращает строку с
    представлением изменений в формате json:
        unchanged: содержит пары ключ/значение, которые не были изменены
        removed: содержит пары ключ/значение отсутствующие во 2-ом словаре
        added: содержит пары ключ/значение, добавленные во 2-ой словарь
        changed: содержит пары ключ/кортеж или ключ/словарь для измененных
            значений. Элементами кортежа будут значения ключа в 1-ом и 2-ом
            словарях соответственно. Значением ключа будет словарь в случае,
            если исходные словари по этому ключу сами содержали словари,
            и те были изменены. Такой словарь будет иметь описаную здесь
            структуру.
        keys: список, содержит отсортированый набор неповторяющихся ключей
            обоих переданых словарей.
    """
    result = json.dumps(diff, sort_keys=True, indent=4)
    return result


def gen_file(file_path):
    input_format = file_path[len(file_path) - 4:]
    if input_format == 'json':
        file = json.load(open(file_path))
    elif input_format == '.yml' or input_format == 'yaml':
        file = yaml.load(open(file_path).read(), Loader=SafeLoader)
    return file


def generate_diff(file_path1, file_path2, decorator=gen_text_diff_tree):
    file1 = gen_file(file_path1)
    file2 = gen_file(file_path2)
    return decorator(gen_base_diff(file1, file2))
