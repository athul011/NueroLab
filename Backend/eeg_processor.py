
import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq
from typing import List, Tuple, Dict
from collections import deque
import time

from config import SAMPLING_RATE, FREQUENCY_BANDS, EEG_BUFFER_SIZE


class EEGProcessor:
    
    def __init__(self, sampling_rate: int = SAMPLING_RATE):
        self.sampling_rate = sampling_rate
        self.buffer = deque(maxlen=EEG_BUFFER_SIZE)
        self.filtered_buffer = deque(maxlen=EEG_BUFFER_SIZE)
        
        self.b, self.a = signal.butter(
            4, 
            [0.5, 45], 
            btype='bandpass', 
            fs=sampling_rate
        )
        self.zi = signal.lfilter_zi(self.b, self.a)
        self.mental_state_history = deque(maxlen=10)
        self.stress_history = deque(maxlen=20)
        
    def add_sample(self, value: float) -> float:
        self.buffer.append(value)
        filtered, self.zi = signal.lfilter(
            self.b, self.a, [value], zi=self.zi
        )
        filtered_value = filtered[0]
        self.filtered_buffer.append(filtered_value)
        
        return filtered_value
    
    def get_frequency_spectrum(self, n_points: int = 256) -> List[Dict[str, float]]:
        if len(self.filtered_buffer) < n_points:
            return [{"frequency": i, "magnitude": 0} for i in range(46)]
        
        data = np.array(list(self.filtered_buffer)[-n_points:])
        
        window = np.hanning(len(data))
        data_windowed = data * window
        
        yf = fft(data_windowed)
        xf = fftfreq(len(data), 1 / self.sampling_rate)
        
        positive_mask = xf >= 0
        xf = xf[positive_mask]
        yf = np.abs(yf[positive_mask])
        
        yf = yf / len(data) * 2
        
        spectrum = []
        for i in range(46):
            idx = np.argmin(np.abs(xf - i))
            magnitude = float(yf[idx]) if idx < len(yf) else 0
            magnitude = min(100, magnitude * 10)
            spectrum.append({"frequency": i, "magnitude": magnitude})
        
        return spectrum
    
    def get_band_powers(self) -> Dict[str, float]:
        if len(self.filtered_buffer) < 256:
            return {"delta": 0, "theta": 0, "alpha": 0, "beta": 0, "gamma": 0}
        
        data = np.array(list(self.filtered_buffer)[-256:])
        
        freqs, psd = signal.welch(
            data, 
            fs=self.sampling_rate, 
            nperseg=min(256, len(data))
        )
        
        band_powers = {}
        total_power = np.sum(psd) + 1e-10
        
        for band_name, (low, high) in FREQUENCY_BANDS.items():
            band_mask = (freqs >= low) & (freqs <= high)
            band_power = np.sum(psd[band_mask])
            band_powers[band_name] = float(band_power / total_power * 100)
        
        return band_powers
    
    def detect_mental_state(self) -> Tuple[str, float]:
        bands = self.get_band_powers()
        
        alpha = bands.get("alpha", 0)
        beta = bands.get("beta", 0)
        theta = bands.get("theta", 0)
        gamma = bands.get("gamma", 0)
        
        total = alpha + beta + theta + gamma + 1e-10
        
        alpha_ratio = alpha / total
        beta_ratio = beta / total
        theta_ratio = theta / total
        gamma_ratio = gamma / total
        
        state = "Neutral"
        confidence = 0.5
        
        if alpha_ratio > 0.35 and beta_ratio < 0.3:
            state = "Relaxed"
            confidence = 0.6 + alpha_ratio * 0.4
        
        elif beta_ratio > 0.35 and gamma_ratio > 0.1:
            state = "Focused"
            confidence = 0.6 + beta_ratio * 0.4
        
        elif beta_ratio > 0.4 and gamma_ratio > 0.2:
            state = "Stressed"
            confidence = 0.6 + (beta_ratio + gamma_ratio) * 0.3
        
        else:
            state = "Neutral"
            confidence = 0.7
        
        self.mental_state_history.append((state, confidence))
        
        if len(self.mental_state_history) >= 3:
            states = [s[0] for s in self.mental_state_history]
            from collections import Counter
            state = Counter(states).most_common(1)[0][0]
            confs = [s[1] for s in self.mental_state_history if s[0] == state]
            confidence = sum(confs) / len(confs)
        
        return state, min(0.95, confidence)
    
    def calculate_stress_level(self) -> float:
        bands = self.get_band_powers()
        
        alpha = bands.get("alpha", 0)
        beta = bands.get("beta", 0)
        gamma = bands.get("gamma", 0)
        
        total = alpha + beta + gamma + 1e-10
        stress = ((beta + gamma * 1.5) / total * 100) - (alpha / total * 30)
        stress = max(0, min(100, stress))
        
        self.stress_history.append(stress)
        smoothed_stress = sum(self.stress_history) / len(self.stress_history)
        
        return round(smoothed_stress, 1)
    
    def get_signal_quality(self) -> float:
        if len(self.filtered_buffer) < 50:
            return 0
        
        data = np.array(list(self.filtered_buffer)[-256:])
        
        variance = np.var(data)
        if variance < 1:
            return 10
        
        if variance > 10000:
            return 30
        
        spectrum = self.get_frequency_spectrum()
        power_line_noise = max(
            spectrum[50]["magnitude"] if len(spectrum) > 50 else 0,
            spectrum[60]["magnitude"] if len(spectrum) > 60 else 0
        )
        
        quality = 85
        
        if power_line_noise > 20:
            quality -= 20
        
        if 100 < variance < 5000:
            quality += 10
        
        return max(0, min(100, quality))
    
    def get_recent_signal(self, n_samples: int = 256) -> List[float]:
        return list(self.filtered_buffer)[-n_samples:]
    
    def reset(self):
        self.buffer.clear()
        self.filtered_buffer.clear()
        self.mental_state_history.clear()
        self.stress_history.clear()
        self.zi = signal.lfilter_zi(self.b, self.a)
