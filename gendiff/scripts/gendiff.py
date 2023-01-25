import argparse

def arguments():
    my_parser = argparse.ArgumentParser(
        description=('Compares two configuration files and shows a difference.'))
    my_parser.add_argument('Help',
                            metavar='first_file second_file',
                            type=str,
                            help='')
    my_parser.add_argument('-f', '--format',
                           help='set format of output' )
    args = my_parser.parse_args()
    print(args.Help)
