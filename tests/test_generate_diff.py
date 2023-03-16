from gendiff.scripts import gendiff


def test_generate_diff():
    right_result = open('tests/fixtures/right_result.json').read()
    different = gendiff.generate_diff('tests/fixtures/file1.json',
                                      'tests/fixtures/file2.json')
    assert type(different) == str
    assert different + '\n' == right_result


def test_generate_diff_yaml():
    right_result = open('tests/fixtures/right_result.json').read()
    different = gendiff.generate_diff_yaml('tests/fixtures/file1.yml',
                                           'tests/fixtures/file2.yml')
    assert type(different) == str
    assert different + '\n' == right_result


def test_recursive_generate_diff():
    right_result = open('tests/fixtures/right_result.json').read()
    different = gendiff.recursive_generate_diff('tests/fixtures/recursive_file1.json', 
                                                'tests/fixtures/recursive_file1.json')
    assert type(different) == str
    assert different + '\n' == right_result


def test_recursive_generate_diff_yaml():
    right_result = open('tests/fixtures/recursive_right_result.yml').read()
    different = gendiff.recursive_generate_diff_yaml('tests/fixtures/recursive_file1.yml',
                                                     'tests/fixtures/recursive_file1.json')
    assert type(different) == str
    assert different + '\n' == right_result
