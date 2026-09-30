from dataclasses import FrozenInstanceError
from datetime import date
from decimal import Decimal

import pytest

from domain.booking_dates import BookingDates
from domain.room import Room


def test_T3_room_rejects_overlaps_and_preserves_its_reservations():
    room = Room("R205", "205", "Double", Decimal("100.00"))
    existing = room.reserve(
        "B001", BookingDates(date(2026, 10, 3), date(2026, 10, 6))
    )
    before = room.reservations

    # Left overlap, right overlap, contained, enclosing and identical stays.
    for start, end in ((1, 4), (5, 8), (4, 5), (1, 8), (3, 6)):
        dates = BookingDates(date(2026, 10, start), date(2026, 10, end))
        with pytest.raises(ValueError, match="overlapping reservation"):
            room.reserve("B002", dates)
        assert room.reservations == before

    # Guests may check in on another guest's checkout day, on either side.
    earlier = room.reserve(
        "B003", BookingDates(date(2026, 10, 1), date(2026, 10, 3))
    )
    later = room.reserve(
        "B004", BookingDates(date(2026, 10, 6), date(2026, 10, 8))
    )
    assert room.reservations == (existing, earlier, later)
    assert before == (existing,)

    # Neither the exposed collection nor its records can bypass the root.
    with pytest.raises(AttributeError):
        room.reservations = ()
    with pytest.raises(FrozenInstanceError):
        existing.dates = later.dates
