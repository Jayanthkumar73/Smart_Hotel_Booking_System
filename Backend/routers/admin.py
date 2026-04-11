from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas

router = APIRouter(prefix="/admin", tags=["Admin"])


# HOTEL CRUD 

@router.post("/hotels")
def create_hotel(hotel: schemas.HotelCreate, db: Session = Depends(get_db)):
    new_hotel = models.Hotel(
        name=hotel.name,
        city=hotel.city,
        rating=hotel.rating,
        price_per_night=hotel.price_per_night  
    )
    db.add(new_hotel)
    db.commit()
    db.refresh(new_hotel)
    return new_hotel


@router.get("/hotels")
def get_hotels(db: Session = Depends(get_db)):
    return db.query(models.Hotel).all()


@router.put("/hotels/{hotel_id}")
def update_hotel(hotel_id: int, hotel: schemas.HotelCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Hotel).filter(models.Hotel.hotel_id == hotel_id).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Hotel not found")

    existing.name = hotel.name
    existing.city = hotel.city
    existing.rating = hotel.rating
    existing.price_per_night = hotel.price_per_night

    db.commit()
    return {"message": "Hotel updated"}


@router.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = db.query(models.Hotel).filter(models.Hotel.hotel_id == hotel_id).first()

    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    db.delete(hotel)
    db.commit()

    return {"message": "Hotel deleted"}


# ROOM CRUD 

@router.post("/rooms")
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    new_room = models.Room(
        hotel_id=room.hotel_id,
        room_type=room.room_type,
        price=room.price,
        capacity=room.capacity,
        available=True
    )

    db.add(new_room)
    db.commit()
    db.refresh(new_room)

    return new_room


@router.get("/rooms")
def get_rooms(db: Session = Depends(get_db)):
    return db.query(models.Room).all()


@router.put("/rooms/{room_id}")
def update_room(room_id: int, room: schemas.RoomCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Room).filter(models.Room.room_id == room_id).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Room not found")

    existing.hotel_id = room.hotel_id
    existing.room_type = room.room_type
    existing.price = room.price
    existing.capacity = room.capacity

    db.commit()

    return {"message": "Room updated"}


@router.delete("/rooms/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.room_id == room_id).first()

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    db.delete(room)
    db.commit()

    return {"message": "Room deleted"}