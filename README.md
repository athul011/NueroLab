# NeuroLab
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-green)
![Next.js](https://img.shields.io/badge/Next.js-frontend-black)
![Arduino](https://img.shields.io/badge/Arduino-EEG-orange)
![License](https://img.shields.io/badge/license-MIT-blue)

NeuroLab, A real-time EEG monitoring platform designed to capture, analyze, and visualize brainwave activity for research, educational, and experimental purposes. The system enables continuous acquisition of neural signals from EEG sensors and processes the data to extract meaningful brainwave patterns such as delta, theta, alpha, beta, and gamma bands. These signals are analyzed to estimate cognitive states, stress levels, and overall signal quality during a monitoring session. NeuroLab provides an interactive environment where users can register participants, initiate recording sessions, observe live brainwave activity, and review session summaries after completion.

### Features

- Real-time EEG streaming via WebSocket
- Arduino-based EEG acquisition (BioAmp EXG Pill)
- Real-time brainwave analysis (delta, theta, alpha, beta, gamma)
- Mental state detection (Relaxed / Focused / Stressed)
- Signal quality scoring
- Patient and session management
- AI-generated session summaries (Gemini API)
- Interactive EEG dashboard

### Hardware

NeuroLab uses an Arduino-based IoT system to acquire real-time EEG signals from the brain via BioAmp EXG Pill sensor. The system features:

- **Microcontroller**: Arduino Uno/Mega (ATmega328P/2560)
- **EEG Sensor**: BioAmp EXG Pill with 256 Hz sampling rate
- **Real-time Display**: 8x2 I2C LCD for local feedback
- **Audio Feedback**: DF Player Mini for session alerts
- **Serial Communication**: 115200 baud to backend

For detailed hardware specifications, pin configurations, wiring diagrams, and component details, see [Hardware Documentation](Hardware/README.md).

---

### Frontend

NeuroLab Frontend is  Next.js web application with real-time EEG visualization, patient management, and interactive dashboards.

- **Framework**: Next.js, TypeScript 5.7
- **UI Components**: Radix UI (30+ components)
- **Styling**: Tailwind CSS 4
- **Visualization**: Recharts (EEG waveforms, frequency spectra)
- **Forms**: React Hook Form + Zod validation
- **Real-time**: WebSocket integration for live EEG streaming

For detailed frontend architecture, component catalog, setup instructions, and API integration, see [Frontend Documentation](Frontend/README.md).

---

### Backend

NeuroLab Backend is FastAPI server that handles real-time EEG signal processing, patient management, and AI-powered session analysis. Built with modern async/await patterns, it streams live neural data via WebSocket while performing complex signal analysis.

- **Framework**: FastAPI 0.115, Uvicorn async server
- **Signal Processing**: NumPy, SciPy (filtering, FFT, spectral analysis)
- **Hardware I/O**: PySerial 3.5 (Arduino communication at 115200 baud)
- **Data Validation**: Pydantic 2.8 for type-safe models
- **Real-time Communication**: WebSockets 12.0
- **AI Integration**: aiohttp + Google Gemini API


For comprehensive backend documentation including API endpoints, signal processing details, WebSocket data formats, setup instructions see [Backend Documentation](Backend/README.md).

---
### Collaborators
<table>
    <tbody>
        <tr>
            <td valign="top" ><a href="https://github.com/riz4d"><img src="https://avatars.githubusercontent.com/u/73955457?v=4?s=100" width="100px;" alt="Mohamed Rizad"/><br /><sub><b>Mohamed Rizad</b></sub></a></td>
        </tr>
    </tbody>
</table>

---
### Security Note

NeuroLab currently stores EEG data locally for research and development purposes.

---
### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
