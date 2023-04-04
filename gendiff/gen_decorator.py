from gendiff import formaters


def gen_decorator(decorator):
    if decorator == 'stylish' or not decorator:
        decorator = formaters.stylish.stylish
    elif decorator == 'plain':
        decorator = formaters.plain.gen_text_diff_plain
    elif decorator == 'json':
        decorator = formaters.json.gen_text_diff_json
    else:
        raise Exception('Error! Wrong output format')
    return decorator
