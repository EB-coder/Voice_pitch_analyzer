# import pyaudio
# import wave



# # Параметры записи
# FORMAT = pyaudio.paInt16      # 16-бит
# CHANNELS = 1                  # Моно
# RATE = 44100                 # Частота дискретизации
# CHUNK = 1024                 # Размер блока
# RECORD_SECONDS = 10          # Длительность записи
# OUTPUT_FILENAME = "voice.wav"  # Имя выходного файла

# # Инициализация
# audio = pyaudio.PyAudio()

# stream = audio.open(format=FORMAT,
#                     channels=CHANNELS,
#                     rate=RATE,
#                     input=True,
#                     frames_per_buffer=CHUNK)

# print("🎙️ Pls speak...")

# frames = []

# for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     frames.append(data)

# print("✅ Recording complete.")

# # Остановить и закрыть
# stream.stop_stream()
# stream.close()
# audio.terminate()

# # Сохранить в WAV файл
# with wave.open(OUTPUT_FILENAME, 'wb') as wf:
#     wf.setnchannels(CHANNELS)
#     wf.setsampwidth(audio.get_sample_size(FORMAT))
#     wf.setframerate(RATE)
#     wf.writeframes(b''.join(frames))

# print(f"📁 File saved as {OUTPUT_FILENAME}")

import sounddevice as sd
import numpy as np
import wave
import time

# Параметры записи
RATE = 44100
CHANNELS = 1
DTYPE = np.int16
RECORD_SECONDS = 10
OUTPUT_FILENAME = "voice.wav"

print("🎙️ Recording... Speak now!")

# Запись с явным указанием длительности
audio = sd.rec(
    int(RECORD_SECONDS * RATE),
    samplerate=RATE,
    channels=CHANNELS,
    dtype=DTYPE
)

# Визуальный прогресс записи
for i in range(RECORD_SECONDS):
    time.sleep(1)
    print(f"⏱️ Recording... {i+1}/{RECORD_SECONDS} seconds")

# Убедимся, что запись завершена
sd.wait()
print("✅ Recording complete.")

# Сохранить в WAV файл
with wave.open(OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)  # Для np.int16
    wf.setframerate(RATE)
    wf.writeframes(audio.tobytes())

print(f"📁 File saved as {OUTPUT_FILENAME}")
