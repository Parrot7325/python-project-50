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


def stringify_dict(dictionary, depth=0):
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
    return f'{"{"}\n' + result + f'{(depth - 1) * "    "}{"}"}'
  

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


def gen_text_diff(diff):
    result = ''
    for key in diff['keys']:
        if key in diff['unchanged'].keys():
            result += f'    {key}: {diff["unchanged"][key]}\n'
        else:
            if key in diff['only in first file'].keys():
                result += f'  - {key}: {diff["only in first file"][key]}\n'
            elif key in diff['only in second file'].keys():
                result += f'  + {key}: {diff["only in second file"][key]}\n'
            elif key in diff['changed'].keys():
                if type(diff['changed'][key]) == dict:
                    result += (f'    {key}: '
                               f'{gen_text_diff(diff["changed"][key])}\n')
                else:
                    result += f'  - {key}: {diff["changed"][key][0]}\n'
                    result += f'  + {key}: {diff["changed"][key][1]}\n'
    result = '{\n' + result + '}'
    return result


def generate_diff(file_path1, file_path2):
    file1 = json.load(open(file_path1))
    file2 = json.load(open(file_path2))
    return gen_text_diff(gen_base_diff(file1, file2))


def generate_diff_yaml(file_path1, file_path2):
    file1 = yaml.load(open(file_path1).read(), Loader=SafeLoader)
    file2 = yaml.load(open(file_path2).read(), Loader=SafeLoader)
    return gen_text_diff(gen_base_diff(file1, file2))
