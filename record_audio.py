import sounddevice as sd
import numpy as np
import wave
import sys

def record_audio():
    RATE = 44100
    CHANNELS = 1
    DTYPE = np.int16
    RECORD_SECONDS = 10
    OUTPUT_FILENAME = "voice.wav"

    print("🎙️ Recording started...", flush=True)
    
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
