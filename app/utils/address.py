"""Utilities for handling addresses."""

from app.models.address import Address
from app.models.school import University

class Address:
    def __init__(self, street, city, state, zip_code, country):
        self. street = street 
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country

    def format(self):
        """Format an address into a single string."""
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}"
    
    @classmethod
    def validate_zip_code(zip_code):
        """Validate the given zip code."""
        if len(zip_code) != 5 or not zip_code.isdigit():
            raise ValueError("Invalid zip code format")
        return True

    def __repr__(self):
        """Get a summary of the address."""
        return f"{self.street}, {self.city}, {self.state}, {self.zip_code}, {self.country}"

    def create(self, address_data):
        """Create an address in the database and return it."""

        new_address = Address(
            street=address_data.street,
            city=address_data.city,
            state=address_data.state,
            zip_code=address_data.zip_code,
            country=address_data.country
        )
      
        return new_address

def format_address(street, city, state, zip_code):
    """Format an address into a single string."""
    return f"{street}, {city}, {state} {zip_code}"

def validate_zip_code(zip_code):
    """Validate the given zip code."""
    if len(zip_code) != 5 or not zip_code.isdigit():
        raise ValueError("Invalid zip code format")
    return True

def get_address_summary(address):
    """Get a summary of the address."""
    return f"{address.street}, {address.city}, {address.state}, {address.zip_code}, {address.country}"

def create_address(address_data, db):
    """Create an address in the database and return its ID."""
    address = db.query(Address).filter_by(
        street=address_data.street,
        city=address_data.city,
        state=address_data.state,
        zip_code=address_data.zip_code,
        country=address_data.country
    ).first()
    if address:
        return address.id
   
   
    # Otherwise create a new address
    new_address = Address(
        street=address_data.street,
        city=address_data.city,
        state=address_data.state,
        zip_code=address_data.zip_code,
        country=address_data.country
    )
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address.id