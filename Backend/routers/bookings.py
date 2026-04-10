# APIRouter to define booking routes separately
from fastapi import APIRouter, Depends, HTTPException, status

# Session for database queries
from sqlalchemy.orm import Session

# date to validate check_in is not in the past
from datetime import date

# Our files
from database import get_db                # DB session dependency
import models                              # Booking, Room, Payment models
import schemas                             # BookingCreate, BookingResponse, PaymentResponse schemas
from auth import get_current_user          # Protects routes — only logged in users can book


# ==================== SETUP ====================

# All routes here will start with /bookings
# tags=["Bookings"] groups them in the /docs page
router = APIRouter(prefix="/bookings", tags=["Bookings"])


# ==================== BOOK A ROOM ====================

@router.post("/book-room", response_model=schemas.BookingResponse)
# POST request — user is sending booking data
# "/book-room" → full path will be /bookings/book-room
# response_model=BookingResponse → returns the created booking details
# current_user=Depends(get_current_user) → route is PROTECTED, user must be logged in
def book_room(
    booking: schemas.BookingCreate,               # Request body — room_id, check_in, check_out
    db: Session = Depends(get_db),                # DB session
    current_user: models.User = Depends(get_current_user)  # Logged in user fetched from JWT token
):

    # ── STEP 1: Check the room exists ──
    room = db.query(models.Room).filter(models.Room.room_id == booking.room_id).first()
    # SELECT * FROM rooms WHERE room_id = ?

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )

    # ── STEP 2: Check the room is actually available ──
    if not room.available:
        # If available = FALSE, someone already booked it
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room is not available"
        )

    # ── STEP 3: Validate check_in is not in the past ──
    if booking.check_in < date.today():
        # e.g. if today is 2026-04-10 and check_in is 2026-04-05 → reject
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check-in date cannot be in the past"
        )

    # ── STEP 4: Validate check_out is after check_in ──
    if booking.check_out <= booking.check_in:
        # check_out must be at least 1 day after check_in
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check-out date must be after check-in date"
        )

    # ── STEP 5: Create the new booking object ──
    new_booking = models.Bookings(
        user_id=current_user.user_id,     # Take user_id from the JWT token (not from request body)
        room_id=booking.room_id,          # Room the user wants to book
        check_in=booking.check_in,        # Check-in date from request
        check_out=booking.check_out,      # Check-out date from request
        status="CONFIRMED"                # Automatically set status to CONFIRMED on creation
    )

    # ── STEP 6: Mark the room as unavailable to prevent double booking ──
    room.available = False
    # UPDATE rooms SET available = FALSE WHERE room_id = ?
    # This is the key step that prevents two users booking the same room

    # ── STEP 7: Save the booking to DB ──
    db.add(new_booking)       # Stage the new booking
    db.commit()               # Save both the booking AND the room availability update together
    db.refresh(new_booking)   # Get the saved booking back with auto-generated booking_id

    # ── STEP 8: Auto-create a payment record for this booking ──
    # Calculate total amount based on number of nights × room price
    nights = (booking.check_out - booking.check_in).days   # e.g. Apr 10 to Apr 13 = 3 nights
    total_amount = nights * float(room.price)               # e.g. 3 × 3000 = 9000.00

    new_payment = models.Payment(
        booking_id=new_booking.booking_id,   # Link payment to the booking we just created
        amount=total_amount,                  # Calculated total
        status="SUCCESS"                      # Auto set to SUCCESS (payment gateway can update later)
    )

    db.add(new_payment)      # Stage the payment
    db.commit()              # Save the payment to DB

    # Return the booking details — formatted using BookingResponse schema
    return new_booking







# ==================== GET BOOKING BY ID ====================

@router.get("/{booking_id}", response_model=schemas.BookingResponse)
# "/{booking_id}" → full path will be /bookings/3
# Returns details of one specific booking
# Protected — must be logged in
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Find the booking by ID
    booking = db.query(models.Booking).filter(
        models.Booking.booking_id == booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    # Make sure the booking belongs to the logged in user
    if booking.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to view this booking"
        )

    return booking