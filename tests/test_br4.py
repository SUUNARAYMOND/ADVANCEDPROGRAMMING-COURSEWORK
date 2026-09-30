from datetime import date
from decimal import Decimal

import pytest

from domain.booking_dates import BookingDates
from domain.booking_pricing_service import BookingPricingService
from domain.room import Room


def test_T4_price_combines_room_rate_and_stay_nights_with_exact_money():
    room = Room("R205", "205", "Double", Decimal("99.95"))
    dates = BookingDates(date(2026, 10, 1), date(2026, 10, 4))
    service = BookingPricingService()

    total = service.calculate_price(room.nightly_price, dates.nights)
    assert total == Decimal("299.85")
    assert isinstance(total, Decimal)
    assert service.calculate_price(Decimal("0.10"), 3) == Decimal("0.30")
    assert service.calculate_price(Decimal("0.00"), 1) == Decimal("0.00")

    for nights in (0, -1, 1.5, True):
        with pytest.raises(ValueError, match="positive integer"):
            service.calculate_price(room.nightly_price, nights)

    for rate in ("-1", "NaN", "Infinity", "invalid"):
        with pytest.raises(ValueError, match="finite non-negative"):
            service.calculate_price(rate, dates.nights)
