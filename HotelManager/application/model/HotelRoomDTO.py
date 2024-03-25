from enum import Enum

from pydantic import BaseModel


class HotelRoomType(Enum):
    SINGLE = 1
    DOUBLE = 2
    SUITE = 3


class HotelRoomDTO(BaseModel):
    room_id: int
    room_size: HotelRoomType
    has_minibar: bool


class HotelRoomTypeMapper:
    def __init__(self):
        self.__string_to_type_map = {
            'SINGLE': HotelRoomType.SINGLE,
            'DOUBLE': HotelRoomType.DOUBLE,
            'SUITE': HotelRoomType.SUITE
        }

        self.__type_to_string_map = {
            HotelRoomType.SINGLE: 'SINGLE',
            HotelRoomType.DOUBLE: 'DOUBLE',
            HotelRoomType.SUITE: 'SUITE'
        }

        self.__type_to_website_german_map = {
            HotelRoomType.SINGLE: 'Einzelzimmer',
            HotelRoomType.DOUBLE: 'Doppelzimmer',
            HotelRoomType.SUITE: 'Suite'
        }

    def string_to_type(self, room_type_str: str) -> HotelRoomType:
        return self.__string_to_type_map[room_type_str]

    def type_to_string(self, room_type: HotelRoomType) -> str:
        return self.__type_to_string_map[room_type]

    def type_to_website_display_german(self, room_type: HotelRoomType) -> str:
        return self.__type_to_website_german_map[room_type]

    def type_is_in_type_map(self, room_type_str) -> bool:
        return room_type_str in self.__string_to_type_map
