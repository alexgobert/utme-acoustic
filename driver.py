from audio_utils import run_threads
from arduino_controller import create_commands, connect_arduino, rotate
from wave import open
from contextlib import closing
from threading import Thread

# default serial settings
PORT = 'COM7'
BAUD = 9600

def main(play_file: str, rec_dir: str, angleStep: int):
    # recordDelay = get_wav_duration(play_file) + 1.25

    commands, batch_size = create_commands(angleStep)

    with closing(connect_arduino(PORT, BAUD)) as arduino:

        for idx, (sleepTime, command) in enumerate(commands):
            # only execute audio if done rotating
            if idx % batch_size == 0:
                run_threads(play_file, rec_dir)
            
            rotate(sleepTime, command, arduino)

        print('test complete')


def get_wav_duration(filename: str) -> float:
    duration = -1
    with closing(open(filename, 'r')) as f:
        frames = f.getnframes()
        rate = float(f.getframerate())

        duration = frames / rate

    return duration