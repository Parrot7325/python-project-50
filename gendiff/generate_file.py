import json
import yaml
from yaml.loader import SafeLoader


def get_file_format(file_path):
    pieces = file_path.split('.')
    pieces.reverse()
    return pieces[0]


def generate_file(file_path):
    input_format = get_file_format(file_path)
    if input_format == 'json':
        file = json.load(open(file_path))
    elif input_format == 'yml' or input_format == 'yaml':
        file = yaml.load(open(file_path).read(), Loader=SafeLoader)
    else:
        raise Exception(f'Error! Wrong input format "{input_format}"')
    return file
