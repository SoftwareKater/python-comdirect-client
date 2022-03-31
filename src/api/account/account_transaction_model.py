from enum import Enum


class BookingStatus(Enum):
    BOOKED: 1
    NOTBOOKED: 2



class AccountTransaction():
    booking_status: BookingStatus
    booking_date: str
    amount: float
