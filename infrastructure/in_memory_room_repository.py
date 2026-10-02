from typing import Any


class InMemoryRoomRepository:
	def __init__(self) -> None:
		self._rooms: dict[str, Any] = {}

	def get(self, room_id: str) -> Any | None:
		return self._rooms.get(room_id)

	def save(self, room: Any) -> None:
		self._rooms[room.room_id] = room
