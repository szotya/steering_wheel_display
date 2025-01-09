"""
Dictionary wrapper to help being accessed from multiple functions.
"""

from typing import List, Any
from modules.logger import Logger
from enum import Enum

class MarshalZoneFlag(Enum):
	"""Possible flags in marshal zones"""
	INVALID=-1
	NONE=0
	GREEN=1
	BLUE=2
	YELLOW=3

class Weather(Enum):
	UNKNOWN=-1
	CLEAR=0
	LIGHT_CLOUD=1
	OVERCAST=2
	LIGHT_RAIN=3
	HEAVY_RAIN=4
	STORM=5

class SessionType(Enum):
	UNKNOWN = 0
	P1 = 1
	P2 = 2
	P3 = 3
	SHORT_P = 4
	Q1 = 5
	Q2 = 6
	Q3 = 7
	SHORT_Q = 8
	OSQ = 9
	R = 10
	R2 = 11
	R3 = 12
	TIME_TRIAL = 13

class FormulaType(Enum):
	F1_MODERN = 0
	F1_CLASSIC = 1
	F2 = 2
	F1_GENERIC = 3
	BETA = 4
	SUPERCARS = 5
	ESPORTS = 6
	F2_2021 = 7

class SessionLength(Enum):
	NONE = 0
	VERY_SHORT = 2
	SHORT = 3
	MEDIUM = 4
	MEDIUM_LONG = 5
	LONG = 6
	FULL = 7

class SafetyCarStatus(Enum):
	NO_SAFETY_CAR = 0
	FULL = 1
	VIRTUAL = 2
	FORMATION_LAP = 3

class Platform(Enum):
	STEAM =1
	PLAYSTAION = 3
	XBOX = 4
	ORIGIN = 6
	UNKNOWN = 255

class MFDPanelIndex(Enum):
	CLOSED = 255
	CARSETUP = 0
	PITS = 1
	DAMAGE = 2
	ENGINE = 3
	TEMPERATURES = 4

class FuelMix(Enum):
	LEAN = 0
	STANDARD = 1
	RICH = 2
	MAX = 3

class F1ModernTyreCompound(Enum):
	C5 = 16
	C4 = 17
	C3 = 18
	C2 = 19
	C1 = 20
	C0 = 21
	INTER = 7
	WET = 8

class F1ClassicTyreCompound(Enum):
	DRY = 9
	WET = 10

class F2TyreCompound(Enum):
	SUPER_SOFT = 11
	SOFT = 12
	MEDIUM = 13
	HARD = 14
	WET = 15

class F1VisualTyreCompound(Enum):
	SOFT = 16
	MEDIUM = 17
	HARD = 18
	INTER = 7
	WET = 8

class F1ClassicVisualTyreCompound(Enum):
	SOFT = 16
	MEDIUM = 17
	HARD = 18
	INTER = 7
	WET = 8

class F219VisualTyreCompound(Enum):
	WET = 15
	SUPER_SOFT = 19
	SOFT = 20
	MEDIUM = 21
	HARD = 22

class VehicleFiaFlagStatus(Enum):
	INVALID_UNKNOWN = -1
	NONE = 0
	GREEN = 1
	BLUE = 2
	YELLOW = 3

class ResultStatus(Enum):
	INVALID = 0
	INACTIVE = 1
	ACTIVE = 2
	FINISHED = 3
	DID_NOT_FINISH = 4
	DISQUALIFIED = 5
	NOT_CLASSIFIED = 6
	RETIRED = 7

class EventStringCode(Enum):
	SESSION_STARTED = 0
	SESSION_ENDED = 1
	FASTEST_LAP = 2
	RETIREMENT = 3
	DRS_ENABLED = 4
	DRS_DISABLED = 5
	TEAM_MATE_IN_PITS = 6
	CHEQUERED_FLAG = 7
	RACE_WINNER = 8
	PENALTY_ISSUED = 9
	SPEED_TRAP_TRIGGERED = 10
	START_LIGHTS = 11
	LIGHTS_OUT = 12
	DRIVE_THROUGH_SERVED = 13
	STOP_GO_SERVED = 14
	FLASHBACK = 15
	BUTTON_STATUS = 16
	RED_FLAG = 17
	OVERTAKE = 18

class SupportedGames(Enum):
    """Supported games"""
    FORZA_HORIZONT_5_2021="Forza Horizont 5 (2021)"
    FORMULA_1_2021="Formula 1 (2021)"

class Storage:
	def __init__(self):
		self.logger = Logger("Storage")
		self.dict = {}

	def read(self, keys: List[str], fallback=None) -> Any:
		"""
		Function to read/get value from the Storage class instance via a given path.
		"""

		if keys is None:
			raise ValueError("Must provide the keys parameter.")
		if len(keys) == 0:
			raise ValueError("The keys param must have to have minimum one item.")

		dict = self.dict
		for key in keys:
			if key not in dict:
				return fallback
			
			dict = dict[key]
		
		return dict

	def write(self, keys: List[str], data: Any) -> None:
		"""
		Function to write/set a value to a given path in the Storage class instance.
		"""
		
		if keys is None:
			raise ValueError("Must provide the keys parameter.")
		if len(keys) == 0:
			raise ValueError("The keys param must have to have minimum one item.")

		dict = self.dict
		for key in keys[:-1]:
			if key not in dict:
				dict[key] = {}
			
			dict = dict[key]
		
		dict[keys[-1]] = data
