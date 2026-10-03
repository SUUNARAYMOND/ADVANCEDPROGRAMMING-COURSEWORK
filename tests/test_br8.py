from datetime import date
from decimal import Decimal

from application.dto import MakeBookingRequest
from domain.room import Room
from interface.main import build_service
from infrastructure.in_memory_booking_repository import InMemoryBookingRepository
from infrastructure.in_memory_room_repository import InMemoryRoomRepository


def test_T8_room_rejects_overlapping_follow_up_and_final_state_is_unchanged():
    rooms = InMemoryRoomRepository()
    bookings = InMemoryBookingRepository()
    rooms.save(Room("R101", "101", "Double", Decimal("100.00")))
    service = build_service(rooms, bookings)

    first = service.make_booking(
        MakeBookingRequest("B001", "R101", "Amina", date(2026, 10, 10), date(2026, 10, 13))
    )
    assert first.success is True

    # 12-14 Oct overlaps B001's 10-13 Oct stay, so Room must refuse (BR3).
    second = service.make_booking(
        MakeBookingRequest("B002", "R101", "John", date(2026, 10, 12), date(2026, 10, 14))
    )

    # Returned outcome reports the rejection and Room's own reason.
    assert second.success is False
    assert "overlapping reservation" in second.message
    assert second.booking_id is None

    # Final state: Room still holds only B001, and B002 was never stored.
    room = rooms.get("R101")
    assert [r.booking_id for r in room.reservations] == ["B001"]
    assert bookings.get("B002") is None
    assert bookings.get("B001") is not None
