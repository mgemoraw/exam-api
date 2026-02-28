from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from .models import Address


class AddressRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id:str):
        return self.db.query(Address).filter(Address.id==id).first()
    
    def get_all(self):
        return self.db.query(Address).all()
    
    def find_address(self, address_data):
        """Finds and Queries address"""
        existing = self.db.query(Address).filter(
            and_(
                Address.street == address_data.get('street'),
                Address.city == address_data.get('city'),
                Address.state == address_data.get('state'),
                Address.zip_code == address_data.get('zip_code'),
                Address.country == address_data.get('country'),
            )
        ).first()

        return existing
        
    def get_address(self, address_data):
        """Queries existing address its ID."""

        existing = self.db.query(Address).filter(
            func.lower(Address.street) == address_data.street.lower(),
            func.lower(Address.city) == address_data.city.lower(),
            ).first()
        
        return existing

        # address = self.db.query(Address).filter_by(
        #     street=address_data.street,
        #     city=address_data.city,
        #     state=address_data.state,
        #     zip_code=address_data.zip_code,
        #     country=address_data.country
        # ).first()
        # if address:
        #     return address.id
        # else:
        #     return None

    
    def create(self, address: Address):        
        self.db.add(address)
        self.db.commit()
        self.db.refresh(address)
        return address
    

    def update(self, address: Address):
        self.db.add(address)
        self.db.commit()
        self.db.refresh(address)
        return address
    
    def delete(self, address:Address) -> Address:
        self.db.delete(address)
        self.db.commit()
        return address 
    
