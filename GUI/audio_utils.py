import pyaudio
import wave
import pygame
import threading
from mutagen.mp3 import MP3
from datetime import datetime
from time import sleep

# Test comment

# Set up Pygame mixer
pygame.mixer.init()

# Define variables for microphone recording
sample_rate = 44100
chunk = 1024

# Define a function to play an audio file
def play_audio(audio_file):
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

# Define a function to record audio from the microphone
def record_audio(audio_filename, audio_length, audio_path):
    audio_format = pyaudio.paInt16
    channels = 1
    audio_buffer = []
    
    audio_recorder = pyaudio.PyAudio()
    audio_stream = audio_recorder.open(format=audio_format, channels=channels,
                                        rate=sample_rate, input=True,
                                        frames_per_buffer=chunk)
    
    for i in range(int(sample_rate / chunk * audio_length)):
        audio_data = audio_stream.read(chunk)
        audio_buffer.append(audio_data)
    
    audio_stream.stop_stream()
    audio_stream.close()
    audio_recorder.terminate()
    
    # Save the audio recording to a WAV file in the specified path
    audio_file_path = audio_path + "/" + audio_filename
    audio_file = wave.open(audio_file_path, 'wb')
    audio_file.setnchannels(channels)
    audio_file.setsampwidth(audio_recorder.get_sample_size(audio_format))
    audio_file.setframerate(sample_rate)
    audio_file.writeframes(b''.join(audio_buffer))
    audio_file.close()

def run_threads(audio_file, audio_path):
    # Get the length of the audio file
    audio_length = int(MP3(audio_file).info.length)

    curTime = int(datetime.now().timestamp())
    
    # Define threads for playing audio and recording from the microphone
    play_audio_thread = threading.Thread(target=play_audio, args=(audio_file,))
    record_audio_thread = threading.Thread(target=record_audio, args=(f"audio-{curTime}.wav", audio_length, audio_path))

    sleep(1)

    # Start the threads
    play_audio_thread.start()
    record_audio_thread.start()
    
    # Wait for both threads to finish
    play_audio_thread.join()
    record_audio_thread.join()

    print('done')

if __name__ == '__main__':
    audio_file = "example.mp3" # replace with the filename of the MP3 file passed from your GUI
    audio_path = "/path/to/save/wav/file" # replace with the path where the WAV file should be saved
    run_threads(audio_file, audio_path)
