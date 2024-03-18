import functools
from pathlib import Path

from HotelManager.adapters.persistence.DatabaseService import DatabaseService
from HotelManager.application.model.HotelRoomConditionsDTO import HotelRoomConditionsDTO
from HotelManager.application.model.HotelRoomDTO import HotelRoomDTO, HotelRoomType, HotelRoomTypeMapper
from HotelManager.application.services.PersistenceServiceInterface import PersistenceServiceInterface


class PersistenceService(PersistenceServiceInterface):
    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path

        self.database_service = None
        self.cached_data = {}

        self.__initialize_database()

        if self.database_service is None:
            raise Exception('Database was not initialized')

        self.__initialize_cache()

    def get_all_hotelrooms(self) -> list[HotelRoomDTO]:
        return [value for key, value in self.cached_data.items()]

    def get_all_hotelrooms_fulfilling_conditions(self, hotel_room_condition: HotelRoomConditionsDTO) -> list[HotelRoomDTO]:
        list_of_ids = self.__get_ids_from_condition(hotel_room_condition)

        return [self.cached_data[hotelroom_id] for hotelroom_id in list_of_ids]

    def add_hotelroom_to_database(self, hotelroom: HotelRoomDTO) -> None:
        if hotelroom.room_id in self.cached_data:
            raise Exception('Error adding hotel room. Hotel room already exists', hotelroom.room_id)

        self.database_service.add_hotelroom_to_database(hotelroom)
        self.cached_data[hotelroom.room_id] = hotelroom
        self.__get_ids_from_condition.cache_clear()

    def get_information_hotelroom_by_id(self, room_id: int) -> HotelRoomDTO:
        if room_id not in self.cached_data:
            raise Exception('Error retrieving data to hotel room. Hotel room does not exist', room_id, self.cached_data)

        return self.cached_data.get(room_id)

    def update_hotelroom_in_database(self, room_id: int, hotelroom: HotelRoomDTO) -> None:
        if room_id not in self.cached_data:
            raise Exception('Error updating hotel room. Hotel room to be updated does not exists', room_id)

        if room_id != hotelroom.room_id and hotelroom.room_id in self.cached_data:
            raise Exception(f'Error updating hotel room. Updated room id already exists {hotelroom.room_id}.',
                            'Please remove it before updating')

        if room_id != hotelroom.room_id:
            del self.cached_data[room_id]

        self.database_service.update_hotelroom_in_database(room_id, hotelroom)
        self.cached_data[hotelroom.room_id] = hotelroom
        self.__get_ids_from_condition.cache_clear()

    def delete_hotelroom_in_database(self, room_id: int):
        if room_id not in self.cached_data:
            raise Exception('Error deleting hotel room. Hotel room does not exist', room_id)

        self.database_service.delete_hotelroom_from_database(room_id)
        del self.cached_data[room_id]
        self.__get_ids_from_condition.cache_clear()

    @functools.lru_cache(maxsize=10)
    def __get_ids_from_condition(self, hotel_room_condition: HotelRoomConditionsDTO) -> list[int]:
        hotelrooms_list = self.database_service.get_all_hotelrooms_with_conditions_from_database(hotel_room_condition)

        return [hotelroom[0] for hotelroom in hotelrooms_list]

    def __initialize_database(self) -> None:
        with open(self.root_path.joinpath('credentials/database_credentials.xml')) as fs:
            xml_file = fs.read()

        self.database_service = DatabaseService(xml_file)
        self.__add_init_data()

    def __add_init_data(self) -> None:
        self.database_service.clear_hotelrooms_database()

        self.add_hotelroom_to_database(HotelRoomDTO(room_id=1, room_size=HotelRoomType.SINGLE, has_minibar=True))
        self.add_hotelroom_to_database(HotelRoomDTO(room_id=2, room_size=HotelRoomType.DOUBLE, has_minibar=True))
        self.add_hotelroom_to_database(HotelRoomDTO(room_id=3, room_size=HotelRoomType.SUITE, has_minibar=False))

    def __initialize_cache(self) -> None:
        hotelroom_list = self.database_service.get_all_hotelrooms_from_database()

        for hotelroom in hotelroom_list:
            self.cached_data[hotelroom[0]] = HotelRoomDTO(room_id=hotelroom[0],
                                                          room_size=HotelRoomTypeMapper().string_to_type(hotelroom[1]),
                                                          has_minibar=hotelroom[2])
