from pydantic import BaseModel


class HotelRoomWebDTO(BaseModel):
    room_id: int
    room_size: str
    has_minibar: str
