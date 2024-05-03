from ctypes import Structure,c_int8, c_uint16, c_uint8, c_uint64, c_float, c_uint32, Union, LittleEndianStructure


class CarDamageData(LittleEndianStructure):

    def __init__(self):
        self.field1 = []
        self.field2 = []
        self.field3 = []

    _fields_ = [
        ('tyresWear', c_float),             # Tyre wear (percentage) *4
        ('tyresDamage', c_uint8),           # Tyre damage (percentage) *4
        ('brakesDamage', c_uint8),          # Brakes damage (percentage) *4
        ('frontLeftWingDamage', c_uint8),       # Front left wing damage (percentage)
        ('frontRightWingDamage', c_uint8),      # Front right wing damage (percentage)
        ('rearWingDamage', c_uint8),            # Rear wing damage (percentage)
        ('floorDamage', c_uint8),               # Floor damage (percentage)
        ('diffuserDamage', c_uint8),            # Diffuser damage (percentage)
        ('sidepodDamage', c_uint8),             # Sidepod damage (percentage)
        ('drsFault', c_uint8),                  # Indicator for DRS fault, 0 = OK, 1 = fault
        ('ersFault', c_uint8),                  # Indicator for ERS fault, 0 = OK, 1 = fault
        ('gearBoxDamage', c_uint8),             # Gear box damage (percentage)
        ('engineDamage', c_uint8),              # Engine damage (percentage)
        ('engineMGUHWear', c_uint8),            # Engine wear MGU-H (percentage)
        ('engineESWear', c_uint8),              # Engine wear ES (percentage)
        ('engineCEWear', c_uint8),              # Engine wear CE (percentage)
        ('engineICEWear', c_uint8),             # Engine wear ICE (percentage)
        ('engineMGUKWear', c_uint8),            # Engine wear MGU-K (percentage)
        ('engineTCWear', c_uint8),              # Engine wear TC (percentage)
        ('engineBlown', c_uint8),               # Engine blown, 0 = OK, 1 = fault
        ('engineSeized', c_uint8),              # Engine seized, 0 = OK, 1 = fault
    ]

def number_to_string(num):
    return str(num)

class CarDamagePacket(LittleEndianStructure):

    def __init__(self):
        self.field1 = []

    _fields_ = [
        ('carDamageData', CarDamageData),
    ]

    def item_from_cardamagepacket(self, list):
        for obj in self.field1:
            for attr, value in obj.__dict__.items():
                if attr == "field1" or attr == "field2" or attr == "field3":
                    for i in range(4):
                        list.append(number_to_string(value[i]))
                else:
                    list.append(value)
        pass