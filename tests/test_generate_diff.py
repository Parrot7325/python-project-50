from gendiff.scripts.gendiff import generate_diff


def test_generate_diff():
    right_result = open('tests/fixtures/right_result.json').read()
    different1 = generate_diff('tests/fixtures/file1.json',
                               'tests/fixtures/file2.yml')
    different2 = generate_diff('tests/fixtures/file1.yml',
                               'tests/fixtures/file2.json')
    assert type(different1) == str
    assert type(different2) == str
    assert different1 + '\n' == right_result
    assert different2 + '\n' == right_result


def test_recursive_generate_diff():
    right_result = open('tests/fixtures/recursive_right_result.json').read()
    different1 = generate_diff('tests/fixtures/recursive_file1.json',
                               'tests/fixtures/recursive_file2.yml')
    different2 = generate_diff('tests/fixtures/recursive_file1.yml',
                               'tests/fixtures/recursive_file2.json')
    assert type(different1) == str
    assert type(different2) == str
    assert different1 + '\n' == right_result
    assert different2 + '\n' == right_result


def test_gen_text_diff_plain():
    right_result = open('tests/fixtures/plain_right_result.json').read()
    different1 = generate_diff('tests/fixtures/recursive_file1.yml',
                               'tests/fixtures/recursive_file2.json',
                               'plain')
    different2 = generate_diff('tests/fixtures/recursive_file1.json',
                               'tests/fixtures/recursive_file2.yml',
                               'plain')
    assert type(different1) == str
    assert type(different2) == str
    assert different1 + '\n' == right_result
    assert different2 + '\n' == right_result


def test_gen_text_diff_json():
    right_result = open('tests/fixtures/json_right_result.json').read()
    different1 = generate_diff('tests/fixtures/recursive_file1.yml',
                               'tests/fixtures/recursive_file2.json',
                               'json')
    different2 = generate_diff('tests/fixtures/recursive_file1.json',
                               'tests/fixtures/recursive_file2.yml',
                               'json')
    assert type(different1) == str
    assert type(different2) == str
    assert different1 + '\n' == right_result
    assert different2 + '\n' == right_result
