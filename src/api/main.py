from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import logging
import json
import os
from datetime import datetime, timezone
from sqlalchemy.orm import Session
import uuid
import time

from src.models.database import get_db
from src.models.cbsd import CBSD
from src.models.grant import Grant
from src.models.sas_auth import SASAuthorization
from src.models.event import Event
from src.config.settings import settings

# Configurar logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Console handler
    ]
)
logger = logging.getLogger(__name__)

# Inicializar FastAPI
app = FastAPI(
    title="SAS (Spectrum Access System) - WINNF SAS-SAS",
    description="API REST compatível com WINNF TS-0096/3003 (SAS-SAS) - Alinhada com contrato Solidity",
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

# Modelos Pydantic alinhados com contrato Solidity
class RegistrationRequest(BaseModel):
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
    cbsdAddress: str

class GrantRequest(BaseModel):
    fccId: str
    cbsdSerialNumber: str
    channelType: str
    maxEirp: int
    lowFrequency: int
    highFrequency: int
    requestedMaxEirp: int
    requestedLowFrequency: int
    requestedHighFrequency: int
    grantExpireTime: int

class RelinquishmentRequest(BaseModel):
    fccId: str
    cbsdSerialNumber: str
    grantId: str

class DeregistrationRequest(BaseModel):
    fccId: str
    cbsdSerialNumber: str

class SASAuthorizeRequest(BaseModel):
    sas_address: str

class SASRevokeRequest(BaseModel):
    sas_address: str

# Modelos de resposta alinhados com contrato Solidity
class RegistrationResponse(BaseModel):
    responseCode: int = 0
    cbsdId: str
    registrationResponse: Dict[str, Any]

class GrantResponse(BaseModel):
    responseCode: int = 0
    cbsdId: str
    grantResponse: Dict[str, Any]

class RelinquishmentResponse(BaseModel):
    responseCode: int = 0
    cbsdId: str
    relinquishmentResponse: Dict[str, Any]

class DeregistrationResponse(BaseModel):
    responseCode: int = 0
    cbsdId: str
    deregistrationResponse: Dict[str, Any]

# Função para verificar autorização SAS
async def verify_sas_authorization(sas_address: str, db: Session) -> bool:
    """Verifica se o SAS está autorizado"""
    auth = db.query(SASAuthorization).filter(
        SASAuthorization.sas_address == sas_address,
        SASAuthorization.authorized == True
    ).first()
    return auth is not None

# Função para gerar chave CBSD (equivalente ao keccak256 do Solidity)
def generate_cbsd_key(fcc_id: str, cbsd_serial_number: str) -> str:
    """Gera chave única para CBSD (equivalente ao keccak256 do Solidity)"""
    return f"{fcc_id}_{cbsd_serial_number}"

# --- Interface Pública SAS-SAS (WINNF TS-0096/3003) - Alinhada com contrato Solidity ---

@app.get("/health")
async def health_check():
    """Health check da API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0"
    }

@app.post("/v1.3/registration")
async def registration(
    request: RegistrationRequest, 
    sas_address: str = Header(..., alias="X-SAS-Address"),
    db: Session = Depends(get_db)
):
    """Registro de CBSD - Alinhado com contrato Solidity"""
    logger.info(f"=== REGISTRATION REQUEST ===")
    logger.info(f"SAS Address: {sas_address}")
    logger.info(f"FCC ID: {request.fccId}")
    logger.info(f"User ID: {request.userId}")
    logger.info(f"CBSD Serial: {request.cbsdSerialNumber}")
    logger.info(f"Thread: {request.fccId.split('-')[1] if '-' in request.fccId else 'N/A'}")
    
    try:
        # Verificar se SAS está autorizado
        logger.info(f"Verificando autorização SAS: {sas_address}")
        if not await verify_sas_authorization(sas_address, db):
            logger.error(f"SAS não autorizado: {sas_address}")
            raise HTTPException(status_code=403, detail="SAS não autorizado")
        logger.info(f"SAS autorizado: {sas_address}")
        
        # Gerar chave CBSD
        cbsd_key = generate_cbsd_key(request.fccId, request.cbsdSerialNumber)
        logger.info(f"Chave CBSD gerada: {cbsd_key}")
        
        # Verificar se CBSD já existe
        logger.info(f"Verificando se CBSD já existe: {request.fccId}/{request.cbsdSerialNumber}")
        existing_cbsd = db.query(CBSD).filter(
            CBSD.fcc_id == request.fccId,
            CBSD.cbsd_serial_number == request.cbsdSerialNumber
        ).first()
        
        if existing_cbsd:
            logger.warning(f"CBSD já existe: {request.fccId}/{request.cbsdSerialNumber}")
            raise HTTPException(status_code=400, detail="CBSD já existe")
        logger.info(f"CBSD não existe, prosseguindo com registro")
        
        # Log dos dados recebidos para debug
        logger.info(f"Dados do request:")
        logger.info(f"  fccId: '{request.fccId}' (tamanho: {len(request.fccId)})")
        logger.info(f"  userId: '{request.userId}' (tamanho: {len(request.userId)})")
        logger.info(f"  cbsdSerialNumber: '{request.cbsdSerialNumber}' (tamanho: {len(request.cbsdSerialNumber)})")
        logger.info(f"  callSign: '{request.callSign}'")
        logger.info(f"  cbsdCategory: '{request.cbsdCategory}'")
        logger.info(f"  airInterface: '{request.airInterface}'")
        logger.info(f"  measCapability: {request.measCapability}")
        logger.info(f"  eirpCapability: {request.eirpCapability}")
        logger.info(f"  latitude: {request.latitude}")
        logger.info(f"  longitude: {request.longitude}")
        logger.info(f"  height: {request.height}")
        logger.info(f"  heightType: '{request.heightType}'")
        logger.info(f"  indoorDeployment: {request.indoorDeployment}")
        logger.info(f"  antennaGain: {request.antennaGain}")
        logger.info(f"  antennaBeamwidth: {request.antennaBeamwidth}")
        logger.info(f"  antennaAzimuth: {request.antennaAzimuth}")
        logger.info(f"  groupingParam: '{request.groupingParam}'")
        logger.info(f"  cbsdAddress: '{request.cbsdAddress}'")
        
        # Criar novo CBSD
        current_timestamp = int(time.time())
        cbsd = CBSD(
            fcc_id=request.fccId,
            user_id=request.userId,
            cbsd_serial_number=request.cbsdSerialNumber,
            call_sign=request.callSign,
            cbsd_category=request.cbsdCategory,
            air_interface=request.airInterface,
            meas_capability=json.dumps(request.measCapability),
            eirp_capability=request.eirpCapability,
            latitude=request.latitude,
            longitude=request.longitude,
            height=request.height,
            height_type=request.heightType,
            indoor_deployment=request.indoorDeployment,
            antenna_gain=request.antennaGain,
            antenna_beamwidth=request.antennaBeamwidth,
            antenna_azimuth=request.antennaAzimuth,
            grouping_param=request.groupingParam,
            cbsd_address=request.cbsdAddress,
            sas_origin=sas_address,
            registration_timestamp=current_timestamp
        )
        db.add(cbsd)
        
        # Registrar evento (equivalente ao emit do Solidity)
        event = Event(
            event_type="CBSD_REGISTERED",
            payload=json.dumps({
                "fccId": request.fccId,
                "serialNumber": request.cbsdSerialNumber,
                "sasOrigin": sas_address
            }),
            transaction_hash=f"0x{uuid.uuid4().hex}",
            block_number=1
        )
        db.add(event)
        db.commit()
        
        logger.info(f"Registro CBSD criado com sucesso: {request.cbsdSerialNumber}")
        logger.info(f"Evento registrado: CBSD_REGISTERED")
        logger.info(f"=== REGISTRATION SUCCESS ===")
        
        return RegistrationResponse(
            cbsdId=request.cbsdSerialNumber,
            registrationResponse={
                "cbsdId": request.cbsdSerialNumber,
                "registration": "SUCCESS"
            }
        )
        
    except HTTPException as he:
        logger.error(f"HTTPException no registro: {he.status_code} - {he.detail}")
        raise
    except Exception as e:
        logger.error(f"Erro interno no registro: {str(e)}")
        logger.error(f"Tipo de erro: {type(e).__name__}")
        logger.error(f"Traceback completo:")
        import traceback
        logger.error(traceback.format_exc())
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro interno no registro")

@app.post("/v1.3/grant")
async def grant(
    request: GrantRequest, 
    sas_address: str = Header(..., alias="X-SAS-Address"),
    db: Session = Depends(get_db)
):
    """Solicitação de grant - Alinhado com contrato Solidity"""
    logger.info(f"=== GRANT REQUEST ===")
    logger.info(f"SAS Address: {sas_address}")
    logger.info(f"FCC ID: {request.fccId}")
    logger.info(f"CBSD Serial: {request.cbsdSerialNumber}")
    logger.info(f"Channel Type: {request.channelType}")
    
    try:
        # Verificar se SAS está autorizado
        logger.info(f"Verificando autorização SAS: {sas_address}")
        if not await verify_sas_authorization(sas_address, db):
            logger.error(f"SAS não autorizado: {sas_address}")
            raise HTTPException(status_code=403, detail="SAS não autorizado")
        logger.info(f"SAS autorizado: {sas_address}")
        
        # Verificar se CBSD existe
        logger.info(f"Verificando se CBSD existe: {request.fccId}/{request.cbsdSerialNumber}")
        cbsd = db.query(CBSD).filter(
            CBSD.fcc_id == request.fccId,
            CBSD.cbsd_serial_number == request.cbsdSerialNumber
        ).first()
        
        if not cbsd:
            raise HTTPException(status_code=404, detail="CBSD não registrado")
        
        # Gerar ID único para o grant (equivalente ao contrato Solidity)
        grant_id = f"grant_{request.fccId}_{request.cbsdSerialNumber}_{uuid.uuid4().hex[:8]}"
        current_timestamp = int(time.time())
        
        # Criar grant
        grant = Grant(
            grant_id=grant_id,
            fcc_id=request.fccId,
            cbsd_serial_number=request.cbsdSerialNumber,
            channel_type=request.channelType,
            max_eirp=request.maxEirp,
            low_frequency=request.lowFrequency,
            high_frequency=request.highFrequency,
            requested_max_eirp=request.requestedMaxEirp,
            requested_low_frequency=request.requestedLowFrequency,
            requested_high_frequency=request.requestedHighFrequency,
            grant_expire_time=request.grantExpireTime,
            state="GRANTED",
            sas_origin=sas_address,
            grant_timestamp=current_timestamp,
            terminated=False
        )
        db.add(grant)
        
        # Registrar evento (equivalente ao emit do Solidity)
        event = Event(
            event_type="GRANT_CREATED",
            payload=json.dumps({
                "fccId": request.fccId,
                "serialNumber": request.cbsdSerialNumber,
                "grantId": grant_id,
                "sasOrigin": sas_address
            }),
            transaction_hash=f"0x{uuid.uuid4().hex}",
            block_number=1
        )
        db.add(event)
        db.commit()
        
        logger.info(f"Grant criado com sucesso: {grant_id}")
        logger.info(f"Evento registrado: GRANT_CREATED")
        logger.info(f"=== GRANT SUCCESS ===")
        
        return GrantResponse(
            cbsdId=request.cbsdSerialNumber,
            grantResponse={
                "cbsdId": request.cbsdSerialNumber,
                "grantId": grant_id,
                "grant": "SUCCESS",
                "channelType": request.channelType,
                "maxEirp": request.maxEirp,
                "lowFrequency": request.lowFrequency,
                "highFrequency": request.highFrequency,
                "grantExpireTime": request.grantExpireTime
            }
        )
        
    except HTTPException as he:
        logger.error(f"HTTPException no grant: {he.status_code} - {he.detail}")
        raise
    except Exception as e:
        logger.error(f"Erro interno na solicitação de grant: {str(e)}")
        logger.error(f"Tipo de erro: {type(e).__name__}")
        logger.error(f"Traceback completo:")
        import traceback
        logger.error(traceback.format_exc())
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro interno na solicitação de grant")

@app.post("/v1.3/relinquishment")
async def relinquishment(
    request: RelinquishmentRequest, 
    sas_address: str = Header(..., alias="X-SAS-Address"),
    db: Session = Depends(get_db)
):
    """Terminar grant - Alinhado com contrato Solidity"""
    logger.info(f"=== RELINQUISHMENT REQUEST ===")
    logger.info(f"SAS Address: {sas_address}")
    logger.info(f"FCC ID: {request.fccId}")
    logger.info(f"CBSD Serial: {request.cbsdSerialNumber}")
    logger.info(f"Grant ID: {request.grantId}")
    
    try:
        # Verificar se SAS está autorizado
        logger.info(f"Verificando autorização SAS: {sas_address}")
        if not await verify_sas_authorization(sas_address, db):
            logger.error(f"SAS não autorizado: {sas_address}")
            raise HTTPException(status_code=403, detail="SAS não autorizado")
        logger.info(f"SAS autorizado: {sas_address}")
        
        # Verificar se CBSD existe
        logger.info(f"Verificando se CBSD existe: {request.fccId}/{request.cbsdSerialNumber}")
        cbsd = db.query(CBSD).filter(
            CBSD.fcc_id == request.fccId,
            CBSD.cbsd_serial_number == request.cbsdSerialNumber
        ).first()
        
        if not cbsd:
            logger.error(f"CBSD não registrado: {request.fccId}/{request.cbsdSerialNumber}")
            raise HTTPException(status_code=404, detail="CBSD não registrado")
        logger.info(f"CBSD encontrado: {request.cbsdSerialNumber}")
        
        # Encontrar e terminar o grant
        logger.info(f"Procurando grant: {request.grantId}")
        grant = db.query(Grant).filter(
            Grant.grant_id == request.grantId,
            Grant.fcc_id == request.fccId,
            Grant.cbsd_serial_number == request.cbsdSerialNumber
        ).first()
        
        if not grant:
            raise HTTPException(status_code=404, detail="Grant não encontrado")
        
        if grant.terminated:
            raise HTTPException(status_code=400, detail="Grant já foi terminado")
        
        grant.terminated = True
        grant.state = "TERMINATED"
        
        # Registrar evento (equivalente ao emit do Solidity)
        event = Event(
            event_type="GRANT_TERMINATED",
            payload=json.dumps({
                "fccId": request.fccId,
                "serialNumber": request.cbsdSerialNumber,
                "grantId": request.grantId,
                "sasOrigin": sas_address
            }),
            transaction_hash=f"0x{uuid.uuid4().hex}",
            block_number=1
        )
        db.add(event)
        db.commit()
        
        logger.info(f"Grant terminado com sucesso: {request.grantId}")
        logger.info(f"Evento registrado: GRANT_TERMINATED")
        logger.info(f"=== RELINQUISHMENT SUCCESS ===")
        
        return RelinquishmentResponse(
            cbsdId=request.cbsdSerialNumber,
            relinquishmentResponse={
                "cbsdId": request.cbsdSerialNumber,
                "grantId": request.grantId,
                "relinquishment": "SUCCESS"
            }
        )
        
    except HTTPException as he:
        logger.error(f"HTTPException no relinquishment: {he.status_code} - {he.detail}")
        raise
    except Exception as e:
        logger.error(f"Erro interno no relinquishment: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro interno no relinquishment")

@app.post("/v1.3/deregistration")
async def deregistration(
    request: DeregistrationRequest, 
    sas_address: str = Header(..., alias="X-SAS-Address"),
    db: Session = Depends(get_db)
):
    """Remover CBSD - Alinhado com contrato Solidity"""
    try:
        # Verificar se SAS está autorizado
        if not await verify_sas_authorization(sas_address, db):
            raise HTTPException(status_code=403, detail="SAS não autorizado")
        
        # Verificar se CBSD existe
        cbsd = db.query(CBSD).filter(
            CBSD.fcc_id == request.fccId,
            CBSD.cbsd_serial_number == request.cbsdSerialNumber
        ).first()
        
        if not cbsd:
            raise HTTPException(status_code=404, detail="CBSD não registrado")
        
        # Remover CBSD e todos os seus grants
        db.delete(cbsd)
        
        # Registrar evento
        event = Event(
            event_type="CBSD_DEREGISTERED",
            payload=json.dumps({
                "fccId": request.fccId,
                "serialNumber": request.cbsdSerialNumber,
                "sasOrigin": sas_address
            }),
            transaction_hash=f"0x{uuid.uuid4().hex}",
            block_number=1
        )
        db.add(event)
        db.commit()
        
        return DeregistrationResponse(
            cbsdId=request.cbsdSerialNumber,
            deregistrationResponse={
                "cbsdId": request.cbsdSerialNumber,
                "deregistration": "SUCCESS"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no deregistration: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro interno no deregistration")

# --- Interface Administrativa (equivalente ao onlyOwner do contrato) ---

@app.post("/sas/authorize")
async def authorize_sas(request: SASAuthorizeRequest, db: Session = Depends(get_db)):
    """Autorizar SAS - Equivalente ao authorizeSAS do contrato"""
    try:
        existing_auth = db.query(SASAuthorization).filter(
            SASAuthorization.sas_address == request.sas_address
        ).first()
        
        if existing_auth:
            existing_auth.authorized = True
        else:
            auth = SASAuthorization(
                sas_address=request.sas_address,
                authorized=True
            )
            db.add(auth)
        
        # Registrar evento
        event = Event(
            event_type="SAS_AUTHORIZED",
            payload=json.dumps({"sas_address": request.sas_address}),
            transaction_hash=f"0x{uuid.uuid4().hex}",
            block_number=1
        )
        db.add(event)
        db.commit()
        
        return {"success": True, "message": f"SAS {request.sas_address} autorizado"}
        
    except Exception as e:
        logger.error(f"Erro na autorização SAS: {str(e)}")
        logger.error(f"Tipo de erro: {type(e).__name__}")
        logger.error(f"Traceback completo:")
        import traceback
        logger.error(traceback.format_exc())
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro interno na autorização")

@app.post("/sas/revoke")
async def revoke_sas(request: SASRevokeRequest, db: Session = Depends(get_db)):
    """Revogar SAS - Equivalente ao revokeSAS do contrato"""
    try:
        auth = db.query(SASAuthorization).filter(
            SASAuthorization.sas_address == request.sas_address
        ).first()
        
        if auth:
            auth.authorized = False
            
            # Registrar evento
            event = Event(
                event_type="SAS_REVOKED",
                payload=json.dumps({"sas_address": request.sas_address}),
                transaction_hash=f"0x{uuid.uuid4().hex}",
                block_number=1
            )
            db.add(event)
            db.commit()
        
        return {"success": True, "message": f"SAS {request.sas_address} revogado"}
        
    except Exception as e:
        logger.error(f"Erro na revogação SAS: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro interno na revogação")

@app.get("/sas/{sas_address}/authorized")
async def check_sas_authorization(sas_address: str, db: Session = Depends(get_db)):
    """Verificar se SAS está autorizado"""
    auth = db.query(SASAuthorization).filter(
        SASAuthorization.sas_address == sas_address
    ).first()
    return {"sas_address": sas_address, "authorized": auth.authorized if auth else False}

# --- Endpoints de consulta (equivalente às funções view do contrato) ---

@app.get("/v1.3/cbsd/{fcc_id}/{cbsd_serial_number}")
async def get_cbsd(fcc_id: str, cbsd_serial_number: str, db: Session = Depends(get_db)):
    """Obter CBSD - Equivalente ao mapping cbsds do contrato"""
    cbsd = db.query(CBSD).filter(
        CBSD.fcc_id == fcc_id,
        CBSD.cbsd_serial_number == cbsd_serial_number
    ).first()
    
    if not cbsd:
        raise HTTPException(status_code=404, detail="CBSD não encontrado")
    
    return {
        "fccId": cbsd.fcc_id,
        "userId": cbsd.user_id,
        "cbsdSerialNumber": cbsd.cbsd_serial_number,
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
        "cbsdAddress": cbsd.cbsd_address,
        "sasOrigin": cbsd.sas_origin,
        "registrationTimestamp": cbsd.registration_timestamp
    }

@app.get("/v1.3/grants/{fcc_id}/{cbsd_serial_number}")
async def get_grants(fcc_id: str, cbsd_serial_number: str, db: Session = Depends(get_db)):
    """Obter grants de um CBSD - Equivalente ao mapping grants do contrato"""
    grants = db.query(Grant).filter(
        Grant.fcc_id == fcc_id,
        Grant.cbsd_serial_number == cbsd_serial_number
    ).all()
    
    return {
        "grants": [
            {
                "grantId": grant.grant_id,
                "channelType": grant.channel_type,
                "grantExpireTime": grant.grant_expire_time,
                "terminated": grant.terminated,
                "maxEirp": grant.max_eirp,
                "lowFrequency": grant.low_frequency,
                "highFrequency": grant.high_frequency,
                "requestedMaxEirp": grant.requested_max_eirp,
                "requestedLowFrequency": grant.requested_low_frequency,
                "requestedHighFrequency": grant.requested_high_frequency,
                "sasOrigin": grant.sas_origin,
                "grantTimestamp": grant.grant_timestamp
            }
            for grant in grants
        ]
    }

# --- Monitoramento ---

@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Estatísticas do sistema - Equivalente aos contadores do contrato"""
    cbsd_count = db.query(CBSD).count()
    grant_count = db.query(Grant).count()
    event_count = db.query(Event).count()
    auth_count = db.query(SASAuthorization).filter(SASAuthorization.authorized == True).count()
    
    return {
        "totalCbsds": cbsd_count,
        "totalGrants": grant_count,
        "totalEvents": event_count,
        "authorizedSAS": auth_count,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/events/recent")
async def get_recent_events(db: Session = Depends(get_db), limit: int = 10):
    """Eventos recentes - Equivalente aos eventos do contrato"""
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