from audio_utils import run_threads
from arduino_controller import create_commands, connect_arduino, rotate, minimizeSpeed, BUTTON_DELAY
from contextlib import closing
from time import sleep

# default serial settings
PORT = 'COM7'
BAUD = 115200

def main(play_file: str, rec_dir: str, angleStep: int, port = PORT, baud = BAUD):
    # sleep(10); # give user time to exit chamber
    commands, batch_size = create_commands(angleStep)

    with closing(connect_arduino(port, baud)) as arduino:
        minimizeSpeed(arduino)
        for idx, (sleepTime, command) in enumerate(commands):
            # only execute audio if done rotating
            if idx % batch_size == 0:
                run_threads(play_file, rec_dir)
            
            rotate(sleepTime, command, arduino)

    print('test complete')


def rotate_only(angleStep: int, port = PORT, baud = BAUD):
    commands, _ = create_commands(angleStep)

    with closing(connect_arduino(port, baud)) as arduino:
        minimizeSpeed(arduino)
        for sleepTime, command in commands:
            sleep(max(0, BUTTON_DELAY - sleepTime))
            rotate(sleepTime, command, arduino)
            

    print('test complete')


if __name__ == '__main__':
    rotate_only(30)