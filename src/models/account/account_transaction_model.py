from dataclasses import dataclass
from enum import Enum

from src.models.shared.amount_model import Amount


class BookingStatus(Enum):
    BOOKED: 1
    NOTBOOKED: 2


@dataclass
class AccountTransaction():
    booking_status: BookingStatus
    booking_date: str
    amount: Amount
