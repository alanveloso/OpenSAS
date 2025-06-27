from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import logging
import json
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from src.models.database import get_db
from src.models.cbsd import CBSD
from src.models.grant import Grant
from src.models.sas_auth import SASAuthorization
from src.models.event import Event
from src.config.settings import settings

# Configurar logging
logging.basicConfig(level=getattr(logging, settings.log_level))
logger = logging.getLogger(__name__)

# Inicializar FastAPI
app = FastAPI(
    title="SAS (Spectrum Access System) - WINNF SAS-SAS",
    description="API REST compatível com WINNF TS-0096/3003 (SAS-SAS)",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic para SAS-SAS (exemplo simplificado)
class CbsdRecord(BaseModel):
    id: str
    fccId: str
    userId: str
    cbsdSerialNumber: str
    callSign: str
    cbsdCategory: str
    airInterface: str
    measCapability: List[str]
    eirpCapability: int
    latitude: int
    longitude: int
    height: int
    heightType: str
    indoorDeployment: bool
    antennaGain: int
    antennaBeamwidth: int
    antennaAzimuth: int
    groupingParam: str
    cbsdAddress: str  # hexadecimal

class ZoneRecord(BaseModel):
    id: str
    name: str
    type: str
    geometry: dict

# --- Interface Pública SAS-SAS (WINNF TS-0096/3003) ---

@app.get("/health")
async def health_check():
    """Health check da API (não faz parte do padrão WINNF, mas útil para operação)"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0"
    }

@app.get("/v1.3/cbsd/{cbsd_id}")
async def get_cbsd_record(cbsd_id: str, db: Session = Depends(get_db)):
    """Obter registro CBSD por ID (SAS-SAS GET)"""
    cbsd = db.query(CBSD).filter(CBSD.cbsd_serial_number == cbsd_id).first()
    if not cbsd:
        raise HTTPException(status_code=404, detail="CBSD não encontrado")
    return {
        "cbsd": {
            "id": cbsd.cbsd_serial_number,
            "fccId": cbsd.fcc_id,
            "userId": cbsd.user_id,
            "callSign": cbsd.call_sign,
            "cbsdCategory": cbsd.cbsd_category,
            "airInterface": cbsd.air_interface,
            "measCapability": json.loads(cbsd.meas_capability),
            "eirpCapability": cbsd.eirp_capability,
            "latitude": cbsd.latitude,
            "longitude": cbsd.longitude,
            "height": cbsd.height,
            "heightType": cbsd.height_type,
            "indoorDeployment": cbsd.indoor_deployment,
            "antennaGain": cbsd.antenna_gain,
            "antennaBeamwidth": cbsd.antenna_beamwidth,
            "antennaAzimuth": cbsd.antenna_azimuth,
            "groupingParam": cbsd.grouping_param,
            "cbsdAddress": cbsd.cbsd_address
        }
    }

@app.post("/v1.3/cbsd/{cbsd_id}")
async def push_cbsd_record(cbsd_id: str, record: CbsdRecord, db: Session = Depends(get_db)):
    """Atualizar ou criar registro CBSD (SAS-SAS POST/push)"""
    cbsd = db.query(CBSD).filter(CBSD.cbsd_serial_number == cbsd_id).first()
    if not cbsd:
        # Criar novo
        cbsd = CBSD(
            fcc_id=record.fccId,
            user_id=record.userId,
            cbsd_serial_number=record.cbsdSerialNumber,
            call_sign=record.callSign,
            cbsd_category=record.cbsdCategory,
            air_interface=record.airInterface,
            meas_capability=json.dumps(record.measCapability),
            eirp_capability=record.eirpCapability,
            latitude=record.latitude,
            longitude=record.longitude,
            height=record.height,
            height_type=record.heightType,
            indoor_deployment=record.indoorDeployment,
            antenna_gain=record.antennaGain,
            antenna_beamwidth=record.antennaBeamwidth,
            antenna_azimuth=record.antennaAzimuth,
            grouping_param=record.groupingParam,
            cbsd_address=record.cbsdAddress
        )
        db.add(cbsd)
    else:
        # Atualizar existente
        cbsd.fcc_id = record.fccId
        cbsd.user_id = record.userId
        cbsd.call_sign = record.callSign
        cbsd.cbsd_category = record.cbsdCategory
        cbsd.air_interface = record.airInterface
        cbsd.meas_capability = json.dumps(record.measCapability)
        cbsd.eirp_capability = record.eirpCapability
        cbsd.latitude = record.latitude
        cbsd.longitude = record.longitude
        cbsd.height = record.height
        cbsd.height_type = record.heightType
        cbsd.indoor_deployment = record.indoorDeployment
        cbsd.antenna_gain = record.antennaGain
        cbsd.antenna_beamwidth = record.antennaBeamwidth
        cbsd.antenna_azimuth = record.antennaAzimuth
        cbsd.grouping_param = record.groupingParam
        cbsd.cbsd_address = record.cbsdAddress
    db.commit()
    return {"success": True, "message": "CBSD atualizado/criado via SAS-SAS"}

@app.get("/v1.3/zone/{zone_id}")
async def get_zone_record(zone_id: str):
    """Obter registro de zona (exemplo simplificado)"""
    # Aqui seria consulta ao banco de zonas
    return {"zone": {"id": zone_id, "name": "Zone Example", "type": "protected", "geometry": {}}}

@app.post("/v1.3/zone/{zone_id}")
async def push_zone_record(zone_id: str, record: ZoneRecord):
    """Atualizar ou criar registro de zona (exemplo simplificado)"""
    # Aqui seria persistência no banco de zonas
    return {"success": True, "message": "Zone atualizado/criado via SAS-SAS"}

@app.get("/v1.3/dump")
async def get_full_activity_dump():
    """Obter full activity dump (exemplo simplificado)"""
    # Aqui seria consulta a todos os registros relevantes
    return {"dump": "full activity dump (exemplo)"}

# --- Interface Administrativa Interna (NÃO faz parte do padrão WINNF SAS-SAS) ---

@app.post("/sas/authorize")
async def authorize_sas(sas_auth: dict, db: Session = Depends(get_db)):
    """Autorizar SAS (interno/admin)"""
    sas_address = sas_auth.get("sas_address")
    if not sas_address:
        raise HTTPException(status_code=400, detail="sas_address obrigatório")
    existing_auth = db.query(SASAuthorization).filter(
        SASAuthorization.sas_address == sas_address
    ).first()
    if existing_auth:
        existing_auth.is_authorized = True
    else:
        auth = SASAuthorization(
            sas_address=sas_address,
            is_authorized=True
        )
        db.add(auth)
    db.commit()
    return {"success": True, "message": f"SAS {sas_address} autorizado"}

@app.post("/sas/revoke")
async def revoke_sas(sas_auth: dict, db: Session = Depends(get_db)):
    """Revogar SAS (interno/admin)"""
    sas_address = sas_auth.get("sas_address")
    if not sas_address:
        raise HTTPException(status_code=400, detail="sas_address obrigatório")
    auth = db.query(SASAuthorization).filter(
        SASAuthorization.sas_address == sas_address
    ).first()
    if auth:
        auth.is_authorized = False
        db.commit()
    return {"success": True, "message": f"SAS {sas_address} revogado"}

@app.get("/sas/{sas_address}/authorized")
async def check_sas_authorization(sas_address: str, db: Session = Depends(get_db)):
    """Verificar se SAS está autorizado (interno/admin)"""
    auth = db.query(SASAuthorization).filter(
        SASAuthorization.sas_address == sas_address
    ).first()
    return {"sas_address": sas_address, "authorized": auth.is_authorized if auth else False}

# --- Monitoramento (opcional, não WINNF) ---

@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Estatísticas do sistema (opcional, não WINNF)"""
    cbsd_count = db.query(CBSD).count()
    grant_count = db.query(Grant).count()
    event_count = db.query(Event).count()
    auth_count = db.query(SASAuthorization).filter(SASAuthorization.is_authorized == True).count()
    return {
        "cbsds": cbsd_count,
        "grants": grant_count,
        "events": event_count,
        "authorized_sas": auth_count,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/events/recent")
async def get_recent_events(db: Session = Depends(get_db), limit: int = 10):
    """Eventos recentes (opcional, não WINNF)"""
    events = db.query(Event).order_by(Event.created_at.desc()).limit(limit).all()
    return {
        "events": [
            {
                "id": event.id,
                "type": event.event_type,
                "payload": json.loads(event.payload),
                "transaction_hash": event.transaction_hash,
                "block_number": event.block_number,
                "created_at": event.created_at.isoformat()
            }
            for event in events
        ],
        "count": len(events)
    } 