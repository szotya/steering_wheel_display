from ctypes import Structure,c_int8, c_uint16, c_uint8, c_uint64, c_float, c_uint32, Union, LittleEndianStructure

class CarSetupData(LittleEndianStructure):
    _fields_ = [
        ('frontWing', c_uint8),                             # Front wing aero
        ('rearWing', c_uint8),                              # Rear wing aero
        ('onThrottle', c_uint8),                            # Differential adjustment on throttle (percentage)
        ('offThrottle', c_uint8),                           # Differential adjustment off throttle (percentage)
        ('frontCamber', c_float),                           # Front camber angle (suspension geometry)
        ('rearCamber', c_float),                            # Rear camber angle (suspension geometry)
        ('frontToe', c_float),                              # Front toe angle (suspension geometry)
        ('rearToe', c_float),                               # Rear toe angle (suspension geometry)
        ('frontSuspension', c_uint8),                       # Front suspension
        ('rearSuspension', c_uint8),                        # Rear suspension
        ('frontAntiRollBar', c_uint8),                      # Front anti-roll bar
        ('rearAntiRollBar', c_uint8),                       # Front anti-roll bar
        ('frontSuspensionHeight', c_uint8),                 # Front suspension height
        ('rearSuspensionHeight', c_uint8),                  # Rear suspension height
        ('brakePressure', c_uint8),                         # Brake pressure (percentage)
        ('brakeBias', c_uint8),                             # Brake bias (percentage)
        ('rearLeftTyrePressure', c_float),                  # Rear left tyre pressure (PSI)
        ('rearRightTyrePressure', c_float),                 # Rear right tyre pressure (PSI)
        ('frontLeftTyrePressure', c_float),                 # Front left tyre pressure (PSI)
        ('frontRightTyrePressure', c_float),                # Front right tyre pressure (PSI)
        ('ballast', c_int8),                                # Ballast
        ('fuelLoad', c_float),                              # Fuel load
    ]

class CarSetupPacket(LittleEndianStructure):

    def __init__(self):
        self.field1 = []

    _fields_ = [
        ('carSetupData', CarSetupData),
    ]

    def item_from_carsetupdata(self, list):
        for obj in self.field1:
            for attr, value in obj.__dict__.items():
                list.append(value)
        pass