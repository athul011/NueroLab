# Backend Documentation - NeuroLab

### Overview

NeuroLab Backend is FastAPI-based server that handles real-time EEG signal processing, patient management, and AI-powered session analysis. It acquires neural data from Arduino hardware via serial communication, processes complex signal analysis algorithms, streams live data to frontend clients via WebSocket, and generates intelligent session summaries using Google's Gemini API.

---



### Project Structure

```
Backend/
├── main.py                    # FastAPI app entry point, WebSocket endpoints
├── config.py                  # Configuration (ports, baud rates, frequency bands)
├── models.py                  # Pydantic data models
├── eeg_processor.py          # Signal processing (filtering, FFT, band analysis)
├── serial_reader.py          # Arduino/IoT serial communication
├── patient_manager.py        # Patient & session file management
├── gemini_service.py         # AI-powered session summary generation
├── requirements.txt          # Python dependencies
├── .env                       # Environment variables (ignored in git)
└── patients/                 # Patient data storage (persisted locally)
    └── {patient_id}/
        ├── patient.json      # Patient profile
        └── sessions/
            └── {session_id}.csv  # EEG samples for session
```

---


### Data Flow

#### Real-time Streaming

```
┌─────────────┐
│ Arduino     │  
│ 256Hz EEG   │
└──────┬──────┘
       │ Serial (115200 baud)
       ▼
┌─────────────────────────────┐
│  SerialReader.start_stream()│  Raw EEG values
└──────┬──────────────────────┘
       │ Every 3.9ms
       ▼
┌─────────────────────────────┐
│  EEGProcessor.add_sample()  │  
│  - Filter (0.5-45 Hz)       │  Butterworth filter
│  - Compute bands            │  Frequency analysis
│  - Detect mental state      │  Classification
│  - Signal quality score     │  50-100ms window
└──────┬──────────────────────┘
       │
       ├─→ Store in eeg_data_buffer
       │
       └─→ Every 40ms (25Hz rate)
           │
           ▼
       ┌──────────────────────┐
       │  WebSocket.broadcast │ Complex object
       │  EEGStreamData       │ with all analytics
       └──────────┬───────────┘
                  │
                  ▼
            Frontend clients
```

#### Session Lifecycle

```
1. POST /patients            Register patient
                             ↓
2. POST /sessions            Start recording session
   start_time = now()
   status = "recording"
                             ↓
3. WebSocket /ws/stream      Real-time streaming
   Store samples in buffer   (live visualization)
   Compute analytics
                             ↓
4. POST /sessions/{id}/stop  Stop recording session
   end_time = now()
   Compute final statistics
                             ↓
5. Call Gemini API           Generate AI summary
   Send eeg_stats
   Receive analysis
                             ↓
6. GET /sessions/{id}        Fetch complete session
   Return with summary
```

---

### Setup Instructions

#### Prerequisites
- Python 3.10 or higher
- Arduino with EEG sensor connected
- Google Gemini API key (optional but recommended)

#### Installation

1. **Navigate to backend directory**
```bash
cd Backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
# Create .env file
cp .env.example .env

# Edit .env with your settings
nano .env
# Add:
# SERIAL_PORT=/dev/ttyACM0
# GEMINI_API_KEY=your_key_here
```

5. **Verify Arduino connection**
```bash
python -m serial.tools.list_ports
# Should show Arduino device
```

#### Running the Server

**Development mode**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Production mode**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

**With simulated data (testing)**
```bash
# Connect to backend endpoint:
# POST /connect?simulate=true
```

---

### Performance Specifications

| Metric | Value | Notes |
|--------|-------|-------|
| Sampling Rate | 256 Hz | Arduino ADC rate |
| Processing Latency | <20ms | Filter + analysis per sample |
| WebSocket Update Rate | 25 Hz | Frontend refresh rate |
| Memory per Record | ~100 KB/min | 256Hz * 60s * 4 bytes |
| Buffer Size | 2560 samples | 10 seconds at 256Hz |
| Max Concurrent Clients | 100+ | Limited by network |
| FFT Resolution | 46 points | 0-45 Hz spectrum |

---


### Database Schema

#### Patient File Structure
```json
{
  "name": "string",
  "patientId": "string (unique)",
  "age": "string",
  "gender": "string",
  "phone": "string",
  "email": "string",
  "emergencyContact": "string",
  "medicalHistory": "string",
  "created_at": "ISO 8601 timestamp",
  "updated_at": "ISO 8601 timestamp"
}
```

#### Session CSV Format
```
timestamp (seconds),raw_eeg_value,filtered_eeg_value
```

---

### Security Notes

⚠️ **Development Only**
- Currently stores data locally (no encryption)
- CORS allows all origins (`allow_origins=["*"]`)
- No authentication/authorization system

---

### Support & Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **Uvicorn**: https://www.uvicorn.org/
- **SciPy Signal Processing**: https://docs.scipy.org/doc/scipy/reference/signal.html
- **Pydantic**: https://docs.pydantic.dev/
- **PySerial**: https://pyserial.readthedocs.io/
- **Gemini API**: https://ai.google.dev/
