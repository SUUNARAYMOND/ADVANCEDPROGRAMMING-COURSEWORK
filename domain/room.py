from dataclasses import dataclass
from decimal import Decimal

from domain.booking_dates import BookingDates


@dataclass(frozen=True)
class Reservation:
    """An immutable record belonging to Room, referencing Booking by ID."""

    booking_id: str
    dates: BookingDates


class Room:
    """BR3: a room cannot accept overlapping reservations."""

    def __init__(self, room_id, room_number, room_type, nightly_price):
        self.room_id = room_id
        self.room_number = room_number
        self.room_type = room_type
        self.nightly_price = Decimal(str(nightly_price))
        self._reservations = []

    @property
    def reservations(self) -> tuple[Reservation, ...]:
        # Callers can inspect reservations, but changes go through reserve().
        return tuple(self._reservations)

    def reserve(self, booking_id: str, dates: BookingDates) -> Reservation:
        for reservation in self._reservations:
            if dates.overlaps(reservation.dates):
                raise ValueError("Room already has an overlapping reservation")

        reservation = Reservation(booking_id, dates)
        self._reservations.append(reservation)
        return reservation
