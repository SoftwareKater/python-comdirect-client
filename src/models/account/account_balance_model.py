from dataclasses import dataclass
from src.models.account.account_model import Account
from src.models.shared.amount_value_model import AmountValue


@dataclass
class AccountBalance():
    account: Account
    balance: AmountValue
