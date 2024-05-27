# audio.py
# A small library for audio processing with lists

# Author: Rick Howell
# rick.howell.arts@gmail.com

import math

DEFAULT_FILENAME = 'audio.wav'
DEFAULT_SAMPLE_RATE = 44100
DEFAULT_BIT_DEPTH = 16

NUM_CHANNELS = 2


def sec2smp(seconds: int = 1, sample_rate: int = DEFAULT_SAMPLE_RATE) -> int:
    # Convert seconds to samples
    # sample_rate: int, sample rate of the audio data
    # seconds: int, number of seconds

    return round(sample_rate * seconds)


def bpm2sec(bpm: int = 120) -> float:
    # Convert beats per minute to seconds
    # bpm: int, beats per minute

    return 60 / bpm


def mono2stereo(data: list) -> list:
    # Convert mono audio data to stereo
    # data: list, mono audio data

    stereo_data = []
    for d in data:
        stereo_data.append(d)
        stereo_data.append(d)

    return stereo_data


def test_data() -> list:
    data = []
    length = sec2smp(seconds=2)
    hz = 400
    for i in range(0, length):
        f = math.sin(2 * math.pi * hz * i / DEFAULT_SAMPLE_RATE)
        if f < -1:
            f = -1
        elif f > 1:
            f = 1
        data.append(f)
    
    return data


def hard_clip(data: list, threshold: float) -> list:
    # Hard clip the audio data
    # data: list of floats
    # threshold: float, threshold for clipping

    clipped_data = []
    for d in data:
        if d > threshold:
            clipped_data.append(threshold)
        elif d < -threshold:
            clipped_data.append(-threshold)
        else:
            clipped_data.append(d)

    return clipped_data


def hpf(data: list, cutoff: float = 1000) -> list:
    # Apply a high-pass filter to the audio data
    # data: list of floats
    # cutoff: float, cutoff frequency in Hz

    # The filter is a simple first-order high-pass filter
    # y[n] = x[n] - x[n-1] + a * y[n-1]

    a = math.exp(-2 * math.pi * cutoff / DEFAULT_SAMPLE_RATE)

    filtered_data = [data[0]]
    for i in range(1, len(data)):
        filtered_data.append(data[i] - data[i - 1] + a * filtered_data[i - 1])

    return filtered_data


def floats2bytes(data: list, bit_depth: int = DEFAULT_BIT_DEPTH) -> bytes:
    # Convert a list of floats in [-1, 1] to a list of bytes
    # data: list of floats
    # bit_depth: int, bit depth of the audio data

    # Make sure the floats are in the correct range
    data = hard_clip(data, 1.0)

    # The maximum value of the audio data with one bit reserved for the sign
    max_val = 2 ** (bit_depth - 1) - 1

    # Convert the floats to ints
    data = [int(d * max_val) for d in data]

    # Convert the integers to bytes
    data = [d.to_bytes(bit_depth // 8, 'little', signed=True) for d in data]

    return data


def mkhdr(data: list, sample_rate: int = DEFAULT_SAMPLE_RATE, bit_depth: int = DEFAULT_BIT_DEPTH) -> bytes:

    # The header is 44 bytes long

    # RIFF header
    riff = b'RIFF'

    # File size in bytes. 32-bit integer
    filesize = len(data) + 36
    filesize = filesize.to_bytes(4, 'little')

    # WAVE header
    wave = b'WAVE'

    # fmt header
    fmt = b'fmt '
    fmt_size = (16).to_bytes(4, 'little')
    audio_format = (1).to_bytes(2, 'little')
    num_channels = (2).to_bytes(2, 'little')

    # Sample rate
    sr = sample_rate.to_bytes(4, 'little')

    # Byte rate
    byte_rate = (sample_rate * bit_depth * NUM_CHANNELS // 8).to_bytes(4, 'little')

    # Block align
    block_align = (bit_depth * NUM_CHANNELS // 8).to_bytes(2, 'little')

    # Bits per sample
    bits_per_sample = bit_depth.to_bytes(2, 'little')

    # data header
    data_header = b'data'

    # data size
    data_size = len(data).to_bytes(4, 'little')

    # Concatenate all the header data
    header = riff + filesize + wave + fmt + fmt_size + audio_format + num_channels + sr + byte_rate + block_align + bits_per_sample + data_header + data_size

    return header


def write_audio_file(data: list, filename: str = DEFAULT_FILENAME, sample_rate: int = DEFAULT_SAMPLE_RATE, bit_depth: int = DEFAULT_BIT_DEPTH, mono: bool = False) -> None:
    '''Input a list of floats in [-1, 1], and write to a .wav file'''

    if mono:
        data = mono2stereo(data)

    data = hard_clip(data, 1.0)

    # Convert the data to bytes
    data = floats2bytes(data, bit_depth)

    with open(filename, 'wb') as f:
        f.write(mkhdr(data, sample_rate, bit_depth))
        for d in data:
            f.write(d)


def main():
    data = test_data()
    write_audio_file(data, mono=True)

    print('Done!')


if __name__ == '__main__':
    main()