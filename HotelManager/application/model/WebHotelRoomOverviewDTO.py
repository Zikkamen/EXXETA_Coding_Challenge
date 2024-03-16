from pydantic import BaseModel

from HotelManager.application.model.HotelRoomWebDTO import HotelRoomWebDTO


class WebHotelRoomOverviewDTO(BaseModel):
    list_of_hotelrooms: list[HotelRoomWebDTO]
