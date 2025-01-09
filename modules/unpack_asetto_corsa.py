from storage import SupportedGames
from rawutil import unpack
from modules.unpack_generic_game import UnpackUDPGame

"""
A dokumentáció alapján a típusok:
	int are 32 bit little endian integers
	float are 32 bit floating point numbers
	bool are 8 bit boolean value
<H means 2byte <B means 1byte <Q means 8byte <f means 4byte
"""


#SUBSCRIBE_UPDATE esetén
class unpackUDPAssettoCorsa(UnpackUDPGame):

	def _unpack_RT_car_info(self, telemetry:bytes):
		storage_path = [SupportedGames.FORMULA_1_2021, "_RT_car_info"]
		values = unpack(
			"<c <i <f <f <f <b <b <b <b <b <b <f <f <f <i <i <i <i <f <f <f <f <f <i <f <4f <4f <4f <4f <4f <4f <4f <4f <4f <4f <4f <4f <4f <4f <f <f <3f",
			telemetry)

		self.storage.write([*storage_path, "_identifier"],	values[0])
		self.storage.write([*storage_path, "_size"],		values[1])
		
		#TODO speed path ala raktam
		group_storage_path = [*storage_path, "_speed"]
		self.storage.write([*group_storage_path, "_kmh"],	values[2])
		self.storage.write([*group_storage_path, "_mph"],	values[3])
		self.storage.write([*group_storage_path, "_ms"],	values[4])
		
		self.storage.write([*storage_path, "_is_abs_enabled"],			values[5])
		self.storage.write([*storage_path, "_is_abs_in_action"],		values[6])
		self.storage.write([*storage_path, "_is_tc_in_action"],			values[7])
		self.storage.write([*storage_path, "_is_tc_enabled"],			values[8])
		self.storage.write([*storage_path, "_is_in_pit"],				values[9])
		self.storage.write([*storage_path, "_is_engine_limiter_on"],	values[10])
		
		group_storage_path = [*storage_path, "_acc_g"]
		self.storage.write([*group_storage_path, "vertical"],	values[11])
		self.storage.write([*group_storage_path, "horizontal"],	values[12])
		self.storage.write([*group_storage_path, "frontal"],	values[13])
		
		self.storage.write([*storage_path, "_lap_time"],	values[14])
		self.storage.write([*storage_path, "_last_lap"],	values[15])
		self.storage.write([*storage_path, "_best_lap"],	values[16])
		self.storage.write([*storage_path, "_lap_count"],	values[17])
		self.storage.write([*storage_path, "_gas"],			values[18])
		self.storage.write([*storage_path, "_brake"],		values[19])
		self.storage.write([*storage_path, "_clutch"],		values[20])
		self.storage.write([*storage_path, "_engine_rpm"],	values[21])
		self.storage.write([*storage_path, "_steer"],		values[22])
		self.storage.write([*storage_path, "_gear"],		values[23])
		self.storage.write([*storage_path, "_cg_height"],	values[24])
		
		group_storage_path = [*storage_path, "_wheel_angular_speed"]
		self.storage.write([*group_storage_path, "rear_left"],		values[25])
		self.storage.write([*group_storage_path, "rear_right"],		values[26])
		self.storage.write([*group_storage_path, "front_left"],		values[27])
		self.storage.write([*group_storage_path, "front_right"],	values[28])
		
		group_storage_path = [*storage_path, "_slip_angle"]
		self.storage.write([*group_storage_path, "rear_left"],		values[29])
		self.storage.write([*group_storage_path, "rear_right"],		values[30])
		self.storage.write([*group_storage_path, "front_left"],		values[31])
		self.storage.write([*group_storage_path, "front_right"],	values[32])
		
		group_storage_path = [*storage_path, "slip_angle_contact_patch"]
		self.storage.write([*group_storage_path, "rear_left"],		values[33])
		self.storage.write([*group_storage_path, "rear_right"],		values[34])
		self.storage.write([*group_storage_path, "front_left"],		values[35])
		self.storage.write([*group_storage_path, "front_right"],	values[36])
		
		group_storage_path = [*storage_path, "_slip_ratio"]
		self.storage.write([*group_storage_path, "rear_left"],		values[37])
		self.storage.write([*group_storage_path, "rear_right"],		values[38])
		self.storage.write([*group_storage_path, "front_left"],		values[39])
		self.storage.write([*group_storage_path, "front_right"],	values[40])
		
		group_storage_path = [*storage_path, "_tyre_slip"]
		self.storage.write([*group_storage_path, "rear_left"],		values[41])
		self.storage.write([*group_storage_path, "rear_right"],		values[42])
		self.storage.write([*group_storage_path, "front_left"],		values[43])
		self.storage.write([*group_storage_path, "front_right"],	values[44])
		
		group_storage_path = [*storage_path, "_nd_slip"]
		self.storage.write([*group_storage_path, "rear_left"],		values[45])
		self.storage.write([*group_storage_path, "rear_right"],		values[46])
		self.storage.write([*group_storage_path, "front_left"],		values[47])
		self.storage.write([*group_storage_path, "front_right"],	values[48])
		
		group_storage_path = [*storage_path, ]
		self.storage.write([storage_path, "_load", "rear_left"], values[49])
		self.storage.write([storage_path, "_load", "rear_right"], values[50])
		self.storage.write([storage_path, "_load", "front_left"], values[51])
		self.storage.write([storage_path, "_load", "front_right"], values[52])
		
		self.storage.write([storage_path, "_Dy", "rear_left"], values[53])
		self.storage.write([storage_path, "_Dy", "rear_right"], values[54])
		self.storage.write([storage_path, "_Dy", "front_left"], values[55])
		self.storage.write([storage_path, "_Dy", "front_right"], values[56])
		
		self.storage.write([storage_path, "_Mz", "rear_left"], values[57])
		self.storage.write([storage_path, "_Mz", "rear_right"], values[58])
		self.storage.write([storage_path, "_Mz", "front_left"], values[59])
		self.storage.write([storage_path, "_Mz", "front_right"], values[60])
		
		self.storage.write([storage_path, "_tyre_dirty_level", "rear_left"], values[61])
		self.storage.write([storage_path, "_tyre_dirty_level", "rear_right"], values[62])
		self.storage.write([storage_path, "_tyre_dirty_level", "front_left"], values[63])
		self.storage.write([storage_path, "_tyre_dirty_level", "front_right"], values[64])
		
		self.storage.write([storage_path, "_camber_RAD", "rear_left"], values[65])
		self.storage.write([storage_path, "_camber_RAD", "rear_right"], values[66])
		self.storage.write([storage_path, "_camber_RAD", "front_left"], values[67])
		self.storage.write([storage_path, "_camber_RAD", "front_right"], values[68])
		
		self.storage.write([storage_path, "_tyre_radius", "rear_left"], values[69])
		self.storage.write([storage_path, "_tyre_radius", "rear_right"], values[70])
		self.storage.write([storage_path, "_tyre_radius", "front_left"], values[71])
		self.storage.write([storage_path, "_tyre_radius", "front_right"], values[72])
		
		self.storage.write([storage_path, "_tyre_loaded_radius", "rear_left"], values[73])
		self.storage.write([storage_path, "_tyre_loaded_radius", "rear_right"], values[74])
		self.storage.write([storage_path, "_tyre_loaded_radius", "front_left"], values[75])
		self.storage.write([storage_path, "_tyre_loaded_radius", "front_right"], values[76])

		self.storage.write([storage_path, "_car_position_normalized"], values[77])
		self.storage.write([storage_path, "_car_slope"], values[78])
		self.storage.write([storage_path, "_car_coordinates","x"], values[79])
		self.storage.write([storage_path, "_car_coordinates","y"], values[80])
		self.storage.write([storage_path, "_car_coordinates","z"], values[81])


	def _unpack_RT_lap(self, telemetry:bytes):
		storage_path = [SupportedGames.FORMULA_1_2021, "_RT_lap"]

		values = unpack("<i <i <50c <50c <i",telemetry)
		self.storage.write([*storage_path, "_car_identifier_number"],	values[0])
		self.storage.write([*storage_path, "_lap"],						values[1])
		self.storage.write([*storage_path, "_driver_name"],				values[2:52])
		self.storage.write([*storage_path, "_car_name"],				values[52:102])
		self.storage.write([*storage_path, "_time"],					values[102])