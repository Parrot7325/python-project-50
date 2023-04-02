from gendiff.scripts import gendiff


def main():
    args = gendiff.arguments()
    if args.output_format == 'plain':
        decorator = gendiff.gen_text_diff_plain
    elif args.output_format == 'json':
        decorator = gendiff.gen_text_diff_json
    else:
        decorator = gendiff.stylish
    print(gendiff.generate_diff(args.first_file, args.second_file, decorator))


if __name__ == '__main__':
    main()
