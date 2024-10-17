from abc import ABC, abstractmethod
from modules.EventPacket import FastestLap, Retirement, DRSStatus, TeamMateInPits, RaceWinner, Penalty, SpeedTrap, StartLights, LightsOut, DriveThroughPenaltyServed, StopGoPenaltyServed, Flashback, Buttons, RedFlag, Overtake, EventPacket
from modules.SessionPacket import MarshalZone, WeatherForecastSample, SessionPacket
from modules.LapDataPacket import LapData, LapDataPacket
from modules.CarTelemetryDataPacket import CarTelemetryData, CarTelemetryDataPacket
from modules.CarStatusPacket import CarStatusData, CarStatusPacket
from modules.CarDamagePacket import CarDamageData, CarDamagePacket
from modules.SessionHistoryPacket import LapHistoryData, SessionHistoryPacket
from modules.TyreSetsPacket import TyreSetData, TyreSetsPacket
from modules.CarSetupPacket import CarSetupData, CarSetupPacket
from modules.Header import Header

# <H means 2byte <B means 1byte <Q means 8byte <f means 4byte

class UnpackUDPGame(ABC):
	def __init__(self) -> None:
		pass

	def unpack_package(self, telemetry: bytes):
		header = self._unpack_header(telemetry)
		marshal_zone = self._unpack_marshal_zone(telemetry)
		weather_forecast = self._unpack_weather_forecast_sample(telemetry)
		session_packet = self._unpack_session_packet(telemetry)
		lap_data = self._unpack_lap_data(telemetry)
		lap_data_packet = self._unpack_lap_data_packet(telemetry)
		fastest_lap = self._unpack_fastest_lap(telemetry)
		retirement = self._unpack_retirement(telemetry)
		drs_status = self._unpack_drs_status(telemetry)
		team_mate_in_pits = self._unpack_team_mate_in_pits(telemetry)
		race_winner = self._unpack_race_winner(telemetry)

		return header, marshal_zone, weather_forecast, session_packet, lap_data, lap_data_packet, fastest_lap, retirement, drs_status, team_mate_in_pits, race_winner
	
	@abstractmethod
	def _unpack_header(self, telemetry: bytes) -> Header:
		pass

	@abstractmethod
	def _unpack_marshal_zone(self, telemetry: bytes) -> MarshalZone:
		pass

	@abstractmethod
	def _unpack_weather_forecast_sample(self, telemetry: bytes) -> WeatherForecastSample:
		pass

	@abstractmethod
	def _unpack_session_packet(self, telemetry: bytes) -> SessionPacket:
		pass
	
	@abstractmethod
	def _unpack_lap_data(self, telemetry: bytes) -> LapData:
		pass

	@abstractmethod
	def _unpack_lap_data_packet(self, telemetry: bytes, car_index) -> LapDataPacket:
		pass

	@abstractmethod
	def _unpack_fastest_lap(self, telemetry: bytes) -> FastestLap:
		pass

	@abstractmethod
	def _unpack_retirement(self, telemetry: bytearray) -> Retirement:
		pass

	@abstractmethod
	def _unpack_drs_status(self, telemetry: bytes) -> DRSStatus:
		pass

	@abstractmethod
	def _unpack_team_mate_in_pits(self, telemetry: bytes) -> TeamMateInPits:
		pass

	@abstractmethod
	def _unpack_race_winner(self, telemetry: bytes) -> RaceWinner:
		pass

	def _unpack_penalty(self, telemetry: bytes) -> Penalty:
		pass

	@abstractmethod
	def _unpack_speed_trap(self, telemetry: bytes) -> SpeedTrap:
		pass

	@abstractmethod
	def _unpack_start_lights(self, telemetry: bytes) -> StartLights:
		pass

	@abstractmethod
	def _unpack_lights_out(self, telemetry: bytes) -> LightsOut:
		pass

	@abstractmethod
	def _unpack_drive_through_penalty_served(self, telemetry: bytes) -> DriveThroughPenaltyServed:
		pass

	@abstractmethod
	def _unpack_stop_go_penalty_served(self, telemetry: bytes) -> StopGoPenaltyServed:
		pass

	@abstractmethod
	def _unpack_flashback(self, telemetry: bytes) -> Flashback:
		pass

	@abstractmethod
	def _unpack_buttons(self, telemetry: bytes) -> Buttons:
		pass

	@abstractmethod
	def _unpack_red_flag(self, telemetry: bytes) -> RedFlag:
		pass

	@abstractmethod
	def _unpack_overtake(self, telemetry: bytes) -> Overtake:
		pass

	@abstractmethod
	def _unpack_eventpacket(self, telemetry: bytes) -> EventPacket:
		pass

	@abstractmethod
	def _unpack_car_telemetry_data(self, telemetry: bytes) -> CarTelemetryData:
		pass

	@abstractmethod
	def _unpack_car_setup_data(self, telemetry: bytes) -> CarSetupData:
		pass

	@abstractmethod
	def _unpack_car_setup_packet(self, telemetry: bytes) -> CarSetupPacket:
		pass

	@abstractmethod
	def _unpack_car_telemetry_data_packet(self, telemetry: bytes) -> CarTelemetryDataPacket:
		pass

	@abstractmethod
	def _unpack_car_status_data(self, telemetry: bytes) -> CarStatusData:
		pass

	@abstractmethod
	def _unpack_car_status_packet(self, telemetry: bytes) -> CarStatusPacket:
		pass

	@abstractmethod
	def _unpack_car_damage_data(self, telemetry: bytes) -> CarDamageData:
		pass

	@abstractmethod
	def _unpack_car_damage_packet(self, telemetry: bytes) -> CarDamagePacket:
		pass

	@abstractmethod
	def _unpack_lap_history_data(self, telemetry: bytes) -> LapHistoryData:
		pass

	@abstractmethod
	def _unpack_session_history_packet(self, telemetry: bytes) -> SessionHistoryPacket:
		pass

	@abstractmethod
	def _unpack_tyre_set_data(self, telemetry: bytes) -> TyreSetData:
		pass

	@abstractmethod
	def _unpack_tyre_sets_packet(self, telemetry: bytes) -> TyreSetsPacket:
		pass
