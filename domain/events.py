from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.booking_dates import BookingDates


@dataclass(frozen=True)
class BookingConfirmed:
    """Confirmation requests reservation of a room for the booking's dates.

    ``dates`` is Member 2's BookingDates value object. The handler uses this
    event to call Room.reserve(booking_id, dates).
    """

    booking_id: str
    room_id: str
    dates: "BookingDates"
