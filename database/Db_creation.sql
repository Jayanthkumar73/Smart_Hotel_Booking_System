CREATE DATABASE hotel_booking_system;
USE hotel_booking_system;




-- USERS TABLE
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- HOTELS TABLE
CREATE TABLE hotels (
    hotel_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    city VARCHAR(50),
    rating FLOAT,
    price_per_night DECIMAL(10,2)
);

-- ROOMS TABLE
CREATE TABLE rooms (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    hotel_id INT,
    room_type VARCHAR(50),
    price DECIMAL(10,2),
    capacity INT,
    available BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id) ON DELETE CASCADE
);

-- BOOKINGS TABLE
CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    room_id INT,
    check_in DATE,
    check_out DATE,
    status VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
);

-- PAYMENTS TABLE
CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT,
    amount DECIMAL(10,2),
    status VARCHAR(20),
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
);




INSERT INTO users (email, password) VALUES
('user1@gmail.com','pass1'), ('user2@gmail.com','pass2'),
('user3@gmail.com','pass3'), ('user4@gmail.com','pass4'),
('user5@gmail.com','pass5'), ('user6@gmail.com','pass6'),
('user7@gmail.com','pass7'), ('user8@gmail.com','pass8'),
('user9@gmail.com','pass9'), ('user10@gmail.com','pass10'),
('user11@gmail.com','pass11'), ('user12@gmail.com','pass12'),
('user13@gmail.com','pass13'), ('user14@gmail.com','pass14'),
('user15@gmail.com','pass15'), ('user16@gmail.com','pass16'),
('user17@gmail.com','pass17'), ('user18@gmail.com','pass18'),
('user19@gmail.com','pass19'), ('user20@gmail.com','pass20'),
('user21@gmail.com','pass21'), ('user22@gmail.com','pass22'),
('user23@gmail.com','pass23'), ('user24@gmail.com','pass24'),
('user25@gmail.com','pass25');




INSERT INTO hotels (name, city, rating, price_per_night) VALUES
('Grand Palace','Delhi',4.5,3000),
('Sea View Resort','Goa',4.2,5000),
('Mountain Retreat','Manali',4.7,4000),
('City Inn','Mumbai',4.0,3500),
('Royal Stay','Jaipur',4.3,3200),
('Lake View Hotel','Udaipur',4.6,4500),
('Urban Lodge','Bangalore',4.1,2800),
('Comfort Suites','Chennai',4.2,3100),
('Green Valley','Kerala',4.8,5500),
('Sunrise Hotel','Pune',4.0,2600),
('Blue Lagoon','Goa',4.4,4800),
('Hilltop Stay','Shimla',4.6,4200),
('Metro Hotel','Delhi',3.9,2400),
('Elite Residency','Hyderabad',4.3,3300),
('Royal Orchid','Mysore',4.5,3700),
('Golden Sands','Goa',4.7,6000),
('Snow Peak','Manali',4.8,5200),
('City Comfort','Kolkata',4.1,2700),
('Palm Resort','Kerala',4.6,4900),
('Heritage Inn','Jaipur',4.2,3100);




INSERT INTO rooms (hotel_id, room_type, price, capacity, available) VALUES
(1,'Single',1500,1,TRUE),(1,'Double',2500,2,TRUE),
(2,'Deluxe',4000,3,TRUE),(2,'Suite',6000,4,TRUE),
(3,'Single',2000,1,TRUE),(3,'Double',3000,2,FALSE),
(4,'Deluxe',3500,3,TRUE),(4,'Suite',5500,4,TRUE),
(5,'Single',1800,1,TRUE),(5,'Double',2800,2,TRUE),
(6,'Deluxe',4200,3,TRUE),(6,'Suite',6500,4,TRUE),
(7,'Single',1600,1,TRUE),(7,'Double',2600,2,TRUE),
(8,'Deluxe',3000,3,TRUE),(8,'Suite',5000,4,TRUE),
(9,'Single',2200,1,TRUE),(9,'Double',3200,2,TRUE),
(10,'Deluxe',2800,3,TRUE),(10,'Suite',4800,4,FALSE),
(11,'Single',2000,1,TRUE),(12,'Double',3000,2,TRUE),
(13,'Deluxe',2600,3,TRUE),(14,'Suite',5200,4,TRUE),
(15,'Single',2100,1,TRUE),(16,'Double',3100,2,TRUE),
(17,'Deluxe',4300,3,TRUE),(18,'Suite',5300,4,TRUE),
(19,'Single',1900,1,TRUE),(20,'Double',2900,2,TRUE);




INSERT INTO bookings (user_id, room_id, check_in, check_out, status) VALUES
(1,1,'2026-04-01','2026-04-03','CONFIRMED'),
(2,2,'2026-04-02','2026-04-04','CONFIRMED'),
(3,3,'2026-04-03','2026-04-06','CANCELLED'),
(4,4,'2026-04-01','2026-04-02','CONFIRMED'),
(5,5,'2026-04-05','2026-04-07','CONFIRMED'),
(6,6,'2026-04-06','2026-04-08','CONFIRMED'),
(7,7,'2026-04-07','2026-04-09','CONFIRMED'),
(8,8,'2026-04-08','2026-04-10','CONFIRMED'),
(9,9,'2026-04-09','2026-04-11','CONFIRMED'),
(10,10,'2026-04-10','2026-04-12','CONFIRMED'),
(11,11,'2026-04-11','2026-04-13','CONFIRMED'),
(12,12,'2026-04-12','2026-04-14','CONFIRMED'),
(13,13,'2026-04-13','2026-04-15','CANCELLED'),
(14,14,'2026-04-14','2026-04-16','CONFIRMED'),
(15,15,'2026-04-15','2026-04-17','CONFIRMED'),
(16,16,'2026-04-16','2026-04-18','CONFIRMED'),
(17,17,'2026-04-17','2026-04-19','CONFIRMED'),
(18,18,'2026-04-18','2026-04-20','CONFIRMED'),
(19,19,'2026-04-19','2026-04-21','CONFIRMED'),
(20,20,'2026-04-20','2026-04-22','CONFIRMED'),
(21,21,'2026-04-21','2026-04-23','CONFIRMED'),
(22,22,'2026-04-22','2026-04-24','CONFIRMED'),
(23,23,'2026-04-23','2026-04-25','CONFIRMED'),
(24,24,'2026-04-24','2026-04-26','CONFIRMED'),
(25,25,'2026-04-25','2026-04-27','CONFIRMED');



INSERT INTO payments (booking_id, amount, status) VALUES
(1,1500,'SUCCESS'),(2,2500,'SUCCESS'),
(3,4000,'FAILED'),(4,6000,'SUCCESS'),
(5,2000,'SUCCESS'),(6,3000,'SUCCESS'),
(7,3500,'SUCCESS'),(8,5500,'FAILED'),
(9,1800,'SUCCESS'),(10,2800,'SUCCESS'),
(11,4200,'SUCCESS'),(12,6500,'SUCCESS'),
(13,1600,'FAILED'),(14,2600,'SUCCESS'),
(15,3000,'SUCCESS'),(16,5000,'SUCCESS'),
(17,2200,'SUCCESS'),(18,3200,'SUCCESS'),
(19,2800,'SUCCESS'),(20,4800,'SUCCESS'),
(21,2000,'SUCCESS'),(22,3000,'SUCCESS'),
(23,2600,'SUCCESS'),(24,5200,'SUCCESS'),
(25,2100,'SUCCESS');





SELECT * FROM users;
SELECT * FROM hotels;
SELECT * FROM rooms;
SELECT * FROM bookings;
SELECT * FROM payments;






CREATE VIEW booking_report AS
SELECT 
    b.booking_id,
    u.email AS user_email,
    h.name AS hotel_name,
    r.room_type,
    b.check_in,
    b.check_out,
    b.status
FROM bookings b
JOIN users u ON b.user_id = u.user_id
JOIN rooms r ON b.room_id = r.room_id
JOIN hotels h ON r.hotel_id = h.hotel_id;



SELECT * FROM booking_report;


CREATE VIEW available_rooms AS
SELECT * FROM rooms
WHERE available = TRUE;


SELECT * FROM available_rooms;




DELIMITER //


-- =========================
-- STEP 18: STORED PROCEDURE
-- =========================

DELIMITER //

CREATE PROCEDURE book_room(
    IN p_user_id INT,
    IN p_room_id INT,
    IN p_check_in DATE,
    IN p_check_out DATE
)
BEGIN
    DECLARE room_available BOOLEAN;

    START TRANSACTION;

    -- Check room availability
    SELECT available INTO room_available
    FROM rooms
    WHERE room_id = p_room_id
    FOR UPDATE;

    IF room_available = TRUE THEN

        -- Insert booking
        INSERT INTO bookings(user_id, room_id, check_in, check_out, status)
        VALUES (p_user_id, p_room_id, p_check_in, p_check_out, 'CONFIRMED');

        -- Update room availability
        UPDATE rooms
        SET available = FALSE
        WHERE room_id = p_room_id;

        COMMIT;

    ELSE
        ROLLBACK;
    END IF;

END //

DELIMITER ;



CALL book_room(1, 1, '2026-05-01', '2026-05-03');


SELECT * FROM bookings ORDER BY booking_id DESC;

SELECT * FROM rooms WHERE room_id = 1;


CALL book_room(2, 1, '2026-05-05', '2026-05-07');



-- =========================
-- STEP 19: TRIGGER
-- =========================

DELIMITER //

CREATE TRIGGER after_booking_insert
AFTER INSERT ON bookings
FOR EACH ROW
BEGIN
    UPDATE rooms
    SET available = FALSE
    WHERE room_id = NEW.room_id;
END //

DELIMITER ;



INSERT INTO bookings(user_id, room_id, check_in, check_out, status)
VALUES (2, 2, '2026-06-01', '2026-06-03', 'CONFIRMED');

SELECT * FROM rooms WHERE room_id = 2;