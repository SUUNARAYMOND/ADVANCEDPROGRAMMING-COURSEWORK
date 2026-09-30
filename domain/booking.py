from domain.booking_status import BookingStatus
from domain.events import BookingConfirmed


class Booking:
    """Booking aggregate root, responsible for BR2 lifecycle transitions."""

    def __init__(self, booking_id, room_id, guest_name, dates, total_price):
        self.booking_id = booking_id
        self.room_id = room_id
        self.guest_name = guest_name
        self.dates = dates
        self.total_price = total_price
        self._status = BookingStatus.PENDING

    @property
    def status(self):
        return self._status

    def confirm(self):
        if self.status != BookingStatus.PENDING:
            raise ValueError(
                f"Cannot confirm a booking with status '{self.status.value}'"
            )

        self._status = BookingStatus.CONFIRMED
        return BookingConfirmed(self.booking_id, self.room_id, self.dates)

    def cancel(self):
        if self.status != BookingStatus.PENDING:
            raise ValueError(
                f"Cannot cancel a booking with status '{self.status.value}'"
            )

        self._status = BookingStatus.CANCELLED
