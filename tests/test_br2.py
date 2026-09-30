import pytest
from datetime import date
from types import SimpleNamespace

from domain.booking import Booking


def test_T2_booking_allows_only_pending_to_confirmed_or_cancelled():
    # Member 2's BookingDates is not implemented yet. This stand-in supplies
    # its agreed date fields; validation belongs to BookingDates, not Booking.
    dates = SimpleNamespace(
        check_in=date(2026, 10, 1),
        check_out=date(2026, 10, 3),
    )

    for terminal_status in ("Confirmed", "Cancelled"):
        booking = Booking(
            booking_id="B001",
            room_id="R205",
            guest_name="John",
            dates=dates,
            total_price=200,
        )
        assert booking.status == "Pending"
        assert booking.dates is dates
        assert booking.total_price == 200

        if terminal_status == "Confirmed":
            event = booking.confirm()
            assert event.booking_id == booking.booking_id
            assert event.room_id == booking.room_id
            assert event.dates is dates
        else:
            booking.cancel()

        assert booking.status == terminal_status

        for transition in (booking.confirm, booking.cancel):
            with pytest.raises(ValueError, match="Cannot"):
                transition()
            assert booking.status == terminal_status

        # State changes must go through the aggregate's methods.
        with pytest.raises(AttributeError):
            booking.status = "Pending"
