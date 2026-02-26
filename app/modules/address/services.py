from .models import Address
from .repository import AddressRepository

class AddressService:
    def __init__(self, repo: AddressRepository):
        self.repo = repo


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

    def create_address(self, address_data):
        """Create an address in the database and return it."""
        existing = self.repo.get_address(address_data)
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
    

    def get_addresses(self):
        return self.repo.read()
    

    
   