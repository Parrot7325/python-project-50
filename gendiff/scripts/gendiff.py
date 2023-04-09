import gendiff


def main():
    args = gendiff.parse_arguments.parse_arguments()
    print(gendiff.gendiff.generate_diff(args.first_file,
                                        args.second_file,
                                        args.output_format))


if __name__ == '__main__':
    main()
