from typing import Optional

from pydantic import BaseModel


class HotelRoomConditionsDTO(BaseModel):
    room_id: Optional[str] = None
    room_size: Optional[str] = None
    has_minibar: Optional[str] = None
