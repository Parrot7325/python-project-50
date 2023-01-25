import argparse
import json


def arguments():
    my_parser = argparse.ArgumentParser(
        prog = 'gendiff',
        description=('Compares two configuration files and shows a difference.'))
    my_parser.add_argument('first_file')
    my_parser.add_argument('second_file')
    my_parser.add_argument('-f', '--format',
                           help='set format of output' )
    args = my_parser.parse_args()

def get_existent(value1, value2):
    if value1:
        return value1
    else:
        return value2


def generate_diff(file_path1, file_path2):
    result = ''
    file1 = json.load(open(file_path1))
    file2 = json.load(open(file_path2))
    keys = set(file1.keys()).union(set(file2.keys()))
    for key in keys:
        if file1.get(key) == file2.get(key):
            result += f'    {key}: {file1.get(key)}\n'
        else:
            if not file1.get(key) or not file2.get(key):
                value = get_existent(file1.get(key), file2.get(key))
                result += f'  - {key}: {value}\n'
            else:
                result += f'  - {key}: {file1.get(key)}\n'
                result += f'  + {key}: {file2.get(key)}\n'
        result = '{\n' + result + '}'
        return result
