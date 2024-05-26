# PNG Encoder using only the Python Standard Library
# Designed to be simple and easy to use

# Author: Rick Howell
# rick.howell.arts@gmail.com

import math
import time
import zlib
from abc import abstractmethod, ABC
from enum import Enum

def angle2rgb(angle: float, bit_depth: int = 255) -> tuple:
    """Angle should be in radians from -pi to pi. \n
    Note: for vectors in R2, math.atan2(y, x) will give the angle."""

    if angle < -math.pi:
        angle = -math.pi
    elif angle > math.pi:
        angle = math.pi

    x = (angle + math.pi) / (2 * math.pi)

    r = int(bit_depth * ((1.0 + math.cos(2 * math.pi * x)) / 2.0))
    g = int(bit_depth * ((1.0 + math.cos(2 * math.pi * (x - 1/3))) / 2.0))
    b = int(bit_depth * ((1.0 + math.cos(2 * math.pi * (x - 2/3))) / 2.0))

    return (r, g, b)

class Color(Enum):
    GRAYSCALE = 0
    RGB = 2

class _pngEncoder(ABC):

    def __init__(self, filename: str, data: list, depth: int = 8, color_type: Enum = Color.GRAYSCALE, compression: bool = False):
    
            # Data Validation
            # TODO: Add more data validation that doesn't increase time complexity too much

            if depth not in [8, 16]:
                raise ValueError('Invalid depth. Must be 8, or 16.')
            
            if filename[-4:] != '.png':
                raise ValueError('Filename must _end with .png')
            
            # Initialize Variables
            self.depth = depth
            self.color_type = color_type.value
            self.color_type_str = color_type.name
            self.filename = filename
            self.data = data
            self.width = len(data[0])
            self.height = len(data)

            if compression:
                self.compression = zlib.Z_BEST_COMPRESSION
            else:
                self.compression = zlib.Z_NO_COMPRESSION

    def __del__(self):
        self.file.close()

    def __str__(self) -> str:
        return f'PNG Encoder: {self.filename}, {self.width} x {self.height}, {self.depth} bit, {self.color_type_str}'

    def _crc32(self, data: bytes):
        return zlib.crc32(data) & 0xffffffff
    
    def _write_chunk(self, chunk_type: str, data: bytes):
        self.file.write(len(data).to_bytes(4, 'big'))
        self.file.write(chunk_type.encode())
        self.file.write(data)
        self.file.write(self._crc32(chunk_type.encode() + data).to_bytes(4, 'big'))

    def _signature(self):
        self.file.write(b'\x89PNG\r\n\x1a\n')

    def _header(self):
        width = self.width.to_bytes(4, 'big')
        height = self.height.to_bytes(4, 'big')
        bit_depth = b'\x08' if self.depth == 8 else b'\x10'
        color_type = self.color_type.to_bytes(1, 'big')
        compression = b'\x00'
        filter_method = b'\x00'
        interlace = b'\x00'

        self._write_chunk('IHDR', width + height + bit_depth + color_type + compression + filter_method + interlace)

    @abstractmethod
    def _imdata(self):
        pass

    def _end(self):
        self._write_chunk('IEND', b'')
        self.file.close()

    def make(self):
        print(f'Making {self.filename}...')
        start_time = time.time()
        self.file = open(self.filename, 'wb')
        self._signature()
        self._header()
        self._imdata()
        self._end()
        print(f'Finished cooking in {time.time() - start_time} seconds.')


class Grayscale(_pngEncoder):

    """
    Creates a grayscale PNG image from a list of pixel values. \n

    Parameters: \n
        filename - The name of the file to be created. Must _end with .png \n
        data - A list of lists containing the pixel values. Each value must be a non-negative integer less than 2^depth - 1. \n
        depth - The bit depth of the image. Must be 8 or 16. \n

    Example: \n
        data = [
            [0, 196, 0],
            [0, 0, 255],
            [128, 196, 255]
        ]
        Will output a 3 x 3 grayscale image with the pixel values given.
        Note the default depth is 8, so the highest value we can utilize is 2^8 - 1.
    """

    def __init__(self, filename: str, data: list, depth: int = 8, compression: bool = False):
        super().__init__(filename, data, depth = depth, color_type = Color.GRAYSCALE, compression = compression)

    def _imdata(self):
        if self.depth == 8:
            byte_size = 1
        else:
            byte_size = 2

        data = b''
        for row in self.data:
                data += b'\x00' + b''.join([x.to_bytes(byte_size, 'big') for x in row])
        
        self._write_chunk('IDAT', zlib.compress(data, level = self.compression, wbits = zlib.MAX_WBITS))

class RGB(_pngEncoder):
    """
    Creates an RGB PNG image from a list of pixel values. \n

    Parameters: \n
        filename - The name of the file to be created. Must _end with .png \n
        data - A list of lists containing pixel tuples (r, g, b). Each value in the tuple must be a non-negative integer less than 2^depth - 1. \n
        depth - The bit depth of the image. Must be 8 or 16. \n

    Example: \n
        data = [
            [(0, 196, 0), (0, 0, 255), (128, 196, 255)],
            [(255, 0, 0), (0, 255, 0), (0, 0, 0)]
        ]
        Will output a 2 x 3 RGB image with the pixel values given.
    """

    def __init__(self, filename: str, data: list, depth: int = 8, compression: bool = False):
        super().__init__(filename, data, depth = depth, color_type = Color.RGB, compression = compression)

    def _imdata(self):
        if self.depth == 8:
            byte_size = 1
        else:
            byte_size = 2

        data = b''
        for row in self.data:
            row_data = b'\x00'
            for col in row:
                r, g, b = col
                row_data += r.to_bytes(byte_size, 'big') + g.to_bytes(byte_size, 'big') + b.to_bytes(byte_size, 'big')
            data += row_data

        self._write_chunk('IDAT', zlib.compress(data, level = self.compression, wbits = zlib.MAX_WBITS))


def test_gray(depth: int = 8):
    width = 256
    height = 256
    max_value = 2**depth - 1
    test_data = []

    for y in range(height):
        row = []
        for x in range(width):
            val = max_value * (x / width)
            val = min(int(val), max_value)
            row.append(val)
        test_data.append(row)

    Grayscale('testg.png', test_data, depth = depth).make()

def test_rgb(depth: int = 8):
    width = 204
    height = 204
    max_value = 2**depth - 1
    test_data = []

    for y in range(height):
        row = []
        for x in range(width):
            x_new = x % 34
            multiplier = (x_new / 34) * max_value 
            multiplier = int(multiplier)
            m = min(multiplier, max_value)
            if x < 34:
                row.append((m , 0, 0))
            elif x < 34 * 2:
                row.append((m, m, 0))
            elif x < 34 * 3:
                row.append((0, m, 0))
            elif x < 34 * 4:
                row.append((0, m, m))
            elif x < 34 * 5:
                row.append((0, 0, m))
            else:
                row.append((m, 0, m))

        test_data.append(row)

    RGB('testc.png', test_data, depth = depth).make()