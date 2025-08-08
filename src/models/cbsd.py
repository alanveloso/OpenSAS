from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class CBSD(Base):
    """Modelo para CBSD (Citizen Broadband Radio Service Device) - Alinhado com contrato Solidity"""
    
    __tablename__ = "cbsds"
    
    id = Column(Integer, primary_key=True, index=True)
    fcc_id = Column(String(50), unique=True, index=True, nullable=False)
    user_id = Column(String(50), nullable=False)
    cbsd_serial_number = Column(String(100), unique=True, index=True, nullable=False)
    call_sign = Column(String(20), nullable=False)
    cbsd_category = Column(String(1), nullable=False)  # A ou B
    air_interface = Column(String(20), nullable=False)
    meas_capability = Column(Text, nullable=False)  # JSON array
    eirp_capability = Column(Integer, nullable=False)
    latitude = Column(Integer, nullable=False)
    longitude = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    height_type = Column(String(10), nullable=False)  # AGL ou AMSL
    indoor_deployment = Column(Boolean, default=False)
    antenna_gain = Column(Integer, nullable=False)
    antenna_beamwidth = Column(Integer, nullable=False)
    antenna_azimuth = Column(Integer, nullable=False)
    grouping_param = Column(String(100), nullable=True)
    cbsd_address = Column(String(42), nullable=False)  # Ethereum address
    
    # Campos adicionais alinhados com contrato Solidity
    sas_origin = Column(String(42), nullable=False)  # Ethereum address do SAS que registrou
    registration_timestamp = Column(Integer, nullable=False)  # Unix timestamp
    
    # Relacionamento com grants (comentado temporariamente)
    # grants = relationship("Grant", primaryjoin="CBSD.fcc_id == Grant.fcc_id", cascade="all, delete-orphan")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<CBSD(fcc_id='{self.fcc_id}', serial='{self.cbsd_serial_number}')>" 