#!/bin/bash

echo "🧠 Starting NeuroLab System..."
echo ""

if ! command -v npm &> /dev/null; then
    echo "Error: npm is not installed"
    exit 1
fi
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed"
    exit 1
fi
echo "Starting backend server..."
cd "$(dirname "$0")/backend"

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1

python main.py &
BACKEND_PID=$!
cd ..
sleep 3

echo "Starting frontend..."
npm run dev &
FRONTEND_PID=$!


cleanup() {
    echo ""
    echo "Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

wait
