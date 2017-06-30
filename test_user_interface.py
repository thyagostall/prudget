import pytest

from decimal import Decimal

from .account import Account

def args_to_dictionary(args):
    result = [arg.split('=') for arg in args]
    result = {key: value for key, value in result}
    return result

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

