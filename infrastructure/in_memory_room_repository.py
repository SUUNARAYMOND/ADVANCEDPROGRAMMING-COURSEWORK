from typing import Dict, Optional

from application.repositories import RoomRepository
from domain.room import Room


class InMemoryRoomRepository(RoomRepository):
    """Keeps Room aggregates in a dictionary keyed by room_id."""

    def __init__(self) -> None:
        self._rooms: Dict[str, Room] = {}

    def get(self, room_id: str) -> Optional[Room]:
        return self._rooms.get(room_id)

    def save(self, room: Room) -> None:
        self._rooms[room.room_id] = room
