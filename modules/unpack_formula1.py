from modules.CarDamagePacket import CarDamageData, CarDamagePacket
from modules.CarSetupPacket import CarSetupData, CarSetupPacket
from modules.CarStatusPacket import CarStatusData, CarStatusPacket
from modules.CarTelemetryDataPacket import CarTelemetryData, CarTelemetryDataPacket
from modules.EventPacket import Buttons, DRSStatus, DriveThroughPenaltyServed, EventPacket, FastestLap, Flashback, LightsOut, Overtake, Penalty, RaceWinner, RedFlag, Retirement, SpeedTrap, StartLights, StopGoPenaltyServed, TeamMateInPits, EventStringCode
from modules.Header import Header
from modules.LapDataPacket import LapData, LapDataPacket
from modules.SessionHistoryPacket import LapHistoryData, SessionHistoryPacket
from modules.SessionPacket import MarshalZone, SessionPacket, WeatherForecastSample
from modules.TyreSetsPacket import TyreSetData, TyreSetsPacket
import rawutil
from modules.unpack_generic_game import UnpackUDPGame

# <H means 2byte <B means 1byte <Q means 8byte <f means 4byte

class UnpackUDPFormulaOne(UnpackUDPGame):
	def _unpack_header(self, telemetry: bytes) -> Header:
		header = Header()

		header.field1 = rawutil.unpack('<H', telemetry[:2])[0]
		header.field2 = rawutil.unpack('<B', telemetry[2:3])[0]
		header.field3 = rawutil.unpack('<B', telemetry[3:4])[0]
		header.field4 = rawutil.unpack('<B', telemetry[4:5])[0]
		header.field5 = rawutil.unpack('<B', telemetry[5:6])[0]
		header.field6 = rawutil.unpack('<B', telemetry[6:7])[0]
		header.field7 = rawutil.unpack('<Q', telemetry[7:15])[0]
		header.field8 = rawutil.unpack('<f', telemetry[15:19])[0]
		header.field9 = rawutil.unpack('<I', telemetry[19:23])[0]
		header.field10 = rawutil.unpack('<I', telemetry[23:27])[0]
		header.field11 = rawutil.unpack('<B', telemetry[27:28])[0]
		header.field12 = rawutil.unpack('<B', telemetry[28:29])[0]

		return header
	
	def _unpack_eventpacket(self, telemetry: bytes) -> EventPacket:
		packet = EventPacket()
		char1 = rawutil.unpack('<c', telemetry[:1])
		char2 = rawutil.unpack('<c', telemetry[1:2])
		char3 = rawutil.unpack('<c', telemetry[2:3])
		char4 = rawutil.unpack('<c', telemetry[3:4])
		bytes_list = char1 + char2 + char3 + char4
		packet.field1 =''.join(b.decode('utf-8') for b in bytes_list)
		if packet.field1 == EventStringCode.FASTEST_LAP.value:
			packet.field2.append(self._unpack_fastest_lap(telemetry[4:]))
		elif packet.field1 == EventStringCode.RETIREMENT.value:
			self._unpack_retirement(telemetry[4:])
		elif packet.field1 == EventStringCode.DRS_ENABLED.value:
			self._unpack_drs_status(1)
		elif packet.field1 == EventStringCode.DRS_DISABLED.value:
			self._unpack_drs_status(0)
		elif packet.field1 == EventStringCode.TEAM_MATE_IN_PITS.value:
			self._unpack_team_mate_in_pits(telemetry[4:])
		elif packet.field1 == EventStringCode.RACE_WINNER.value:
			self._unpack_race_winner(telemetry[4:])
		elif packet.field1 == EventStringCode.PENALTY.value:
			self._unpack_penalty(telemetry[4:])
		elif packet.field1 == EventStringCode.SPEED_TRAP.value:
			self._unpack_speed_trap(telemetry[4:])
		elif packet.field1 == EventStringCode.START_LIGHTS.value:
			self._unpack_start_lights(telemetry[4:])
		elif packet.field1 == EventStringCode.LIGHTS_OUT.value:
			self._unpack_lights_out()
		elif packet.field1 == EventStringCode.DRIVE_THROUGH_SERVED.value:
			self._unpack_drive_through_penalty_served(telemetry[4:])
		elif packet.field1 == EventStringCode.STOP_GO_SERVED.value:
			self._unpack_stop_go_penalty_served(telemetry[4:])
		elif packet.field1 == EventStringCode.FLASHBACK.value:
			self._unpack_flashback(telemetry[4:])
		elif packet.field1 == EventStringCode.BUTTON.value:
			self._unpack_buttons(telemetry[4:])
		elif packet.field1 == EventStringCode.RED_FLAG.value:
			self._unpack_red_flag(telemetry[4:])
		elif packet.field1 == EventStringCode.OVERTAKE.value:
			self._unpack_overtake(telemetry[4:])

		return packet
	
	def _unpack_marshal_zone(self, telemetry: bytes) -> MarshalZone:
		marshal_zone = MarshalZone()

		marshal_zone.field1 = rawutil.unpack('<f', telemetry[:4])[0]
		marshal_zone.field2 = rawutil.unpack('<b', telemetry[4:5])[0]

		return marshal_zone
	
	def _unpack_weather_forecast_sample(self, telemetry: bytes) -> WeatherForecastSample:
		wfs = WeatherForecastSample()

		wfs.field1 = rawutil.unpack('<B', telemetry[:1])[0]
		wfs.field2 = rawutil.unpack('<B', telemetry[1:2])[0]
		wfs.field3 = rawutil.unpack('<B', telemetry[2:3])[0]
		wfs.field4 = rawutil.unpack('<b', telemetry[3:4])[0]
		wfs.field5 = rawutil.unpack('<b', telemetry[4:5])[0]
		wfs.field6 = rawutil.unpack('<b', telemetry[5:6])[0]
		wfs.field7 = rawutil.unpack('<b', telemetry[6:7])[0]
		wfs.field8 = rawutil.unpack('<B', telemetry[7:8])[0]

		return wfs
	
	def _unpack_session_packet(self, telemetry: bytes) -> SessionPacket:
		session_packet = SessionPacket()

		session_packet.field1 = rawutil.unpack('<B', telemetry[:1])[0]
		session_packet.field2 = rawutil.unpack('<B', telemetry[1:2])[0]
		session_packet.field3 = rawutil.unpack('<B', telemetry[2:3])[0]
		session_packet.field4 = rawutil.unpack('<B', telemetry[3:4])[0]
		session_packet.field5 = rawutil.unpack('<H', telemetry[4:6])[0]
		session_packet.field6 = rawutil.unpack('<B', telemetry[6:7])[0]
		session_packet.field7 = rawutil.unpack('<b', telemetry[7:8])[0]
		session_packet.field8 = rawutil.unpack('<B', telemetry[8:9])[0]
		session_packet.field9 = rawutil.unpack('<H', telemetry[9:11])[0]
		session_packet.field10 = rawutil.unpack('<H', telemetry[11:13])[0]
		session_packet.field11 = rawutil.unpack('<B', telemetry[13:14])[0]
		session_packet.field12 = rawutil.unpack('<B', telemetry[14:15])[0]
		session_packet.field13 = rawutil.unpack('<B', telemetry[15:16])[0]
		session_packet.field14 = rawutil.unpack('<B', telemetry[16:17])[0]
		session_packet.field15 = rawutil.unpack('<B', telemetry[17:18])[0]
		session_packet.field16 = rawutil.unpack('<B', telemetry[18:19])[0]

		offset = 19
		for _ in range(session_packet.field16):
			session_packet.field17.append(self._unpack_marshal_zone(telemetry[offset:offset+5]))
			offset += 5
		
		session_packet.field18 = rawutil.unpack('<B', telemetry[124:125])[0]
		session_packet.field19 = rawutil.unpack('<B', telemetry[125:126])[0]
		session_packet.field20 = rawutil.unpack('<B', telemetry[126:127])[0]

		offset = 127
		for _ in range(session_packet.field20):
			session_packet.field21.append(self._unpack_weather_forecast_sample(telemetry[offset:offset+8]))
			offset += 8
		
		session_packet.field22 = rawutil.unpack('<B', telemetry[575:576])[0]
		session_packet.field23 = rawutil.unpack('<B', telemetry[576:577])[0]
		session_packet.field24 = rawutil.unpack('<I', telemetry[577:581])[0]
		session_packet.field25 = rawutil.unpack('<I', telemetry[581:585])[0]
		session_packet.field26 = rawutil.unpack('<I', telemetry[585:589])[0]
		session_packet.field27 = rawutil.unpack('<B', telemetry[589:590])[0]
		session_packet.field28 = rawutil.unpack('<B', telemetry[590:591])[0]
		session_packet.field29 = rawutil.unpack('<B', telemetry[591:592])[0]
		session_packet.field30 = rawutil.unpack('<B', telemetry[592:593])[0]
		session_packet.field31 = rawutil.unpack('<B', telemetry[593:594])[0]
		session_packet.field32 = rawutil.unpack('<B', telemetry[594:595])[0]
		session_packet.field33 = rawutil.unpack('<B', telemetry[595:596])[0]
		session_packet.field34 = rawutil.unpack('<B', telemetry[596:597])[0]
		session_packet.field35 = rawutil.unpack('<B', telemetry[597:598])[0]
		session_packet.field36 = rawutil.unpack('<B', telemetry[598:599])[0]
		session_packet.field37 = rawutil.unpack('<B', telemetry[599:600])[0]
		session_packet.field38 = rawutil.unpack('<B', telemetry[600:601])[0]
		session_packet.field39 = rawutil.unpack('<B', telemetry[601:602])[0]
		session_packet.field40 = rawutil.unpack('<B', telemetry[602:603])[0]
		session_packet.field41 = rawutil.unpack('<I', telemetry[603:607])[0]
		session_packet.field42 = rawutil.unpack('<B', telemetry[607:608])[0]
		session_packet.field43 = rawutil.unpack('<B', telemetry[608:609])[0]
		session_packet.field44 = rawutil.unpack('<B', telemetry[609:610])[0]
		session_packet.field45 = rawutil.unpack('<B', telemetry[610:611])[0]
		session_packet.field46 = rawutil.unpack('<B', telemetry[611:612])[0]
		session_packet.field47 = rawutil.unpack('<B', telemetry[612:613])[0]
		session_packet.field48 = rawutil.unpack('<B', telemetry[613:614])[0]
		session_packet.field49 = rawutil.unpack('<B', telemetry[614:615])[0]

		return session_packet
	
	def _unpack_lap_data(self, telemetry: bytes) -> LapData:
		lap_data = LapData()

		lap_data.field1 = rawutil.unpack('<I', telemetry[:4])[0]
		lap_data.field2 = rawutil.unpack('<I', telemetry[4:8])[0]
		lap_data.field3 = rawutil.unpack('<H', telemetry[8:10])[0]
		lap_data.field4 = rawutil.unpack('<B', telemetry[10:11])[0]
		lap_data.field5 = rawutil.unpack('<H', telemetry[11:13])[0]
		lap_data.field6 = rawutil.unpack('<B', telemetry[13:14])[0]
		lap_data.field7 = rawutil.unpack('<H', telemetry[14:16])[0]
		lap_data.field8 = rawutil.unpack('<H', telemetry[16:18])[0]
		lap_data.field9 = rawutil.unpack('<f', telemetry[18:22])[0]
		lap_data.field10 = rawutil.unpack('<f', telemetry[22:26])[0]
		lap_data.field11 = rawutil.unpack('<f', telemetry[26:30])[0]
		lap_data.field12 = rawutil.unpack('<B', telemetry[30:31])[0]
		lap_data.field13 = rawutil.unpack('<B', telemetry[31:32])[0]
		lap_data.field14 = rawutil.unpack('<B', telemetry[32:33])[0]
		lap_data.field15 = rawutil.unpack('<B', telemetry[33:34])[0]
		lap_data.field16 = rawutil.unpack('<B', telemetry[34:35])[0]
		lap_data.field17 = rawutil.unpack('<B', telemetry[35:36])[0]
		lap_data.field18 = rawutil.unpack('<B', telemetry[36:37])[0]
		lap_data.field19 = rawutil.unpack('<B', telemetry[37:38])[0]
		lap_data.field20 = rawutil.unpack('<B', telemetry[38:39])[0]
		lap_data.field21 = rawutil.unpack('<B', telemetry[39:40])[0]
		lap_data.field22 = rawutil.unpack('<B', telemetry[40:41])[0]
		lap_data.field23 = rawutil.unpack('<B', telemetry[41:42])[0]
		lap_data.field24 = rawutil.unpack('<B', telemetry[42:43])[0]
		lap_data.field25 = rawutil.unpack('<B', telemetry[43:44])[0]
		lap_data.field26 = rawutil.unpack('<B', telemetry[44:45])[0]
		lap_data.field27 = rawutil.unpack('<H', telemetry[45:47])[0]
		lap_data.field28 = rawutil.unpack('<H', telemetry[47:49])[0]
		lap_data.field29 = rawutil.unpack('<B', telemetry[49:50])[0]

		return lap_data
	
	def _unpack_lap_data_packet(self, telemetry: bytes, car_index) -> LapDataPacket:
		ldp = LapDataPacket()

		offset = car_index * 50
		ldp.field1.append(self._unpack_lap_data(telemetry[offset:offset+50]))
		ldp.field2 = rawutil.unpack('<B', telemetry[1100:1101])[0]
		ldp.field3 = rawutil.unpack('<B', telemetry[1101:1102])[0]

		return ldp
	
	def _unpack_fastest_lap(self, telemetry: bytes) -> FastestLap:
		fastest_lap = FastestLap()

		fastest_lap.field1 = rawutil.unpack('<B', telemetry[:1])[0]
		fastest_lap.field2 = rawutil.unpack('<I', telemetry[1:5])[0]

		return fastest_lap
	
	def _unpack_retirement(self, telemetry: bytearray) -> Retirement:
		retirement = Retirement()
		retirement.field1 = rawutil.unpack('<B', telemetry[0:1])
		return retirement
	
	def _unpack_drs_status(self, status: int) -> DRSStatus:
		drs_status = DRSStatus()
		drs_status.field1 = status
		return drs_status
	
	def _unpack_team_mate_in_pits(self, telemetry: bytes) -> TeamMateInPits:
		tmip = TeamMateInPits()
		tmip.field1 = rawutil.unpack('<B', telemetry[0:1])
		return tmip
	
	def _unpack_race_winner(self, telemetry: bytes) -> RaceWinner:
		race_winner = RaceWinner()
		race_winner.field1 = rawutil.unpack('<B', telemetry[0:1])
		return race_winner
	
	def _unpack_penalty(self, telemetry: bytes) -> Penalty:
		penalty = Penalty()

		penalty.field1 = rawutil.unpack('<B', telemetry[0:1])
		penalty.field2 = rawutil.unpack('<B', telemetry[1:2])
		penalty.field3 = rawutil.unpack('<B', telemetry[2:3])
		penalty.field4 = rawutil.unpack('<B', telemetry[3:4])
		penalty.field5 = rawutil.unpack('<B', telemetry[4:5])
		penalty.field6 = rawutil.unpack('<B', telemetry[5:6])
		penalty.field7 = rawutil.unpack('<B', telemetry[6:7])

		return penalty
	
	def _unpack_speed_trap(self, telemetry: bytes) -> SpeedTrap:
		speed_trap = SpeedTrap()

		speed_trap.field1 = rawutil.unpack('<B', telemetry[0:1])
		speed_trap.field2 = rawutil.unpack('<f', telemetry[1:5])
		speed_trap.field3 = rawutil.unpack('<B', telemetry[5:6])
		speed_trap.field4 = rawutil.unpack('<B', telemetry[6:7])
		speed_trap.field5 = rawutil.unpack('<B', telemetry[7:8])
		speed_trap.field6 = rawutil.unpack('<f', telemetry[8:12])

		return speed_trap
	
	def _unpack_start_lights(self, telemetry: bytes) -> StartLights:
		start_lights = StartLights()
		start_lights.field1 = rawutil.unpack('<B', telemetry[0:1])
		return start_lights
	
	def _unpack_lights_out(self, telemetry: bytes) -> LightsOut:
		lights_out = LightsOut()
		lights_out.field1 = 1
		return lights_out
	
	def _unpack_drive_through_penalty_served(self, telemetry: bytes) -> DriveThroughPenaltyServed:
		dtps = DriveThroughPenaltyServed()
		dtps.field1 = rawutil.unpack('<B', telemetry[0:1])
		return dtps
	
	def _unpack_stop_go_penalty_served(self, telemetry: bytes) -> StopGoPenaltyServed:
		sgps = StopGoPenaltyServed()
		sgps.field1 = rawutil.unpack('<B', telemetry[0:1])
		return sgps
	
	def _unpack_flashback(self, telemetry: bytes) -> Flashback:
		flash_back = Flashback()
		flash_back.field1 = rawutil.unpack('<I', telemetry[0:4])
		flash_back.field2 = rawutil.unpack('<f', telemetry[4:8])
		return flash_back
	
	def _unpack_buttons(self, telemetry: bytes) -> Buttons:
		buttons = Buttons()
		buttons.field1 = rawutil.unpack('<f', telemetry[0:4])
		return buttons
	
	def _unpack_red_flag(self, telemetry: bytes) -> RedFlag:
		red_flag = RedFlag()
		red_flag.field1 = 1
		return red_flag
	
	def _unpack_overtake(self, telemetry: bytes) -> Overtake:
		overtake = Overtake()
		overtake.field1 = rawutil.unpack('<B', telemetry[0:1])
		overtake.field2 = rawutil.unpack('<B', telemetry[1:2])
		return overtake
	
	def _unpack_car_telemetry_data(self, telemetry: bytes) -> CarTelemetryData:
		ctd = CarTelemetryData()

		ctd.field1 = rawutil.unpack('<H', telemetry[:2])[0]
		ctd.field2 = rawutil.unpack('<f', telemetry[2:6])[0]
		ctd.field3 = rawutil.unpack('<f', telemetry[6:10])[0]
		ctd.field4 = rawutil.unpack('<f', telemetry[10:14])[0]
		ctd.field5 = rawutil.unpack('<B', telemetry[14:15])[0]
		ctd.field6 = rawutil.unpack('<b', telemetry[15:16])[0]
		ctd.field7 = rawutil.unpack('<H', telemetry[16:18])[0]
		ctd.field8 = rawutil.unpack('<B', telemetry[18:19])[0]
		ctd.field9 = rawutil.unpack('<B', telemetry[19:20])[0]
		ctd.field10 = rawutil.unpack('<H', telemetry[20:22])[0]

		offset = 22
		for _ in range(4):
			ctd.field11.append(rawutil.unpack('<H', telemetry[offset:offset+2])[0])
			offset += 2
		
		offset = 30
		for _ in range(4):
			ctd.field12.append(rawutil.unpack('<B', telemetry[offset:offset+1])[0])
			offset += 1
		
		offset = 34
		for _ in range(4):
			ctd.field13.append(rawutil.unpack('<B', telemetry[offset:offset+1])[0])
			offset += 1
		
		ctd.field14 = rawutil.unpack('<H', telemetry[38:40])[0]

		offset = 40
		for _ in range(4):
			ctd.field15.append(rawutil.unpack('<f', telemetry[offset:offset+4])[0])
			offset += 4
		
		offset = 56
		for _ in range(4):
			ctd.field16.append(rawutil.unpack('<B', telemetry[offset:offset+1])[0])
			offset += 1

		return ctd
	
	def _unpack_car_setup_data(self, telemetry: bytes) -> CarSetupData:
		csd = CarSetupData()

		csd.field1 = rawutil.unpack('<B', telemetry[:1])[0]
		csd.field2 = rawutil.unpack('<B', telemetry[1:2])[0]
		csd.field3 = rawutil.unpack('<B', telemetry[2:3])[0]
		csd.field4 = rawutil.unpack('<B', telemetry[3:4])[0]
		csd.field5 = rawutil.unpack('<f', telemetry[4:8])[0]
		csd.field6 = rawutil.unpack('<f', telemetry[8:12])[0]
		csd.field7 = rawutil.unpack('<f', telemetry[12:16])[0]
		csd.field8 = rawutil.unpack('<f', telemetry[16:20])[0]
		csd.field9 = rawutil.unpack('<B', telemetry[20:21])[0]
		csd.field10 = rawutil.unpack('<B', telemetry[21:22])[0]
		csd.field11 = rawutil.unpack('<B', telemetry[22:23])[0]
		csd.field12 = rawutil.unpack('<B', telemetry[23:24])[0]
		csd.field13 = rawutil.unpack('<B', telemetry[24:25])[0]
		csd.field14 = rawutil.unpack('<B', telemetry[25:26])[0]
		csd.field15 = rawutil.unpack('<B', telemetry[26:27])[0]
		csd.field16 = rawutil.unpack('<B', telemetry[27:28])[0]
		csd.field17 = rawutil.unpack('<f', telemetry[28:32])[0]
		csd.field18 = rawutil.unpack('<f', telemetry[32:36])[0]
		csd.field19 = rawutil.unpack('<f', telemetry[36:40])[0]
		csd.field20 = rawutil.unpack('<f', telemetry[40:44])[0]
		csd.field21 = rawutil.unpack('<B', telemetry[44:45])[0]
		csd.field22 = rawutil.unpack('<f', telemetry[45:49])[0]

	def _unpack_car_setup_packet(self, telemetry: bytes, car_index) -> CarSetupPacket:
		csp = CarSetupPacket()

		offset = car_index * 49
		csp.field1.append(self._unpack_car_setup_data(telemetry[offset:offset+49]))

		return csp
	
	def _unpack_car_telemetry_data_packet(self, telemetry: bytes, car_index) -> CarTelemetryDataPacket:
		ctdp = CarTelemetryDataPacket()

		offset = car_index * 60
		ctdp.field1.append(self._unpack_car_telemetry_data(telemetry[offset:offset+60]))
		ctdp.field2 = rawutil.unpack('<B', telemetry[1320:1321])[0]
		ctdp.field3 = rawutil.unpack('<B', telemetry[1321:1322])[0]
		ctdp.field4 = rawutil.unpack('<b', telemetry[1322:1323])[0]

		return ctdp
	
	def _unpack_car_status_data(self, telemetry: bytes) -> CarStatusData:
		csd = CarStatusData()

		csd.field1 = rawutil.unpack('<B', telemetry[:1])[0]
		csd.field2 = rawutil.unpack('<B', telemetry[1:2])[0]
		csd.field3 = rawutil.unpack('<B', telemetry[2:3])[0]
		csd.field4 = rawutil.unpack('<B', telemetry[3:4])[0]
		csd.field5 = rawutil.unpack('<B', telemetry[4:5])[0]
		csd.field6 = rawutil.unpack('<f', telemetry[5:9])[0]
		csd.field7 = rawutil.unpack('<f', telemetry[9:13])[0]
		csd.field8 = rawutil.unpack('<f', telemetry[13:17])[0]
		csd.field9 = rawutil.unpack('<H', telemetry[17:19])[0]
		csd.field10 = rawutil.unpack('<H', telemetry[19:21])[0]
		csd.field11 = rawutil.unpack('<B', telemetry[21:22])[0]
		csd.field12 = rawutil.unpack('<B', telemetry[22:23])[0]
		csd.field13 = rawutil.unpack('<H', telemetry[23:25])[0]
		csd.field14 = rawutil.unpack('<B', telemetry[25:26])[0]
		csd.field15 = rawutil.unpack('<B', telemetry[26:27])[0]
		csd.field16 = rawutil.unpack('<B', telemetry[27:28])[0]
		csd.field17 = rawutil.unpack('<B', telemetry[28:29])[0]
		csd.field18 = rawutil.unpack('<f', telemetry[29:33])[0]
		csd.field19 = rawutil.unpack('<f', telemetry[33:37])[0]
		csd.field20 = rawutil.unpack('<f', telemetry[37:41])[0]
		csd.field21 = rawutil.unpack('<B', telemetry[41:42])[0]
		csd.field22 = rawutil.unpack('<f', telemetry[42:46])[0]
		csd.field23 = rawutil.unpack('<f', telemetry[46:50])[0]
		csd.field24 = rawutil.unpack('<f', telemetry[50:54])[0]
		csd.field25 = rawutil.unpack('<B', telemetry[54:55])[0]

		return csd
	
	def _unpack_car_status_packet(self, telemetry: bytes, car_index) -> CarStatusPacket:
		packet = CarStatusPacket()

		offset = car_index * 55
		car_status_data = self._unpack_car_status_data(telemetry[offset:offset + 55])
		packet.field1.append(car_status_data)

		return packet
	
	def _unpack_car_damage_data(self, telemetry: bytes) -> CarDamageData:
		cdd = CarDamageData()

		offset = 0
		for _ in range(4):
			cdd.field1.append(rawutil.unpack('<I', telemetry[offset:offset+4])[0])
			offset += 4
		
		offset = 16
		for _ in range(4):
			cdd.field2.append(rawutil.unpack('<B', telemetry[offset:offset+1])[0])
			offset += 1
		
		offset = 20
		for _ in range(4):
			cdd.field3.append(rawutil.unpack('<B', telemetry[offset:offset+1])[0])
			offset += 1
		
		cdd.field4 = rawutil.unpack('<B', telemetry[24:25])[0]
		cdd.field5 = rawutil.unpack('<B', telemetry[25:26])[0]
		cdd.field6 = rawutil.unpack('<B', telemetry[26:27])[0]
		cdd.field7 = rawutil.unpack('<B', telemetry[27:28])[0]
		cdd.field8 = rawutil.unpack('<B', telemetry[28:29])[0]
		cdd.field9 = rawutil.unpack('<B', telemetry[29:30])[0]
		cdd.field10 = rawutil.unpack('<B', telemetry[30:31])[0]
		cdd.field11 = rawutil.unpack('<B', telemetry[31:32])[0]
		cdd.field12 = rawutil.unpack('<B', telemetry[32:33])[0]
		cdd.field13 = rawutil.unpack('<B', telemetry[33:34])[0]
		cdd.field14 = rawutil.unpack('<B', telemetry[34:35])[0]
		cdd.field15 = rawutil.unpack('<B', telemetry[35:36])[0]
		cdd.field16 = rawutil.unpack('<B', telemetry[36:37])[0]
		cdd.field17 = rawutil.unpack('<B', telemetry[37:38])[0]
		cdd.field18 = rawutil.unpack('<B', telemetry[38:39])[0]
		cdd.field19 = rawutil.unpack('<B', telemetry[39:40])[0]
		cdd.field20 = rawutil.unpack('<B', telemetry[40:41])[0]
		cdd.field21 = rawutil.unpack('<B', telemetry[41:42])[0]

		return cdd
	
	def _unpack_car_damage_packet(self, telemetry: bytes, car_index) -> CarDamagePacket:
		packet = CarDamagePacket()

		offset = car_index * 42
		packet.field1.append(self._unpack_cardamagedata(telemetry[offset:offset+42]))

		return packet
	
	#TODO: Optimalizálni kell, mert nagyon lassú a feldolgozási idejük.
	def _unpack_lap_history_data(self, telemetry: bytes) -> LapHistoryData:
		lhd = LapHistoryData()

		lhd.field1 = rawutil.unpack('<I', telemetry[:4])[0]
		lhd.field2 = rawutil.unpack('<H', telemetry[4:6])[0]
		lhd.field3 = rawutil.unpack('<B', telemetry[6:7])[0]
		lhd.field4 = rawutil.unpack('<H', telemetry[7:9])[0]
		lhd.field5 = rawutil.unpack('<B', telemetry[9:10])[0]
		lhd.field6 = rawutil.unpack('<H', telemetry[10:12])[0]
		lhd.field7 = rawutil.unpack('<B', telemetry[12:13])[0]
		lhd.field8 = rawutil.unpack('<B', telemetry[13:14])[0]

		return lhd
	
	#TODO: Optimalizálni kell, mert nagyon lassú a feldolgozási idejük.
	def _unpack_session_history_packet(self, telemetry: bytes, car_index) -> SessionHistoryPacket:
		shp = SessionHistoryPacket()

		id = rawutil.unpack('<B', telemetry[:1])[0]

		if id != car_index:
			return 404
		
		shp.field1 = id
		shp.field2 = rawutil.unpack('<B', telemetry[1:2])[0]
		shp.field3 = rawutil.unpack('<B', telemetry[2:3])[0]
		shp.field4 = rawutil.unpack('<B', telemetry[3:4])[0]
		shp.field5 = rawutil.unpack('<B', telemetry[4:5])[0]
		shp.field6 = rawutil.unpack('<B', telemetry[5:6])[0]
		shp.field7 = rawutil.unpack('<B', telemetry[6:7])[0]

		offset = 7
		for _ in range(100):
			shp.field8.append(
				self._unpack_lap_history_data(telemetry[offset:offset+14])
			)
			offset += 14

		return shp
	
	def _unpack_tyre_set_data(self, telemetry: bytes) -> TyreSetData:
		tsd = TyreSetData()

		tsd.field1 = rawutil.unpack('<B', telemetry[:1])[0]
		tsd.field2 = rawutil.unpack('<B', telemetry[1:2])[0]
		tsd.field3 = rawutil.unpack('<B', telemetry[2:3])[0]
		tsd.field4 = rawutil.unpack('<B', telemetry[3:4])[0]
		tsd.field5 = rawutil.unpack('<B', telemetry[4:5])[0]
		tsd.field6 = rawutil.unpack('<B', telemetry[5:6])[0]
		tsd.field7 = rawutil.unpack('<B', telemetry[6:7])[0]
		tsd.field8 = rawutil.unpack('<H', telemetry[7:9])[0]
		tsd.field9 = rawutil.unpack('<B', telemetry[9:10])[0]

		return tsd
	
	def _unpack_tyre_sets_packet(self, telemetry: bytes) -> TyreSetsPacket:
		tsp = TyreSetsPacket()

		tsp.field1 = rawutil.unpack('<B', telemetry[:1])[0]

		offset = 1
		for _ in range(20):
			tsp.field2.append(self._unpack_tyre_set_data(telemetry[offset:offset+10]))
			offset += 10
		
		tsp.field3 = rawutil.unpack('<B', telemetry[201:202])[0]
		
		return tsp