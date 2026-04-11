from fastapi import FastAPI
from database import Base, engine
import models
from routers import user,hotels,rooms,bookings, admin

app = FastAPI()

Base.metadata.create_all(bind=engine)   # Creates tables if they don't exist

app.include_router(user.router)         # Registers the /auth/register and /auth/login routes
app.include_router(hotels.router) 
app.include_router(rooms.router)         # Registers the /rooms/{hotel_id}/all and /rooms/{hotel_id}/available routes
app.include_router(bookings.router)      # Registers the /bookings routes
app.include_router(admin.router)