from types import SimpleNamespace

from infrastructure.in_memory_booking_repository import InMemoryBookingRepository
from infrastructure.in_memory_room_repository import InMemoryRoomRepository


def test_T7_in_memory_repositories_save_and_get_aggregates():
	booking = SimpleNamespace(booking_id="B001")
	room = SimpleNamespace(room_id="R101")
	bookings = InMemoryBookingRepository()
	rooms = InMemoryRoomRepository()

	assert bookings.get("B001") is None
	assert rooms.get("R101") is None

	bookings.save(booking)
	rooms.save(room)

	assert bookings.get("B001") is booking
	assert rooms.get("R101") is room
