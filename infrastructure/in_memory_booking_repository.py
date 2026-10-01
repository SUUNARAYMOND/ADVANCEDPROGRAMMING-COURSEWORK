from typing import Dict, Optional

from application.repositories import BookingRepository
from domain.booking import Booking


class InMemoryBookingRepository(BookingRepository):
    """Keeps Booking aggregates in a dictionary keyed by booking_id."""

    def __init__(self) -> None:
        self._bookings: Dict[str, Booking] = {}

    def get(self, booking_id: str) -> Optional[Booking]:
        return self._bookings.get(booking_id)

    def save(self, booking: Booking) -> None:
        self._bookings[booking.booking_id] = booking
