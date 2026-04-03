from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class PatientData(BaseModel):
    name: str
    patient_id: str = Field(alias="patientId")
    age: str
    gender: str
    phone: str
    email: str = ""
    emergency_contact: str = Field(default="", alias="emergencyContact")
    medical_history: str = Field(default="", alias="medicalHistory")
    
    class Config:
        populate_by_name = True


class SessionInfo(BaseModel):
    session_id: str
    patient_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: int = 0
    notes: str = ""


class EEGDataPoint(BaseModel):
    timestamp: float
    value: float
    filtered_value: float


class BrainwaveBands(BaseModel):
    delta: float = 0.0
    theta: float = 0.0
    alpha: float = 0.0
    beta: float = 0.0
    gamma: float = 0.0


class MentalState(BaseModel):
    state: str
    confidence: float
    timestamp: float


class EEGStreamData(BaseModel):
    timestamp: float
    raw_signal: List[float]
    signal_quality: float
    brainwaves: BrainwaveBands
    mental_state: MentalState
    stress_level: float
    frequency_spectrum: List[Dict[str, float]]


class PatientSession(BaseModel):
    patient: PatientData
    session: SessionInfo
    eeg_data: List[EEGDataPoint] = []


class ConnectionStatus(BaseModel):
    connected: bool
    port: str
    sampling_rate: int
    signal_quality: float
    message: str
