import streamlit as st
import time
from datetime import datetime, timedelta
from pathlib import Path
import base64

# Function to encode audio file to base64
def encode_file_to_base64(file_path):
    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return encoded

# Function to embed audio in HTML
def embed_audio(encoded_audio, audio_type="mp3", autoplay=False, loop=False):
    autoplay_attr = "autoplay" if autoplay else ""
    loop_attr = "loop" if loop else ""
    return f"""
    <audio {autoplay_attr} {loop_attr}>
        <source src="data:audio/{audio_type};base64,{encoded_audio}" type="audio/{audio_type}">
        Your browser does not support the audio element.
    </audio>
    """

# Streamlit App
def pomodoro_app():
    st.title("📚 Real-Time Pomodoro Timer with Background Music and Alarms")
    
    # Input for Pomodoro settings
    st.sidebar.header("Customize Your Timer")
    session_hours = st.sidebar.number_input("Total Study Session (hours):", min_value=1, max_value=12, value=1)
    study_time = st.sidebar.number_input("Study Time (minutes):", min_value=1, max_value=120, value=25)
    break_time = st.sidebar.number_input("Break Time (minutes):", min_value=1, max_value=60, value=5)
    
    # Convert total hours into cycles
    total_minutes = session_hours * 60
    cycle_time = study_time + break_time
    total_cycles = total_minutes // cycle_time
    
    st.sidebar.write(f"Estimated Cycles: {total_cycles}")
    
    # Load and encode audio files
    music_file = "trois-gymnopedie-gymnopedie-no-1-erik-satie-351s-12664.mp3"  # Ensure this file is in the same directory
    alarm_file = "mixkit-interface-hint-notification-911.mp3"       # Ensure this file is in the same directory
    
    music_encoded = ""
    alarm_encoded = ""
    
    if Path(music_file).is_file():
        music_encoded = encode_file_to_base64(music_file)
    else:
        st.sidebar.warning("Background music file not found.")
    
    if Path(alarm_file).is_file():
        alarm_encoded = encode_file_to_base64(alarm_file)
    else:
        st.sidebar.warning("Alarm sound file not found.")
    
    # Placeholders for audio
    music_placeholder = st.empty()
    alarm_placeholder = st.empty()
    
    # Timer button
    if st.button("Start Timer"):
        if not music_encoded:
            st.sidebar.error("Background music file is missing.")
            return
        if not alarm_encoded:
            st.sidebar.error("Alarm sound file is missing.")
            return
        
        st.success("Timer Started! Stay focused!")
        run_pomodoro(total_cycles, study_time, break_time, music_encoded, alarm_encoded, music_placeholder, alarm_placeholder)

# Pomodoro Timer Function
def run_pomodoro(cycles, study_time, break_time, music_encoded, alarm_encoded, music_placeholder, alarm_placeholder):
    for cycle in range(1, cycles + 1):
        # Study Phase
        st.markdown(f"### Cycle {cycle}/{cycles} - **Study for {study_time} minutes!**")
        
        # Start Background Music
        music_html = embed_audio(music_encoded, autoplay=True, loop=True)
        music_placeholder.markdown(music_html, unsafe_allow_html=True)
        
        # Countdown for Study Time
        countdown(study_time, phase="Study")
        
        # Stop Background Music by clearing the placeholder
        music_placeholder.empty()
        
        # Play Alarm Sound at end of Study Phase
        alarm_html = embed_audio(alarm_encoded, autoplay=True)
        alarm_placeholder.markdown(alarm_html, unsafe_allow_html=True)
        
        # Break Phase
        if cycle < cycles:
            st.markdown(f"### Cycle {cycle}/{cycles} - **Take a {break_time}-minute break.**")
            countdown(break_time, phase="Break")
            # Clear Alarm Sound after it plays
            time.sleep(2)  # Wait to ensure the alarm has time to play
            alarm_placeholder.empty()
        else:
            st.markdown("### **Session Complete! Great job!**")
            st.balloons()
            # Ensure the alarm plays at the end
            time.sleep(2)
            alarm_placeholder.empty()

# Countdown Timer Function
def countdown(duration_minutes, phase="Study"):
    timer_placeholder = st.empty()  # Placeholder for the timer
    end_time = datetime.now() + timedelta(minutes=duration_minutes)
    while True:
        remaining_time = end_time - datetime.now()
        if remaining_time.total_seconds() <= 0:
            break
        mins, secs = divmod(int(remaining_time.total_seconds()), 60)
        current_time = datetime.now().strftime("%H:%M:%S")
        # Update the timer in the placeholder
        timer_placeholder.markdown(f"🕒 Current Time: {current_time} | **⏳ Time Remaining: {mins:02d}:{secs:02d}**")
        time.sleep(1)
    timer_placeholder.empty()

# Run the app
if __name__ == "__main__":
    pomodoro_app()