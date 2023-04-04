import json
import yaml
from yaml.loader import SafeLoader


def gen_file(file_path):
    input_format = file_path[len(file_path) - 4:]
    if input_format == 'json':
        file = json.load(open(file_path))
    elif input_format == '.yml' or input_format == 'yaml':
        file = yaml.load(open(file_path).read(), Loader=SafeLoader)
    else:
        raise Exception(f'Error! Wrong input format "{input_format}"')
    return file
