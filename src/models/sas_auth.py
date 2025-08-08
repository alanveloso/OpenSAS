from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base

class SASAuthorization(Base):
    """Modelo para autorização de SAS"""
    
    __tablename__ = "sas_authorizations"
    
    id = Column(Integer, primary_key=True, index=True)
    sas_address = Column(String(42), unique=True, index=True, nullable=False)
    authorized = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<SASAuthorization(address='{self.sas_address}', authorized={self.authorized})>" 