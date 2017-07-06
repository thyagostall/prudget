# -*- coding: utf-8 -*-

from prudget.object_utils import *


def test_is_partial_arg():
    candidates = {
        '': False,
        'n': True,
        'na': True,
        'nam': True,
        'name': True,
        'names': False,
        'somethingelse': False
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

    assert set(keys_actual) == set(keys_expected)


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

    assert set(keys_actual) == set(keys_expected)
