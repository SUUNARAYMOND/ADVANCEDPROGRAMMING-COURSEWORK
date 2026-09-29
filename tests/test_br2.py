import pytest
from domain.booking import Booking


def test_cancelled_booking_cannot_be_confirmed():
    booking = Booking(
        booking_id="B001",
        room_id="R205",
        guest_name="John"
    )

    booking.cancel()

    with pytest.raises(ValueError):
        booking.confirm()