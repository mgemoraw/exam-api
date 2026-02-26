from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session 
from app.infrastructure.database import get_db
from .repository import AddressRepository
from .services import AddressService
from .schemas import AddressResponse
from typing import List

address_router = APIRouter()


@address_router.get("/", response_model=List[AddressResponse])
async def get_addresses(db:Session = Depends(get_db)):

    service = AddressService(
        AddressRepository(db)
    )
    return service.get_addresses()

