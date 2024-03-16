from HotelManager.application.model.HotelRoomConditionsDTO import HotelRoomConditionsDTO
from HotelManager.application.model.HotelRoomDTO import HotelRoomTypeMapper


def list_to_str_and(list_of_conditions: list[tuple]) -> str:
    if len(list_of_conditions) == 0:
        return ""

    base_sql_str = ""

    for condition in list_of_conditions:
        if len(base_sql_str) > 0:
            base_sql_str += " AND "

        if isinstance(condition[1], str):
            base_sql_str += f"{condition[0]}='{condition[1]}'"
        else:
            base_sql_str += f"{condition[0]}={condition[1]}"

    return " WHERE " + base_sql_str


class SQLCheckerAndMapper:
    def __init__(self):
        self.hotelRoomTypeMapper = HotelRoomTypeMapper()

    def convert_and_check_hotelroom_to_sql(self, hotel_room_condition: HotelRoomConditionsDTO) -> str:
        list_conditions = []

        if hotel_room_condition.room_id is not None:
            list_conditions.append(('ID', int(hotel_room_condition.room_id)))

        if hotel_room_condition.room_size is not None:
            if not self.hotelRoomTypeMapper.type_is_in_type_map(hotel_room_condition.room_size):
                raise Exception('This type is not a Room Type', hotel_room_condition.room_size)

            list_conditions.append(('hotelroom_size', hotel_room_condition.room_size))

        if hotel_room_condition.has_minibar is not None:
            if hotel_room_condition.has_minibar == 'True':
                list_conditions.append(('has_minibar', True))
            elif hotel_room_condition.has_minibar == 'False':
                list_conditions.append(('has_minibar', False))
            else:
                raise Exception('This is not a valid boolean', hotel_room_condition.has_minibar)

        return list_to_str_and(list_conditions)
