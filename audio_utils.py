from pyaudio import paInt16, PyAudio
from wave import open as wave_open
from threading import Thread
from mutagen.mp3 import MP3
from datetime import datetime
from time import sleep
from audioop import rms
from numpy import log10
from queue import Queue
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide' # hide welcome
from pygame import mixer

# Set up Pygame mixer
mixer.init()

# Define variables for microphone recording
sample_rate = 44100
chunk = 1024

def checkVolume(queue: Queue, loudness_threshold: float = 60):
    '''
    Intended for use in a Thread. Determines whether or not a loud sound is detected from the microphone, like the beep of a turntable. Stores a boolean result in a Queue. The result is True if a loud sound is detected, False otherwise.

    Parameters
    ----------
    queue : Queue
        An instance of the Queue class. Used to store result
    loudness_threshold : float, optional
        Loudness threshold used to determine whether a sound is too loud in decibels. Defaults at 60 dB.
    '''

    beepDetected = False
    db = lambda x: 20 * log10(x) if x > 0 else 0

    audio_recorder = PyAudio()
    audio_stream = audio_recorder.open(
        format=paInt16, 
        channels=1,
        rate=sample_rate, 
        input=True,
        frames_per_buffer=chunk
    )
    
    for _ in range(sample_rate // chunk * 4):
        audio_data = audio_stream.read(chunk)
        loudness = db(abs(rms(audio_data, 2)))

        if loudness > loudness_threshold:
            beepDetected = True
            break
    
    audio_stream.stop_stream()
    audio_stream.close()
    audio_recorder.terminate()
    
    queue.put(beepDetected)

# Define a function to play an audio file
def play_audio(audio_file: str):
    '''
    Plays audio through default speaker

    Parameters
    ----------
    audio_file : str
        Audio file to play
    '''
    sleep(1)
    
    mixer.music.load(audio_file)
    mixer.music.play()

# Define a function to record audio from the microphone
def record_audio(audio_filename: str, audio_length: int, audio_path: str):
    '''
    Records audio from default microphone

    Parameters
    ----------
    audio_filename : str
        Filename to record to
    audio_length : int
        Length of recording
    audio_path : str
        Directory to save recorded file to
    '''
    audio_format = paInt16
    channels = 1
    
    audio_recorder = PyAudio()
    audio_stream = audio_recorder.open(
        format=audio_format, 
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk
    )
    
    audio_buffer = (
        audio_stream.read(chunk)
        for _ in range(sample_rate // chunk * audio_length)
    )
    
    # Save the audio recording to a WAV file in the specified path
    audio_file_path = f'{audio_path}/{audio_filename}'
    with wave_open(audio_file_path, 'wb') as audio_file:
        audio_file.setnchannels(channels)
        audio_file.setsampwidth(audio_recorder.get_sample_size(audio_format))
        audio_file.setframerate(sample_rate)
        audio_file.writeframes(b''.join(audio_buffer))
    
    audio_stream.stop_stream()
    audio_stream.close()
    audio_recorder.terminate()

def run_threads(audio_file: str, audio_path: str):
    '''
    Runs playback and recording threads

    Parameters
    ----------
    audio_file : str
        Audio file to play
    audio_path : str
        Directory to store recorded file
    '''
    # Get the length of the audio file
    audio_length = int(MP3(audio_file).info.length)

    curTime = int(datetime.now().timestamp())
    
    # Define threads for playing audio and recording from the microphone
    play_audio_thread = Thread(target=play_audio, args=(audio_file,))
    record_audio_thread = Thread(target=record_audio, args=(f"audio-{curTime}.wav", audio_length+1, audio_path))

    sleep(1)

    # Start the threads
    play_audio_thread.start()
    record_audio_thread.start()
    
    # Wait for both threads to finish
    play_audio_thread.join()
    record_audio_thread.join()

    print('done playing')

if __name__ == '__main__':
    audio_file = "01-White-Noise-10sec.mp3" # replace with the filename of the MP3 file passed from your GUI
    audio_path = "." # replace with the path where the WAV file should be saved
    run_threads(audio_file, audio_path)
