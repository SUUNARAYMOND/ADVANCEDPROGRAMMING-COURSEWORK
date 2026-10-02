from dataclasses import dataclass


@dataclass(frozen=True)
class BookingConfirmed:
	booking_id: str
	room_id: str
	dates: object
