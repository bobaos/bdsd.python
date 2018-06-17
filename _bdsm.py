import struct
import array

BDSM = b'BDSM'


def compose(dataStr):
    DATA = dataStr.encode()
    DATA_ARR = array.array('B', DATA)
    L = DATA.__len__()
    CHECKSUM = sum(DATA_ARR) % 256

    fmt_str = '>' + BDSM.__len__().__str__() + 'sH' + L.__str__() + 'sB'
    frame = struct.pack(fmt_str, BDSM, L, DATA, CHECKSUM)
    return frame


def parse(frame):
    fmt_str = '>4sH' + (frame.__len__() - 4 - 2 - 1).__str__() + 'sB'
    tuple_of_data = struct.unpack(fmt_str, frame)
    # TODO: check checksum
    return tuple_of_data
