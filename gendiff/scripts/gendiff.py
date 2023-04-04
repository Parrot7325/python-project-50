from gendiff import gendiff


def main():
    args = gendiff.arguments()
    print(gendiff.generate_diff(args.first_file,
                                args.second_file,
                                args.output_format))


if __name__ == '__main__':
    main()
