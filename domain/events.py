from dataclasses import dataclass
from domain.booking_dates import BookingDates


@dataclass(frozen=True)
class BookingConfirmed:
    """BR5: tell the handler which booking, room and dates to reserve."""

    booking_id: str
    room_id: str
    dates: BookingDates
