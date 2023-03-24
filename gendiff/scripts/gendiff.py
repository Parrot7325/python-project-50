import argparse
import json
import yaml
from yaml.loader import SafeLoader


def arguments():
    my_parser = argparse.ArgumentParser(prog='gendiff',
                                        description=('Compares two'
                                                     ' configuration '
                                                     'files and shows'
                                                     ' a difference.'))
    my_parser.add_argument('first_file')
    my_parser.add_argument('second_file')
    my_parser.add_argument('-f', '--format',
                           help='set format of output')
    args = my_parser.parse_args()
    return args


def stringify_dict(dictionary, depth=1):
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
            result += f'{depth * "    "}{key}: {item}\n'
    return '{\n' + result + f'{(depth - 1) * "    "}' + '}'


def gen_base_diff(file1, file2):
    diff = {
        'unchanged': {},
        'only in first file': {},
        'only in second file': {},
        'changed': {},
        'keys': []
    }
    keys = list(set(file1.keys()).union(set(file2.keys())))
    diff['keys'].extend(keys)
    for key in keys:
        if file1.get(key) == file2.get(key):
            diff['unchanged'][key] = file1.get(key)
        else:
            if key in file1.keys() and key not in file2.keys():
                diff['only in first file'][key] = file1.get(key)
            elif key not in file1.keys() and key in file2.keys():
                diff['only in second file'][key] = file2.get(key)
            elif key in file1.keys() and key in file2.keys():
                if type(file1[key]) == dict and type(file2[key]) == dict:
                    diff['changed'][key] = gen_base_diff(file1[key], file2[key])
                else:
                    diff['changed'][key] = (file1[key], file2[key])
    diff['keys'].sort()
    return diff


def gen_text_diff(diff, depth=1): #_recursive
    result = ''
    for key in diff['keys']:
        if key in diff['unchanged'].keys():
            item = stringify_dict(diff["unchanged"][key], depth + 1)
            result += f'{depth * "    "}{key}: {item}\n'
        else:
            if key in diff['only in first file'].keys():
                item = stringify_dict(diff["only in first file"][key], depth + 1)
                result += f'{(depth - 1) * "    "}  - {key}: {item}\n'
            elif key in diff['only in second file'].keys():
                item = stringify_dict(diff["only in second file"][key], depth + 1)
                result += f'{(depth - 1) * "    "}  + {key}: {item}\n'
            elif key in diff['changed'].keys():
                if type(diff['changed'][key]) == dict:
                    result += (f'{depth * "    "}{key}: '
                               f'{gen_text_diff(diff["changed"][key], depth + 1)}\n')
                else:
                    item1 = stringify_dict(diff['changed'][key][0], depth + 1)
                    item2 = stringify_dict(diff['changed'][key][1], depth + 1)
                    result += f'{(depth - 1) * "    "}  - {key}: {item1}\n'
                    result += f'{(depth - 1) * "    "}  + {key}: {item2}\n'
    result = '{\n' + result + f'{(depth - 1) * "    "}' + '}'
    return result


def generate_diff(file_path1, file_path2):
    file1 = json.load(open(file_path1))
    file2 = json.load(open(file_path2))
    return gen_text_diff(gen_base_diff(file1, file2))


def generate_diff_yaml(file_path1, file_path2):
    file1 = yaml.load(open(file_path1).read(), Loader=SafeLoader)
    file2 = yaml.load(open(file_path2).read(), Loader=SafeLoader)
    return gen_text_diff(gen_base_diff(file1, file2))
