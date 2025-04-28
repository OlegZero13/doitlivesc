import numpy as np
from pvrecorder import PvRecorder
import wave

def record_audio(filename, duration):
    # Create an instance of PvRecorder
    recorder = PvRecorder(device_index=-1, frame_length=512)  # Use -1 for default microphone
    recorder.start()

    print("Recording...")
    frames = []
    
    for _ in range(int(duration * 1000 / 32)):  # 32 ms per frame (16 kHz)
        frame = recorder.read()
        frames.append(frame)

    recorder.stop()
    print("Finished recording.")

    audio_data = np.concatenate(frames).astype(np.int16)
    audio_bytes = audio_data.tobytes()

    # Save the recorded audio as a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)  # Mono audio
        wf.setsampwidth(2)  # 16 bits per sample
        wf.setframerate(16000)  # Sample rate
        wf.writeframes(audio_bytes)

# Record audio for a specific duration (in seconds)
record_audio("videos/microphone_recording.wav", 3)  # Adjust duration as needed
