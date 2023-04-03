from gendiff.scripts import gendiff
from gendiff import formaters


def main():
    args = gendiff.arguments()
    if args.output_format == 'plain':
        decorator = formaters.gen_text_diff_plain.gen_text_diff_plain
    elif args.output_format == 'json':
        decorator = formaters.gen_text_diff_json.gen_text_diff_json
    elif args.output_format == 'stylish' or args.output_format == '':
        decorator = formaters.stylish
    else:
        print('Error! Wrong output format')
        return 'Error! Wrong output format'
    print(gendiff.generate_diff(args.first_file, args.second_file, decorator))


if __name__ == '__main__':
    main()
