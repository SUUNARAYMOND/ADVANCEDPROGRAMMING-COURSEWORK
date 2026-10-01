from abc import ABC, abstractmethod
from typing import Optional

from domain.booking import Booking
from domain.room import Room


class RoomRepository(ABC):
    """Abstraction for the Room aggregate root (BR6 lookup)."""

    @abstractmethod
    def get(self, room_id: str) -> Optional[Room]:
        """Return the Room with this ID, or None if it does not exist."""

    @abstractmethod
    def save(self, room: Room) -> None:
        """Store the Room, replacing any existing one with the same ID."""


class BookingRepository(ABC):
    """Abstraction for the Booking aggregate root."""

    @abstractmethod
    def get(self, booking_id: str) -> Optional[Booking]:
        """Return the Booking with this ID, or None if it does not exist."""

    @abstractmethod
    def save(self, booking: Booking) -> None:
        """Store the Booking, replacing any existing one with the same ID."""
