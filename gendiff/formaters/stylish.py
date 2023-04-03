from gendiff.formaters.stringify_dict import stringify_dict


def gen_tree_changed(item, key, depth):
    result = ''
    if type(item) == dict:
        result += (f'{depth * "    "}{key}: '
                   f'{stylish(item, depth + 1)}\n')
    else:
        item1 = stringify_dict(item[0], depth + 1)
        item2 = stringify_dict(item[1], depth + 1)
        result += f'{(depth - 1) * "    "}  - {key}: {item1}\n'
        result += f'{(depth - 1) * "    "}  + {key}: {item2}\n'
    return result


def stylish(diff, depth=1):
    """
    stylish(diff, depth=1)
    Принимает словарь, созданный gen_base_diff. Возвращает строку с
    представлением изменений в формате дерева. Например:
        file1.json
        {
          "host": "hexlet.io",
          "timeout": 50,
          "proxy": "123.234.53.22",
          "follow": false
        }

        file2.json
        {
          "host": "hexlet.io",
          "timeout": 50,
          "proxy": "123.234.53.22",
          "follow": false
        }

        gen_text_diff_tree(gen_base_diff(file1.json, file2.json))
        {
          - follow: false
            host: hexlet.io
          - proxy: 123.234.53.22
          - timeout: 50
          + timeout: 20
          + verbose: true
        }

        Отсутствие плюса или минуса говорит о том, что ключ есть в обоих
        файлах, и его значения совпадают. Во всех остальных ситуациях значение
        по ключу либо отличается, либо ключ есть только в одном файле.
        В примере выше ключ timeout есть в обоих файлах, но имеет разные
        значения, proxy находится только в file1.json, а verbose только
        в file2.json.
    """
    result = ''
    for key in diff['keys']:
        if key in diff['unchanged'].keys():
            item = stringify_dict(diff["unchanged"][key], depth + 1)
            result += f'{depth * "    "}{key}: {item}\n'
        elif key in diff['removed'].keys():
            item = stringify_dict(diff["removed"][key], depth + 1)
            result += f'{(depth - 1) * "    "}  - {key}: {item}\n'
        elif key in diff['added'].keys():
            item = stringify_dict(diff["added"][key], depth + 1)
            result += f'{(depth - 1) * "    "}  + {key}: {item}\n'
        elif key in diff['changed'].keys():
            item = diff['changed'][key]
            result += gen_tree_changed(item, key, depth)
    result = '{\n' + result + f'{(depth - 1) * "    "}' + '}'
    return result
