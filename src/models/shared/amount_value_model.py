from dataclasses import dataclass

from src.models.shared.currency_enum import Currency


@dataclass
class AmountValue():
    value: float
    unit: Currency