import json


def gen_text_diff_json(diff):
    """
    gen_text_diff_json(diff)
    Принимает словарь, созданный gen_base_diff. Возвращает строку с
    представлением изменений в формате json:
        unchanged: содержит пары ключ/значение, которые не были изменены
        removed: содержит пары ключ/значение отсутствующие во 2-ом словаре
        added: содержит пары ключ/значение, добавленные во 2-ой словарь
        changed: содержит пары ключ/кортеж или ключ/словарь для измененных
            значений. Элементами кортежа будут значения ключа в 1-ом и 2-ом
            словарях соответственно. Значением ключа будет словарь в случае,
            если исходные словари по этому ключу сами содержали словари,
            и те были изменены. Такой словарь будет иметь описаную здесь
            структуру.
        keys: список, содержит отсортированый набор неповторяющихся ключей
            обоих переданых словарей.
    """
    result = json.dumps(diff, sort_keys=True, indent=4)
    return result
