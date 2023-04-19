from audio_utils import run_threads
from arduino_controller import create_commands, connect_arduino, sendCommand, setupTurntable, BUTTON_DELAY
from contextlib import closing
from time import sleep
from SignalProcessing import process_files

# default serial settings
BAUD = 115200

def main(play_file: str, rec_dir: str, angleStep: int, freq: int, port: str, baud = BAUD):
    '''
    Main driver that handles rotation, audio playback, audio recording, and plotting results.

    Parameters
    ----------
    play_file : str
        Path to file to send to speaker
    rec_dir : str
        Path to directory to store recorded data
    angleStep : int
        Angle increment in degrees
    freq : int
        Frequency to plot in Hz
    port : str
        Serial port that Arduino is connected to
    baud : str, optional
        Baud rate of Arduino Serial connection. This is always set to 115,200
    '''
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


def rotate_only(angleStep: int, port: str, baud = BAUD):
    '''
    Debug function that only performs the rotation component of the test.
    
    Parameters
    ----------
    angleStep : int
        Angle increment in degrees
    port : str
        Serial port that Arduino is connected to
    baud : str, optional
        Baud rate of Arduino Serial connection. This is always set to 115,200
    '''
    commands, _ = create_commands(angleStep)

    with closing(connect_arduino(port, baud)) as arduino:
        setupTurntable(arduino)
        for sleepTime, command in commands:
            # sleep(max(0, BUTTON_DELAY - sleepTime))
            sendCommand(sleepTime, command, arduino)
            

    print('test complete')


if __name__ == '__main__':
    rotate_only(1, 'COM7')
