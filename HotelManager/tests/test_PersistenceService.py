from pathlib import Path
from typing import Dict
from unittest import TestCase, mock
from unittest.mock import Mock

from HotelManager.adapters.persistence.PersistenceService import PersistenceService
from HotelManager.application.model.HotelRoomConditionsDTO import HotelRoomConditionsDTO
from HotelManager.application.model.HotelRoomDTO import HotelRoomDTO, HotelRoomType


def get_persistence_service() -> PersistenceService:
    persistence_service = PersistenceService(Path(), False)

    persistence_service.database_service = Mock()
    persistence_service.cached_data = {}

    return persistence_service


def init_cached_data(persistence_service: PersistenceService) -> list[HotelRoomDTO]:
    hotelroom_1 = HotelRoomDTO(room_id=1, room_size=HotelRoomType.SINGLE, has_minibar=False)
    hotelroom_2 = HotelRoomDTO(room_id=2, room_size=HotelRoomType.DOUBLE, has_minibar=True)
    hotelroom_3 = HotelRoomDTO(room_id=3, room_size=HotelRoomType.SUITE, has_minibar=False)

    persistence_service.cached_data = {
        hotelroom_1.room_id: hotelroom_1,
        hotelroom_2.room_id: hotelroom_2,
        hotelroom_3.room_id: hotelroom_3
    }

    return [hotelroom_1, hotelroom_2, hotelroom_3]


class TestPersistenceService(TestCase):
    def test_get_all_hotelrooms(self):
        persistence_service = get_persistence_service()
        list_of_hotelrooms = init_cached_data(persistence_service)

        assert persistence_service.get_all_hotelrooms() == list_of_hotelrooms

    def test_get_all_hotelrooms_fulfilling_conditions(self):
        persistence_service = get_persistence_service()

        persistence_service.database_service.get_all_hotelrooms_with_conditions_from_database.return_value = [(1,), (3,)]
        list_of_hotelrooms = init_cached_data(persistence_service)

        list_of_filtered_ids = persistence_service.get_all_hotelrooms_fulfilling_conditions(HotelRoomConditionsDTO())

        assert len(list_of_filtered_ids) == 2
        assert list_of_filtered_ids[0] == list_of_hotelrooms[0]
        assert list_of_filtered_ids[1] == list_of_hotelrooms[2]

    def test_add_hotelroom_to_database(self):
        persistence_service = get_persistence_service()

        hotelroom_1 = HotelRoomDTO(room_id=1, room_size=HotelRoomType.SINGLE, has_minibar=False)
        persistence_service.add_hotelroom_to_database(hotelroom_1)

        assert persistence_service.database_service.add_hotelroom_to_database.call_count == 1
        assert persistence_service.cached_data == {1: hotelroom_1}

    def test_add_hotelroom_to_database_already_inside(self):
        persistence_service = get_persistence_service()

        hotelroom_1 = HotelRoomDTO(room_id=1, room_size=HotelRoomType.SINGLE, has_minibar=False)
        persistence_service.cached_data = {1: hotelroom_1}

        self.assertRaises(
            Exception,
            persistence_service.add_hotelroom_to_database,
            hotelroom_1
        )

    def test_get_information_hotelroom_by_id(self):
        persistence_service = get_persistence_service()

        hotelroom_1 = HotelRoomDTO(room_id=1, room_size=HotelRoomType.SINGLE, has_minibar=False)
        persistence_service.cached_data = {1: hotelroom_1}

        assert persistence_service.get_information_hotelroom_by_id(1) == hotelroom_1

    def test_get_information_hotelroom_by_id_not_inside(self):
        persistence_service = get_persistence_service()

        self.assertRaises(
            Exception,
            persistence_service.get_information_hotelroom_by_id,
            1
        )

    def test_update_hotelroom_in_database_self(self):
        persistence_service = get_persistence_service()

        hotelroom_1 = HotelRoomDTO(room_id=1, room_size=HotelRoomType.SINGLE, has_minibar=False)
        hotelroom_1_new = HotelRoomDTO(room_id=1, room_size=HotelRoomType.SINGLE, has_minibar=True)
        persistence_service.cached_data = {1: hotelroom_1}

        persistence_service.update_hotelroom_in_database(1, hotelroom_1_new)

        assert persistence_service.database_service.update_hotelroom_in_database.call_count == 1
        assert persistence_service.cached_data == {1: hotelroom_1_new}

    def test_update_hotelroom_in_database_other_id(self):
        persistence_service = get_persistence_service()

        hotelroom_1 = HotelRoomDTO(room_id=1, room_size=HotelRoomType.SINGLE, has_minibar=False)
        hotelroom_1_new = HotelRoomDTO(room_id=2, room_size=HotelRoomType.SINGLE, has_minibar=False)
        persistence_service.cached_data = {1: hotelroom_1}

        persistence_service.update_hotelroom_in_database(1, hotelroom_1_new)

        assert persistence_service.database_service.update_hotelroom_in_database.call_count == 1
        assert persistence_service.cached_data == {2: hotelroom_1_new}

    def test_update_hotelroom_in_database_room_not_existent(self):
        persistence_service = get_persistence_service()

        hotelroom_1 = HotelRoomDTO(room_id=1, room_size=HotelRoomType.SINGLE, has_minibar=False)

        self.assertRaises(
            Exception,
            persistence_service.update_hotelroom_in_database,
            1,
            hotelroom_1
        )

    def test_update_hotelroom_in_database_new_room_exists(self):
        persistence_service = get_persistence_service()

        hotelroom_1 = HotelRoomDTO(room_id=1, room_size=HotelRoomType.SINGLE, has_minibar=False)
        hotelroom_1_new = HotelRoomDTO(room_id=2, room_size=HotelRoomType.SINGLE, has_minibar=False)
        hotelroom_2 = HotelRoomDTO(room_id=2, room_size=HotelRoomType.DOUBLE, has_minibar=False)
        persistence_service.cached_data = {1: hotelroom_1, 2: hotelroom_2}

        self.assertRaises(
            Exception,
            persistence_service.update_hotelroom_in_database,
            1,
            hotelroom_1_new
        )

        assert persistence_service.cached_data == {1: hotelroom_1, 2: hotelroom_2}

    def test_delete_hotelroom(self):
        persistence_service = get_persistence_service()

        hotelroom_1 = HotelRoomDTO(room_id=1, room_size=HotelRoomType.SINGLE, has_minibar=False)
        persistence_service.cached_data = {1: hotelroom_1}

        persistence_service.delete_hotelroom_in_database(1)

        assert persistence_service.cached_data == {}

    def test_delete_hotelroom_not_exists(self):
        persistence_service = get_persistence_service()

        hotelroom_1 = HotelRoomDTO(room_id=1, room_size=HotelRoomType.SINGLE, has_minibar=False)
        persistence_service.cached_data = {1: hotelroom_1}

        self.assertRaises(
            Exception,
            persistence_service.delete_hotelroom_in_database,
            2
        )
