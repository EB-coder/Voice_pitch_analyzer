import pyaudio
import wave



# Параметры записи
FORMAT = pyaudio.paInt16      # 16-бит
CHANNELS = 1                  # Моно
RATE = 44100                 # Частота дискретизации
CHUNK = 1024                 # Размер блока
RECORD_SECONDS = 10          # Длительность записи
OUTPUT_FILENAME = "voice.wav"  # Имя выходного файла

# Инициализация
audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

print("🎙️ Pls speak...")

frames = []

for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("✅ Recording complete.")

# Остановить и закрыть
stream.stop_stream()
stream.close()
audio.terminate()

# Сохранить в WAV файл
with wave.open(OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"📁 File saved as {OUTPUT_FILENAME}")

