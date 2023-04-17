from audio_utils import run_threads
from arduino_controller import create_commands, connect_arduino, sendCommand, setupTurntable, BUTTON_DELAY
from contextlib import closing
from time import sleep
from SignalProcessing import process_files

# default serial settings
BAUD = 115200

def main(play_file: str, rec_dir: str, angleStep: int, freq: int, port: str, baud = BAUD):
    commands, batch_size = create_commands(angleStep)

    with closing(connect_arduino(port, baud)) as arduino:
        setupTurntable(arduino)
        for idx, (sleepTime, command) in enumerate(commands):
            # only execute audio if done rotating
            if idx % batch_size == 0:
                run_threads(play_file, rec_dir)
            
            sendCommand(sleepTime, command, arduino)

    print('test complete, beginning processing')
    process_files(angleStep, freq)


def rotate_only(angleStep: int, port = PORT, baud = BAUD):
    commands, _ = create_commands(angleStep)

    with closing(connect_arduino(port, baud)) as arduino:
        setupTurntable(arduino)
        for sleepTime, command in commands:
            sleep(max(0, BUTTON_DELAY - sleepTime))
            sendCommand(sleepTime, command, arduino)
            

    print('test complete')


def process_only(angleStep: int, rec_dir: str):
    pass


if __name__ == '__main__':
    rotate_only(30)