from dataclasses import dataclass
from typing import Optional, Protocol

from domain.events import BookingConfirmed


@dataclass(frozen=True)
class ReservationOutcome:
    """Result of the follow-up reservation requested by BookingConfirmed."""

    accepted: bool
    reason: Optional[str] = None


class BookingConfirmedHandler(Protocol):
    """What the Application Service needs from an event handler (BR5)."""

    def handle(self, event: BookingConfirmed) -> ReservationOutcome:
        ...
