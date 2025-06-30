from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .database import Base

class Event(Base):
    """Modelo para eventos do sistema"""
    
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(50), nullable=False)  # registration, grant, heartbeat, etc.
    payload = Column(Text, nullable=False)  # JSON payload
    transaction_hash = Column(String(66), nullable=True)  # Para compatibilidade com blockchain
    block_number = Column(Integer, nullable=True)  # Para compatibilidade com blockchain
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Event(type='{self.event_type}', created_at='{self.created_at}')>" 