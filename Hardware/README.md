# Hardware Documentation - NeuroLab EEG System

## Overview
The NeuroLab hardware layer consists of an Arduino-based EEG acquisition system that captures neural signals and transmits real-time data to the backend via serial communication at 115200 baud.

---

## Components Used

### Core Components

| Component | Model | Purpose | Specification |
|-----------|-------|---------|-----------------|
| **Microcontroller** | Arduino Uno/Nano | Main processing unit | ATmega328P / ATmega168 |
| **EEG Sensor** | BioAmp EXG Pill | Neural signal acquisition | Analog input on pin A0 |
| **LCD Display** | 8x2 I2C LCD | Real-time data display | Address: 0x27, I2C interface |
| **Audio Module** | DFRobot DF Player Mini | Session audio feedback | Serial/SoftwareSerial interface |
| **Serial Interface** | USB/Serial | Communication with backend | 115200 baud rate |

### Pin Configuration

- **EEG Input**: A0 (Analog)
- **I2C Clock (SCL)**: A5 (SDA) / A4 (SCL)
- **DF Player Mini RX**: Pin 11
- **DF Player Mini TX**: Pin 10

### Signal Processing

- **Sampling Rate**: 256 Hz
- **Sample Interval**: ~3906 microseconds (1,000,000 µs / 256 Hz)
- **LCD Update Rate**: 200 ms

---

## PCB & Board Pin Diagrams


### Component Wiring Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     Arduino Board                        │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Pin A0      ←──────  EEG Sensor Output            │ │
│  │  Pin 10 (TX) ←──────  DF Player Mini RX            │ │
│  │  Pin 11 (RX) ←──────  DF Player Mini TX            │ │
│  │  Pin 20 (SDA) ←──────  LCD I2C SDA  (Uno: A4)      │ │
│  │  Pin 21 (SCL) ←──────  LCD I2C SCL  (Uno: A5)      │ │
│  │  TX/RX ←──────  USB Serial (to Backend at 115200)  │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
         │              │              │
         ▼              ▼              ▼
    ┌─────────┐   ┌──────────┐   ┌──────────┐
    │  EEG    │   │  DF Player│   │8x2 LCD   │
    │ Sensor  │   │ Mini Amp  │   │Display   │
    │         │   │           │   │I2C 0x27  │
    └─────────┘   └──────────┘   └──────────┘
```


---

## Libraries Used

### 1. **Wire.h**  (Built-in)
- **Purpose**: I2C communication protocol
- **Used For**: LCD display communication
- **Credits**: Arduino Core Library

### 2. **LiquidCrystal_I2C v1.1.3** 
- **Purpose**: Control 16x2/8x2 I2C LCD displays
- **Used For**: Real-time EEG value and sampling rate display
- **Author**: Frank de Brabander
- **License**: LGPL
- **GitHub**: https://github.com/johnrickman/LiquidCrystal_I2C
- **Installation**: Arduino Library Manager or Manual

### 3. **SoftwareSerial.h**  (Built-in)
- **Purpose**: Software-based serial communication
- **Used For**: Communication with DF Player Mini module
- **Credits**: Arduino Core Library

### 4. **DFRobotDFPlayerMini v1.0.5** 
- **Purpose**: Control DFRobot DF Player Mini audio module
- **Used For**: Audio feedback during sessions (startup sound, session alerts)
- **Author**: DFRobot
- **License**: MIT
- **GitHub**: https://github.com/DFRobot/DFRobotDFPlayerMini
- **Features**:
  - Volume control (1-30)
  - MP3/WAV playback
  - Supports microSD cards
  - Simple serial protocol

---

## Data Flow

### Hardware Layer Data Flow Diagram

```
EEG Sensor (A0)
    ↓
Arduino Reads @ 256Hz
    ↓
EEG Filter Applied (DSP)
    ↓
├─→ LCD Display Updated (200ms)
│   └─→ Local Real-time Feedback
├─→ Serial Buffer (255,200 baud)
│   └─→ Backend Processing
└─→ Optional Audio Feedback
```

### Detailed Diagrams
For complete circuit schematics, PCB layouts, and detailed flowcharts, see:
- 📋 **Schematics**: `schematics/hardware/`
- 📊 **Flowcharts**: `schematics/hardware/flowchart/`

---

## Complete Hardware Wiring Diagram

### Full System Connection Diagram with Specifications

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          NEUROLAB HARDWARE SYSTEM                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  🔋 POWER SUPPLY                                                              │
│  ├─ USB 5V (500mA)                                                            │
│  └─ GND (Common Reference)                                                    │
│     │                                                                          │
│     ├──────────────────────────────────────────────────────┐                 │
│                                                             ▼                 │
│  🧠 EEG SENSOR (BioAmp EXG Pill)        📟 ARDUINO UNO/MEGA                 │
│  ├─ GND (Black)  ───────────────────────→ GND                                │
│  ├─ +5V (Red)    ───────────────────────→ +5V                                │
│  └─ OUT (Yellow) ───────────────────────→ A0 (ADC Ch 0, 10-bit, 0-5V)       │
│                                          │                                    │
│                                          ├─ A4/SDA (I2C) ──┐                │
│                                          ├─ A5/SCL (I2C) ──┼─→ 🖥️ LCD DISPLAY   │
│                                          │                  ├─ PCF8574       │
│  ┌──────────────────────────────────────→ Pin 10 (SoftSerial TX) │  I2C 0x27 │
│  │                                       │                  │  8x2 Module     │
│  │ 🔊 DF PLAYER MINI (Audio)            ├─ Pin 11 (SoftSerial RX) │         │
│  │ ├─ GND          ────────────────────→ GND                 └─→ SDA/SCL     │
│  │ ├─ +3.3V        ────────────────────→ +3.3V (150mA)           +5V        │
│  │ ├─ RX (Pin 3)   ←───────────────────── Pin 10 (9600 baud)  GND           │
│  │ ├─ TX (Pin 4)   ───────────────────→ Pin 11 (9600 baud)                  │
│  │ ├─ Speaker     (2W output)                                              │
│  │ └─ MicroSD Card (MP3 files)         ├─ TX0 (UART) ──┐                   │
│  │    (FAT32)                           └─ RX0 (UART) ──┴─→ 💻 BACKEND     │
│  │                                         115200 baud      FastAPI/PC      │
│  │                                                                           │
│  └────────────────────────────────────────────────────────────────→ GND     │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Pin Mapping Reference Table

#### Arduino Uno Pin Configuration
| Pin | Function | Connection | Signal Type | Spec |
|-----|----------|-----------|-------------|------|
| A0 | ADC Input | EEG Sensor | Analog 0-5V | 10-bit, 256Hz sampling |
| A4 | SDA | LCD Display | I2C Data | 100 kHz clock |
| A5 | SCL | LCD Display | I2C Clock | - |
| Pin 10 | SoftSerial TX | DF Player RX | Digital | 9600 baud |
| Pin 11 | SoftSerial RX | DF Player TX | Digital | 9600 baud |
| TX0 (Pin 1) | UART TX | Backend PC | Serial | 115200 baud |
| RX0 (Pin 0) | UART RX | Backend PC | Serial | 115200 baud |
| +5V | Power | EEG, LCD, Arduino | DC Power | 40mA per pin |
| GND | Ground | All Components | Reference | Common return |

#### Arduino Mega 2560 Pin Configuration
| Pin | Function | Connection | Signal Type | Spec |
|-----|----------|-----------|-------------|------|
| A0 | ADC Input | EEG Sensor | Analog 0-5V | 10-bit, 256Hz sampling |
| 20 (SDA) | I2C Data | LCD Display | I2C Data | 100 kHz clock |
| 21 (SCL) | I2C Clock | LCD Display | I2C Clock | - |
| Pin 10 | SoftSerial TX | DF Player RX | Digital | 9600 baud |
| Pin 11 | SoftSerial RX | DF Player TX | Digital | 9600 baud |
| TX1 (Pin 18) | UART1 TX | Backend PC | Serial | 115200 baud |
| RX1 (Pin 19) | UART1 RX | Backend PC | Serial | 115200 baud |
| +5V | Power | EEG, LCD, Arduino | DC Power | 40mA per pin |
| GND | Ground | All Components | Reference | Common return |

### Component Signal Specifications

**EEG Sensor (BioAmp EXG Pill)**
- Input: Bioelectric signals from electrodes
- Output: 0-5V analog voltage (proportional to EEG)
- Sampling: 256 Hz continuous
- Resolution: Arduino 10-bit ADC (0-1023 levels)

**I2C Bus (LCD)**
- Clock Speed: 100 kHz
- Address: 0x27 (7-bit)
- Data Line: SDA (Pin A4/20)
- Clock Line: SCL (Pin A5/21)
- Protocol: I2C Standard

**Serial Connections**
- **SoftSerial (DF Player)**: 9600 baud, 8N1
- **UART (Backend)**: 115200 baud, 8N1
- **Format**: Plain text float values (e.g., "512.5\n")

**Power Budget**
- USB Supply: 5V @ 500mA
- Arduino: ~150mA
- LCD Display: ~50mA
- DF Player Mini: ~100mA (3.3V regulator required)
- EEG Sensor: ~10mA
- **Total**: ~310mA (within USB limit)

---

## Serial Communication Protocol

### Output Format
```
<filtered_eeg_value>\n
```
- **Example**: `512.5\n`
- **Baud Rate**: 115200
- **Data Type**: Float values
- **Frequency**: 256 samples per second

---

## Arduino Setup Instructions

### 1. Install Required Libraries
```bash
# Via Arduino IDE Library Manager:
- Search "LiquidCrystal I2C" → Install by Frank de Brabander
- Search "DFRobotDFPlayerMini" → Install by DFRobot
```

### 2. Upload Code
- Connect Arduino via USB
- Select Board: Arduino Uno/Nano
- Select Port: /dev/ttyUSB* (Linux) or COM* (Windows)
- Upload `main.ino`

### 3. Hardware Connections
- Connect BioAmp EXG Pill output to A0
- Connect LCD I2C to SDA/SCL
- Connect DF Player Mini RX/TX to pins 11/10
- Power Arduino via USB or external power supply

---

## Performance Specifications

| Parameter | Value |
|-----------|-------|
| Sampling Frequency | 256 Hz |
| Sample Interval | 3,906 µs |
| Serial Baud Rate | 115,200 bps |
| LCD Update Frequency | 5 Hz (200 ms) |
| Input Voltage | 5V (Arduino) |
| Current Draw | ~150 mA (approximate) |

---

## Troubleshooting

### Display Issues
- Verify I2C address is 0x27 (check with I2C scanner)
- Ensure LCD power and connections are secure
- Try adjusting contrast potentiometer

### Serial Communication Issues
- Verify baud rate matches backend (115200)
- Check USB cable quality
- Ensure Arduino drivers are installed

### Audio Module Issues
- Verify microSD card is inserted and formatted
- Check DFPlayer power supply (3.3V typically)
- Ensure audio files are in correct format (MP3)

---

## References & Credits

- **Arduino**: https://www.arduino.cc/
- **BioAmp EXG Pill**: https://github.com/upsidedownlabs/BioAmp-EXG-Pill
- **DFRobot DF Player Mini**: https://www.dfrobot.com/
- **LiquidCrystal_I2C**: https://github.com/johnrickman/LiquidCrystal_I2C

