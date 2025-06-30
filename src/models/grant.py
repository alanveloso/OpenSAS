from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class Grant(Base):
    """Modelo para Grants de espectro - Alinhado com contrato Solidity"""
    
    __tablename__ = "grants"
    
    id = Column(Integer, primary_key=True, index=True)
    grant_id = Column(String(100), unique=True, index=True, nullable=False)
    fcc_id = Column(String(50), ForeignKey("cbsds.fcc_id"), nullable=False)
    cbsd_serial_number = Column(String(100), nullable=False)
    channel_type = Column(String(10), nullable=False)  # GAA, PAL
    max_eirp = Column(Integer, nullable=False)
    low_frequency = Column(Integer, nullable=False)
    high_frequency = Column(Integer, nullable=False)
    requested_max_eirp = Column(Integer, nullable=False)
    requested_low_frequency = Column(Integer, nullable=False)
    requested_high_frequency = Column(Integer, nullable=False)
    grant_expire_time = Column(Integer, nullable=False)
    transmit_expire_time = Column(Integer, nullable=True)
    state = Column(String(20), default="GRANTED")  # GRANTED, AUTHORIZED, TERMINATED
    
    # Campos adicionais alinhados com contrato Solidity
    sas_origin = Column(String(42), nullable=False)  # Ethereum address do SAS que criou o grant
    grant_timestamp = Column(Integer, nullable=False)  # Unix timestamp
    terminated = Column(Boolean, default=False)  # Se o grant foi terminado
    
    # Relacionamento
    cbsd = relationship("CBSD", back_populates="grants")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Grant(grant_id='{self.grant_id}', fcc_id='{self.fcc_id}')>" 