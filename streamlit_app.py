import streamlit as st
import os
import wave
import numpy as np
from scipy.fft import fft
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import subprocess
from fpdf import FPDF
import yagmail
from dotenv import load_dotenv
import time  # Добавьте эту строку

load_dotenv()  # загрузка переменных из .env

# Настройки email
SENDER_EMAIL = os.getenv("EMAIL_USER")
SENDER_PASS = os.getenv("EMAIL_PASS")


st.title("🎤 Voice Pitch Analyzer")
st.markdown("Measure and visualize your voice pitch (fundamental frequency).")

st.markdown("## 🗣 Choose a Phrase to Read")
phrase_level = st.selectbox("Select difficulty level", ["Simple", "Intermediate", "Advanced", "Technical"])

phrases = {
    "Simple": "Hello, my name is [   ]. I am testing my voice pitch using this app.",
    "Intermediate": "Good morning! I’m using the Voice Pitch Analyzer to check the tone and frequency of my voice. Let’s see the results!",
    "Advanced": "Hi there! This is a short test to measure the pitch and quality of my voice using the Voice Pitch Analyzer. I’m curious to know if my voice falls into the low, mid, or high frequency range.",
    "Technical": "This is a voice pitch analysis. The goal is to evaluate the frequency of my speech and categorize it accordingly. This test will help identify whether my voice is considered low, medium, or high pitched."
}

selected_phrase = phrases[phrase_level]
st.info(f"📖 **Read this phrase aloud:**\n\n*{selected_phrase}*")



# Кнопка записи
# if st.button("🔴 Record voice (10 seconds)"):
#     with st.spinner("Recording..."):
#         subprocess.run(["python", "record_audio.py"])
#     st.success("✅ Voice recorded!")

if st.button("🔴 Record voice (10 seconds)"):
    with st.spinner("Recording... Please speak now"):
        # Создаем элементы интерфейса
        status_text = st.empty()
        progress_bar = st.progress(0)
        
        # Запускаем запись в фоне
        process = subprocess.Popen(["python", "record_audio.py"])
        
        # Отображаем прогресс
        for i in range(10):
            time.sleep(1)
            progress_bar.progress((i + 1) / 10)
            status_text.text(f"Recording... {i+1}/10 seconds")
        
        # Дожидаемся завершения
        process.wait()
    
    # Проверяем результат
    if os.path.exists("voice.wav"):
        st.success("✅ Voice recorded!")
        st.audio("voice.wav", format='audio/wav')
    else:
        st.error("❌ Recording failed - no audio file created")

# Анализ
if os.path.exists("voice.wav"):
    st.audio("voice.wav", format='audio/wav')

    wf = wave.open("voice.wav", 'rb')
    framerate = wf.getframerate()
    frames = wf.readframes(wf.getnframes())
    wf.close()

    audio = np.frombuffer(frames, dtype=np.int16)
    audio = audio / np.max(np.abs(audio))

    WINDOW_SIZE = 2048
    HOP_SIZE = 512
    pitches = []
    times = []

    for i in range(0, len(audio) - WINDOW_SIZE, HOP_SIZE):
        window = audio[i:i + WINDOW_SIZE]
        fft_spectrum = np.abs(fft(window))[:WINDOW_SIZE // 2]
        freqs = np.fft.fftfreq(WINDOW_SIZE, d=1.0 / framerate)[:WINDOW_SIZE // 2]
        peaks, _ = find_peaks(fft_spectrum, height=0.1)

        if len(peaks) > 0:
            pitches.append(freqs[peaks[0]])
        else:
            pitches.append(0)

        times.append(i / framerate)

    cleaned = [p for p in pitches if 50 < p < 1000]
    mean_pitch = np.mean(cleaned)
    max_pitch = np.max(cleaned)
    min_pitch = np.min(cleaned)
    std_pitch = np.std(cleaned)

    def classify_pitch(pitch_hz):
        if pitch_hz < 85:
            return "Very Low Voice (Bass)"
        elif pitch_hz < 165:
            return "Low Voice (Male range)"
        elif pitch_hz < 255:
            return "Medium Voice (Female/Child range)"
        else:
            return "High Voice (Falsetto/Special speech)"

    st.markdown("### 📊 Analysis Results:")
    st.write(f"**Average Pitch**: {mean_pitch:.2f} Hz")
    st.write(f"**Maximum Pitch**: {max_pitch:.2f} Hz")
    st.write(f"**Minimum Pitch**: {min_pitch:.2f} Hz")
    st.write(f"**Standard Deviation**: {std_pitch:.2f} Hz")

    st.markdown("### 🎯 Visual Indicator")
    st.progress(min(mean_pitch / 400, 1.0))
    st.write("🟣 Pitch within vocal range")

    voice_type = classify_pitch(mean_pitch)
    st.markdown(f"### 🧠 Voice Type: **{voice_type}**")

    st.markdown("### 📈 Pitch Graph")
    fig, ax = plt.subplots()
    ax.plot(times, pitches, color='purple')
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Pitch (Hz)")
    ax.set_title("Pitch Analysis")
    ax.grid(True)
    st.pyplot(fig)

    # Генерация PDF
    if st.button("📄 Generate PDF Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, txt="Voice Pitch Report", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", "", 12)
        pdf.cell(200, 10, txt=f"Average Pitch: {mean_pitch:.2f} Hz", ln=True)
        pdf.cell(200, 10, txt=f"Maximum Pitch: {max_pitch:.2f} Hz", ln=True)
        pdf.cell(200, 10, txt=f"Minimum Pitch: {min_pitch:.2f} Hz", ln=True)
        pdf.cell(200, 10, txt=f"Standard Deviation: {std_pitch:.2f} Hz", ln=True)
        pdf.cell(200, 10, txt=f"Voice Type: {voice_type}", ln=True)

        output_path = "pitch_report.pdf"
        pdf.output(output_path)
        st.success("📄 PDF report generated!")
        with open(output_path, "rb") as f:
            st.download_button("⬇️ Download PDF", f, file_name="voice_pitch_report.pdf")

    # Отправка по Email
    if os.path.exists("pitch_report.pdf"):
        st.markdown("### ✉️ Send PDF Report via Email")
        recipient_email = st.text_input("Enter recipient email address")

        if st.button("📤 Send Email"):
            if recipient_email and SENDER_EMAIL and SENDER_PASS:
                try:
                    yag = yagmail.SMTP(user=SENDER_EMAIL, password=SENDER_PASS)
                    yag.send(
                        to=recipient_email,
                        subject="Voice Pitch Report 📄",
                        contents="Hello, I hope this message finds you well.<br>" \
                        " Attached to this email is the PDF report for the “Voice Pitch Analyzer”<br>" \
                        " This report includes the results of the analysis.<br>" \
                        "Please let me know if you have any questions or need any additional information.<br>" \
                        "Best regards,",
                        attachments="pitch_report.pdf"
                    )
                    st.success(f"✅ Email sent to {recipient_email}")
                except Exception as e:
                    st.error(f"❌ Failed to send email: {e}")
            else:
                st.warning("⚠️ Please enter email and ensure credentials are set in .env")

