from domain.events import BookingConfirmed
from infrastructure.event_handler import RoomReservationHandler


class RejectingRoom:
	def __init__(self, reservations):
		self.reservations = list(reservations)

	def reserve(self, booking_id, dates):
		raise ValueError("Room already has an overlapping reservation")


class FakeRoomRepository:
	def __init__(self, room):
		self.room = room
		self.saved_rooms = []

	def get(self, room_id):
		return self.room if room_id == "R101" else None

	def save(self, room):
		self.saved_rooms.append(room)


def test_T8_room_rejection_is_reported_without_saving_room():
	existing_reservation = ("B-existing", object())
	room = RejectingRoom([existing_reservation])
	repository = FakeRoomRepository(room)
	event = BookingConfirmed("B001", "R101", object())

	outcome = RoomReservationHandler(repository).handle(event)

	assert outcome.accepted is False
	assert outcome.reason == "Room already has an overlapping reservation"
	assert room.reservations == [existing_reservation]
	assert repository.saved_rooms == []
