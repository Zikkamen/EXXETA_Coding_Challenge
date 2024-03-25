from unittest import TestCase

from HotelManager.application.Language import Language
from HotelManager.application.model.HotelRoomDTO import HotelRoomDTO, HotelRoomType
from HotelManager.application.services.HotelManagerService import hotelroom_to_website_mapper


def generate_hotelroom_1() -> HotelRoomDTO:
    return HotelRoomDTO(room_id=0, room_size=HotelRoomType.SINGLE, has_minibar=False)


def generate_hotelroom_2() -> HotelRoomDTO:
    return HotelRoomDTO(room_id=1, room_size=HotelRoomType.DOUBLE, has_minibar=True)


class Test(TestCase):
    def test_hotelroom_to_website_mapper_german_single(self):
        hotel_room = generate_hotelroom_1()

        web_hotel_room = hotelroom_to_website_mapper(hotel_room, Language.GERMAN)

        assert web_hotel_room.room_id == 0
        assert web_hotel_room.room_size == 'Einzelzimmer'
        assert web_hotel_room.has_minibar == 'False'

    def test_hotelroom_to_website_mapper_single(self):
        hotel_room = generate_hotelroom_1()

        web_hotel_room = hotelroom_to_website_mapper(hotel_room, None)

        assert web_hotel_room.room_id == 0
        assert web_hotel_room.room_size == 'SINGLE'
        assert web_hotel_room.has_minibar == 'False'

    def test_hotelroom_to_website_mapper_german_double(self):
        hotel_room = generate_hotelroom_2()

        web_hotel_room = hotelroom_to_website_mapper(hotel_room, Language.GERMAN)

        assert web_hotel_room.room_id == 1
        assert web_hotel_room.room_size == 'Doppelzimmer'
        assert web_hotel_room.has_minibar == 'True'

    def test_hotelroom_to_website_mapper_double(self):
        hotel_room = generate_hotelroom_2()

        web_hotel_room = hotelroom_to_website_mapper(hotel_room, None)

        assert web_hotel_room.room_id == 1
        assert web_hotel_room.room_size == 'DOUBLE'
        assert web_hotel_room.has_minibar == 'True'
