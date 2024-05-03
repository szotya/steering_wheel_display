from ctypes import Structure,c_int8, c_uint16, c_uint8, c_uint64, c_float, c_uint32, Union, LittleEndianStructure


class CarTelemetryData(LittleEndianStructure):

    def __init__(self):
        self.field11 = []
        self.field12 = []
        self.field13 = []
        self.field15 = []
        self.field16 = []

    _fields_ = [
        ('speed', c_uint16),                                # Speed of car in kilometres per hour
        ('throttle', c_float),                              # Amount of throttle applied (0.0 to 1.0)
        ('steer', c_float),                                 # Steering (-1.0 (full lock left) to 1.0 (full lock right))
        ('brake', c_float),                                 # Amount of brake applied (0.0 to 1.0)
        ('clutch', c_uint8),                                # Amount of clutch applied (0 to 100)
        ('gear', c_int8),                                   # Gear selected (1-8, N=0, R=-1)
        ('engineRPM', c_uint16),                            # Engine RPM
        ('drs', c_uint8),                                   # 0 = off, 1 = on
        ('revLightsPercent', c_uint8),                      # Rev lights indicator (percentage)
        ('revLightsBitValue', c_uint16),                    # Rev lights (bit 0 = leftmost LED, bit 14 = rightmost LED)
        ('brakesTemperature', c_uint16),                    # Brakes temperature (celsius)  *4
        ('tyresSurfaceTemperature', c_uint8),               # Tyres surface temperature (celsius) *4
        ('tyresInnerTemperature', c_uint8),                 # Tyres inner temperature (celsius) *4
        ('engineTemperature', c_uint16),                    # Engine temperature (celsius)
        ('tyresPressure', c_float),                         # Tyres pressure (PSI) *4
        ('surfaceType', c_uint8 ),                          # Driving surface, see appendices *4
    ]


def number_to_string(num):
    return str(num)


class CarTelemetryDataPacket(LittleEndianStructure):

    def __init__(self):
        self.field1 = []

    _fields_ = [
        ('carTelemetryData', CarTelemetryData),
        ('mfdPanelIndex', c_uint8),
        ('mfdPanelIndexSecondaryPlayer', c_uint8),
        ('suggestedGear', c_int8),
    ]

    def item_from_cartelemetrydata(self, list):
        for obj in self.field1:
            for attr, value in obj.__dict__.items():
                if attr == "field11" or attr == "field12" or attr == "field13" or attr == "field15" or attr == "field16":
                    for i in range(4):
                        list.append(number_to_string(value[i]))
                else:
                    list.append(value)
        pass