# NeuroLab
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-green)
![Next.js](https://img.shields.io/badge/Next.js-frontend-black)
![Arduino](https://img.shields.io/badge/Arduino-EEG-orange)
![License](https://img.shields.io/badge/license-MIT-blue)

NeuroLab, A real-time EEG monitoring platform designed to capture, analyze, and visualize brainwave activity for research, educational, and experimental purposes. The system enables continuous acquisition of neural signals from EEG sensors and processes the data to extract meaningful brainwave patterns such as delta, theta, alpha, beta, and gamma bands. These signals are analyzed to estimate cognitive states, stress levels, and overall signal quality during a monitoring session. NeuroLab provides an interactive environment where users can register participants, initiate recording sessions, observe live brainwave activity, and review session summaries after completion.

## Features

- Real-time EEG streaming via WebSocket
- Arduino-based EEG acquisition (BioAmp EXG Pill)
- Real-time brainwave analysis (delta, theta, alpha, beta, gamma)
- Mental state detection (Relaxed / Focused / Stressed)
- Signal quality scoring
- Patient and session management
- AI-generated session summaries (Gemini API)
- Interactive EEG dashboard

## Contributing

Pull requests are welcome.
If you would like to contribute

## Security Note

NeuroLab currently stores EEG data locally for research and development purposes.
