import socket
import struct
from enum import Enum
from ctypes import Structure, c_uint16, c_uint8, c_uint64, c_float, c_uint32, Union, LittleEndianStructure

class EventStringCode(Enum):
    """String codes used to identify an event."""

    SESSION_START = 'SSTA'
    SESSION_END = 'SEND'
    FASTEST_LAP = 'FTLP'
    RETIREMENT = 'RTMT'
    DRS_ENABLED = 'DRSE'
    DRS_DISABLED = 'DRSD'
    TEAM_MATE_IN_PITS = 'TMPT'
    CHEQUERED_FLAG = 'CHQF'
    RACE_WINNER = 'RCWN'
    PENALTY = 'PENA'
    SPEED_TRAP = 'SPTP'
    START_LIGHTS = 'STLG'
    LIGHTS_OUT = 'LGOT'
    DRIVE_THROUGH_SERVED = 'DTSV'
    STOP_GO_SERVED = 'SGSV'
    FLASHBACK = 'FLBK'
    BUTTON = 'BUTN'
    RED_FLAG = 'RDFL'
    OVERTAKE = 'OVTK'

class FastestLap(LittleEndianStructure):
    _fields_ = [
        ('vehicleIdx', c_uint8),
        ('lapTime', c_float),
    ]


class Retirement(LittleEndianStructure):
    _fields_ = [
        ('vehicleIdx', c_uint8),
    ]

class DRSStatus(LittleEndianStructure):
    _fields_ = [
        ('status', c_uint8),
    ]


class TeamMateInPits(LittleEndianStructure):
    _fields_ = [
        ('vehicleIdx', c_uint8),
    ]


class RaceWinner(LittleEndianStructure):
    _fields_ = [
        ('vehicleIdx', c_uint8),
    ]


class Penalty(LittleEndianStructure):
    _fields_ = [
        ('penaltyType', c_uint8),
        ('infringementType', c_uint8),
        ('vehicleIdx', c_uint8),
        ('otherVehicleIdx', c_uint8),
        ('time', c_uint8),
        ('lapNum', c_uint8),
        ('placesGained', c_uint8),
    ]


class SpeedTrap(LittleEndianStructure):
    _fields_ = [
        ('vehicleIdx', c_uint8),
        ('speed', c_float),
        ('isOverallFastestInSession', c_uint8),
        ('isDriverFastestInSession', c_uint8),
        ('fastestVehicleIdxInSession', c_uint8),
        ('fastestSpeedInSession', c_float),
    ]


class StartLights(LittleEndianStructure):
    _fields_ = [
        ('numLights', c_uint8),
    ]

class LightsOut():
    _fields_ = [
        ('lightsOut', c_uint8),
    ]

class DriveThroughPenaltyServed(LittleEndianStructure):
    _fields_ = [
        ('vehicleIdx', c_uint8),
    ]


class StopGoPenaltyServed(LittleEndianStructure):
    _fields_ = [
        ('vehicleIdx', c_uint8),
    ]


class Flashback(LittleEndianStructure):
    _fields_ = [
        ('flashbackFrameIdentifier', c_uint32),
        ('flashbackSessionTime', c_float),
    ]


class Buttons(LittleEndianStructure):
    _fields_ = [
        ('buttonStatus', c_uint32),
    ]

class RedFlag():
    _fields_ = [
        ('redFlag', c_uint8),
    ]

class Overtake(LittleEndianStructure):
    _fields_ = [
        ('overtakingVehicleIdx', c_uint8),       # Vehicle index of the vehicle overtaking
        ('beingOvertakenVehicleIdx', c_uint8),   # Vehicle index of the vehicle being overtaken
    ]

class EventDataDetails(Union):
    _fields_ = [
        ('FastestLap', FastestLap),
        ('Retirement', Retirement),
        ('TeamMateInPits', TeamMateInPits),
        ('RaceWinner', RaceWinner),
        ('Penalty', Penalty),
        ('SpeedTrap', SpeedTrap),
        ('StartLights', StartLights),
        ('DriveThroughPenaltyServed', DriveThroughPenaltyServed),
        ('StopGoPenaltyServed', StopGoPenaltyServed),
        ('Flashback', Flashback),
        ('Buttons', Buttons),
        #('RedFlad'),
        ('Overtake', Overtake),
    ]

class EventPacket(LittleEndianStructure):
    def __init__(self):
        self.field2 = []

    _fields_ = [
        ('eventStringCode', c_uint8 * 4),
        ('eventDetails', EventDataDetails),
    ]

    def fasteslap(self, list):
        if self.field1 == "FTLP":
            list.append(self.field2.FastestLap.field1)
            list.append(self.field2.FastestLap.field2)
