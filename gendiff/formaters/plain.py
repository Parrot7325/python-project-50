from gendiff.formaters.stringify_dict import stringify_dict


def get_value_plain(value):
    """
    get_value_plain(value)
    Возвращает значение, приведенное к формату для представления в
    формате plain (gen_text_diff_plain).
    """
    if type(value) == dict:
        return '[complex value]'
    elif type(value) == str:
        return f"'{value}'"
    else:
        return stringify_dict(value)


def get_path_plain(previous_path, new_part):
    """
    get_path_plain(previous_path, new_part)
    Принимает путь для обрабатываемого объекта и имя следующего,
    возвращает путь для конечного описываемого объекта для формата plain
    (gen_text_diff_plain).
    """
    new_path = f'{previous_path}.{new_part}'[1:]
    return new_path


def gen_text_diff_plain_real(diff, path=''):
    """
    gen_text_diff_plain_real(diff, path='')
    Принимает словарь, созданный gen_base_diff. Возвращает строку с
    представлением изменений в формате plain:

    Property 'common.follow' was added with value: false
    Property 'common.setting2' was removed
    Property 'common.setting3' was updated. From true to null
    Property 'common.setting4' was added with value: 'blah blah'
    Property 'common.setting5' was added with value: [complex value]
    Property 'common.setting6.doge.wow' was updated. From '' to 'so much'
    Property 'common.setting6.ops' was added with value: 'vops'
    Property 'group1.baz' was updated. From 'bas' to 'bars'
    Property 'group1.nest' was updated. From [complex value] to 'str'
    Property 'group2' was removed
    Property 'group3' was added with value: [complex value]


    Если новое значение свойства является составным, то пишется [complex value].
    Если свойство вложенное, то отображается весь путь до корня, а не только с
    учетом родителя, например выше это: common.setting6.ops
    """
    result = ''
    for key in diff['keys']:
        if key in diff['removed'].keys():
            result += f"Property '{get_path_plain(path, key)}' was removed\n"
        elif key in diff['added'].keys():
            item = diff['added'][key]
            result += (f"Property '{get_path_plain(path, key)}' was added with"
                       f" value: {get_value_plain(item)}\n")
        elif key in diff['changed'].keys():
            if type(diff['changed'][key]) == dict:
                result += gen_text_diff_plain_real(diff['changed'][key],
                                                   path + f'.{key}')
            else:
                was = get_value_plain(diff['changed'][key][0])
                now = get_value_plain(diff['changed'][key][1])
                result += (f"Property '{get_path_plain(path, key)}' was "
                           f"updated. From {was} to {now}\n")
    return result


def gen_text_diff_plain(diff):
    plain_diff = gen_text_diff_plain_real(diff)
    return plain_diff[:len(plain_diff) - 1]
