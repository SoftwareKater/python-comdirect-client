
from typing import Sequence

from src.models.account.account_balance_model import AccountBalance


def account_balances_to_table(account_balances: Sequence[AccountBalance]) -> list:
    table = []
    table.append(['Account Id', 'IBAN', 'Currency', 'Balance'])
    for i in range(len(account_balances)):
        table.append([account_balances[i].account_display_id, account_balances[i].iban, account_balances[i].balance.unit,
                     account_balances[i].balance.value])
    return table
