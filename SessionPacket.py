from ctypes import Structure,c_int8, c_uint16, c_uint8, c_uint64, c_float, c_uint32, Union, LittleEndianStructure


class MarshalZone(LittleEndianStructure):
    _fields_ = [
        ('zoneStart', c_float),    # Fraction (0..1) of way through the lap the marshal zone starts
        ('zoneFlag', c_int8),      # -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow
    ]

class WeatherForecastSample(LittleEndianStructure):
    _fields_ = [
        ('sessionType', c_uint8),              # 0 = unknown, 1 = P1, 2 = P2, 3 = P3, 4 = Short P, 5 = Q1, 6 = Q2, 7 = Q3, 8 = Short Q, 9 = OSQ, 10 = R, 11 = R2, 12 = R3, 13 = Time Trial
        ('timeOffset', c_uint8),               # Time in minutes the forecast is for
        ('weather', c_uint8),                  # Weather - 0 = clear, 1 = light cloud, 2 = overcast, 3 = light rain, 4 = heavy rain, 5 = storm
        ('trackTemperature', c_int8),          # Track temp. in degrees Celsius
        ('trackTemperatureChange', c_int8),    # Track temp. change – 0 = up, 1 = down, 2 = no change
        ('airTemperature', c_int8),            # Air temp. in degrees celsius
        ('airTemperatureChange', c_int8),      # Air temp. change – 0 = up, 1 = down, 2 = no change
        ('rainPercentage', c_uint8),           # Rain percentage (0-100)
    ]

class SessionPacket(LittleEndianStructure):

    def __init__(self):
        self.field17 = []
        self.field21 = []

    _fields_ = [
        ('weather', c_uint8),
        # Weather - 0 = clear, 1 = light cloud, 2 = overcast, 3 = light rain, 4 = heavy rain, 5 = storm
        ('trackTemperature', c_int8),  # Track temp. in degrees Celsius
        ('airTemperature', c_int8),  # Air temp. in degrees Celsius
        ('totalLaps', c_uint8),  # Total number of laps in this race
        ('trackLength', c_uint16),  # Track length in metres
        ('sessionType', c_uint8),
        # 0 = unknown, 1 = P1, 2 = P2, 3 = P3, 4 = Short P, 5 = Q1, 6 = Q2, 7 = Q3, 8 = Short Q, 9 = OSQ, 10 = R, 11 = R2, 12 = R3, 13 = Time Trial
        ('trackId', c_int8),  # -1 for unknown, see appendix
        ('formula', c_uint8),
        # Formula, 0 = F1 Modern, 1 = F1 Classic, 2 = F2, 3 = F1 Generic, 4 = Beta, 5 = Supercars, 6 = Esports, 7 = F2 2021
        ('sessionTimeLeft', c_uint16),  # Time left in session in seconds
        ('sessionDuration', c_uint16),  # Session duration in seconds
        ('pitSpeedLimit', c_uint8),  # Pit speed limit in kilometres per hour
        ('gamePaused', c_uint8),  # Whether the game is paused – network game only
        ('isSpectating', c_uint8),  # Whether the player is spectating
        ('spectatorCarIndex', c_uint8),  # Index of the car being spectated
        ('sliProNativeSupport', c_uint8),  # SLI Pro support, 0 = inactive, 1 = active
        ('numMarshalZones', c_uint8),  # Number of marshal zones to follow
        ('marshalZone', MarshalZone),  #List of marshal zones – max 21
        ('safetyCarStatus', c_uint8),  # 0 = no safety car, 1 = full, 2 = virtual, 3 = formation lap
        ('networkGame', c_uint8),  # 0 = offline, 1 = online
        ('numWeatherForecastSamples', c_uint8),  # Number of weather samples to follow
        ('weatherForecastSamples', WeatherForecastSample),  # Array of weather forecast samples
        ('forecastAccuracy', c_uint8),  # 0 = Perfect, 1 = Approximate
        ('aiDifficulty', c_uint8),  # AI Difficulty rating – 0-110
        ('seasonLinkIdentifier', c_uint32),  # Identifier for season - persists across saves
        ('weekendLinkIdentifier', c_uint32),  # Identifier for weekend - persists across saves
        ('sessionLinkIdentifier', c_uint32),  # Identifier for session - persists across saves
        ('pitStopWindowIdealLap', c_uint8),  # Ideal lap to pit on for current strategy (player)
        ('pitStopWindowLatestLap', c_uint8),  # Latest lap to pit on for current strategy (player)
        ('pitStopRejoinPosition', c_uint8),  # Predicted position to rejoin at (player)
        ('steeringAssist', c_uint8),  # 0 = off, 1 = on
        ('brakingAssist', c_uint8),  # 0 = off, 1 = low, 2 = medium, 3 = high
        ('gearboxAssist', c_uint8),  # 1 = manual, 2 = manual & suggested gear, 3 = auto
        ('pitAssist', c_uint8),  # 0 = off, 1 = on
        ('pitReleaseAssist', c_uint8),  # 0 = off, 1 = on
        ('ERSAssist', c_uint8),  # 0 = off, 1 = on
        ('DRSAssist', c_uint8),  # 0 = off, 1 = on
        ('dynamicRacingLine', c_uint8),  # 0 = off, 1 = corners only, 2 = full
        ('dynamicRacingLineType', c_uint8),  # 0 = 2D, 1 = 3D
        ('gameMode', c_uint8),  # Game mode id - see appendix
        ('ruleSet', c_uint8),  # Ruleset - see appendix
        ('timeOfDay', c_uint32),  # Local time of day - minutes since midnight
        ('sessionLength', c_uint8),
        # 0 = None, 2 = Very Short, 3 = Short, 4 = Medium, 5 = Medium Long, 6 = Long, 7 = Full
        ('speedUnitsLeadPlayer', c_uint8),  # 0 = MPH, 1 = KPH
        ('temperatureUnitsLeadPlayer', c_uint8),  # 0 = Celsius, 1 = Fahrenheit
        ('speedUnitsSecondaryPlayer', c_uint8),  # 0 = MPH, 1 = KPH
        ('temperatureUnitsSecondaryPlayer', c_uint8),  # 0 = Celsius, 1 = Fahrenheit
        ('numSafetyCarPeriods', c_uint8),  # Number of safety cars called during session
        ('numVirtualSafetyCarPeriods', c_uint8),  # Number of virtual safety cars called
        ('numRedFlagPeriods', c_uint8),  # Number of red flags called during session
    ]