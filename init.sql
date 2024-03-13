CREATE TYPE hotel_room_types AS ENUM('(Einzelzimmer', 'Doppelzimmer,', 'Suite');
CREATE TABLE IF NOT EXISTS hotel_rooms (
    ID INT UNIQUE PRIMARY KEY,
    hotel_size hotel_room_types,
    has_minibar BOOLEAN
);
CREATE INDEX IF NOT EXISTS index_room_type ON hotel_rooms(hotel_size);