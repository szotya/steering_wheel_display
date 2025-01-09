from ctypes import c_uint8, c_uint16, c_uint32, c_uint64, c_float, LittleEndianStructure

class Header(LittleEndianStructure):
    _fields_ = [
        ('packetFormat', c_uint16),
        ('gameYear', c_uint8),
        ('gameMajorVersion', c_uint8),
        ('gameMinorVersion', c_uint8),
        ('packetVersion', c_uint8),
        ('packetId', c_uint8),
        ('sessionUID', c_uint64),
        ('sessionTime', c_float),
        ('frameIdentifier', c_uint32),
        ('overallFrameIdentifier', c_uint32),
        ('playerCarIndex', c_uint8),
        ('secondaryPlayerCarIndex', c_uint8),
    ]
