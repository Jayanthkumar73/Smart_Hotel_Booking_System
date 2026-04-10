# APIRouter to define room routes separately
from fastapi import APIRouter, Depends, HTTPException, status

# Session for database queries
from sqlalchemy.orm import Session

# Our files
from database import get_db       # DB session dependency
import models                     # Room model (maps to rooms table)
import schemas                    # RoomResponse schema for output formatting


# ==================== SETUP ====================

# All routes here will start with /rooms
# tags=["Rooms"] groups them in the /docs page
router = APIRouter(prefix="/rooms", tags=["Rooms"])


# ==================== GET ALL ROOMS OF A HOTEL ====================

@router.get("/{hotel_id}/all", response_model=list[schemas.RoomResponse])
# "/{hotel_id}/all" → full path will be /rooms/1/all
# Returns ALL rooms of a hotel regardless of availability
# response_model=list[RoomResponse] → returns a list of rooms
def get_all_rooms(hotel_id: int, db: Session = Depends(get_db)):
    # hotel_id: int → FastAPI reads this from the URL path
    # e.g. /rooms/1/all → hotel_id = 1

    # First check if the hotel itself exists in the DB
    hotel = db.query(models.Hotel).filter(models.Hotel.hotel_id == hotel_id).first()
    # SELECT * FROM hotels WHERE hotel_id = 1

    # If hotel doesn't exist, stop and return 404
    if not hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with id {hotel_id} not found"
        )

    # Fetch all rooms that belong to this hotel
    rooms = db.query(models.Room).filter(models.Room.hotel_id == hotel_id).all()
    # SELECT * FROM rooms WHERE hotel_id = 1

    # If hotel exists but has no rooms in DB, return 404
    if not rooms:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No rooms found for hotel {hotel_id}"
        )

    # Return the full list of rooms
    return rooms


# ==================== GET ONLY AVAILABLE ROOMS OF A HOTEL ====================

@router.get("/{hotel_id}/available", response_model=list[schemas.RoomResponse])
# "/{hotel_id}/available" → full path will be /rooms/1/available
# Returns ONLY rooms where available = TRUE
# This is the main route used before booking
def get_available_rooms(hotel_id: int, db: Session = Depends(get_db)):

    # First check if the hotel exists
    hotel = db.query(models.Hotel).filter(models.Hotel.hotel_id == hotel_id).first()

    if not hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with id {hotel_id} not found"
        )

    # Fetch only rooms where available column is True
    # This filters out already booked rooms
    rooms = db.query(models.Room).filter(
        models.Room.hotel_id == hotel_id,    # must belong to this hotel
        models.Room.available == True         # AND must be available
    ).all()
    # SELECT * FROM rooms WHERE hotel_id = 1 AND available = TRUE

    # If no available rooms found, return 404
    if not rooms:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No available rooms for hotel {hotel_id}"
        )

    return rooms


# ==================== GET A SINGLE ROOM BY ROOM ID ====================

@router.get("/room/{room_id}", response_model=schemas.RoomResponse)
# "/room/{room_id}" → full path will be /rooms/room/5
# Returns details of one specific room
def get_room(room_id: int, db: Session = Depends(get_db)):
    # room_id: int → FastAPI reads this from the URL
    # e.g. /rooms/room/5 → room_id = 5

    # Query rooms table for the specific room
    room = db.query(models.Room).filter(models.Room.room_id == room_id).first()
    # SELECT * FROM rooms WHERE room_id = 5

    # If room not found return 404
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {room_id} not found"
        )

    return room


# ==================== FILTER ROOMS BY TYPE ====================

@router.get("/{hotel_id}/type", response_model=list[schemas.RoomResponse])
# "/{hotel_id}/type" → full path will be /rooms/1/type?room_type=Suite
# Lets user filter rooms by type e.g. Single, Double, Suite
def get_rooms_by_type(hotel_id: int, room_type: str, db: Session = Depends(get_db)):
    # hotel_id → from URL path
    # room_type → from query parameter e.g. ?room_type=Suite

    # Check hotel exists first
    hotel = db.query(models.Hotel).filter(models.Hotel.hotel_id == hotel_id).first()

    if not hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with id {hotel_id} not found"
        )

    # Filter by both hotel_id AND room_type AND available
    rooms = db.query(models.Room).filter(
        models.Room.hotel_id == hotel_id,        # must belong to this hotel
        models.Room.room_type == room_type,       # must match the requested type
        models.Room.available == True             # must be available
    ).all()
    # SELECT * FROM rooms WHERE hotel_id = 1 AND room_type = 'Suite' AND available = TRUE

    if not rooms:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No available {room_type} rooms for hotel {hotel_id}"
        )

    return rooms