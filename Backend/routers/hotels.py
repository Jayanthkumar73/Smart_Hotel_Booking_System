# APIRouter to define hotel routes separately from main.py
from fastapi import APIRouter, Depends, HTTPException, status

# Session for database queries
from sqlalchemy.orm import Session

# Our files
from database import get_db       # DB session dependency
import models                     # Hotel model (maps to hotels table)
import schemas                    # HotelResponse schema for output formatting


# ==================== SETUP ====================

# All routes here will start with /hotels
# tags=["Hotels"] groups them in the /docs page
router = APIRouter(prefix="/hotels", tags=["Hotels"])


# ==================== SEARCH HOTELS BY CITY ====================

@router.get("/search", response_model=list[schemas.HotelResponse])
# GET request — user is fetching data, not sending data
# "/search" → full path will be /hotels/search
# response_model=list[HotelResponse] → returns a LIST of hotels formatted by HotelResponse schema
def search_hotels(city: str, db: Session = Depends(get_db)):
    # city: str → FastAPI reads this from the URL query parameter
    # e.g. /hotels/search?city=Goa → city = "Goa"
    # db → database session injected automatically by FastAPI

    # Query the hotels table and filter by city
    # .all() returns a list of all matching hotels (not just the first one)
    hotels = db.query(models.Hotel).filter(models.Hotel.city == city).all()
    # SELECT * FROM hotels WHERE city = 'Goa'

    # If no hotels found for that city, return a 404 error
    if not hotels:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No hotels found in {city}"   # e.g. "No hotels found in Goa"
        )

    # Return the list of hotels — FastAPI formats each one using HotelResponse schema
    return hotels


# ==================== GET ALL HOTELS ====================

@router.get("/all", response_model=list[schemas.HotelResponse])
# "/all" → full path will be /hotels/all
# No filter — returns every hotel in the DB
def get_all_hotels(db: Session = Depends(get_db)):

    # Fetch every row from the hotels table
    hotels = db.query(models.Hotel).all()
    # SELECT * FROM hotels

    # If the hotels table is completely empty, return 404
    if not hotels:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hotels found"
        )

    # Return all hotels as a list
    return hotels


# ==================== GET SINGLE HOTEL BY ID ====================

@router.get("/{hotel_id}", response_model=schemas.HotelResponse)
# "/{hotel_id}" → full path will be /hotels/5  (5 is the hotel_id)
# response_model=HotelResponse → returns a single hotel object (not a list)
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    # hotel_id: int → FastAPI reads this from the URL path
    # e.g. /hotels/3 → hotel_id = 3

    # Query the hotels table for a hotel with the matching hotel_id
    hotel = db.query(models.Hotel).filter(models.Hotel.hotel_id == hotel_id).first()
    # SELECT * FROM hotels WHERE hotel_id = 3

    # If no hotel found with that ID, return 404
    if not hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with id {hotel_id} not found"
        )

    # Return the single hotel object
    return hotel