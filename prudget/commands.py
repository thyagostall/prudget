import argparse
import os
import pickle

from prudget.dashboard import Dashboard
from prudget.parser import Parser
from prudget.uiprinter.account import UIAccountPrinter
from prudget.uiprinter.envelope import UIEnvelopePrinter
from prudget.uiprinter.transaction import UITransactionPrinter


def get_filename():
    return os.environ['PRUDGET_FILE_NAME']


def args_to_dictionary(args):
    result = [arg.split('=') for arg in args]
    result = {key: value for key, value in result}
    return result


def print_dashboard(dashboard):
    printer = UIAccountPrinter(dashboard.accounts)
    result = printer.print()
    print(result)

    printer = UIEnvelopePrinter(dashboard.envelopes)
    result = printer.print()
    print(result)

    printer = UITransactionPrinter(dashboard.transactions)
    result = printer.print()
    print(result)


def load_dashboard():
    try:
        filename = get_filename()
        with open(filename, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return Dashboard()


def save_dashboard(dashboard):
    filename = get_filename()
    with open(filename, 'wb') as file:
        return pickle.dump(dashboard, file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--status', action='store_true', help='shows the status of the dashboard')
    parser.add_argument('-t', '--transaction', type=str, nargs='*', help='create a transaction')
    parser.add_argument('-a', '--account', type=str, nargs='*', help='create an account')
    parser.add_argument('-e', '--envelope', type=str, nargs='*', help='create an envelope')

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
        if not answer.lower().startswith('y'):
            return
        dashboard.add_transaction(transaction)
    elif args.account:
        account = args_to_dictionary(args.account)
        account = parser.create_account(account)
        dashboard.add_account(account)
    elif args.envelope:
        envelope = args_to_dictionary(args.envelope)
        envelope = parser.create_envelope(envelope)
        dashboard.add_envelope(envelope)
    else:
        print(args)

    save_dashboard(dashboard)
