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


def gen_diff_from_dicts(file1, file2):
    result = ''
    keys = list(set(file1.keys()).union(set(file2.keys())))
    keys.sort()
    for key in keys:
        if file1.get(key) == file2.get(key):
            result += f'    {key}: {file1.get(key)}\n'
        else:
            if key in file1.keys() and key not in file2.keys():
                result += f'  - {key}: {file1.get(key)}\n'
            elif key not in file1.keys() and key in file2.keys():
                result += f'  + {key}: {file2.get(key)}\n'
            elif key in file1.keys() and key in file2.keys():
                result += f'  - {key}: {file1.get(key)}\n'
                result += f'  + {key}: {file2.get(key)}\n'
    result = '{\n' + result + '}'
    return result

def generate_diff(file_path1, file_path2):
    file1 = json.load(open(file_path1))
    file2 = json.load(open(file_path2))
    return gen_diff_from_dicts(file1, file2)
    


def generate_diff_yaml(file_path1, file_path2):
    file1 = yaml.load(open(file_path1).read(), Loader=SafeLoader)
    file2 = yaml.load(open(file_path1).read(), Loader=SafeLoader)
    
