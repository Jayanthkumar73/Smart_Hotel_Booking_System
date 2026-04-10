from pydantic import BaseModel,EmailStr
from typing import Optional ,List
from datetime import date


class UserCreate(BaseModel):
    email:EmailStr
    password:str
class UserResponse(BaseModel):
    user_id:int
    email:EmailStr
    class Config:
        from_attributes=True
class LoginSchema(BaseModel):
    email:EmailStr
    password:str


class HotelResponse(BaseModel):
    hotel_id:int
    name:str
    city:str
    rating:float
    price_per_night:float
    class Config:
        from_attributes=True


class RoomResponse(BaseModel):
    room_id:int
    hotel_id:int
    room_type:str
    price:float
    capacity:int
    available:bool
    class Config:
        from_attributes=True


class BookingCreate(BaseModel):
    room_id:int
    check_in:date   
    check_out:date
class BookingResponse(BaseModel):
    booking_id:int
    user_id:int
    room_id:int
    check_in:date
    check_out:date
    status:str
    class Config:
        from_attributes=True
class PaymentResponse(BaseModel):
    payment_id:int
    booking_id:int
    amount:float
    status:str
    class Config:
        from_attributes=True
class Token(BaseModel):
    access_token:str
    token_type:str
