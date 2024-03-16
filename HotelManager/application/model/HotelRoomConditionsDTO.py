from typing import Optional

from pydantic import BaseModel


class HotelRoomConditionsDTO(BaseModel):
    room_id: Optional[str] = None
    room_size: Optional[str] = None
    has_minibar: Optional[str] = None

    def __hash__(self):
        return hash((self.room_id, self.room_size, self.has_minibar))
