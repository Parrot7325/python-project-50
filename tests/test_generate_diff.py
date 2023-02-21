import json
import pytest
from gendiff.scripts.gendiff import generate_diff


@pytest.fixture
def get_right_result():
    result = set()
    with open('tests/fixtures/right_result.txt') as right_result_file:
        for line in right_result_file:
            result.add(line)
    return result


def test_generate_diff(get_right_result):
    different = generate_diff('tests/fixtures/file1.json', 'tests/fixtures/file2.json')
    assert type(different) == str
    different = set(different.split('\n'))
    print(get_right_result)
    assert different == get_right_result
