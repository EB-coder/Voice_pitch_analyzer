import wave
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from scipy.signal import find_peaks

# Параметры окна
WINDOW_SIZE = 2048
HOP_SIZE = 512

# Открытие WAV файла
filename = "voice.wav"
wf = wave.open(filename, 'rb')
n_channels = wf.getnchannels()
sampwidth = wf.getsampwidth()
framerate = wf.getframerate()
n_frames = wf.getnframes()

# Загрузка данных
raw_data = wf.readframes(n_frames)
wf.close()

# Преобразование в массив
audio = np.frombuffer(raw_data, dtype=np.int16)
audio = audio / np.max(np.abs(audio))  # нормализация

# Анализ окон
pitches = []
times = []

for i in range(0, len(audio) - WINDOW_SIZE, HOP_SIZE):
    window = audio[i:i+WINDOW_SIZE]
    fft_spectrum = np.abs(fft(window))[:WINDOW_SIZE // 2]
    freqs = np.fft.fftfreq(WINDOW_SIZE, d=1.0 / framerate)[:WINDOW_SIZE // 2]

    # Поиск пиков
    peak_indices, _ = find_peaks(fft_spectrum, height=0.1)
    if len(peak_indices) > 0:
        dominant_freq = freqs[peak_indices[0]]
    else:
        dominant_freq = 0

    pitches.append(dominant_freq)
    times.append(i / framerate)

# Фильтрация нулей
cleaned_pitches = [p for p in pitches if p > 50 and p < 1000]

# Статистика
mean_pitch = np.mean(cleaned_pitches)
max_pitch = np.max(cleaned_pitches)
min_pitch = np.min(cleaned_pitches)
std_pitch = np.std(cleaned_pitches)

# Вывод
print(f"📈 Средняя частота (pitch): {mean_pitch:.2f} Гц")
print(f"🔼 Максимум: {max_pitch:.2f} Гц")
print(f"🔽 Минимум: {min_pitch:.2f} Гц")
print(f"± Стандартное отклонение: {std_pitch:.2f} Гц")

# Построение графика
plt.figure(figsize=(10, 4))
plt.plot(times, pitches, color='purple', label='Pitch (Hz)')
plt.xlabel("Время (сек)")
plt.ylabel("Частота (Гц)")
plt.title("Анализ pitch голоса")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# python analyze_pitch.py