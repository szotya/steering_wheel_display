from tkinter import *
import tkinter as tk
import threading
import socket
from Graphics import *
from UDPunpack import unpack_carsetupdatapacket, unpack_header, unpack_eventpacket, unpack_sessionpacket, unpack_lapdatapacket, unpack_cartelemetrydatapacket, unpack_carstatuspacket, unpack_cardamagepacket,unpack_tyresetspacket, unpack_sessionhistorypacket
from SharedVars import *
import time

###Ez kell a ledekhez
#from rpi_ws281x import *


### IP cím lekérdezése
def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP



def udp_server(host='0.0.0.0', port=20777):
    print("im starting the server")
    global data_dict_cartelemetry
    global mfdPanelIndex
    global mfdPanelIndex_isChanged
    global data_dict_sessionpacket
    global data_dict_lapdata
    global data_dict_eventpacket
    global data_dict_carstatus
    global data_dict_cardamage
    global data_dict_delta
    global bestlap
    global besttyresetslist
    global packetType
    global data_dict_flyingdelta
    whereIsHeJoin = "notmid"
    data_dict_bestlap_meters = {}
    data_bestlap_sectors = {}
    data_dict_currentlap_sectors = {}
    data_dict_currentlap_meters_even = {}
    data_dict_currentlap_meters_odd = {}
    delta =  0.000
    deltaSector1 = 0.000
    MAX_LED_COUNT = 24  # Number of LED pixels.
    LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
    # LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10  # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
    DRS = 0  # DRS is not active
    RPM = 0
    LED_COUNT = 0

    '''strip = Adafruit_NeoPixel(MAX_LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()'''

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set the SO_REUSEADDR option to reuse the socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    server_address = (host, port)
    sock.bind(server_address)
    start_time = int(time.time())

    while True:

        try:
            data, address = sock.recvfrom(65507)
            #Data parsing
            header = data[:29]
            telemetry = data[29:]
            h = unpack_header(header)
            packetType = h.field6

            match packetType:
                case 1:
                    sp = unpack_sessionpacket(telemetry)
                    data_dict_sessionpacket.update({
                        'sessionType': sp.field6,
                        'trackLength': sp.field5,
                        'safetyCarStatus': sp.field18,
                        'pitStopWindowIdealLap': sp.field27,
                        'pitStopWindowLatestLap': sp.field28,
                        'pitStopRejoinPosition': sp.field29,
                        'speedUnit': sp.field43,
                    })
                case 2:
                    ldp = unpack_lapdatapacket(telemetry, h.field11)
                    list = []
                    ldp.item_from_lapdatapacket(list)
                    data_dict_lapdata.update({
                        'lastLapTime': list[0],
                        'currentLapTimeInMs': list[1],
                        'sector1TimeInMs': list[2],
                        'sector1TimeMinutes': list[3],
                        'sector2TimeInMs': list[4],
                        'sector2TimeMinutes': list[5],
                        'deltaToCarInFrontInMs': list[6],
                        'deltaToRaceLeaderInMs': list[7],
                        'lapDistance': list[8],
                        'totalDistance': list[9],
                        'safetyCarDelta': list[10],
                        'carPosition': list[11],
                        'currentLapNum': list[12],
                        'pitStatus': list[13],
                        'numPitStops': list[14],
                        'sector': list[15],
                        'currentLapInvalid': list[16],
                        'penalties': list[17],
                        'totalWarnings': list[18],
                        'cornerCuttingWarnings': list[19],
                        'numUnservedDriveThroughPens': list[20],
                        'numUnservedStopGoPens': list[21],
                        'gridPosition': list[22],
                        'driverStatus': list[23],
                        'resultStatus': list[24],
                        'pitLaneTimerActive': list[25],
                        'pitLaneTimeInLaneInMs': list[26],
                        'pitStopTimerInMs': list[27],
                        'pitStopShouldServePen': list[28],
                        'timeTrialPBCarIdx': ldp.field2,
                    })
                    data_dict_delta.update({
                        'lastLapTime': list[0],
                        'currentLapTimeInMs': list[1],
                        'sector1TimeInMs': list[2],
                        'sector2TimeInMs': list[4],
                        'lapDistance': int(list[8]),
                        'currentLapNum': list[12],
                        'sector': list[15],
                    })
                    try:
                        if len(data_dict_bestlap_meters) >= 3000 and len(data_bestlap_sectors) == 2 and data_dict_delta['currentLapTimeInMs'] > 0 and data_dict_delta['currentLapNum'] > 1:
                            sector = data_dict_delta['sector']
                            if f"{data_dict_delta['lapDistance']}" in data_dict_bestlap_meters:
                                delta = (data_dict_delta['currentLapTimeInMs'] - data_dict_bestlap_meters[f"{data_dict_delta['lapDistance']}"])/1000
                                data_dict_flyingdelta.update({'delta': delta})

                            if data_dict_delta['currentLapNum'] % 2 == 0:
                                print("even")
                                data_dict_currentlap_meters_even.update({f"{data_dict_delta['lapDistance']}": data_dict_delta['currentLapTimeInMs']})
                            else:
                                print("odd")
                                data_dict_currentlap_meters_odd.update({f"{data_dict_delta['lapDistance']}": data_dict_delta['currentLapTimeInMs']})
                            '''match sector:
                                case 0:
                                    delta = 0.000
                                    data_dict_flyingdelta.update({'delta': delta})
                                case 1:
                                    print(f'legjobb szektor1: {data_bestlap_sectors['sector1TimeInMs']}')
                                    print(f'jelenlegi szektor1: {data_dict_delta['sector1TimeInMs']}')
                                    deltaSector1 = (int(data_dict_delta['sector1TimeInMs']) - int(data_bestlap_sectors['sector1TimeInMs']))/1000
                                    data_dict_currentlap_sectors.update({'sector1TimeInMs': data_dict_delta['sector1TimeInMs']})
                                    data_dict_flyingdelta.update({'delta': deltaSector1})
                                case 2:
                                    print(f'legjobb szektor2: {data_bestlap_sectors['sector2TimeInMs']}')
                                    print(f'jelenlegi szektor2: {data_dict_delta['sector2TimeInMs']}')
                                    delta = deltaSector1 + (int(data_dict_delta['sector2TimeInMs']) - int(data_bestlap_sectors['sector2TimeInMs']))/1000
                                    data_dict_currentlap_sectors.update({'sector2TimeInMs': data_dict_delta['sector2TimeInMs']})
                                    data_dict_flyingdelta.update({'delta': delta})'''

                            if data_dict_delta['lastLapTime'] == bestlap[0] and data_dict_delta['currentLapNum'] >= 3:
                                #data_bestlap_sectors = data_dict_currentlap_sectors.copy()
                                if data_dict_delta['currentLapNum'] % 2 == 0 and len(data_dict_currentlap_meters_odd) > 0:
                                    data_dict_bestlap_meters = data_dict_currentlap_meters_odd.copy()
                                    data_dict_currentlap_meters_odd.clear()
                                elif data_dict_delta['currentLapNum'] % 2 != 0 and len(data_dict_currentlap_meters_even) > 0:
                                    data_dict_bestlap_meters = data_dict_currentlap_meters_even.copy()
                                    data_dict_currentlap_meters_even.clear()
                        elif data_dict_delta['currentLapNum'] > 1 and data_dict_delta['currentLapTimeInMs'] > 0 and len(bestlap) > 0:
                            if not bool(data_bestlap_sectors):
                                print("midgamejoin")
                                whereIsHeJoin = "mid"
                                data_bestlap_sectors = {
                                    'sector1TimeInMs': bestlap[1],
                                    'sector2TimeInMs': bestlap[3],
                                }
                            pass
                        else:
                            if data_dict_delta['currentLapTimeInMs'] > 0:
                                #Első körös mérer és másodpercgyűjtés
                                data_dict_bestlap_meters.update({f"{data_dict_delta['lapDistance']}": data_dict_delta['currentLapTimeInMs']})

                                # Első körös szektor
                                if 'sector1TimeInMs' in data_dict_delta and data_dict_delta['sector1TimeInMs'] > 0:
                                    data_bestlap_sectors.update({
                                        'sector1TimeInMs': data_dict_delta['sector1TimeInMs'],
                                    })
                                if 'sector2TimeInMs' in data_dict_delta and data_dict_delta['sector2TimeInMs'] > 0:
                                    data_bestlap_sectors.update({
                                        'sector2TimeInMs': data_dict_delta['sector2TimeInMs'],
                                    })

                    except Exception as e:
                        print(f"Error in flying_delta_calculation: {e}")
                case 3:
                    ep = unpack_eventpacket(telemetry)
                    data_dict_eventpacket.update({
                        'eventStringCode': ep.field1,
                    })
                    if ep.field1 == "SEND":
                        mfdPanelIndex = 6
                        mfdPanelIndex_isChanged = True
                        delta_reset(data_bestlap_sectors, data_dict_bestlap_meters)
                    elif ep.field1 == "CHQF":
                        mfdPanelIndex = 6
                        mfdPanelIndex_isChanged = True
                case 5:
                    csd = unpack_carsetupdatapacket(telemetry, h.field11)
                    list = []
                    csd.item_from_carsetupdata(list)
                    if len(list) > 0:
                        data_dict_carsetup.update({
                            'frontWing': list[0],
                            'rearWing': list[1],
                            'onThrottle': list[2],
                            'offThrottle': list[3],
                            'frontCamber': list[4],
                            'rearCamber': list[5],
                            'frontToe': list[6],
                            'rearToe': list[7],
                            'frontSuspension': list[8],
                            'rearSuspension': list[9],
                            'frontAntiRollBar': list[10],
                            'rearAntiRollBar': list[11],
                            'frontSuspensionHeight': list[12],
                            'rearSuspensionHeight': list[13],
                            'brakePressure': list[14],
                            'brakeBias': list[15],
                            'rearLeftTyrePressure': list[16],
                            'rearRightTyrePressure': list[17],
                            'frontLeftTyrePressure': list[18],
                            'frontRightTyrePressure': list[19],
                            'ballast': list[20],
                            'fuelLoad': list[21],
                        })

                case 6:
                    ctp = unpack_cartelemetrydatapacket(telemetry, h.field11)
                    list = []
                    ctp.item_from_cartelemetrydata(list)
                    data_dict_cartelemetry.update({
                        'RLBrakeTemperature': list[0],
                        'RRBrakeTemperature': list[1],
                        'FLBrakeTemperature': list[2],
                        'FRBrakeTemperature': list[3],
                        'RLTyreSurfaceTemperature': list[4],
                        'RRTyreSurfaceTemperature': list[5],
                        'FLTyreSurfaceTemperature': list[6],
                        'FRTyreSurfaceTemperature': list[7],
                        'RLTyreInnerTemperature': list[8],
                        'RRTyreInnerTemperature': list[9],
                        'FLTyreInnerTemperature': list[10],
                        'FRTyreInnerTemperature': list[11],
                        'RLTyrePressure': list[12],
                        'RRTyrePressure': list[13],
                        'FLTyrePressure': list[14],
                        'FRTyrePressure': list[15],
                        'RLSurfaceType': list[16],
                        'RRSurfaceType': list[17],
                        'FLSurfaceType': list[18],
                        'FRSurfaceType': list[19],
                        "speed": list[20],
                        "throttle": list[21],
                        "steer": list[22],
                        "brake": list[23],
                        "clutch": list[24],
                        "gear": list[25],
                        "engineRPM": list[26],
                        "drs": list[27],
                        "revLightsPercent": list[28],
                        "revLigthsBitValue": list[29],
                        "engineTemperature": list[30],
                    })

                    '''try:
                        if 'revLightsPercent' in data_dict_cartelemetry:
                            LED_COUNT = int(18 * (data_dict_cartelemetry['revLightsPercent'] / 100))

                        else:
                            LED_COUNT = 0

                        if 'drs' in data_dict_cartelemetry:
                            DRS = data_dict_cartelemetry['drs']

                        if DRS == 1:
                            strip.setPixelColor(0, Color(0, 255, 0))
                            strip.setPixelColor(1, Color(0, 255, 0))
                            strip.setPixelColor(2, Color(0, 0, 0))
                            strip.setPixelColor(3, Color(0, 0, 0))
                            strip.setPixelColor(4, Color(0, 0, 0))
                            strip.setPixelColor(5, Color(0, 0, 0))

                            for x in range(6, MAX_LED_COUNT):
                                if x <= LED_COUNT:
                                    if x < 12:
                                        strip.setPixelColor(x, Color(255, 0, 0))
                                    else:
                                        strip.setPixelColor(x, Color(102, 0, 255))
                                else:
                                    if x < 12:
                                        strip.setPixelColor(x, Color(0, 0, 0))
                                    else:
                                        strip.setPixelColor(x, Color(0, 0, 0))


                        else:
                            for x in range(0, MAX_LED_COUNT):
                                if x <= LED_COUNT:
                                    if x < 6:
                                        strip.setPixelColor(x, Color(0, 255, 0))
                                    elif x < 12:
                                        strip.setPixelColor(x, Color(255, 0, 0))
                                    else:
                                        strip.setPixelColor(x, Color(102, 0, 255))
                                else:
                                    if x < 6:
                                        strip.setPixelColor(x, Color(0, 0, 0))
                                    elif x < 12:
                                        strip.setPixelColor(x, Color(0, 0, 0))
                                    else:
                                        strip.setPixelColor(x, Color(0, 0, 0))

                    except Exception as e:
                        print(f"Error in LED handling: {e}")'''

                    ## MFD Panel Index változásának ellenőrzése
                    if ctp.field2 != mfdPanelIndex:
                        mfdPanelIndex_isChanged = True
                        mfdPanelIndex = ctp.field2
                    else:
                        mfdPanelIndex_isChanged = False

                case 7:
                    csp = unpack_carstatuspacket(telemetry, h.field11)
                    list = []
                    csp.item_from_carstatuspacket(list)
                    data_dict_carstatus.update({
                        'tractionControl': list[0],
                        'antiLockBrakes': list[1],
                        'fuelMix': list[2],
                        'frontBrakeBias': list[3],
                        'pitLimiterStatus': list[4],
                        'fuelInTank': list[5],
                        'fuelCapacity': list[6],
                        'fuelRemainingLaps': list[7],
                        'maxRPM': list[8],
                        'idleRPM': list[9],
                        'maxGears': list[10],
                        'drsAllowed': list[11],
                        'drsActivationDistance': list[12],
                        'actualTyreCompound': list[13],
                        'visualTyreCompound': list[14],
                        'tyresAgeLaps': list[15],
                        'vehicleFiaFlags': list[16],
                        'enginePowerICE': list[17],
                        'enginePowerMGUK': list[18],
                        'ersStoreEnergy': list[19],
                        'ersDeployMode': list[20],
                        'ersHarvestedThisLapMGUK': list[21],
                        'ersHarvestedThisLapMGUH': list[22],
                        'ersDeployedThisLap': list[23],
                        'networkPaused': list[24],
                    })

                    '''try:
                        current_time = int(time.time())
                        if 'vehicleFiaFlags' in data_dict_carstatus:
                            if current_time - start_time % 2 == 0:
                                if data_dict_carstatus['vehicleFiaFlags'] == 1:
                                    for x in range(19, 25):
                                        strip.setPixelColor(x, Color(0, 255, 0))

                                elif data_dict_carstatus['vehicleFiaFlags'] == 2:
                                    for x in range(19, 25):
                                        strip.setPixelColor(x, Color(0, 0, 255))

                                elif data_dict_carstatus['vehicleFiaFlags'] == 3:
                                    for x in range(19, 25):
                                        strip.setPixelColor(x, Color(255, 255, 0))
                                else:
                                    for x in range(19, 25):
                                        strip.setPixelColor(x, Color(0, 0, 0))
                            else:
                                for x in range(19, 25):
                                    strip.setPixelColor(x, Color(0, 0, 0))


                    except Exception as e:
                        print(f"Error in LED handling (flags): {e}")'''

                case 10:
                    cdp = unpack_cardamagepacket(telemetry, h.field11)
                    list = []
                    cdp.item_from_cardamagepacket(list)
                    data_dict_cardamage.update({
                        'RLTyreWear': list[0],
                        'RRTyreWear': list[1],
                        'FLTyreWear': list[2],
                        'FRTyreWear': list[3],
                        'RLTyreDamage': list[4],
                        'RRTyreDamage': list[5],
                        'FLTyreDamage': list[6],
                        'FRTyreDamage': list[7],
                        'RLBrakeDamage': list[8],
                        'RRBrakeDamage': list[9],
                        'FLBrakeDamage': list[10],
                        'FRBrakeDamage': list[11],
                        'frontLeftWingDamage': list[12],
                        'frontRightWingDamage': list[13],
                        'rearWingDamage': list[14],
                        'floorDamage': list[15],
                        'diffuserDamage': list[16],
                        'sidepodDamage': list[17],
                        'drsFault': list[18],
                        'ersFault': list[19],
                        'gearBoxDamage': list[20],
                        'engineDamage': list[21],
                        'engineMGUHWear': list[22],
                        'engineESWear': list[23],
                        'engineCEWear': list[24],
                        'engineICEWear': list[25],
                        'engineMGUKWear': list[26],
                        'engineTCWear': list[27],
                        'engineBlown': list[28],
                        'engineSeized': list[29],
                    })
                case 11:
                    shp = unpack_sessionhistorypacket(telemetry, h.field11)

                    if shp != 404:
                        bestlap.clear()
                        shp.get_bestlaptimedata(bestlap, shp.field4)
                    else:
                        pass
                case 12:
                    tsp = unpack_tyresetspacket(telemetry)
                    if h.field11 == tsp.field1:
                        besttyresetslist.clear()
                        tsp.get_tyresetdata(besttyresetslist)
                case _:
                    pass



            #strip.show()

        except socket.error as e:
            print(f"Socket error: {e}")
            break


def delta_reset(bestlapsector: dict, bestlapmeters: dict):
    global data_dict_flyingdelta
    data_dict_flyingdelta.update({'delta': 0.000})
    bestlapsector.clear()
    bestlapmeters.clear()

class Master:
    def __init__(self,root):
        self.root = root
        self.displayed_canvas = None
        self.connect = ConnectDisplay(root)
        self.df = DefaultDisplay(root)
        self.ps = PitStop(root)
        self.cd = CarDamage(root)
        self.ct = CarTemperature(root)
        self.e = Engine(root)

    def __call__(self, mfdnum):
        # Define what should happen when the object is "called"
        self.mfdnum = mfdnum
        self.Master()

    def Master(self):
        global data_dict_sessionpacket
        mfdnum = self.mfdnum

        if 'sessionType' in data_dict_sessionpacket:
            if data_dict_sessionpacket['sessionType'] == 10 or data_dict_sessionpacket['sessionType'] == 11 or data_dict_sessionpacket['sessionType'] == 12:
                if mfdnum == 6:
                    if self.displayed_canvas is not None:
                        self.displayed_canvas.destroy()
                    self.displayed_canvas = self.connect.create_connect_display()
                    self.root.after(5, self.connect.update_connection_display)

                elif mfdnum == 255 or mfdnum == 0:
                    if self.displayed_canvas is not None:
                        self.displayed_canvas.destroy()
                    self.displayed_canvas = self.df.create_default_display()
                    self.root.after(5, self.df.update_labels)

                elif mfdnum == 1:
                    if self.displayed_canvas is not None:
                        self.displayed_canvas.destroy()
                    self.displayed_canvas = self.ps.create_pitstop_display()
                    self.root.after(5, self.ps.update_pitstop_labels)

                elif mfdnum == 2:
                    if self.displayed_canvas is not None:
                        self.displayed_canvas.destroy()
                    self.displayed_canvas = self.cd.create_cardamage_display()
                    self.root.after(5, self.cd.update_damage_display)

                elif mfdnum == 3:
                    if self.displayed_canvas is not None:
                        self.displayed_canvas.destroy()
                    self.displayed_canvas = self.ct.create_cartemp_display()
                    self.root.after(5, self.ct.update_temp_labels)

                elif mfdnum == 4:
                    if self.displayed_canvas is not None:
                        self.displayed_canvas.destroy()
                    self.displayed_canvas = self.e.create_engine_display()
                    self.root.after(5, self.e.update_engine_display)

            elif data_dict_sessionpacket['sessionType'] >= 1 and data_dict_sessionpacket['sessionType'] <= 9:
                if mfdnum == 6:
                    if self.displayed_canvas is not None:
                        self.displayed_canvas.destroy()
                    self.displayed_canvas = self.connect.create_connect_display()
                    self.root.after(5, self.connect.update_connection_display)

                elif mfdnum == 255 or mfdnum == 0:
                    if self.displayed_canvas is not None:
                        self.displayed_canvas.destroy()
                    self.displayed_canvas = self.df.create_default_display()
                    self.root.after(5, self.df.update_labels)

                elif mfdnum == 1:
                    if self.displayed_canvas is not None:
                        self.displayed_canvas.destroy()
                    self.displayed_canvas = self.cd.create_cardamage_display()
                    self.root.after(5, self.cd.update_damage_display)

                elif mfdnum == 2:
                    if self.displayed_canvas is not None:
                        self.displayed_canvas.destroy()
                    self.displayed_canvas = self.ct.create_cartemp_display()
                    self.root.after(5, self.ct.update_temp_labels)

                elif mfdnum == 3:
                    if self.displayed_canvas is not None:
                        self.displayed_canvas.destroy()
                    self.displayed_canvas = self.e.create_engine_display()
                    self.root.after(5, self.e.update_engine_display)

            elif data_dict_sessionpacket['sessionType'] == 13:
                print("time trial")
                if mfdnum == 6:
                    if self.displayed_canvas is not None:
                        self.displayed_canvas.destroy()
                    self.displayed_canvas = self.connect.create_connect_display()
                    self.root.after(5, self.connect.update_connection_display)

                elif mfdnum == 255 or mfdnum == 0:
                    if self.displayed_canvas is not None:
                        self.displayed_canvas.destroy()
                    self.displayed_canvas = self.df.create_default_display()
                    self.root.after(5, self.df.update_labels)

                elif mfdnum == 1:
                    if self.displayed_canvas is not None:
                        self.displayed_canvas.destroy()
                    self.displayed_canvas = self.ct.create_cartemp_display()
                    self.root.after(5, self.ct.update_temp_labels)

            else:
                if mfdnum == 6:
                    if self.displayed_canvas is not None:
                        self.displayed_canvas.destroy()
                    self.displayed_canvas = self.connect.create_connect_display()
                    self.root.after(5, self.connect.update_connection_display)

                elif mfdnum == 255 or mfdnum == 0:
                    if self.displayed_canvas is not None:
                        self.displayed_canvas.destroy()
                    self.displayed_canvas = self.df.create_default_display()
                    self.root.after(5, self.df.update_labels)

                elif mfdnum == 1:
                    if self.displayed_canvas is not None:
                        self.displayed_canvas.destroy()
                    self.displayed_canvas = self.ps.create_pitstop_display()
                    self.root.after(5, self.ps.update_pitstop_labels)

                elif mfdnum == 2:
                    if self.displayed_canvas is not None:
                        self.displayed_canvas.destroy()
                    self.displayed_canvas = self.cd.create_cardamage_display()
                    self.root.after(5, self.cd.update_damage_display)

                elif mfdnum == 3:
                    if self.displayed_canvas is not None:
                        self.displayed_canvas.destroy()
                    self.displayed_canvas = self.ct.create_cartemp_display()
                    self.root.after(5, self.ct.update_temp_labels)

                elif mfdnum == 4:
                    if self.displayed_canvas is not None:
                        self.displayed_canvas.destroy()
                    self.displayed_canvas = self.e.create_engine_display()
                    self.root.after(5, self.e.update_engine_display)

        else:
            if mfdnum == 6:
                if self.displayed_canvas is not None:
                    self.displayed_canvas.destroy()
                self.displayed_canvas = self.connect.create_connect_display()
                self.root.after(5, self.connect.update_connection_display)

            elif mfdnum == 255 or mfdnum == 0:
                if self.displayed_canvas is not None:
                    self.displayed_canvas.destroy()
                self.displayed_canvas = self.df.create_default_display()
                self.root.after(5, self.df.update_labels)

            elif mfdnum == 1:
                if self.displayed_canvas is not None:
                    self.displayed_canvas.destroy()
                self.displayed_canvas = self.ps.create_pitstop_display()
                self.root.after(5, self.ps.update_pitstop_labels)

            elif mfdnum == 2:
                if self.displayed_canvas is not None:
                    self.displayed_canvas.destroy()
                self.displayed_canvas = self.cd.create_cardamage_display()
                self.root.after(5, self.cd.update_damage_display)

            elif mfdnum == 3:
                if self.displayed_canvas is not None:
                    self.displayed_canvas.destroy()
                self.displayed_canvas = self.ct.create_cartemp_display()
                self.root.after(5, self.ct.update_temp_labels)

            elif mfdnum == 4:
                if self.displayed_canvas is not None:
                    self.displayed_canvas.destroy()
                self.displayed_canvas = self.e.create_engine_display()
                self.root.after(5, self.e.update_engine_display)

    def update_mfd(self):
        global mfdPanelIndex_isChanged
        global mfdPanelIndex

        self.mfdnum = mfdPanelIndex
        if mfdPanelIndex_isChanged == True:
            self.__call__(self.mfdnum)
            mfdPanelIndex_isChanged = False
        else:
            pass
        root.after(5, self.update_mfd)

if __name__ == '__main__':

    udp_thread = threading.Thread(target=udp_server)
    udp_thread.start()

    root = tk.Tk()
    root.title("Steering Wheel Display")
    root.geometry("800x480")

    ## Csak a kijelzőt mutatja, nincs ablakkeret
    #root.overrideredirect(True)

    #defdisplay = DefaultDisplay(root)
    #defdisplay.create_default_display()

    M = Master(root)
    M.__call__(mfdPanelIndex)
    root.after(5, M.update_mfd)

    # Run the Tkinter main loop
    root.mainloop()