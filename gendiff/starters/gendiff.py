from gendiff.scripts import gendiff


def main():
    args = gendiff.arguments()
    input_format = args.first_file[len(args.first_file) - 4:]
    if args. == 'plain':
        decorator = gendiff.gen_text_diff_plain
    else:
        decorator = gendiff.gen_text_diff_tree
    if input_format == 'json':
        print(gendiff.generate_diff(args.first_file, args.second_file, decorator))
    elif input_format == 'yaml' or input_format == '.yml':
        print(gendiff.generate_diff_yaml(args.first_file, args.second_file, decorator))


if __name__ == '__main__':
    main()
