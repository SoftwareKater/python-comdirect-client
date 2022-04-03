from dataclasses import dataclass

from src.models.shared.currency_enum import Currency


@dataclass
class Amount():
    value: float
    unit: Currency