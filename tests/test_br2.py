from datetime import date

import pytest

from domain.booking import Booking
from domain.booking_dates import BookingDates
from domain.booking_status import BookingStatus


def test_T2_booking_allows_only_pending_to_confirmed_or_cancelled():
    dates = BookingDates(
        check_in=date(2026, 10, 1),
        check_out=date(2026, 10, 3),
    )

    confirmed = Booking(
        "B001",
        "R205",
        "John",
        dates,
        200
    )

    cancelled = Booking(
        "B002",
        "R205",
        "Jane",
        dates,
        200
    )

    # Both bookings start as Pending.
    assert confirmed.status == BookingStatus.PENDING
    assert cancelled.status == BookingStatus.PENDING

    # Pending -> Confirmed is allowed.
    confirmed.confirm()
    assert confirmed.status == BookingStatus.CONFIRMED

    # Pending -> Cancelled is allowed.
    cancelled.cancel()
    assert cancelled.status == BookingStatus.CANCELLED

    # Confirmed bookings cannot change state.
    with pytest.raises(ValueError):
        confirmed.confirm()

    with pytest.raises(ValueError):
        confirmed.cancel()

    # Cancelled bookings cannot change state.
    with pytest.raises(ValueError):
        cancelled.confirm()

    with pytest.raises(ValueError):
        cancelled.cancel()

    # The failed transitions did not change the final states.
    assert confirmed.status == BookingStatus.CONFIRMED
    assert cancelled.status == BookingStatus.CANCELLED