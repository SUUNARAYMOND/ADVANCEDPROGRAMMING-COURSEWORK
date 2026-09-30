from datetime import date

import pytest

from domain.booking import Booking
from domain.booking_dates import BookingDates


def test_T2_booking_allows_only_pending_to_confirmed_or_cancelled():
    dates = BookingDates(
        check_in=date(2026, 10, 1),
        check_out=date(2026, 10, 3),
    )

    confirmed = Booking("B001", "R205", "John", dates, 200)
    cancelled = Booking("B002", "R205", "Jane", dates, 200)

    for booking in (confirmed, cancelled):
        assert booking.status == "Pending"
        assert booking.dates is dates
        assert booking.total_price == 200

    event = confirmed.confirm()
    assert confirmed.status == "Confirmed"
    assert event.booking_id == "B001"
    assert event.room_id == "R205"
    assert event.dates is dates

    cancelled.cancel()
    assert cancelled.status == "Cancelled"

    # Neither terminal booking can change state again.
    for booking in (confirmed, cancelled):
        previous_status = booking.status
        for transition in (booking.confirm, booking.cancel):
            with pytest.raises(ValueError, match="Cannot"):
                transition()
            assert booking.status == previous_status

        # State changes must go through the aggregate's methods.
        with pytest.raises(AttributeError):
            booking.status = "Pending"
