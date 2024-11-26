from rawutil import unpack
from modules.unpack_generic_game import UnpackUDPGame
from storage import EventStringCode, SupportedGames

# <H means 2byte <B means 1byte <Q means 8byte <f means 4byte
class UnpackUDPFormulaOne(UnpackUDPGame):
	def unpack_header(self, header: bytes) -> None:
		values = unpack("<H <B <B <B <B <B <Q <f <I <I <B <B", header)

		storage_path = [SupportedGames.FORMULA_1_2021, "header"]
		self.storage.write([*storage_path, "_packet_format"],				values[0])
		self.storage.write([*storage_path, "_game_year"],					values[1])
		self.storage.write([*storage_path, "_game_major_version"],			values[2])
		self.storage.write([*storage_path, "_game_minor_version"],			values[3])
		self.storage.write([*storage_path, "_packet_version"],				values[4])
		self.storage.write([*storage_path, "_session_uid"],					values[5])
		self.storage.write([*storage_path, "_session_time"],				values[6])
		self.storage.write([*storage_path, "_packet_format"],				values[7])
		self.storage.write([*storage_path, "_overall_frame_identifier"],	values[8])
		self.storage.write([*storage_path, "_player_car_index"],			values[9])
		self.storage.write([*storage_path, "_overall_frame_identifier"],	values[10])
		self.storage.write([*storage_path, "_secondary_player_car_index"],	values[11])

	def _unpack_motion_data_packet(self, telemetry: bytes) -> None:
		for i in range(22):
			storage_path = [SupportedGames.FORMULA_1_2021, "_packet_motion_data", "_car_moiton_data", i]
			values = unpack("<f <f <f <f <f <f <h <h <h <h <h <h <f <f <f <f <f <f", telemetry[29+i*60:])

			self.storage.write([*storage_path, "_world_position", "x"],	values[0])
			self.storage.write([*storage_path, "_world_position","y"],	values[1])
			self.storage.write([*storage_path, "_world_position","z"],	values[2])

			self.storage.write([*storage_path, "_world_velocity", "x"],	values[3])
			self.storage.write([*storage_path, "_world_velocity", "y"],	values[4])
			self.storage.write([*storage_path, "_world_velocity", "z"],	values[5])

			self.storage.write([*storage_path, "_world_forward_dir", "x"],	values[6])
			self.storage.write([*storage_path, "_world_forward_dir", "y"],	values[7])
			self.storage.write([*storage_path, "_world_forward_dir", "z"],	values[8])

			self.storage.write([*storage_path, "_world_right_dir", "x"],	values[9])
			self.storage.write([*storage_path, "_world_right_dir", "y"],	values[10])
			self.storage.write([*storage_path, "_world_right_dir", "z"],	values[11])

			self.storage.write([*storage_path, "_g_force","_lateral"],		values[12])
			self.storage.write([*storage_path, "_g_force","_longitudinal"],	values[13])
			self.storage.write([*storage_path, "_g_force","_vertical"],		values[14])

			self.storage.write([*storage_path, "_yaw"],		values[15])
			self.storage.write([*storage_path, "_pitch"],	values[16])
			self.storage.write([*storage_path, "_roll"],	values[17])

	def _unpack_session_data(self, telemetry: bytes) -> None:
		# 29B header
		storage_path = [SupportedGames.FORMULA_1_2021, "_packet_session_data",]
		values = unpack("<B <b <b <B <H <B <b <B <H <H <B <B <B <B <B <B" , telemetry[29:])

		self.storage.write([*storage_path, "_weather"],					values[0])
		self.storage.write([*storage_path, "_track_temperature"],		values[1])
		self.storage.write([*storage_path, "_air_temperature"],			values[2])
		self.storage.write([*storage_path, "_total_laps"],				values[3])
		self.storage.write([*storage_path, "_track_length"],			values[4])
		self.storage.write([*storage_path, "_session_type"],			values[5])
		self.storage.write([*storage_path, "_track_id"],				values[6])
		self.storage.write([*storage_path, "_formula"],					values[7])
		self.storage.write([*storage_path, "_session_time_left"],		values[8])
		self.storage.write([*storage_path, "_session_duration"],		values[9])
		self.storage.write([*storage_path, "_pit_speed_limit"],			values[10])
		self.storage.write([*storage_path, "_game_paused"],				values[11])
		self.storage.write([*storage_path, "_is_spectating"],			values[12])
		self.storage.write([*storage_path, "_spectator_car_index"],		values[13])
		self.storage.write([*storage_path, "_sli_pro_native_support"],	values[14])
		#TODO szerintem ezt se tároljuk el
		self.storage.write([*storage_path, "_num_marshal_zones"],		values[15])

		num_marshal_zone = values[15]
		for i in range(num_marshal_zone):
			inner_storage_path = [*storage_path, "_marshalZones", i]
			values = unpack("<f <b", telemetry[29+19+i*5:])
			self.storage.write([*inner_storage_path, "_zone_start"],	values[0])
			self.storage.write([*inner_storage_path, "_zone_flag"],		values[1])

		values = unpack("<B <B <B", telemetry[29+19+num_marshal_zone*5:])
		self.storage.write( [*storage_path, "_safety_car_status"],				values[0])
		self.storage.write( [*storage_path, "_network_game"],					values[1])
		#TODO Szerintem ezt az adatot nem kell elmenteni
		self.storage.write( [*storage_path, "_num_weather_forecast_samples"],	values[2])

		num_weaher_forecast_sample = values[2]
		for i in range(num_weaher_forecast_sample):
			inner_storage_path = [*storage_path, "_weather_forecast_samples", i]
			values = unpack("<B <B <B <b <b <b <b <B", telemetry[29+19+num_marshal_zone*5+i*8:])

			self.storage.write([*inner_storage_path, "session_type"],				values[0])
			self.storage.write([*inner_storage_path, "time_offset"],				values[1])
			self.storage.write([*inner_storage_path,"weather"],						values[2])
			self.storage.write([*inner_storage_path, "track_temperatue"],			values[3])
			self.storage.write([*inner_storage_path, "track_temperature_change"],	values[4])
			self.storage.write([*inner_storage_path, "air_temperature"],			values[5])
			self.storage.write([*inner_storage_path, "air_temperature_change"],		values[6])
			self.storage.write([*inner_storage_path, "rain_change"],				values[7])

		values = unpack("<B <B <I <I <I <B <B <B <B <B <B <B <B <B <B <B <B <B <B <I <B <B <B <B <B <B <B <B", telemetry[29 + 19 + num_marshal_zone * 5 + num_weaher_forecast_sample * 8:])

		self.storage.write([*storage_path, "_forecast_accuracy"],					values[0])
		self.storage.write([*storage_path, "_ai_difficulty"],						values[1])
		self.storage.write([*storage_path, "_season_link_identifier"],				values[2])
		self.storage.write([*storage_path, "_weekend_link_identifier"],				values[3])
		self.storage.write([*storage_path, "_session_link_identifier"],				values[4])
		self.storage.write([*storage_path, "_pit_stop_window_ideal_lap"],			values[5])
		self.storage.write([*storage_path, "_pit_stop_window_latest_lap"],			values[6])
		self.storage.write([*storage_path, "_pit_stop_rejoin_position"],			values[7])
		self.storage.write([*storage_path, "_steering_assist"],						values[8])
		self.storage.write([*storage_path, "_braking_assist"],						values[9])
		self.storage.write([*storage_path, "_gearbox_assist"],						values[10])
		self.storage.write([*storage_path, "_pit_assist"],							values[11])
		self.storage.write([*storage_path, "_pit_release_assist"],					values[12])
		self.storage.write([*storage_path, "_ers_assist"],							values[13])
		self.storage.write([*storage_path, "_drs_assist"],							values[14])
		self.storage.write([*storage_path, "_dynamic_racing_line"],					values[15])
		self.storage.write([*storage_path, "_dynamic_racing_line_type"],			values[16])
		self.storage.write([*storage_path, "_game_mode"],							values[17])
		self.storage.write([*storage_path, "_rule_set"],							values[18])
		self.storage.write([*storage_path, "_time_of_day"],							values[19])
		self.storage.write([*storage_path, "_session_length"],						values[20])
		self.storage.write([*storage_path, "_speed_units_lead_player"],				values[21])
		self.storage.write([*storage_path, "_temperature_units_lead_player"],		values[22])
		self.storage.write([*storage_path, "_speed_units_secondary_player"],		values[23])
		self.storage.write([*storage_path, "_temperature_units_secondary_player"],	values[24])
		self.storage.write([*storage_path, "_num_safety_car_periods"],				values[25])
		self.storage.write([*storage_path, "_num_virtual_safety_car_periods"],		values[26])
		self.storage.write([*storage_path, "_num_red_flag_periods"],				values[27])

	def _unpack_lap_data_packet(self, telemetry:bytes) -> None:
		storage_path = [SupportedGames.FORMULA_1_2021, "_packet_lap_data"]
		for i in range(22):
			inner_storage_path = [*storage_path, "_lap_data", i]

			base_index = 29 + i * 50
			values = unpack("<I <I <H <B <H <B <H <H <f <f <f <B <B <B <B <B <B <B <B <B <B <B <B <B <B <B <H <H <B", telemetry[base_index:])

			#TODO maradjunk a snace_case-nél, csak lover case
			self.storage.write([*inner_storage_path, "_last_lap_time_in_MS"],				values[0])
			self.storage.write([*inner_storage_path, "_current_lap_time_in_MS"],			values[1])
			self.storage.write([*inner_storage_path, "_sector1_time_in_MS"],				values[2])
			self.storage.write([*inner_storage_path, "_sector1_time_minutes"],				values[3])
			self.storage.write([*inner_storage_path, "_sector2_time_in_MS"],				values[4])
			self.storage.write([*inner_storage_path, "_sector2_time_minutes"],				values[5])
			self.storage.write([*inner_storage_path, "_delta_to_car_in_front_in_MS"],		values[6])
			self.storage.write([*inner_storage_path, "_delta_to_race_leader_in_MS"],		values[7])
			self.storage.write([*inner_storage_path, "_lap_distance"],						values[8])
			self.storage.write([*inner_storage_path, "_total_distance"],					values[9])
			self.storage.write([*inner_storage_path, "_safety_car_delta"],					values[10])
			self.storage.write([*inner_storage_path, "_car_position"],						values[11])
			self.storage.write([*inner_storage_path, "_current_lap_num"],					values[12])
			self.storage.write([*inner_storage_path, "_pit_status"],						values[13])
			self.storage.write([*inner_storage_path, "_num_pit_stops"],						values[14])
			self.storage.write([*inner_storage_path, "_sector"],							values[15])
			self.storage.write([*inner_storage_path, "_current_lap_invalid"],				values[16])
			self.storage.write([*inner_storage_path, "_penalties"],							values[17])
			self.storage.write([*inner_storage_path, "_total_warnings"],					values[18])
			self.storage.write([*inner_storage_path, "_corner_cutting_warnings"],			values[19])
			self.storage.write([*inner_storage_path, "_num_unserved_drive_through_pens"],	values[20])
			self.storage.write([*inner_storage_path, "_num_unserved_stop_go_pens"],			values[21])
			self.storage.write([*inner_storage_path, "_grid_position"],						values[22])
			self.storage.write([*inner_storage_path, "_driver_status"],						values[23])
			self.storage.write([*inner_storage_path, "_result_status"],						values[24])
			self.storage.write([*inner_storage_path, "_pit_lane_timer_active"],				values[25])
			self.storage.write([*inner_storage_path, "_pit_lane_time_in_lane_in_MS"],		values[26])
			self.storage.write([*inner_storage_path, "_pit_stop_timer_in_MS"],				values[27])
			self.storage.write([*inner_storage_path, "_pit_stop_should_serve_pen"],			values[28])

		base_index = 29 + 22 * 50
		values = unpack("<B <B",telemetry[base_index:])
		self.storage.write([storage_path, "_time_trial_PB_car_index"],		values[0])
		self.storage.write([storage_path, "_time_trial_rival_car_index"],	values[0])

	def _unpack_participations_data_packet(self,telemetry:bytes) -> None:
		storage_path = [SupportedGames.FORMULA_1_2021, "_packet_participants_data"]

		num_active_cars = unpack('<B', telemetry[:29])[0]
		self.storage.write([storage_path, "_num_active_cars"], num_active_cars)

		# Résztvevők adatainak kibontása
		for i in range(num_active_cars):
			inner_storage_path = [*storage_path, "_participants", i]
			base_index = 30 + i * 58
			values = unpack(f"<B <B <B <B <B <B <B { '<c'*48 } <B <B <B", telemetry[base_index:base_index + 58])

			self.storage.write([*inner_storage_path, "_ai_controlled"],		values[0])
			self.storage.write([*inner_storage_path, "_driver_id"],			values[1])
			self.storage.write([*inner_storage_path, "_network_id"],		values[2])
			self.storage.write([*inner_storage_path, "_team_id"],			values[3])
			self.storage.write([*inner_storage_path, "_my_team"],			values[4])
			self.storage.write([*inner_storage_path, "_race_number"],		values[5])
			self.storage.write([*inner_storage_path, "_nationality"],		values[6])
			#TODO itt a szelés mit akar jelenteni?
			self.storage.write([*inner_storage_path, "_name"],				values[7:55])
			self.storage.write([*inner_storage_path, "_your_telemetry"],	values[55])
			self.storage.write([*inner_storage_path, "_show_online_names"],	values[56])
			self.storage.write([*inner_storage_path, "_platform"],			values[57])

	def _unpack_car_setup_data_packet(self,telemetry:bytes) -> None:
		for i in range(22):
			storage_path = [SupportedGames.FORMULA_1_2021, "_packet_car_setup_data", "_car_setups", i]
			base_index = 29 + i * 49
			values = unpack("<B <B <B <B <f <f <f <f <B <B <B <B <B <B <B <B <f <f <f <f <B <f", telemetry[base_index:base_index + 49])

			group_storage_path = [*storage_path, "_wing"]
			self.storage.write([*group_storage_path, "front"],	values[0])
			self.storage.write([*group_storage_path, "rear"],	values[1])

			group_storage_path = [*storage_path, "_throttle"]
			#TODO ez itt lehetne egy sima boolean érték?
			self.storage.write([*group_storage_path, "on"],		values[2])
			self.storage.write([*group_storage_path, "off"],	values[3])

			group_storage_path = [*storage_path, "_camber"]
			self.storage.write([*group_storage_path, "front"],	values[4])
			self.storage.write([*group_storage_path, "rear"],	values[5])

			group_storage_path = [*storage_path, "_toe"]
			self.storage.write([*group_storage_path, "front"],	values[6])
			self.storage.write([*group_storage_path, "rear"],	values[7])

			group_storage_path = [*storage_path, "_suspension"]
			self.storage.write([*group_storage_path, "front"],	values[8])
			self.storage.write([*group_storage_path, "rear"],	values[9])

			group_storage_path = [*storage_path, "_anti_roll_bar"]
			self.storage.write([*group_storage_path, "front"],	values[10])
			self.storage.write([*group_storage_path, "rear"],	values[11])

			group_storage_path = [*storage_path, "_suspension_height"]
			self.storage.write([*group_storage_path, "front"],	values[12])
			self.storage.write([*group_storage_path, "rear"],	values[13])

			group_storage_path = [*storage_path, "_brake"]
			self.storage.write([*group_storage_path, "pressure"],	values[14])
			self.storage.write([*group_storage_path, "bias"],		values[15])

			group_storage_path = [*storage_path, "_tyre_pressure"]
			self.storage.write([*group_storage_path, "rear_left"],		values[16])
			self.storage.write([*group_storage_path, "rear_right"],		values[17])
			self.storage.write([*group_storage_path, "front_left"], 	values[18])
			self.storage.write([*group_storage_path, "front_right"],	values[19])

			self.storage.write([*storage_path, "_ballast"],		values[20])
			self.storage.write([*storage_path, "_fuel_load"],	values[21])

	def _unpack_car_telemetry_data_packet(self,telemetry:bytes) -> None:
		storage_path = [SupportedGames.FORMULA_1_2021, "_packet_car_telemetry_data"]
		for i in range(22):
			base_index = 29 + i * 60
			inner_storage_path = [*storage_path, "_car_telemetry_data", i]
			values = unpack("<H <f <f <f <B <b <H <B <B <H <4H <4B <4B <H <4f <4B", telemetry[base_index:base_index + 60])

			self.storage.write([*inner_storage_path, "_speed"],					values[0])
			self.storage.write([*inner_storage_path, "_throttle"],				values[1])
			self.storage.write([*inner_storage_path, "_steer"],					values[2])
			self.storage.write([*inner_storage_path, "_brake"],					values[3])
			self.storage.write([*inner_storage_path, "_clutch"],				values[4])
			self.storage.write([*inner_storage_path, "_gear"],					values[5])
			self.storage.write([*inner_storage_path, "_engine_rpm"],			values[6])
			self.storage.write([*inner_storage_path, "_drs"],					values[7])
			self.storage.write([*inner_storage_path, "_rev_lights_percent"],	values[8])
			self.storage.write([*inner_storage_path, "_rev_lights_bit_value"],	values[9])

			group_storage_path = [*inner_storage_path, "_brakes_temperature"]
			self.storage.write([*group_storage_path, "rear_left"],		values[10])
			self.storage.write([*group_storage_path, "rear_right"],		values[11])
			self.storage.write([*group_storage_path, "front_left"],		values[12])
			self.storage.write([*group_storage_path, "front_right"],	values[13])

			group_storage_path = [*inner_storage_path, "_tyres_surface_temperature"]
			self.storage.write([*group_storage_path, "rear_left"],		values[14])
			self.storage.write([*group_storage_path, "rear_right"],		values[15])
			self.storage.write([*group_storage_path, "front_left"],		values[16])
			self.storage.write([*group_storage_path, "front_right"],	values[17])

			group_storage_path = [*inner_storage_path, "_tyres_inner_temperature"]
			self.storage.write([*group_storage_path, "rear_left"],		values[18])
			self.storage.write([*group_storage_path, "rear_right"],		values[19])
			self.storage.write([*group_storage_path, "front_left"],		values[20])
			self.storage.write([*group_storage_path, "front_right"],	values[21])

			self.storage.write([*inner_storage_path, "_engine_temperature"], values[22])

			group_storage_path = [*inner_storage_path, "_tyres_pressure"]
			self.storage.write([*group_storage_path, "rear_left"],		values[23])
			self.storage.write([*group_storage_path, "rear_right"],		values[24])
			self.storage.write([*group_storage_path, "front_left"],		values[25])
			self.storage.write([*group_storage_path, "front_right"],	values[26])

			group_storage_path = [*inner_storage_path, "_surface_type"]
			self.storage.write([*inner_storage_path, "rear_left"],		values[27])
			self.storage.write([*inner_storage_path, "rear_right"],		values[28])
			self.storage.write([*inner_storage_path, "front_left"],		values[29])
			self.storage.write([*inner_storage_path, "front_right"],	values[30])

		base_index = 29 + 22 * 60
		values = unpack("<B <B <b", telemetry[base_index:])
		self.storage.write([*storage_path, "_mfdPanelIndex"],					values[0])
		self.storage.write([*storage_path, "_mfdPanelIndexSecondaryPlayer"],	values[1])
		self.storage.write([*storage_path, "_suggestedGear"],					values[2])

	def _unpack_car_status_data_packet(self,telemetry:bytes) -> None:
		for i in range(22):
			storage_path = [SupportedGames.FORMULA_1_2021, "_packet_car_status_data", "_car_status_data", i]
			base_index = 29 + i * 55
			values = unpack("<B <B <B <B <B <f <f <f <H <H <B <B <H <B <B <B <b <f <f <f <B <f <f <f <B", telemetry[base_index:base_index + 55])
			self.storage.write([*storage_path, "_traction_control"],			values[0])
			self.storage.write([*storage_path, "_anti_lock_brakes"],			values[1])
			self.storage.write([*storage_path, "_fuel_mix"],					values[2])
			self.storage.write([*storage_path, "_front_brake_bias"],			values[3])
			self.storage.write([*storage_path, "_pit_limiter_status"],			values[4])
			self.storage.write([*storage_path, "_fuel_in_tank"],				values[5])
			self.storage.write([*storage_path, "_fuel_capacity"],				values[6])
			self.storage.write([*storage_path, "_fuel_remaining_laps"],			values[7])
			self.storage.write([*storage_path, "_max_rpm"],						values[8])
			self.storage.write([*storage_path, "_idle_rpm"],					values[9])
			self.storage.write([*storage_path, "_max_gears"],					values[10])
			self.storage.write([*storage_path, "_drs_allowed"],					values[11])
			self.storage.write([*storage_path, "_drs_activation_distance"],		values[12])
			self.storage.write([*storage_path, "_actual_tyre_compound"],		values[13])
			self.storage.write([*storage_path, "_visual_tyre_compound"],		values[14])
			self.storage.write([*storage_path, "_tyres_age_laps"],				values[15])
			self.storage.write([*storage_path, "_vehicle_fia_flags"],			values[16])
			self.storage.write([*storage_path, "_engine_power_ice"],			values[17])
			self.storage.write([*storage_path, "_engine_power_mguk"],			values[18])
			self.storage.write([*storage_path, "_ers_store_energy"],			values[19])
			self.storage.write([*storage_path, "_ers_deploy_mode"],				values[20])
			self.storage.write([*storage_path, "_ers_harvested_this_lap_mguk"],	values[21])
			self.storage.write([*storage_path, "_ers_harvested_this_lap_mguh"],	values[22])
			self.storage.write([*storage_path, "_ers_deployed_this_lap"],		values[23])
			self.storage.write([*storage_path, "_network_paused"], 				values[24])

	def _unpack_final_classification_data_packet(self,telemetry: bytes) -> None:
		#storage_path = [SupportedGames.FORMULA_1_2021, "_packet_final_classification_data"]

		num_cars = unpack('<B', telemetry[29:30])[0]
		#TODO szerintem felesleges eltárolni
		#self.storage.write([storage_path, "_numCars"], num_cars)

		# Végső besorolási adatok kibontása
		for i in range(num_cars):
			base_index = 30 + i * 45
			storage_path = [SupportedGames.FORMULA_1_2021, "_packet_final_classification_data", "_classification_data", i]
			values = unpack("<B <B <B <B <B <B <I <d <B <B <B <8B <8B <8B", telemetry[base_index:base_index + 45])
			self.storage.write([storage_path, "_classification_data", i, "_position"], values[0])
			self.storage.write([storage_path, "_classification_data", i, "_num_laps"], values[1])
			self.storage.write([storage_path, "_classification_data", i, "_grid_position"], values[2])
			self.storage.write([storage_path, "_classification_data", i, "_points"], values[3])
			self.storage.write([storage_path, "_classification_data", i, "_num_pit_stops"], values[4])
			self.storage.write([storage_path, "_classification_data", i, "_result_status"], values[5])
			self.storage.write([storage_path, "_classification_data", i, "_best_lap_time_in_ms"], values[6])
			self.storage.write([storage_path, "_classification_data", i, "_total_race_time"], values[7])
			self.storage.write([storage_path, "_classification_data", i, "_penalties_time"], values[8])
			self.storage.write([storage_path, "_classification_data", i, "_num_penalties"], values[9])
			self.storage.write([storage_path, "_classification_data", i, "_num_tyre_stints"], values[10])
			self.storage.write([storage_path, "_classification_data", i, "_tyre_stints_actual"],
							   list(values[11:19]))
			self.storage.write([storage_path, "_classification_data", i, "_tyre_stints_visual"],
							   list(values[19:27]))
			self.storage.write([storage_path, "_classification_data", i, "_tyre_stints_end_laps"],
							   list(values[27:35]))

	def _unpack_car_damage_data_packet(self,telemetry:bytes):
		storage_path = [SupportedGames.FORMULA_1_2021, "_packet_car_damage_data"]

		for i in range(22):
			baseInd = 29 + i * 42
			values = unpack("<4f <4B <4B <B <B <B <B <B <B <B <B <B <B <B <B <B <B <B <B <B <B <B <B",
							telemetry[baseInd:baseInd + 42])

			# Tyres Wear
			self.storage.write([storage_path, "_car_damage_data", i, "_tyres_wear", "rear_left"], values[0])
			self.storage.write([storage_path, "_car_damage_data", i, "_tyres_wear", "rear_right"], values[1])
			self.storage.write([storage_path, "_car_damage_data", i, "_tyres_wear", "front_left"], values[2])
			self.storage.write([storage_path, "_car_damage_data", i, "_tyres_wear", "front_right"], values[3])

			# Tyres Damage
			self.storage.write([storage_path, "_car_damage_data", i, "_tyres_damage", "rear_left"], values[4])
			self.storage.write([storage_path, "_car_damage_data", i, "_tyres_damage", "rear_right"], values[5])
			self.storage.write([storage_path, "_car_damage_data", i, "_tyres_damage", "front_left"], values[6])
			self.storage.write([storage_path, "_car_damage_data", i, "_tyres_damage", "front_right"], values[7])

			# Brakes Damage
			self.storage.write([storage_path, "_car_damage_data", i, "_brakes_damage", "rear_left"], values[8])
			self.storage.write([storage_path, "_car_damage_data", i, "_brakes_damage", "rear_right"], values[9])
			self.storage.write([storage_path, "_car_damage_data", i, "_brakes_damage", "front_left"], values[10])
			self.storage.write([storage_path, "_car_damage_data", i, "_brakes_damage", "front_right"], values[11])

			# Other Damage
			self.storage.write([storage_path, "_car_damage_data", i, "_front_left_wing_damage"], values[12])
			self.storage.write([storage_path, "_car_damage_data", i, "_front_right_wing_damage"], values[13])
			self.storage.write([storage_path, "_car_damage_data", i, "_rear_wing_damage"], values[14])
			self.storage.write([storage_path, "_car_damage_data", i, "_floor_damage"], values[15])
			self.storage.write([storage_path, "_car_damage_data", i, "_diffuser_damage"], values[16])
			self.storage.write([storage_path, "_car_damage_data", i, "_sidepod_damage"], values[17])
			self.storage.write([storage_path, "_car_damage_data", i, "_drs_fault"], values[18])
			self.storage.write([storage_path, "_car_damage_data", i, "_ers_fault"], values[19])
			self.storage.write([storage_path, "_car_damage_data", i, "_gear_box_damage"], values[20])
			self.storage.write([storage_path, "_car_damage_data", i, "_engine_damage"], values[21])
			self.storage.write([storage_path, "_car_damage_data", i, "_engine_mguh_wear"], values[22])
			self.storage.write([storage_path, "_car_damage_data", i, "_engine_es_wear"], values[23])
			self.storage.write([storage_path, "_car_damage_data", i, "_engine_ce_wear"], values[24])
			self.storage.write([storage_path, "_car_damage_data", i, "_engine_ice_wear"], values[25])
			self.storage.write([storage_path, "_car_damage_data", i, "_engine_mguk_wear"], values[26])
			self.storage.write([storage_path, "_car_damage_data", i, "_engine_tc_wear"], values[27])
			self.storage.write([storage_path, "_car_damage_data", i, "_engine_blown"], values[28])
			self.storage.write([storage_path, "_car_damage_data", i, "_engine_seized"], values[29])

	def _unpack_session_history_data_packet(self, telemetry:bytes):
		storage_path = [SupportedGames.FORMULA_1_2021, "_packet_session_history_data"]

		baseInd = 29
		values = unpack("<B <B <B <B <B <B <B", telemetry[baseInd:baseInd + 7])
		self.storage.write([storage_path, "_car_idx"], values[0])
		self.storage.write([storage_path, "_num_laps"], values[1])
		self.storage.write([storage_path, "_num_tyre_stints"], values[2])
		self.storage.write([storage_path, "_best_lap_time_lap_num"], values[3])
		self.storage.write([storage_path, "_best_sector1_lap_num"], values[4])
		self.storage.write([storage_path, "_best_sector2_lap_num"], values[5])
		self.storage.write([storage_path, "_best_sector3_lap_num"], values[6])

		for i in range(100):
			baseInd = 36 + i * 14
			lap_values = unpack("<I <H <B <H <B <H <B <B", telemetry[baseInd:baseInd + 14])
			self.storage.write([storage_path, "_lap_history_data", i, "_lap_time_in_ms"], lap_values[0])
			self.storage.write([storage_path, "_lap_history_data", i, "_sector1_time_in_ms"], lap_values[1])
			self.storage.write([storage_path, "_lap_history_data", i, "_sector1_time_minutes"], lap_values[2])
			self.storage.write([storage_path, "_lap_history_data", i, "_sector2_time_in_ms"], lap_values[3])
			self.storage.write([storage_path, "_lap_history_data", i, "_sector2_time_minutes"], lap_values[4])
			self.storage.write([storage_path, "_lap_history_data", i, "_sector3_time_in_ms"], lap_values[5])
			self.storage.write([storage_path, "_lap_history_data", i, "_sector3_time_minutes"], lap_values[6])
			self.storage.write([storage_path, "_lap_history_data", i, "_lap_valid_bit_flags"], lap_values[7])

		for i in range(8):
			baseInd = 1436 + i * 3
			values = unpack("<B <B <B", telemetry[baseInd:baseInd + 3])
			self.storage.write([storage_path, "_tyre_stints_history_data", i, "_end_lap"], values[0])
			self.storage.write([storage_path, "_tyre_stints_history_data", i, "_tyre_actual_compound"],
							   values[1])
			self.storage.write([storage_path, "_tyre_stints_history_data", i, "_tyre_visual_compound"],
							   values[2])

	def _unpack_tyre_sets_data_packet(self, telemetry:bytes):
		storage_path = [SupportedGames.FORMULA_1_2021, "_packet_tyre_sets_data"]

		# Autó indexének kibontása
		car_idx = unpack('<B', telemetry[29:30])[0]
		self.storage.write([storage_path, "_car_idx"], car_idx)

		# Gumiabroncs készletek adatainak kibontása
		for i in range(20):
			baseInd = 30 + i * 10
			values = unpack("<B <B <B <B <B <B <B <h <B", telemetry[baseInd:baseInd + 10])
			self.storage.write([storage_path, "_tyre_set_data", i, "_actual_tyre_compound"], values[0])
			self.storage.write([storage_path, "_tyre_set_data", i, "_visual_tyre_compound"], values[1])
			self.storage.write([storage_path, "_tyre_set_data", i, "_wear"], values[2])
			self.storage.write([storage_path, "_tyre_set_data", i, "_available"], values[3])
			self.storage.write([storage_path, "_tyre_set_data", i, "_recommended_session"], values[4])
			self.storage.write([storage_path, "_tyre_set_data", i, "_life_span"], values[5])
			self.storage.write([storage_path, "_tyre_set_data", i, "_usable_life"], values[6])
			self.storage.write([storage_path, "_tyre_set_data", i, "_lap_delta_time"], values[7])
			self.storage.write([storage_path, "_tyre_set_data", i, "_fitted"], values[8])

		baseInd = 30 + 20 * 10
		self.storage.write([storage_path, "_fitted_idx"], unpack('<B', telemetry[baseInd:baseInd + 1])[0])

	def _unpack_motion_ex_data_packet(self, telemetry:bytes):
		storage_path = [SupportedGames.FORMULA_1_2021, "_packet_motion_ex_data"]

		baseInd = 29
		values = unpack(
			"<4f <4f <4f <4f <4f <4f <4f <4f <f <f <f <f <f <f <f <f <f <f <f <f <f <f <f <f <f <f <f <f <f <f <4f",
			telemetry[baseInd:baseInd + 188])

		# Suspension Position
		self.storage.write([storage_path, "_suspension_position", "rear_left"], values[0])
		self.storage.write([storage_path, "_suspension_position", "rear_right"], values[1])
		self.storage.write([storage_path, "_suspension_position", "front_left"], values[2])
		self.storage.write([storage_path, "_suspension_position", "front_right"], values[3])

		# Suspension Velocity
		self.storage.write([storage_path, "_suspension_velocity", "rear_left"], values[4])
		self.storage.write([storage_path, "_suspension_velocity", "rear_right"], values[5])
		self.storage.write([storage_path, "_suspension_velocity", "front_left"], values[6])
		self.storage.write([storage_path, "_suspension_velocity", "front_right"], values[7])

		# Suspension Acceleration
		self.storage.write([storage_path, "_suspension_acceleration", "rear_left"], values[8])
		self.storage.write([storage_path, "_suspension_acceleration", "rear_right"], values[9])
		self.storage.write([storage_path, "_suspension_acceleration", "front_left"], values[10])
		self.storage.write([storage_path, "_suspension_acceleration", "front_right"], values[11])

		# Wheel Speed
		self.storage.write([storage_path, "_wheel_speed", "rear_left"], values[12])
		self.storage.write([storage_path, "_wheel_speed", "rear_right"], values[13])
		self.storage.write([storage_path, "_wheel_speed", "front_left"], values[14])
		self.storage.write([storage_path, "_wheel_speed", "front_right"], values[15])

		# Wheel Slip Ratio
		self.storage.write([storage_path, "_wheel_slip_ratio", "rear_left"], values[16])
		self.storage.write([storage_path, "_wheel_slip_ratio", "rear_right"], values[17])
		self.storage.write([storage_path, "_wheel_slip_ratio", "front_left"], values[18])
		self.storage.write([storage_path, "_wheel_slip_ratio", "front_right"], values[19])

		# Wheel Slip Angle
		self.storage.write([storage_path, "_wheel_slip_angle", "rear_left"], values[20])
		self.storage.write([storage_path, "_wheel_slip_angle", "rear_right"], values[21])
		self.storage.write([storage_path, "_wheel_slip_angle", "front_left"], values[22])
		self.storage.write([storage_path, "_wheel_slip_angle", "front_right"], values[23])

		# Wheel Lateral Force
		self.storage.write([storage_path, "_wheel_lat_force", "rear_left"], values[24])
		self.storage.write([storage_path, "_wheel_lat_force", "rear_right"], values[25])
		self.storage.write([storage_path, "_wheel_lat_force", "front_left"], values[26])
		self.storage.write([storage_path, "_wheel_lat_force", "front_right"], values[27])

		# Wheel Longitudinal Force
		self.storage.write([storage_path, "_wheel_long_force", "rear_left"], values[28])
		self.storage.write([storage_path, "_wheel_long_force", "rear_right"], values[29])
		self.storage.write([storage_path, "_wheel_long_force", "front_left"], values[30])
		self.storage.write([storage_path, "_wheel_long_force", "front_right"], values[31])

		# Height of COG Above Ground
		self.storage.write([storage_path, "_height_of_cog_above_ground"], values[32])

		# Local Velocity
		self.storage.write([storage_path, "_local_velocity_x"], values[33])
		self.storage.write([storage_path, "_local_velocity_y"], values[34])
		self.storage.write([storage_path, "_local_velocity_z"], values[35])

		# Angular Velocity
		self.storage.write([storage_path, "_angular_velocity_x"], values[36])
		self.storage.write([storage_path, "_angular_velocity_y"], values[37])
		self.storage.write([storage_path, "_angular_velocity_z"], values[38])

		# Angular Acceleration
		self.storage.write([storage_path, "_angular_acceleration_x"], values[39])
		self.storage.write([storage_path, "_angular_acceleration_y"], values[40])
		self.storage.write([storage_path, "_angular_acceleration_z"], values[41])

		# Front Wheels Angle
		self.storage.write([storage_path, "_front_wheels_angle"], values[42])

		# Wheel Vertical Force
		self.storage.write([storage_path, "_wheel_vert_force", "rear_left"], values[43])
		self.storage.write([storage_path, "_wheel_vert_force", "rear_right"], values[44])
		self.storage.write([storage_path, "_wheel_vert_force", "front_left"], values[45])
		self.storage.write([storage_path, "_wheel_vert_force", "front_right"], values[46])

	def _unpack_event_data_packet(self, telemetry: bytes) -> None:
		storage_path = [SupportedGames.FORMULA_1_2021, "_packet_event_data"]

		baseInd = 29
		event_string_code = unpack('<4B', telemetry[baseInd:baseInd + 4])
		self.storage.write([storage_path, "_event_string_code"], list(event_string_code))

		# Event Details
		event_code = event_string_code.value
		if event_code == EventStringCode.FASTEST_LAP:
			fastest_lap_data = unpack('<B <f', telemetry[baseInd + 4:baseInd + 9])
			self.storage.write([storage_path, "_event_details", "_fastest_lap", "vehicle_idx"], fastest_lap_data[0])
			self.storage.write([storage_path, "_event_details", "_fastest_lap", "lap_time"], fastest_lap_data[1])
		elif event_code == EventStringCode.RETIREMENT:
			retirement_data = unpack('<B', telemetry[baseInd + 4:baseInd + 5])
			self.storage.write([storage_path, "_event_details", "_retirement", "vehicle_idx"], retirement_data[0])
		elif event_code == EventStringCode.TEAM_MATE_IN_PITS:
			team_mate_in_pits_data = unpack('<B', telemetry[baseInd + 4:baseInd + 5])
			self.storage.write([storage_path, "_event_details", "_team_mate_in_pits", "vehicle_idx"],
							   team_mate_in_pits_data[0])
		elif event_code == EventStringCode.RACE_WINNER:
			race_winner_data = unpack('<B', telemetry[baseInd + 4:baseInd + 5])
			self.storage.write([storage_path, "_event_details", "_race_winner", "vehicle_idx"], race_winner_data[0])
		elif event_code == EventStringCode.PENALTY_ISSUED:
			penalty_data = unpack('<B <B <B <B <B <B <B', telemetry[baseInd + 4:baseInd + 11])
			self.storage.write([storage_path, "_event_details", "_penalty", "penalty_type"], penalty_data[0])
			self.storage.write([storage_path, "_event_details", "_penalty", "infringement_type"], penalty_data[1])
			self.storage.write([storage_path, "_event_details", "_penalty", "vehicle_idx"], penalty_data[2])
			self.storage.write([storage_path, "_event_details", "_penalty", "other_vehicle_idx"], penalty_data[3])
			self.storage.write([storage_path, "_event_details", "_penalty", "time"], penalty_data[4])
			self.storage.write([storage_path, "_event_details", "_penalty", "lap_num"], penalty_data[5])
			self.storage.write([storage_path, "_event_details", "_penalty", "places_gained"], penalty_data[6])
		elif event_code == EventStringCode.SPEED_TRAP_TRIGGERED:
			speed_trap_data = unpack('<B <f <B <B <B <f', telemetry[baseInd + 4:baseInd + 17])
			self.storage.write([storage_path, "_event_details", "_speed_trap", "vehicle_idx"], speed_trap_data[0])
			self.storage.write([storage_path, "_event_details", "_speed_trap", "speed"], speed_trap_data[1])
			self.storage.write([storage_path, "_event_details", "_speed_trap", "is_overall_fastest_in_session"],
							   speed_trap_data[2])
			self.storage.write([storage_path, "_event_details", "_speed_trap", "is_driver_fastest_in_session"],
							   speed_trap_data[3])
			self.storage.write([storage_path, "_event_details", "_speed_trap", "fastest_vehicle_idx_in_session"],
							   speed_trap_data[4])
			self.storage.write([storage_path, "_event_details", "_speed_trap", "fastest_speed_in_session"],
							   speed_trap_data[5])
		elif event_code == EventStringCode.START_LIGHTS:
			start_lights_data = unpack('<B', telemetry[baseInd + 4:baseInd + 5])
			self.storage.write([storage_path, "_event_details", "_start_lights", "num_lights"],
							   start_lights_data[0])
		elif event_code == EventStringCode.DRIVE_THROUGH_SERVED:
			drive_through_penalty_served_data = unpack('<B', telemetry[baseInd + 4:baseInd + 5])
			self.storage.write([storage_path, "_event_details", "_drive_through_penalty_served", "vehicle_idx"],
							   drive_through_penalty_served_data[0])
		elif event_code == EventStringCode.STOP_GO_SERVED:
			stop_go_penalty_served_data = unpack('<B', telemetry[baseInd + 4:baseInd + 5])
			self.storage.write([storage_path, "_event_details", "_stop_go_penalty_served", "vehicle_idx"],
							   stop_go_penalty_served_data[0])
		elif event_code == EventStringCode.FLASHBACK:
			flashback_data = unpack('<I <f', telemetry[baseInd + 4:baseInd + 9])
			self.storage.write([storage_path, "_event_details", "_flashback", "flashback_frame_identifier"],
							   flashback_data[0])
			self.storage.write([storage_path, "_event_details", "_flashback", "flashback_session_time"],
							   flashback_data[1])
		elif event_code == EventStringCode.BUTTON_STATUS:
			buttons_data = unpack('<I', telemetry[baseInd + 4:baseInd + 8])
			self.storage.write([storage_path, "_event_details", "_buttons", "button_status"], buttons_data[0])
		elif event_code == EventStringCode.OVERTAKE:
			overtake_data = unpack('<B <B', telemetry[baseInd + 4:baseInd + 6])
			self.storage.write([storage_path, "_event_details", "_overtake", "overtaking_vehicle_idx"],
							   overtake_data[0])
			self.storage.write([storage_path, "_event_details", "_overtake", "being_overtaken_vehicle_idx"],
							   overtake_data[1])
