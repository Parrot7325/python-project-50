import json
from tests.fixtures.get_right_result import get_right_result
from gendiff.scripts.gendiff import generate_diff


def test_generate_diff(get_right_result):
    different = generate_diff('tests/fixtures/file1.json', 'tests/fixtures/file2.json')
    assert type(different) == str
    assert different == get_right_result
