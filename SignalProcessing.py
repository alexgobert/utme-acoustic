import numpy as np
from acoustics._signal import Signal
from data_processing import get_filenames_in_order
import matplotlib.pyplot as plt

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


def main(angleStep: int):
    directory_path = 'test_results'
    directory_path = 'test1-30'
    files = get_filenames_in_order(directory_path, 360 // angleStep)

    # read WAV file and perform A weighting
    raw_data = [
        fft_process(Signal.from_wav(f'{directory_path}/{file}').weigh())
        for file in files
    ]

    FREQ = 12000

    data = np.fromiter((10*np.log10(angle[FREQ]) for angle in raw_data), float)
    data -= np.max(data)

    theta = np.arange(0, 360, angleStep) * np.pi / 180

    plt.polar(theta, data, marker='.')
    plt.title(f'Beam Pattern of Receiver at {FREQ:,} Hz')
    plt.show()


def plotMain():
    directory_path = 'test_results'
    files = get_filenames_in_order(directory_path)

    for file in files:
        data = fft_process(Signal.from_wav(f'{directory_path}/{file}').weigh(), True)

        plt.plot(data)
        plt.show()


if __name__ == '__main__':
    main(30)
    # plotMain()