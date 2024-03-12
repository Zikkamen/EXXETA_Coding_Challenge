CREATE TYPE hotel_room_types AS ENUM('(Einzelzimmer', 'Doppelzimmer,', 'Suite');
CREATE TABLE IF NOT EXISTS hotel_rooms (
    ID INT PRIMARY KEY,
    hotel_size hotel_room_types,
    has_minibar BOOLEAN
);