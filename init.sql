CREATE TYPE hotel_room_types AS ENUM('SINGLE', 'DOUBLE', 'SUITE');
DROP TABLE IF EXISTS hotel_rooms;
CREATE TABLE IF NOT EXISTS hotel_rooms (
    ID INT UNIQUE PRIMARY KEY,
    hotelroom_size hotel_room_types,
    has_minibar BOOLEAN
);
CREATE INDEX IF NOT EXISTS index_room_type ON hotel_rooms(hotel_size);