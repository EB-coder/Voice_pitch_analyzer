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
import sys  # Добавлено для вывода в реальном времени

def record_audio():
    RATE = 44100
    CHANNELS = 1
    DTYPE = np.int16
    RECORD_SECONDS = 10
    OUTPUT_FILENAME = "voice.wav"

    print("🎙️ Recording started...", flush=True)  # flush для Streamlit
    
    try:
        audio = sd.rec(
            int(RECORD_SECONDS * RATE),
            samplerate=RATE,
            channels=CHANNELS,
            dtype=DTYPE
        )
        
        # Выводим прогресс в консоль
        for i in range(RECORD_SECONDS):
            print(f"⏱️ {i+1}/{RECORD_SECONDS} sec", flush=True)
            sd.sleep(1000)  # Используем встроенное ожидание sounddevice
        
        sd.wait()
        print("✅ Recording complete", flush=True)
        
        with wave.open(OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(2)
            wf.setframerate(RATE)
            wf.writeframes(audio.tobytes())
        
        print(f"📁 Saved to {OUTPUT_FILENAME}", flush=True)
        return True
    
    except Exception as e:
        print(f"❌ Error: {str(e)}", flush=True)
        return False

if __name__ == "__main__":
    record_audio()
