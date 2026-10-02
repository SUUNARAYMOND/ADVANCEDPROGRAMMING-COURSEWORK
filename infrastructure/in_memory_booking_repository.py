from typing import Any


class InMemoryBookingRepository:
	def __init__(self) -> None:
		self._bookings: dict[str, Any] = {}

	def get(self, booking_id: str) -> Any | None:
		return self._bookings.get(booking_id)

	def save(self, booking: Any) -> None:
		self._bookings[booking.booking_id] = booking
