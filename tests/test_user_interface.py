# -*- coding: utf-8 -*-

from decimal import Decimal

from prudget.user_interface import *


def test_args_to_dictionary():
    result = ['d=2017/01/01', 'v=10.00', 'n="Hello World"']
    keys = ['d', 'n', 'v']
    result = args_to_dictionary(result)
    result = result.keys()

    assert set(keys) == set(result)

def test_create_account_from_command_line_args():
    dictionary = args_to_dictionary(['n=Itaú', 'b=3000.00'])

    result = Account.create_from_dictionary(dictionary)

    assert result.balance == Decimal(dictionary['b'])
    assert result.name == dictionary['n']
