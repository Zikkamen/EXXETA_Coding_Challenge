from pathlib import Path
from typing import Optional

from HotelManager.adapters.persistence.PersitenceService import PersistenceService
from HotelManager.application.Language import Language
from HotelManager.application.model.HotelRoomDTO import HotelRoomDTO, HotelRoomTypeMapper


def hotelroom_to_website_mapper(hotelroom: HotelRoomDTO, language: Optional[Language]) -> tuple:
    if language is None:
        return (hotelroom.room_id,
                HotelRoomTypeMapper().type_to_string(hotelroom.room_size),
                str(hotelroom.has_minibar))

    return (hotelroom.room_id,
            HotelRoomTypeMapper().type_to_website_display_german(hotelroom.room_size),
            str(hotelroom.has_minibar))


class HotelManagerService:
    def __init__(self, root_path: Path) -> None:
        self.persistence_service = PersistenceService(root_path)

    def add_hotelroom(self, hotel_room: HotelRoomDTO) -> None:
        self.persistence_service.add_hotelroom_to_database(hotel_room)

    def get_all_hotelrooms(self, language: Language) -> list[tuple]:
        list_of_hotelrooms_dto = self.persistence_service.get_all_hotelrooms()

        converted_hotelrooms = []

        for hotelroom in list_of_hotelrooms_dto:
            converted_hotelrooms.append(hotelroom_to_website_mapper(hotelroom, language))

        return converted_hotelrooms

    def update_room(self, room_id: int, hotel_room: HotelRoomDTO) -> None:
        self.persistence_service.update_hotelroom_in_database(room_id, hotel_room)

    def delete_hotelroom(self, room_id: int) -> None:
        self.persistence_service.delete_hotelroom_in_database(room_id)

    def get_information_hotelroom(self, room_id: int, language: Language = None) -> tuple[str]:
        hotelroom_dto = self.persistence_service.get_information_hotelroom_by_id(room_id)

        return hotelroom_to_website_mapper(hotelroom_dto, language)
