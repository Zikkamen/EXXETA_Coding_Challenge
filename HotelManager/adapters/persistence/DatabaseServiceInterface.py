from abc import ABC, abstractmethod

from HotelManager.application.model.HotelRoomConditionsDTO import HotelRoomConditionsDTO
from HotelManager.application.model.HotelRoomDTO import HotelRoomDTO


class DatabaseServiceInterface(ABC):
    @abstractmethod
    def add_hotelroom_to_database(self, hotelroom: HotelRoomDTO) -> None:
        pass

    @abstractmethod
    def get_all_hotelrooms_from_database(self) -> list:
        pass

    @abstractmethod
    def get_all_hotelrooms_with_conditions_from_database(self, hotel_room_condition: HotelRoomConditionsDTO) -> list[tuple]:
        pass

    @abstractmethod
    def delete_hotelroom_from_database(self, room_id: int) -> None:
        pass

    @abstractmethod
    def update_hotelroom_in_database(self, room_id: int, hotelroom: HotelRoomDTO) -> None:
        pass

    @abstractmethod
    def clear_hotelrooms_database(self) -> None:
        pass
