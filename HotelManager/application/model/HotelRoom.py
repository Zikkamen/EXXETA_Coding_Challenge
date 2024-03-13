from typing import Optional

from pydantic import BaseModel


class HotelRoom(BaseModel):
    room_id: str
    room_size: str
    has_minibar: Optional[str] = None