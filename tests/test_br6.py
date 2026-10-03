from datetime import date
from decimal import Decimal

from application.booking_service import BookingService
from application.dto import MakeBookingRequest
from application.event_handling import ReservationOutcome
from domain.room import Room
from infrastructure.in_memory_booking_repository import InMemoryBookingRepository
from infrastructure.in_memory_room_repository import InMemoryRoomRepository


class SpyHandler:
    """Records any event it receives, so the test can prove none was sent."""

    def __init__(self):
        self.events = []

    def handle(self, event):
        self.events.append(event)
        return ReservationOutcome(True)


def test_T6_booking_for_unknown_room_is_rejected_after_lookup():
    rooms = InMemoryRoomRepository()
    bookings = InMemoryBookingRepository()
    rooms.save(Room("R101", "101", "Double", Decimal("100.00")))
    handler = SpyHandler()
    service = BookingService(rooms, bookings, handler)

    # Repository lookup: a stored aggregate is found, an unknown ID is not.
    assert rooms.get("R101") is not None
    assert rooms.get("R999") is None

    result = service.make_booking(
        MakeBookingRequest("B001", "R999", "Amina", date(2026, 10, 10), date(2026, 10, 13))
    )

    # The use case stops at the failed lookup.
    assert result.success is False
    assert "R999" in result.message
    assert "not found" in result.message
    assert bookings.get("B001") is None
    assert handler.events == []
    assert rooms.get("R101").reservations == ()
