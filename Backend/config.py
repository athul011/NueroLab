import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "patients"

DATA_DIR.mkdir(exist_ok=True)

SERIAL_PORT = os.environ.get("SERIAL_PORT", "/dev/ttyACM0")
SERIAL_BAUD_RATE = 115200

SAMPLING_RATE = 256
EEG_BUFFER_SIZE = 256 * 10

WS_BROADCAST_RATE = 25

FREQUENCY_BANDS = {
    "delta": (0.5, 4),
    "theta": (4, 8),
    "alpha": (8, 12),
    "beta": (13, 30),
    "gamma": (30, 45),
}

MENTAL_STATE_CONFIG = {
    "relaxed": {"alpha_threshold": 0.4, "beta_threshold": 0.2},
    "focused": {"beta_threshold": 0.4, "gamma_threshold": 0.2},
    "stressed": {"beta_threshold": 0.5, "gamma_threshold": 0.3},
}
