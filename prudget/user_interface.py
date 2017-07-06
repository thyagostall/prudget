import argparse
import shlex

from .account import Account

def args_to_dictionary(args):
    result = [arg.split('=') for arg in args]
    result = {key: value for key, value in result}
    return result

def create_transaction(args):
    print(args_to_dictionary(args))

def create_account(args):
    dictionary = args_to_dictionary(args)
    Account.create_account_from_dictionary(dictionary)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--status', action='store_true', help='shows the status of the dashboard')
    parser.add_argument('-t', '--transaction', type=str, nargs='*', help='create a transaction')
    parser.add_argument('-a', '--account', type=str, nargs='*', help='create an account')

    args = parser.parse_args()
        
    if args.status:
        print('Here it should print the dashboard status')
    elif args.transaction:
        create_transaction(args.transaction)
    elif args.account:
        create_account(args.account)
    else:
        print(args)
