from gendiff.scripts import gendiff


def main():
    args = gendiff.arguments()
    form = args.first_file[len(args.first_file) - 4:]
    if form == 'json':
        print(gendiff.generate_diff(args.first_file, args.second_file))
    elif form == 'yaml' or form == '.yml':
        print(gendiff.generate_diff_yaml(args.first_file, args.second_file))


if __name__ == '__main__':
    main()
