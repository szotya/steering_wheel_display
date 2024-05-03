from ctypes import Structure,c_int8, c_uint16, c_uint8, c_uint64, c_float, c_uint32, Union, LittleEndianStructure



class LapData(LittleEndianStructure):

    _fields_ = [
        ('lastLapTimeInMS', c_uint32),             # Last lap time in milliseconds
        ('currentLapTimeInMS', c_uint32),          # Current time around the lap in milliseconds
        ('sector1TimeInMS', c_uint16),             # Sector 1 time in milliseconds
        ('sector1TimeMinutes', c_uint8),           # Sector 1 whole minute part
        ('sector2TimeInMS', c_uint16),             # Sector 2 time in milliseconds
        ('sector2TimeMinutes', c_uint8),           # Sector 2 whole minute part
        ('deltaToCarInFrontInMS', c_uint16),       # Time delta to car in front in milliseconds
        ('deltaToRaceLeaderInMS', c_uint16),       # Time delta to race leader in milliseconds
        ('lapDistance', c_float),                  # Distance vehicle is around current lap in metres
        ('totalDistance', c_float),                # Total distance travelled in session in metres
        ('safetyCarDelta', c_float),               # Delta in seconds for safety car
        ('carPosition', c_uint8),                  # Car race position
        ('currentLapNum', c_uint8),                # Current lap number
        ('pitStatus', c_uint8),                    # Pit status - 0 = none, 1 = pitting, 2 = in pit area
        ('numPitStops', c_uint8),                  # Number of pit stops taken in this race
        ('sector', c_uint8),                       # Sector - 0 = sector1, 1 = sector2, 2 = sector3
        ('currentLapInvalid', c_uint8),            # Current lap invalid - 0 = valid, 1 = invalid
        ('penalties', c_uint8),                    # Accumulated time penalties in seconds to be added
        ('totalWarnings', c_uint8),                # Accumulated number of warnings issued
        ('cornerCuttingWarnings', c_uint8),        # Accumulated number of corner cutting warnings issued
        ('numUnservedDriveThroughPens', c_uint8),  # Number of drive through penalties left to serve
        ('numUnservedStopGoPens', c_uint8),        # Number of stop-go penalties left to serve
        ('gridPosition', c_uint8),                 # Grid position the vehicle started the race in
        ('driverStatus', c_uint8),                 # Status of driver - 0 = in garage, 1 = flying lap, 2 = in lap, 3 = out lap, 4 = on track
        ('resultStatus', c_uint8),                 # Result status - 0 = invalid, 1 = inactive, 2 = active, 3 = finished, 4 = did not finish, 5 = disqualified, 6 = not classified, 7 = retired
        ('pitLaneTimerActive', c_uint8),           # Pit lane timing - 0 = inactive, 1 = active
        ('pitLaneTimeInLaneInMS', c_uint16),       # If active, the current time spent in the pit lane in ms
        ('pitStopTimerInMS', c_uint16),            # Time of the actual pit stop in ms
        ('pitStopShouldServePen', c_uint8),        # Whether the car should serve a penalty at this stop
    ]

class LapDataPacket(LittleEndianStructure):

    def __init__(self):
        self.field1 = []

    _fields_ = [
        ('LapData', LapData),
        ('timeTrialPBCarIdx', c_uint8),
        ('timeTrialRivalCarIdx', c_uint8),
    ]

    def item_from_lapdatapacket(self, list):
        for obj in self.field1:
            for attr, value in obj.__dict__.items():
                list.append(value)
        pass

