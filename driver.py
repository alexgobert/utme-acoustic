from audio_utils import run_threads
from arduino_controller import create_commands, connect_arduino, rotate
from contextlib import closing

# default serial settings
PORT = 'COM7'
BAUD = 9600

def main(play_file: str, rec_dir: str, angleStep: int):
    commands, batch_size = create_commands(angleStep)

    with closing(connect_arduino(PORT, BAUD)) as arduino:
        for idx, (sleepTime, command) in enumerate(commands):
            # only execute audio if done rotating
            if idx % batch_size == 0:
                run_threads(play_file, rec_dir)
            
            rotate(sleepTime, command, arduino)

        print('test complete')