import argparse
import json
import yaml
from yaml.loader import SafeLoader
from gendiff import formaters


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


def gen_different(item1, item2):
    if type(item1) == dict and type(item2) == dict:
        return gen_base_diff(item1, item2)
    else:
        return (item1, item2)


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
        elif key in dict1.keys() and key not in dict2.keys():
            diff['removed'][key] = dict1.get(key)
        elif key not in dict1.keys() and key in dict2.keys():
            diff['added'][key] = dict2.get(key)
        elif key in dict1.keys() and key in dict2.keys():
            diff['changed'][key] = gen_different(dict1[key], dict2[key])
    diff['keys'].sort()
    return diff


def gen_file(file_path):
    input_format = file_path[len(file_path) - 4:]
    if input_format == 'json':
        file = json.load(open(file_path))
    elif input_format == '.yml' or input_format == 'yaml':
        file = yaml.load(open(file_path).read(), Loader=SafeLoader)
    return file


def generate_diff(file_path1, file_path2, decorator='stylish'):
    if decorator == 'stylish' or decorator == '':
        decorator = formaters.stylish.stylish
    elif decorator == 'plain':
        decorator = formaters.plain.gen_text_diff_plain
    elif decorator == 'json':
        decorator = formaters.json.gen_text_diff_json
    file1 = gen_file(file_path1)
    file2 = gen_file(file_path2)
    return decorator(gen_base_diff(file1, file2))
