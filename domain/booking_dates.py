from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class BookingDates:
    """BR1: immutable dates with checkout later than check-in."""

    check_in: date
    check_out: date

    def __post_init__(self):
        if self.check_out <= self.check_in:
            raise ValueError("Check-out must be after check-in")

    @property
    def nights(self) -> int:
        return (self.check_out - self.check_in).days

    def overlaps(self, other: "BookingDates") -> bool:
        # Checkout day can be another guest's check-in day.
        return self.check_in < other.check_out and other.check_in < self.check_out
