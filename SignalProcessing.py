import numpy as np
from acoustics._signal import Signal
import matplotlib.pyplot as plt
from os import listdir
from datetime import datetime
from threading import Thread

NDArray = np.ndarray

def fft_process(signal: Signal, plot=False) -> NDArray:
    '''
    Function for performing an FFT on a .WAV file. Because FFTs are symmetric, this function discards the second half of the FFT and doubles the magnitude of the first half to preserve the energy of the wave. The DC offset and the Nyquist point are unique, and are therefore not doubled.

    Parameters
    ---------
    signal : Signal
        Instance of Signal class, contains .WAV data
    
    plot : bool, optional
        If true, plots data as Power (dB) vs Frequency (kHz)

    Returns
    -------
    data : NDArray[Floating]
        NDArray of the FFT'ed data. There is a one-to-one correlation between array index and frequency.
    '''

    n = signal.samples
    p = np.fft.fft(signal.values)

    nUniquePts = int(np.ceil((n+1)/2.0))

    p = (np.abs(p[:nUniquePts]) / float(n)) ** 2

    # multiply by 2 bc cut of half of data
    # DC and Nyquist should not be scaled
    end = nUniquePts - (n % 2 == 0) # -1 if even, 0 if odd
    p[1:end] *= 2

    if plot:
        freqArray = np.arange(nUniquePts) * (signal.fs / n)

        plt.plot(freqArray/1000, 10*np.log10(p))
        plt.xlabel('Frequency (kHz)')
        plt.ylabel('Power (dB)')
        plt.show()

    return p


def process_files(angleStep: int, freq: int, dir_path: str = 'test_results', raw_data: NDArray = None) -> NDArray:
    '''
    Process and plot test results on a polar plot. Returns processed data intended for storage to use in future computations.

    Parameters
    ---------
    angleStep : int
        Angle increment at which data was gathered
    freq : int
        Frequency at which to plot
    dir_path : str, optional
        Directory that contains the files to plot. Defaults to 'test_results'
    raw_data : NDArray, optional
        NDArray of FFT'ed data. If provided, skips computing another FFT

    Returns
    -------
    raw_data : NDArray
        Array of FFT'ed data. Can store to reduce computational repetitiveness.
    '''
    if raw_data == None:
        files = get_filenames_in_order(dir_path, 360 // angleStep)

        # read WAV file and perform A weighting
        raw_data = [
            fft_process(Signal.from_wav(f'{dir_path}/{file}').weigh())
            for file in files
        ]

    data = np.fromiter((10*np.log10(angle[freq]) for angle in raw_data), float) # convert to decibels
    data -= np.max(data)
    data = np.append(data, data[0]) # connect first and last points

    plot_polar(data, angleStep, freq)

    return raw_data


def plot_polar(r: NDArray, angleStep: int, freq: int):
    '''
    Plots data on a polar plot.

    Parameters
    ----------
    r : NDArray
        Radial data to plot
    angleStep : int
        Angle increment at which data was gathered
    freq : int
        Frequency at which to plot
    '''
    # need extra point to connect first and last points
    theta = np.arange(0, 360+angleStep, angleStep) * np.pi / 180

    plot, = plt.polar(theta, r, marker='.')
    plot.set_label(f'{freq:,} Hz')

    plt.legend(loc='upper left', bbox_to_anchor=(-0.3, 1))
    plt.title(f'Beam Pattern of Receiver at {angleStep}$\degree$ Increments in Decibels')
    plt.show(block=False)


def plotMain():
    directory_path = 'test_results'
    files = get_filenames_in_order(directory_path)

    for file in files:
        data = fft_process(Signal.from_wav(f'{directory_path}/{file}').weigh(), True)

        plt.plot(data)
        plt.show()


def get_filenames_in_order(directory: str, limit=None) -> list:
    '''
    Gets list of filenames sorted in chronological order.

    Parameters
    ----------
    directory : str
        Directory from which to get files
    limit : int, optional
        Optional, number of files to return

    Returns
    -------
    List that contains filesnames sorted in chronological order, with a limit if given.
    '''
    filenames = listdir(directory)
    timestamps = []
    for filename in filenames:
        timestamp_str = filename.split('-')[-1].split('.')[0]
        timestamp = datetime.fromtimestamp(int(timestamp_str))
        timestamps.append((timestamp, filename))
    
    files = [filename for _, filename in sorted(timestamps)]
    return files[:limit] if limit else files


if __name__ == '__main__':
    process_files(30, 8000, 'test2-30')
    # plotMain()