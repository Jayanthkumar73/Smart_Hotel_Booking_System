from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from database import get_db
import models
import schemas
from auth import get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])


# ==================== BOOK A ROOM ====================

@router.post("/book-room", response_model=schemas.BookingResponse)
def book_room(
    booking: schemas.BookingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    room = db.query(models.Room).filter(models.Room.room_id == booking.room_id).first()

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    if not room.available:
        raise HTTPException(status_code=400, detail="Room is not available")

    if booking.check_in < date.today():
        raise HTTPException(status_code=400, detail="Check-in date cannot be in the past")

    if booking.check_out <= booking.check_in:
        raise HTTPException(status_code=400, detail="Check-out date must be after check-in date")

    new_booking = models.Bookings(
        user_id=current_user.user_id,
        room_id=booking.room_id,
        check_in=booking.check_in,
        check_out=booking.check_out,
        status="CONFIRMED"
    )

    room.available = False

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    # Payment
    nights = (booking.check_out - booking.check_in).days
    total_amount = nights * float(room.price)

    new_payment = models.Payment(
        booking_id=new_booking.booking_id,
        amount=total_amount,
        status="SUCCESS"
    )

    db.add(new_payment)
    db.commit()

    return new_booking


# ==================== BOOKING HISTORY ====================

@router.get("/my-bookings")   # ✅ MOVED ABOVE
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    bookings = db.query(models.Bookings).filter(
        models.Bookings.user_id == current_user.user_id
    ).all()

    result = []

    for booking in bookings:
        room = db.query(models.Room).filter(
            models.Room.room_id == booking.room_id
        ).first()

        hotel_name = None

        if room:
            hotel = db.query(models.Hotel).filter(
                models.Hotel.hotel_id == room.hotel_id
            ).first()

            if hotel:
                hotel_name = hotel.name

        result.append({
            "booking_id": booking.booking_id,
            "room_id": booking.room_id,
            "hotel_name": hotel_name,
            "check_in": booking.check_in,
            "check_out": booking.check_out,
            "status": booking.status
        })

    return result


# ==================== GET BOOKING BY ID ====================

@router.get("/{booking_id}", response_model=schemas.BookingResponse)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    booking = db.query(models.Bookings).filter(
        models.Bookings.booking_id == booking_id
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return booking


# ==================== CANCEL BOOKING ====================

@router.put("/cancel/{booking_id}")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    booking = db.query(models.Bookings).filter(
        models.Bookings.booking_id == booking_id
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    booking.status = "CANCELLED"

    room = db.query(models.Room).filter(
        models.Room.room_id == booking.room_id
    ).first()

    if room:
        room.available = True

    db.commit()

    return {"message": "Booking cancelled successfully"}


# ==================== PAYMENT STATUS ====================

@router.get("/payment/{booking_id}", response_model=schemas.PaymentResponse)
def get_payment_status(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    booking = db.query(models.Bookings).filter(
        models.Bookings.booking_id == booking_id
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    payment = db.query(models.Payment).filter(
        models.Payment.booking_id == booking_id
    ).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    return payment