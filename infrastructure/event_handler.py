from dataclasses import dataclass
from typing import Any, Protocol

from domain.events import BookingConfirmed


@dataclass(frozen=True)
class ReservationOutcome:
	accepted: bool
	reason: str | None = None


class RoomRepository(Protocol):
	def get(self, room_id: str) -> Any | None: ...

	def save(self, room: Any) -> None: ...


class RoomReservationHandler:
	def __init__(self, room_repository: RoomRepository) -> None:
		self._rooms = room_repository

	def handle(self, event: BookingConfirmed) -> ReservationOutcome:
		room = self._rooms.get(event.room_id)
		if room is None:
			return ReservationOutcome(False, f"Room '{event.room_id}' not found")

		try:
			room.reserve(event.booking_id, event.dates)
		except ValueError as error:
			return ReservationOutcome(False, str(error))

		self._rooms.save(room)
		return ReservationOutcome(True)
