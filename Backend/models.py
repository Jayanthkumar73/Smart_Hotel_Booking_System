from sqlalchemy import Column,Integer,Date,String,Numeric,ForeignKey,Boolean,Float,DateTime

from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


# --USER table--

class User(Base):
    __tablename__="users"

    user_id=Column(Integer,primary_key=True,index=True)
    email=Column(String(100),unique=True,nullable=False)
    password=Column(String(100),nullable=False)

    bookings=relationship("Bookings",back_populates="user")

# --HOTEL table--
class Hotel(Base):
    __tablename__="hotels"
    hotel_id=Column(Integer,primary_key=True,index=True)
    name=Column(String(100),nullable=False)
    city=Column(String(100))
    rating=Column(Float)
    price_per_night=Column(Numeric(10,2))

    rooms=relationship("Room",back_populates="hotel")

class Room(Base):
    __tablename__="rooms"
    room_id=Column(Integer,primary_key=True,index=True)
    hotel_id=Column(Integer,ForeignKey("hotels.hotel_id"))
    room_type=Column(String(50))
    price=Column(Numeric(10,2))
    capacity=Column(Integer)
    available=Column(Boolean,default=True)

    hotel=relationship("Hotel",back_populates="rooms")
    bookings=relationship("Bookings",back_populates="room")

# --BOOKINGS table--
class Bookings(Base):
    __tablename__="bookings"
    booking_id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.user_id"))
    room_id=Column(Integer,ForeignKey("rooms.room_id"))
    check_in=Column(Date,nullable=False)
    check_out=Column(Date,nullable=False)
    status=Column(String(20))

    user=relationship("User",back_populates="bookings")
    room=relationship("Room",back_populates="bookings")
    payment=relationship("Payment",back_populates="booking")

# --PAYMENT table--
class Payment(Base):
    __tablename__="payments"
    payment_id=Column(Integer,primary_key=True,index=True)
    booking_id=Column(Integer,ForeignKey("bookings.booking_id"))
    amount=Column(Numeric(10,2))
    status=Column(String(20))

    booking=relationship("Bookings",back_populates="payment")
    

    
