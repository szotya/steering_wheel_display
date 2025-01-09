from ctypes import Structure,c_int8, c_uint16, c_uint8, c_uint64, c_float, c_uint32, Union, LittleEndianStructure


class CarStatusData(LittleEndianStructure):
    _fields_ = [
        ('tractionControl', c_uint8),                      # Traction control - 0 = off, 1 = medium, 2 = full
        ('antiLockBrakes', c_uint8),                       # 0 (off) - 1 (on)
        ('fuelMix', c_uint8),                              # Fuel mix - 0 = lean, 1 = standard, 2 = rich, 3 = max
        ('frontBrakeBias', c_uint8),                       # Front brake bias (percentage)
        ('pitLimiterStatus', c_uint8),                     # Pit limiter status - 0 = off, 1 = on
        ('fuelInTank', c_float),                           # Current fuel mass
        ('fuelCapacity', c_float),                         # Fuel capacity
        ('fuelRemainingLaps', c_float),                    # Fuel remaining in terms of laps (value on MFD)
        ('maxRPM', c_uint16),                              # Cars max RPM, point of rev limiter
        ('idleRPM', c_uint16),                             # Cars idle RPM
        ('maxGears', c_uint8),                             # Maximum number of gears
        ('drsAllowed', c_uint8),                           # 0 = not allowed, 1 = allowed
        ('drsActivationDistance', c_uint16),               # 0 = DRS not available, non-zero - DRS will be available in [X] metres
        ('actualTyreCompound', c_uint8),                   # Tyre compound enumeration
        ('visualTyreCompound', c_uint8),                   # Visual tyre compound enumeration
        ('tyresAgeLaps', c_uint8),                         # Age in laps of the current set of tyres
        ('vehicleFiaFlags', c_int8),                       # -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow
        ('enginePowerICE', c_float),                       # Engine power output of ICE (W)
        ('enginePowerMGUK', c_float),                      # Engine power output of MGU-K (W)
        ('ersStoreEnergy', c_float),                       # ERS energy store in Joules
        ('ersDeployMode', c_uint8),                        # ERS deployment mode, 0 = none, 1 = medium, 2 = hotlap, 3 = overtake
        ('ersHarvestedThisLapMGUK', c_float),              # ERS energy harvested this lap by MGU-K
        ('ersHarvestedThisLapMGUH', c_float),              # ERS energy harvested this lap by MGU-H
        ('ersDeployedThisLap', c_float),                   # ERS energy deployed this lap
        ('networkPaused', c_uint8),                        # Whether the car is paused in a network game
    ]

class CarStatusPacket(LittleEndianStructure):

    def __init__(self):
        self.field1 = []

    _fields_ = [
        ('carStatusData', CarStatusData),
    ]

    def item_from_carstatuspacket(self, list):
        for obj in self.field1:
            for attr, value in obj.__dict__.items():
                list.append(value)
        pass
