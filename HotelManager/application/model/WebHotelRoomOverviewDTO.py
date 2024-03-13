from pydantic import BaseModel


class WebHotelRoomOverviewDTO(BaseModel):
    list_of_rooms: list[list[str]]
