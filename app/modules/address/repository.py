from sqlalchemy.orm import Session
from .models import Address


class AddressRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id:str):
        return self.db.query(Address).filter(Address.id==id).first()
    
    def read(self):
        return self.db.query(Address).all()
    
    def get_address(self, address_data):
        """Queries existing address its ID."""
        address = self.db.query(Address).filter_by(
            street=address_data.street,
            city=address_data.city,
            state=address_data.state,
            zip_code=address_data.zip_code,
            country=address_data.country
        ).first()
        if address:
            return address.id
        else:
            return None
    
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
    
    def delete(self, address_id: str) -> Address:
        address = self.db.query(Address).filter(Address.id==address_id).first()
        self.db.delete(address)
        self.db.commit()
        return address 
    
