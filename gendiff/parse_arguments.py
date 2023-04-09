import argparse


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
    return argsimport argparse
