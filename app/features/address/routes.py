from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  
from app.infrastructure.database import get_db
from .services import AddressService
from .schemas import AddressResponse, AddressUpdateRequest, AddressCreateRequest
from .exceptions import AddressAlreadyExistsError, AddressNotFoundError
from typing import List

address_router = APIRouter()



@address_router.post("/find-one", response_model=AddressResponse)
async def find_address(address: AddressCreateRequest, db:Session=Depends(get_db)):
    service = AddressService(db)
    existing = service.find_address(address)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found!"
        )
    return existing

@address_router.post("/")
async def create_address(address: AddressCreateRequest=None, db:Session=Depends(get_db)):
    service = AddressService(db)
    try:
       return service.create_address(address)
    
    except AddressAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Address Already Exists"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{str(e)}",
        )


@address_router.get("/all", response_model=List[AddressResponse])
async def get_addresses(db:Session = Depends(get_db)):
    try:
        service = AddressService(db)
        return  service.get_addresses()
    except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Server failed to fetch address data: {str(e)}",
            )


@address_router.get("/{address_id}")
async def get_address(address_id: str, db:Session = Depends(get_db)):
    
    service = AddressService(db)
    try:
        address = service.get_by_id(address_id)
        return address
    
    except AddressNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )

        
@address_router.put("/{id}")
async def update_address(id:str, address_data: AddressUpdateRequest, db:Session=Depends(get_db)):
    service = AddressService(db)
    try:
        address = service.update_address(id, address_data)
    
    except AddressNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Error: {str(e)}"
        )


@address_router.delete("/delete-one")
async def find_and_delete_one_address(address_data: AddressCreateRequest, db:Session=Depends(get_db)):
    service = AddressService(db)
    try:
        return service.find_and_delete(address_data)
    
    except AddressNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Address: {address_data} not found!"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Error: {str(e)}"
        )

@address_router.delete("/{address_id}")
async def delete_address(address_id:str, db:Session=Depends(get_db)):
    service = AddressService(db)

    try:
        return service.delete(address_id)
    
    except AddressNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Address with ID: {address_id} not found!"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Error: {str(e)}"
        )
    