from gendiff.scripts import gendiff


def test_generate_diff():
    right_result = open('tests/fixtures/right_result.json').read()
    different1 = gendiff.generate_diff('tests/fixtures/file1.json',
                                       'tests/fixtures/file2.yml')
    different2 = gendiff.generate_diff('tests/fixtures/file1.yml',
                                       'tests/fixtures/file2.json')
    assert type(different1) == str
    assert type(different2) == str
    assert different1 + '\n' == right_result
    assert different2 + '\n' == right_result


def test_recursive_generate_diff():
    right_result = open('tests/fixtures/recursive_right_result.json').read()
    different1 = gendiff.generate_diff('tests/fixtures/recursive_file1.json',
                                       'tests/fixtures/recursive_file2.yml')
    different2 = gendiff.generate_diff('tests/fixtures/recursive_file1.yml',
                                       'tests/fixtures/recursive_file2.json')
    assert type(different1) == str
    assert type(different2) == str
    assert different1 + '\n' == right_result
    assert different2 + '\n' == right_result


def test_gen_text_diff_plain():
    right_result = open('tests/fixtures/plain_right_result.json').read()
    different1 = gendiff.generate_diff('tests/fixtures/recursive_file1.yml',
                                       'tests/fixtures/recursive_file2.json',
                                       gendiff.gen_text_diff_plain)
    different2 = gendiff.generate_diff('tests/fixtures/recursive_file1.json',
                                       'tests/fixtures/recursive_file2.yml',
                                       gendiff.gen_text_diff_plain)
    assert type(different1) == str
    assert type(different2) == str
    assert different1 + '\n' == right_result
    assert different2 + '\n' == right_result


def test_gen_text_diff_json():
    right_result = open('tests/fixtures/json_right_result.json').read()
    different1 = gendiff.generate_diff('tests/fixtures/recursive_file1.yml',
                                       'tests/fixtures/recursive_file2.json',
                                       gendiff.gen_text_diff_json)
    different2 = gendiff.generate_diff('tests/fixtures/recursive_file1.json',
                                       'tests/fixtures/recursive_file2.yml',
                                       gendiff.gen_text_diff_json)
    assert type(different1) == str
    assert type(different2) == str
    assert different1 + '\n' == right_result
    assert different2 + '\n' == right_result
