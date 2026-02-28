from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .exceptions import AddressNotFoundError 
from .models import Address
from .repository import AddressRepository
from .schemas import AddressCreateRequest

class AddressService:
    def __init__(self, db:Session):
        self.db = db
        self.repo = AddressRepository(db)

    def get_by_id(self, address_id:str):
        return self.repo.get_by_id(address_id)


    def format_address(self, address):
        """Format an address into a single string."""
        return f"{address.street}, {address.city}, {address.state} {address.zip_code} {address.country}"
    

    @classmethod
    def validate_zip_code(zip_code):
        """Validate the given zip code."""
        if len(zip_code) != 5 or not zip_code.isdigit():
            raise ValueError("Invalid zip code format")
        return True

    def address_summary(self, address):
        """Get a summary of the address."""
        return f"{address.street}, {address.city}, {address.state}, {address.zip_code}, {address.country}"

    def create_address(self, address_data:AddressCreateRequest):
        """Create an address in the database and return it."""
        existing = self.repo.find_address(address_data.model_dump())
        if existing:
            return existing
            # raise ValueError("Address already rgistered")
        
        new_address = Address(
            street=address_data.street,
            city=address_data.city,
            state=address_data.state,
            zip_code=address_data.zip_code,
            country=address_data.country
        )
      
        return self.repo.create(new_address)
    

    def find_address(self, address_data: AddressCreateRequest) -> Address:
        try:
            return self.repo.find_address(address_data.model_dump())
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Address {address_data} Not found"
            )
    

    def get_addresses(self):
        return self.repo.get_all()
    

    def update(self, id, address_data: AddressCreateRequest):

        """Create an address in the database and return it."""
        # existing = self.repo.get_address(address_data)
        try:
            existing = self.repo.get_by_id(self.id)
            if existing:
                return existing
                # raise ValueError("Address already rgistered")
            
            updated_address = Address(
                street=address_data.street,
                city=address_data.city,
                state=address_data.state,
                zip_code=address_data.zip_code,
                country=address_data.country
            )
        
            # return self.repo.create(updated_address)
            return self.repo.update(existing.id, updated_address)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Server Error, {str(e)}"
            )
        

    def find_and_delete(self, address_data):
        existing = self.find_address(address_data)

        if not existing:
            raise AddressNotFoundError()
        
        return self.repo.delete(existing)



    def delete(self, id: str):
        existing = self.get_by_id(id)
        if not existing:
            raise AddressNotFoundError()
        
        return self.repo.delete(existing)
    
        # if result:
        #     return JSONResponse(
        #         status_code=status.HTTP_200_OK,
        #         content={"detail": f"Address with id '{id}' deleted successfully!"}
        #     )
        # else:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail=f"Address with id '{id}' not found!"
        #     ) 
   