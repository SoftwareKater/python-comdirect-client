from dataclasses import dataclass
from enum import Enum
from src.models.account.transaction_type_enum import TransactionType
from src.models.shared.amount_value_model import AmountValue


class BookingStatus(Enum):
    BOOKED: 1
    NOTBOOKED: 2


@dataclass
class AccountTransaction():
    booking_status: BookingStatus
    booking_date: str
    amount: AmountValue
    transaction_type: TransactionType
