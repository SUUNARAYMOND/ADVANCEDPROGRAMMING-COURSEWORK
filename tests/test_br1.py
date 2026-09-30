from dataclasses import FrozenInstanceError
from datetime import date

import pytest

from domain.booking_dates import BookingDates


def test_T1_dates_reject_invalid_stays_and_accept_one_night_boundary():
    check_in = date(2026, 10, 1)

    # Equal dates are the invalid boundary; earlier checkout is also rejected.
    for check_out in (check_in, date(2026, 9, 30)):
        with pytest.raises(ValueError, match="Check-out must be after check-in"):
            BookingDates(check_in, check_out)

    dates = BookingDates(check_in, date(2026, 10, 2))
    assert dates.nights == 1
    assert dates == BookingDates(check_in, date(2026, 10, 2))
    with pytest.raises(FrozenInstanceError):
        dates.check_out = check_in
