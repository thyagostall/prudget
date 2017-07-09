import argparse
import pickle

from prudget.dashboard import Dashboard
from prudget.parser import Parser
from prudget.uiprinter.uiaccountprinter import UIAccountPrinter
from prudget.uiprinter.uitransactionprinter import UITransactionPrinter


def args_to_dictionary(args):
    result = [arg.split('=') for arg in args]
    result = {key: value for key, value in result}
    return result


def print_dashboard(dashboard):
    printer = UIAccountPrinter()
    result = printer.print(dashboard.accounts)
    print(result)

    printer = UITransactionPrinter()
    result = printer.print(dashboard.transactions)
    print(result)


def load_dashboard():
    try:
        with open('data', 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return Dashboard()


def save_dashboard(dashboard):
    with open('data', 'wb') as file:
        return pickle.dump(dashboard, file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--status', action='store_true', help='shows the status of the dashboard')
    parser.add_argument('-t', '--transaction', type=str, nargs='*', help='create a transaction')
    parser.add_argument('-a', '--account', type=str, nargs='*', help='create an account')

    args = parser.parse_args()
    dashboard = load_dashboard()
    parser = Parser(dashboard.accounts)

    if args.status:
        print_dashboard(dashboard)
    elif args.transaction:
        transaction = args_to_dictionary(args.transaction)
        transaction = parser.create_transaction(transaction)
        printer = UITransactionPrinter()
        print(printer.print_transaction(transaction))
        answer = input('Is it correct? [y/N]: ')
        if answer.lower().startswith('y'):
            dashboard.add_transaction(transaction)
    elif args.account:
        account = args_to_dictionary(args.account)
        account = parser.create_account(account)
        dashboard.add_account(account)
    else:
        print(args)

    save_dashboard(dashboard)
