from application.event_handling import BookingConfirmedHandler, ReservationOutcome
from application.repositories import RoomRepository
from domain.events import BookingConfirmed


class RoomReservationHandler(BookingConfirmedHandler):
    """BR5: when a booking is confirmed, ask the Room to reserve itself.

    The handler only retrieves the Room and delegates. Room enforces its own
    overlap rule (BR3); this class never edits reservations directly.
    """

    def __init__(self, room_repository: RoomRepository) -> None:
        self._rooms = room_repository

    def handle(self, event: BookingConfirmed) -> ReservationOutcome:
        room = self._rooms.get(event.room_id)
        if room is None:
            return ReservationOutcome(False, f"Room '{event.room_id}' not found")

        try:
            room.reserve(event.booking_id, event.dates)
        except ValueError as error:
            # Room refused: its reservations are unchanged, so nothing to save.
            return ReservationOutcome(False, str(error))

        self._rooms.save(room)
        return ReservationOutcome(True)
