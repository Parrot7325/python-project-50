import pytest
from gendiff.scripts.gendiff import generate_diff


@pytest.mark.parametrize("file1,file2", [
    ('tests/fixtures/file1.json', 'tests/fixtures/file2.yml'),
    ('tests/fixtures/file1.yml', 'tests/fixtures/file2.json')
])
def test_generate_diff(file1, file2):
    right_result = open('tests/fixtures/right_result.json').read()
    different = generate_diff(file1, file2)
    assert type(different) == str
    assert different + '\n' == right_result


parametrizer = pytest.mark.parametrize("file1,file2", [
    ('tests/fixtures/recursive_file1.json',
     'tests/fixtures/recursive_file2.yml'),
    ('tests/fixtures/recursive_file1.yml',
     'tests/fixtures/recursive_file2.json')
])


@parametrizer()
def test_recursive_generate_diff(file1, file2):
    right_result = open('tests/fixtures/recursive_right_result.json').read()
    different = generate_diff(file1, file2)
    assert type(different) == str
    assert different + '\n' == right_result


@parametrizer()
def test_gen_text_diff_plain(file1, file2):
    right_result = open('tests/fixtures/plain_right_result.json').read()
    different = generate_diff(file1, file2, 'plain')
    assert type(different) == str
    assert different + '\n' == right_result


@parametrizer()
def test_gen_text_diff_json(file1, file2):
    right_result = open('tests/fixtures/json_right_result.json').read()
    different = generate_diff(file1, file2, 'json')
    assert type(different) == str
    assert different + '\n' == right_result
