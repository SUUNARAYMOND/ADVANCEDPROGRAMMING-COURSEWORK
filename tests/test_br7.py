from datetime import date
from decimal import Decimal

from application.dto import MakeBookingRequest
from domain.booking_dates import BookingDates
from domain.room import Room
from interface.main import build_service
from infrastructure.in_memory_booking_repository import InMemoryBookingRepository
from infrastructure.in_memory_room_repository import InMemoryRoomRepository


def test_T7_successful_booking_is_handled_and_room_is_reserved():
    rooms = InMemoryRoomRepository()
    bookings = InMemoryBookingRepository()
    rooms.save(Room("R101", "101", "Double", Decimal("100.00")))
    service = build_service(rooms, bookings)

    result = service.make_booking(
        MakeBookingRequest("B001", "R101", "Amina", date(2026, 10, 10), date(2026, 10, 13))
    )

    # Output DTO reports success with the BR4 price for 3 nights.
    assert result.success is True
    assert result.booking_status == "Confirmed"
    assert result.total_price == Decimal("300.00")

    # Aggregate A (Booking) was stored.
    stored_booking = bookings.get("B001")
    assert stored_booking is not None
    assert stored_booking.status.value == "Confirmed"

    # The BookingConfirmed event was handled: Aggregate B (Room) changed.
    room = rooms.get("R101")
    assert len(room.reservations) == 1
    assert room.reservations[0].booking_id == "B001"
    assert room.reservations[0].dates == BookingDates(date(2026, 10, 10), date(2026, 10, 13))
