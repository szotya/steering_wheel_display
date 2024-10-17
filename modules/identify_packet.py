from enum import Enum
from modules.unpack_generic_game import UnpackUDPGame
from modules.unpack_formula1 import UnpackUDPFormulaOne

class Games(Enum):
	Formula1 = 1
	ForzaMotorsport = 2

def identify_packet(data: bytes) -> Games:
	pass

def get_unpacker(game: Games) -> UnpackUDPGame:
	if (game == Games.Formula1):
		return UnpackUDPFormulaOne;
	if (game == Games.ForzaMotorsport):
		pass