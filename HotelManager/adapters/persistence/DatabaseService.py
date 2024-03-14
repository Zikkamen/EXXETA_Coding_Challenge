import xml.etree.ElementTree as ET

import psycopg2

from HotelManager.application.model.HotelRoomDTO import HotelRoomDTO, HotelRoomTypeMapper


class DatabaseService:
    def __init__(self, xml_string: str) -> None:
        xml_tree = ET.fromstring(xml_string)

        self.conn = psycopg2.connect(
            database=xml_tree.find('database').text,
            user=xml_tree.find('user').text,
            password=xml_tree.find('password').text,
            host=xml_tree.find('host').text,
            port=xml_tree.find('port').text
        )

    def __del__(self) -> None:
        self.conn.close()

    def add_hotelroom_to_database(self, hotelroom: HotelRoomDTO) -> None:
        add_hotelroom_query = "INSERT INTO hotel_rooms(ID, hotel_size, has_minibar) VALUES (%s, '%s', %s);" \
                              % (hotelroom.room_id, HotelRoomTypeMapper().type_to_string(hotelroom.room_size),
                                 hotelroom.has_minibar)

        self.__execute_modify_query(add_hotelroom_query)

    def get_all_hotelrooms_from_database(self) -> list:
        get_all_hotelrooms_query = "SELECT * FROM hotel_rooms"

        return self.__execute_read_query(get_all_hotelrooms_query)

    def delete_hotelroom_from_database(self, room_id: int) -> None:
        delete_hotelroom_query = "DELETE FROM hotel_rooms WHERE ID = %s;" % (room_id)

        self.__execute_modify_query(delete_hotelroom_query)

    def update_hotelroom_in_database(self, room_id: int, hotelroom: HotelRoomDTO) -> None:
        update_hotelroom_query = "UPDATE hotel_rooms SET ID=%s, hotel_size='%s', has_minbar=%s WHERE ID=%s;" \
                       % (hotelroom.room_id, HotelRoomTypeMapper().type_to_string(hotelroom.room_size),
                          hotelroom.has_minibar, room_id)

        self.__execute_modify_query(update_hotelroom_query)

    def clear_hotelrooms_database(self) -> None:
        delete_everything_query = "DELETE FROM hotel_rooms;"

        self.__execute_modify_query(delete_everything_query)

    def __execute_modify_query(self, query: str) -> None:
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def __execute_read_query(self, query: str) -> list:
        cur = self.conn.cursor()
        cur.execute(query)

        return cur.fetchall()
