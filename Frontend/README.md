# Frontend Documentation - NeuroLab

## Overview

NeuroLab Frontend is a responsive web application built with **Next.js**that provides real-time EEG data visualization and patient management. The frontend connects to the FastAPI backend via WebSocket for live streaming neural signals and displays interactive dashboards with brainwave analysis, mental state detection, and session summaries.

---


## Setup Instructions

### Prerequisites
- Node.js 18+ and npm/yarn
- Backend running on `http://localhost:8000`
- Python 3.10+ (backend prerequisite)

### Installation

1. **Navigate to frontend directory**
```bash
cd Frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Create environment configuration**
```bash
# Create .env.local file
cp .env.example .env.local
```

4. **Configure backend URL** (if needed)
Edit `.env.local`:
```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

### Development

**Start development server**
```bash
npm run dev
```
✅ Opens at `http://localhost:3000`

**Build for production**
```bash
npm run build
```

**Start production server**
```bash
npm start
```

**Lint code**
```bash
npm run lint
```

---

## Key Features

### ✅ Real-time EEG Monitoring
- WebSocket connection for live data streaming
- 256Hz sampling rate support
- Multi-component display (waveform, spectrum, bands)

### ✅ Patient Management
- Patient registration with validation
- Session history tracking
- Patient verification system

### ✅ Advanced Visualization
- Interactive charts (Recharts)
- Frequency band analysis
- Mental state detection display
- Stress/Relaxation gauges
- Signal quality scoring

### ✅ AI Integration
- AI-generated session summaries (Gemini API)
- Cognitive state inference
- Trend analysis

### ✅ Responsive Design
- Mobile-first approach
- Tailwind CSS responsive utilities
- Adaptive dashboard layout
- Dark mode support (Next Themes)

### ✅ Accessibility
- Semantic HTML
- ARIA labels on components
- Keyboard navigation
- High contrast mode support

---

## API Integration

### Backend Endpoints Used

**REST API (HTTP)**
```
POST /api/patients                 # Register new patient
GET  /api/patients/{id}            # Fetch patient details
POST /api/sessions                 # Start new session
GET  /api/sessions/{id}            # Fetch session data
```

**WebSocket (WS)**
```
ws://localhost:8000/ws/stream      # Real-time EEG data
  - Receives: {eeg_value, bands, mental_state, quality_score}
  - Updates: 256 times per second
```

---

## Environment Variables

```env
# Backend API configuration
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

# Vercel Analytics (optional)
NEXT_PUBLIC_VERCEL_ANALYTICS_ID=
```

---

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

---

## Dependencies Overview

| Category | Package | Version | Purpose |
|----------|---------|---------|---------|
| **UI Framework** | next | 16.1.6 | React framework |
| **UI Framework** | react | 19.2.4 | React library |
| **Components** | @radix-ui/* | 1.x | Headless UI components |
| **Styling** | tailwindcss | 4.1.9 | CSS framework |
| **Charts** | recharts | 2.15.0 | Data visualization |
| **Forms** | react-hook-form | 7.54.1 | Form management |
| **Validation** | zod | 3.24.1 | Schema validation |
| **Icons** | lucide-react | 0.564.0 | Icon library |
| **Themes** | next-themes | 0.4.6 | Dark mode support |
| **Type Safety** | typescript | 5.7.3 | Type checking |

---

## Contributing

When contributing to the frontend:

1. Follow existing code style and component patterns
2. Use TypeScript for new code
3. Test components in development
4. Update this README if adding new sections
5. Ensure responsive design on mobile devices

---

## License

MIT License - See main [README.md](../README.md) for details

---

## Support & Resources

- **Next.js Docs**: https://nextjs.org/docs
- **React Docs**: https://react.dev
- **Tailwind CSS**: https://tailwindcss.com/docs
- **Radix UI**: https://www.radix-ui.com/docs
- **Recharts**: https://recharts.org/
- **TypeScript**: https://www.typescriptlang.org/docs
