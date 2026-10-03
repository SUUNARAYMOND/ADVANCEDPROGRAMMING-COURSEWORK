"""Console entry point: wires the layers together and runs the use case.

Run from the project root with:  py -m interface.main
This is the only place that knows about both Application and Infrastructure,
so it is where dependency injection is visible.
"""

from datetime import date
from decimal import Decimal

from application.booking_service import BookingService
from application.dto import MakeBookingRequest, MakeBookingResult
from domain.room import Room
from infrastructure.event_handler import RoomReservationHandler
from infrastructure.in_memory_booking_repository import InMemoryBookingRepository
from infrastructure.in_memory_room_repository import InMemoryRoomRepository


def build_service(rooms: InMemoryRoomRepository, bookings: InMemoryBookingRepository) -> BookingService:
    handler = RoomReservationHandler(rooms)
    return BookingService(rooms, bookings, handler)


def print_result(label: str, result: MakeBookingResult) -> None:
    print(f"\n{label}")
    print(f"  success : {result.success}")
    print(f"  message : {result.message}")
    if result.success:
        print(f"  booking : {result.booking_id} ({result.booking_status})")
        print(f"  price   : {result.total_price}")


def main() -> None:
    rooms = InMemoryRoomRepository()
    bookings = InMemoryBookingRepository()
    rooms.save(Room("R101", "101", "Double", Decimal("100.00")))

    service = build_service(rooms, bookings)

    first = MakeBookingRequest("B001", "R101", "Amina", date(2026, 10, 10), date(2026, 10, 13))
    overlapping = MakeBookingRequest("B002", "R101", "John", date(2026, 10, 12), date(2026, 10, 14))

    print_result("Request 1: B001, 10-13 Oct", service.make_booking(first))
    print_result("Request 2: B002, 12-14 Oct (overlaps B001)", service.make_booking(overlapping))


if __name__ == "__main__":
    main()
