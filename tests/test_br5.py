from domain.events import BookingConfirmed
from infrastructure.event_handler import RoomReservationHandler


class FakeRoom:
	def __init__(self):
		self.reservations = []

	def reserve(self, booking_id, dates):
		self.reservations.append((booking_id, dates))


class FakeRoomRepository:
	def __init__(self, room):
		self.room = room
		self.saved_rooms = []

	def get(self, room_id):
		return self.room if room_id == "R101" else None

	def save(self, room):
		self.saved_rooms.append(room)


def test_T5_booking_confirmed_event_reserves_and_saves_room():
	room = FakeRoom()
	repository = FakeRoomRepository(room)
	dates = object()
	event = BookingConfirmed("B001", "R101", dates)

	outcome = RoomReservationHandler(repository).handle(event)

	assert outcome.accepted is True
	assert room.reservations == [("B001", dates)]
	assert repository.saved_rooms == [room]
