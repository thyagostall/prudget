import json
from decimal import Decimal

from prudget.account import Account
from prudget.dashboard import Dashboard


class DashboardEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Dashboard):
            result = {}
            if obj.accounts:
                result.update({'accounts': obj.accounts})
            return result
        elif isinstance(obj, Account):
            result = {'name': obj.name, 'balance': obj.balance}
            return result
        elif isinstance(obj, Decimal):
            return str(obj)
        else:
            return super().default(obj)


def serialize_dashboard(dashboard):
    return json.dumps(dashboard, cls=DashboardEncoder)


def serialize_account(account):
    return json.dumps(account, cls=DashboardEncoder)


def test_serialize_empty_dashboard():
    dashboard = Dashboard()
    result = serialize_dashboard(dashboard)
    result = json.loads(result)

    assert result == {}


def test_serialize_account():
    account = Account('Some account')
    account.deposit(100)

    result = serialize_account(account)
    result = json.loads(result)

    assert result == {'balance': '100', 'name': 'Some account'}


def test_serialize_dashboard_with_one_account():
    account = Account('Some account')
    account.deposit(100)

    dashboard = Dashboard()
    dashboard.add_account(account)

    result = serialize_dashboard(dashboard)
    result = json.loads(result)

    assert result == {'accounts': [{'name': 'Some account', 'balance': '100'}]}
