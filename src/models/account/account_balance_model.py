from dataclasses import dataclass
from src.models.shared.amount_model import Amount

from src.models.shared.currency_enum import Currency


@dataclass
class AccountBalance():
    account_id: str
    account_display_id: str
    currency: Currency
    iban: str
    balance: Amount

