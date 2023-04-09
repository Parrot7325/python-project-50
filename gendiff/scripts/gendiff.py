from gendiff import gendiff
from gendiff.parse_arguments


def main():
    args = gendiff.parse_arguments()
    print(gendiff.generate_diff(args.first_file,
                                args.second_file,
                                args.output_format))


if __name__ == '__main__':
    main()
