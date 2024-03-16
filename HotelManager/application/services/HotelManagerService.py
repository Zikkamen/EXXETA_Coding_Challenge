from pathlib import Path
from typing import Optional

from HotelManager.adapters.persistence.PersitenceService import PersistenceService
from HotelManager.application.Language import Language
from HotelManager.application.model.HotelRoomConditionsDTO import HotelRoomConditionsDTO
from HotelManager.application.model.HotelRoomDTO import HotelRoomDTO, HotelRoomTypeMapper
from HotelManager.application.model.HotelRoomWebDTO import HotelRoomWebDTO


def hotelroom_to_website_mapper(hotelroom: HotelRoomDTO, language: Optional[Language]) -> HotelRoomWebDTO:
    if language is Language.GERMAN:
        return HotelRoomWebDTO(room_id=hotelroom.room_id,
                               room_size=HotelRoomTypeMapper().type_to_website_display_german(hotelroom.room_size),
                               has_minibar=str(hotelroom.has_minibar))

    return HotelRoomWebDTO(room_id=hotelroom.room_id,
                           room_size=hotelroom.room_size,
                           has_minibar=str(hotelroom.has_minibar))


class HotelManagerService:
    def __init__(self, root_path: Path) -> None:
        self.persistence_service = PersistenceService(root_path)

    def add_hotelroom(self, hotelroom: HotelRoomDTO) -> None:
        self.persistence_service.add_hotelroom_to_database(hotelroom)

    def get_all_hotelrooms(self, language: Language) -> list[HotelRoomWebDTO]:
        hotelrooms_dto_list = self.persistence_service.get_all_hotelrooms()

        converted_hotelrooms = []

        for hotelroom in hotelrooms_dto_list:
            converted_hotelrooms.append(hotelroom_to_website_mapper(hotelroom, language))

        return converted_hotelrooms

    def get_hotelrooms_fulfilling_conditions(self, hotelroom_conditions: HotelRoomConditionsDTO) -> list[HotelRoomWebDTO]:
        pass

    def update_room(self, room_id: int, hotelroom: HotelRoomDTO) -> None:
        self.persistence_service.update_hotelroom_in_database(room_id, hotelroom)

    def delete_hotelroom(self, room_id: int) -> None:
        self.persistence_service.delete_hotelroom_in_database(room_id)

    def get_information_hotelroom(self, room_id: int, language: Language = None) -> HotelRoomWebDTO:
        hotelroom_dto = self.persistence_service.get_information_hotelroom_by_id(room_id)

        return hotelroom_to_website_mapper(hotelroom_dto, language)
