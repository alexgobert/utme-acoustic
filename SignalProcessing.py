import numpy as np
from acoustics._signal import Signal
from data_processing import get_filenames_in_order
import matplotlib.pyplot as plt


def example(signal: Signal, plot=False):
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
    directory_path = 'test1-30'
    directory_path = 'test_results'
    files = get_filenames_in_order(directory_path, 360 // angleStep)

    # Loop over each WAV file and extract the SPL data
    # data = []
    # for file in files:

    #     # Read the WAV file and extract the data
    #     signal = Signal.from_wav(f'{directory_path}/{file}').weigh()

    #     data.append(example(signal, plot=False))
    # replaced above with list comp
    raw_data = [
        example(Signal.from_wav(f'{directory_path}/{file}').weigh())
        for file in files
    ]

    FREQ = 12000
    data = np.array([angle[FREQ] for angle in raw_data])
    data = 20 * np.log10(data)
    # data = [(20*np.log10(angle[FREQ])) for angle in raw_data]
    data /= np.min(data)
    theta = np.arange(0, 360, angleStep) * np.pi / 180
    print(list(theta))
    print(data)
    plt.polar(theta, data, marker='.')
    plt.show()


def plotMain():
    directory_path = 'test_results'
    files = get_filenames_in_order(directory_path)

    for file in files:
        data = example(Signal.from_wav(f'{directory_path}/{file}').weigh(), True)

        plt.plot(data)
        plt.show()


if __name__ == '__main__':
    main(30)
    # plotMain()