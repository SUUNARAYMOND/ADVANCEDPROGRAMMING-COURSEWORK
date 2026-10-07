from datetime import date
from decimal import Decimal

from domain.booking import Booking
from domain.booking_dates import BookingDates
from domain.booking_status import BookingStatus
from domain.events import BookingConfirmed
from domain.room import Room
from infrastructure.event_handler import RoomReservationHandler
from infrastructure.in_memory_room_repository import InMemoryRoomRepository


def test_T5_confirmation_produces_event_that_requests_room_reservation():
    dates = BookingDates(date(2026, 10, 10), date(2026, 10, 13))
    booking = Booking("B001", "R101", "Amina", dates, Decimal("300.00"))
    room = Room("R101", "101", "Double", Decimal("100.00"))
    rooms = InMemoryRoomRepository()
    rooms.save(room)

    event = booking.confirm()

    assert booking.status == BookingStatus.CONFIRMED
    assert isinstance(event, BookingConfirmed)
    assert event.booking_id == "B001"
    assert event.room_id == "R101"
    assert event.dates == dates
    assert room.reservations == ()  # Booking does not reserve Room directly.

    outcome = RoomReservationHandler(rooms).handle(event)

    assert outcome.accepted is True
    assert outcome.reason is None
    saved_room = rooms.get("R101")
    assert len(saved_room.reservations) == 1
    assert saved_room.reservations[0].booking_id == "B001"
    assert saved_room.reservations[0].dates == dates
