from ctypes import Structure,c_int8, c_int16, c_uint8, c_uint64, c_float, c_uint32, Union, LittleEndianStructure

class TyreSetData(LittleEndianStructure):
    _fields_ = [
        ('actualTyreCompound', c_uint8),  # Actual tyre compound used
        ('visualTyreCompound', c_uint8),  # Visual tyre compound used
        ('wear', c_uint8),  # Tyre wear (percentage)
        ('available', c_uint8),  # Whether this set is currently available
        ('recommendedSession', c_uint8),  # Recommended session for tyre set
        ('lifeSpan', c_uint8), # Laps left in this tyre set
        ('usableLife', c_uint8), # Max number of laps recommended for this compound
        ('lapDeltaTime', c_int16), # Lap delta time in milliseconds compared to fitted set
        ('fitted', c_uint8) # Whether the set is fitted or not
    ]

class TyreSetsPacket(LittleEndianStructure):
    def __init__(self):
        self.field2 = []

    _fields_ = [
        ('carIdx', c_uint8),  # Index of the car this data relates to
        ('tyreSet', TyreSetData * 20),  # 13 (dry) + 7 (wet)
        ('fittedIdx', c_uint8),  # Index of the tyre set that is fitted
    ]

    def get_tyresetdata(self,listslist):
        list = []
        bestsoft = 100
        bestsoftdatas = []
        bestmedium = 100
        bestmediumdatas = []
        besthard = 100
        bestharddatas = []
        bestintermediate = 100
        bestintermediatedatas = []
        bestwet = 100
        bestwetdatas = []
        for obj in self.field2:
            list.clear()
            for attr, value in obj.__dict__.items():
                list.append(value)

            if list[8] != 1:

                #16 = soft, 17 = medium, 18 = hard, 7 = inter, 8 = wet

                if list[1] == 16 and list[2] < bestsoft and list[3] == 1:
                    bestsoft = list[2]
                    bestsoftdatas.clear()
                    bestsoftdatas.extend(list)
                elif list[1] == 17 and list[2] < bestmedium and list[3] == 1:
                    bestmedium = list[2]
                    bestmediumdatas.clear()
                    bestmediumdatas.extend(list)
                elif list[1] == 18 and list[2] < besthard and list[3] == 1:
                    besthard = list[2]
                    bestharddatas.clear()
                    bestharddatas.extend(list)
                elif list[1] == 7 and list[2] < bestintermediate and list[3] == 1:
                    bestintermediate = list[2]
                    bestintermediatedatas.clear()
                    bestintermediatedatas.extend(list)
                elif list[1] == 8 and list[2] < bestwet and list[3] == 1:
                    bestwet = list[2]
                    bestwetdatas.clear()
                    bestwetdatas.extend(list)

        listslist.append(bestsoftdatas)
        listslist.append(bestmediumdatas)
        listslist.append(bestharddatas)
        listslist.append(bestintermediatedatas)
        listslist.append(bestwetdatas)
        pass
