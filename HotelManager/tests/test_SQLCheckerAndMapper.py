from unittest import TestCase

from HotelManager.adapters.persistence.SQLCheckerAndMapper import SQLCheckerAndMapper
from HotelManager.application.model.HotelRoomConditionsDTO import HotelRoomConditionsDTO


class TestSQLCheckerAndMapper(TestCase):
    def test_convert_and_check_hotelroom_to_sql_good(self):
        sql_query_1 = SQLCheckerAndMapper().convert_and_check_hotelroom_to_sql(
            HotelRoomConditionsDTO(room_id='0', room_size='SINGLE', has_minibar='False')
        )

        assert sql_query_1 == " WHERE ID=0 AND hotelroom_size='SINGLE' AND has_minibar=False"

        sql_query_2 = SQLCheckerAndMapper().convert_and_check_hotelroom_to_sql(
            HotelRoomConditionsDTO(room_id='0', has_minibar='False')
        )

        assert sql_query_2 == " WHERE ID=0 AND has_minibar=False"

        sql_query_3 = SQLCheckerAndMapper().convert_and_check_hotelroom_to_sql(
            HotelRoomConditionsDTO(room_size='SINGLE')
        )

        assert sql_query_3 == " WHERE hotelroom_size='SINGLE'"

        sql_query_3 = SQLCheckerAndMapper().convert_and_check_hotelroom_to_sql(
            HotelRoomConditionsDTO()
        )

        assert sql_query_3 == ""

    def test_convert_and_check_hotelroom_to_sql_bad(self):
        self.assertRaises(
            ValueError,
            SQLCheckerAndMapper().convert_and_check_hotelroom_to_sql,
            HotelRoomConditionsDTO(room_id='0x00', room_size='SINGLE', has_minibar='False')
        )

        self.assertRaises(
            Exception,
            SQLCheckerAndMapper().convert_and_check_hotelroom_to_sql,
            HotelRoomConditionsDTO(room_id='0', room_size='Not Existent', has_minibar='False')
        )

        self.assertRaises(
            Exception,
            SQLCheckerAndMapper().convert_and_check_hotelroom_to_sql,
            HotelRoomConditionsDTO(room_id='0', room_size='SINGLE', has_minibar='Not a Boolean')
        )

        self.assertRaises(
            Exception,
            SQLCheckerAndMapper().convert_and_check_hotelroom_to_sql,
            HotelRoomConditionsDTO(room_id='0', room_size='SQL INJECTION\' WHERE 1=1\'', has_minibar='Not a Boolean')
        )
