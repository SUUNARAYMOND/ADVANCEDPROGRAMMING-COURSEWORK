from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class BookingDates:
    """BR1: a valid, immutable stay, with no separate identity.

    Check-in is inclusive and check-out exclusive, so adjacent stays do not
    overlap. Equality compares dates rather than an identifier.
    """

    check_in: date
    check_out: date

    def __post_init__(self):
        if self.check_out <= self.check_in:
            raise ValueError("Check-out must be after check-in")

    @property
    def nights(self) -> int:
        return (self.check_out - self.check_in).days

    def overlaps(self, other: "BookingDates") -> bool:
        return self.check_in < other.check_out and other.check_in < self.check_out
