from dataclasses import dataclass

from src.models.shared.currency_enum import Currency


@dataclass
class Account():
    account_id: str
    account_display_id: str
    currency: Currency
    iban: str
