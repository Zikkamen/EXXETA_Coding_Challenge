from abc import ABC, abstractmethod

from HotelManager.application.model.HotelRoomConditionsDTO import HotelRoomConditionsDTO
from HotelManager.application.model.HotelRoomDTO import HotelRoomDTO


class PersistenceServiceInterface(ABC):
    @abstractmethod
    def get_all_hotelrooms(self) -> list[HotelRoomDTO]:
        pass

    @abstractmethod
    def get_all_hotelrooms_fulfilling_conditions(self, hotel_room_condition: HotelRoomConditionsDTO) -> list[HotelRoomDTO]:
        pass

    @abstractmethod
    def add_hotelroom_to_database(self, hotelroom: HotelRoomDTO) -> None:
        pass

    @abstractmethod
    def get_information_hotelroom_by_id(self, room_id: int) -> HotelRoomDTO:
        pass

    @abstractmethod
    def update_hotelroom_in_database(self, room_id: int, hotelroom: HotelRoomDTO) -> None:
        pass

    @abstractmethod
    def delete_hotelroom_in_database(self, room_id: int):
        pass
