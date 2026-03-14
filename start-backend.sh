#!/bin/bash
cd "$(dirname "$0")/backend"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
echo "Installing dependencies..."
pip install -r requirements.txt

if [ -e /dev/ttyACM0 ] || [ -e /dev/ttyUSB0 ]; then
    echo "Arduino device detected"
    sudo chmod 666 /dev/ttyACM0 2>/dev/null || true
    sudo chmod 666 /dev/ttyUSB0 2>/dev/null || true
else
    echo "No Arduino detected - simulation mode will be available"
fi

python main.py
