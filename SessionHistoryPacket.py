from ctypes import Structure,c_int8, c_uint16, c_uint8, c_uint64, c_float, c_uint32, Union, LittleEndianStructure

class LapHistoryData(LittleEndianStructure):
    _fields_ = [
        # 14bytes
        ('lapTimeInMS', c_uint32),
        ('sector1TimeInMS', c_uint16),
        ('sector1TimeMinutes', c_uint8),
        ('sector2TimeInMS', c_uint16),
        ('sector2TimeMinutes', c_uint8),
        ('sector3TimeInMS', c_uint16),
        ('sector3TimeMinutes', c_uint8),
        ('lapValidBitFlags', c_uint8),
    ]

class SessionHistoryPacket(LittleEndianStructure):

    def __init__(self):
        self.field8 = []

    _fields_ = [
        ('carIdx', c_uint8),
        ('numLaps', c_uint8),
        ('numTyreStints', c_uint8),
        ('bestLapTimeLapNum', c_uint8),
        ('bestSector1LapNum', c_uint8),
        ('bestSector2LapNum', c_uint8),
        ('bestSector3LapNum', c_uint8),
        ('lapHistoryData', LapHistoryData),
        ]

    def lapsofmycar(self, list):
        for obj in self.field8:
            for attr, value in obj.__dict__.items():
                if attr == "field1":
                    list.append(value)
        pass
            



