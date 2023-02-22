import json
from gendiff.scripts.gendiff import generate_diff


def test_generate_diff():
    right_result = open('tests/fixtures/right_result.json').read()
    different = generate_diff('tests/fixtures/file1.json', 'tests/fixtures/file2.json')
    assert type(different) == str
    assert different+'\n' == right_result
    right_result.close()
