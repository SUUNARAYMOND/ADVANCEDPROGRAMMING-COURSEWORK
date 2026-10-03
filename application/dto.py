from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class MakeBookingRequest:
    """Input DTO: plain data describing the guest's request."""

    booking_id: str
    room_id: str
    guest_name: str
    check_in: date
    check_out: date


@dataclass(frozen=True)
class MakeBookingResult:
    """Output DTO: plain data describing what happened."""

    success: bool
    message: str
    booking_id: Optional[str] = None
    booking_status: Optional[str] = None
    total_price: Optional[Decimal] = None
