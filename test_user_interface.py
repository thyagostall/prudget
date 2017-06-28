import pytest

from collections import OrderedDict

def is_partial_arg(partial, arg):
    partial = partial.strip()
    if partial == '':
        return False

    return arg.startswith(partial)

def infer_dictionary(dictionary, keys):
    keys.sort()
    dictionary = OrderedDict(dictionary)

    result = {}
    for candidate in dictionary.keys():
        for key in keys:
            if is_partial_arg(candidate, key):
                result[key] = dictionary[candidate]

    return result

def args_to_dictionary(args):
    result = [arg.split('=') for arg in args]
    result = {key: value for key, value in result}
    return result

def test_args_to_dictionary():
    result = ['d=2017/01/01', 'v=10.00', 'n="Hello World"']
    keys = ['date', 'name', 'value']
    result = args_to_dictionary(result)
    result = infer_dictionary(result, keys)

    assert set(keys) == set(result.keys())

def test_is_partial_arg():
    candidates = {
            ''              : False,
            'n'             : True,
            'na'            : True,
            'nam'           : True,
            'name'          : True,
            'names'         : False,
            'somethingelse' : False
            }

    for arg, result in candidates.items():
        assert is_partial_arg(arg, 'name') == result

def test_match_dict_keys_with_exact_values():
    keys_expected = [
            'name',
            'value',
            'other',
            ]

    actual = {
            'name': None, 
            'value': None, 
            'other': None
            }
    keys_actual = infer_dictionary(actual, keys_expected)
    keys_actual = keys_actual.keys()

    assert keys_actual == False
    for expected, actual in zip(keys_expected, keys_actual):
        assert actual == expected

def test_match_dict_keys_with_partial_values():
    keys_expected = [
            'name',
            'value',
            'other',
            ]

    actual = {
            'n': None, 
            'o': None, 
            'v': None
            }
    keys_actual = infer_dictionary(actual, keys_expected)
    keys_actual = keys_actual.keys()

    for expected, actual in zip(keys_expected, keys_actual):
        assert actual == expected
