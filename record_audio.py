import sounddevice as sd
import numpy as np
import wave
import sys
from datetime import datetime

def record_audio(filename="voice.wav", duration=10, sample_rate=44100):
    print(f"🎤 Starting recording for {duration} seconds...", flush=True)
    
    try:
        # Записываем аудио
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype=np.int16
        )
        
        # Выводим прогресс в консоль
        for i in range(duration):
            print(f"⏳ {i+1}/{duration} seconds recorded", flush=True)
            sd.sleep(1000)  # Ждем 1 секунду
        
        sd.wait()  # Ожидаем завершения записи
        
        # Сохраняем в файл
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(recording.tobytes())
        
        print(f"✅ Successfully saved to {filename}", flush=True)
        return True
    
    except Exception as e:
        print(f"❌ Error during recording: {str(e)}", flush=True)
        return False

if __name__ == "__main__":
    record_audio()
