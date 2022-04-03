
from typing import Sequence

from src.models.account.account_balance_model import AccountBalance
from src.models.account.account_transaction_model import AccountTransaction


def account_balances_to_table(account_balances: Sequence[AccountBalance]) -> Sequence:
    table = []
    table.append(['Account Id', 'IBAN', 'Währung', 'Wert'])
    for i in range(len(account_balances)):
        table.append([account_balances[i].account.account_id, account_balances[i].account.iban, account_balances[i].balance.unit,
                     account_balances[i].balance.value])
    return table


def account_transactions_to_table(account_transactions: Sequence[AccountTransaction]) -> Sequence:
    table = []
    table.append(['Date', 'Typ', 'Währung', 'Wert'])
    for i in range(len(account_transactions)):
        table.append([account_transactions[i].booking_date, account_transactions[i].transaction_type, account_transactions[i].amount.unit,
                     account_transactions[i].amount.value])
    return table
