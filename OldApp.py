from tkinter import *
import tkinter as tk
import threading
import socket
import time
import os
from SessionHistoryPacket import *
from PIL import Image as PilImage, ImageTk
from UDPunpack import unpack_header, unpack_eventpacket, unpack_sessionpacket, unpack_lapdatapacket, unpack_cartelemetrydatapacket, unpack_carstatuspacket, unpack_cardamagepacket,unpack_tyresetspacket, unpack_sessionhistorypacket
from listsandconstants import *
from Graphics import *
#from rpi_ws281x import *




## Egyenlőre használaton kívül
listlengthiscreated = False
currentlapmspermeter = []
delta = 0.000
track_length = 0
data_dict_main = {
    'isSafetyCar': False,
    'formationLap': False,
    'isSafetyCarProcess': False,
}

## Használatban van
mfdPanelIndex = 6
maximum_energy_storage = 4000000
besttyresetslist = []
log_list = []
mfdPanelIndex_isChanged = False
data_dict_tyresets = {}
data_dict_sessionpacket = {}
data_dict_cardamage = {}
data_dict_cartelemetry = {}
data_dict_carstatus = {}
data_dict_lapdata = {}
data_dict_sessionhistory = {}
data_dict_eventpacket = {}
currentLapTimeInMs = 0
lap_distance = 0.0
throttle = 0.0
brake = 0.0
engineRPM = 0
bestlapms = 0
speed = 0
current_lap_record = []
delta = -100.000
isFastestLap = False
bestlapnum = 0
sessionType = 255
packetType = -1
data_dict_delta = {}
bestlap = []


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


### UDP csomagokat feldolgozó függvény
def udp_server(host='0.0.0.0', port=20777):
    print("im starting the server")
    global track_length
    global tyresetslist
    global bestlapmillisecpermetertodeltacalc
    global data_dict_main
    global mfdPanelIndex_isChanged
    global mfdPanelIndex
    global data_dict_sessionhistory
    global data_dict_sessionpacket
    global data_dict_cartelemetry
    global data_dict_cardamage
    global data_dict_carstatus
    global data_dict_lapdata
    global running_or_not
    global bestlapms
    global currentLapTimeInMs
    global lap_distance
    global throttle
    global brake
    global engineRPM
    global speed
    global delta
    global isFastestLap
    global current_lap_record
    global bestlapnum
    global sessionType
    global packetType
    global data_dict_delta
    global bestlap


    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set the SO_REUSEADDR option to reuse the socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    server_address = (host, port)
    sock.bind(server_address)
    while True:
        start_time = time.time() * 1000
        data, address = sock.recvfrom(65507)
        #start_time = time.time()*1000
        # Parse the data
        header = data[:29]
        telemetry = data[29:]
        h = unpack_header(header)
        #unpacked_packet = h.field6
        packetType = h.field6

        ## SessionPacket
        if h.field6 == 1:
            sp = unpack_sessionpacket(telemetry)
            sessionType = sp.field6
            track_length = sp.field5
            data_dict_sessionpacket = {
                'sessionType': sp.field6,
                'trackLength': sp.field5,
                'pitStopWindowIdealLap': sp.field27,
                'pitStopWindowLatestLap': sp.field28,
                'pitStopRejoinPosition': sp.field29,
                'speedUnit': sp.field43,
            }

        ## LapDataPacket
        elif h.field6 == 2:
            lapdata_time = time.time()*1000 - start_time
            ldp = unpack_lapdatapacket(telemetry, h.field11)
            list = []
            ldp.item_from_lapdatapacket(list)
            data_dict_lapdata = {
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
            }
            data_dict_delta = {
                'lastLapTime': list[0],
                'currentLapTimeInMs': list[1],
                'sector1TimeInMs': list[2],
                'sector2TimeInMs': list[4],
                'lapDistance': int(list[8]),
                'currentLapNum': list[12],
                'sector': list[15],
            }




        ## EventPacket (egyenlőre nem használjuk)
        elif h.field6 == 3:
            ep = unpack_eventpacket(telemetry)
            data_dict_eventpacket = {
                'eventStringCode': ep.field1,
            }
            if ep.field1 == "SEND":
                mfdPanelIndex = 6
                mfdPanelIndex_isChanged = True

            '''elif ep.field1 == "FTLP":
                list = []
                ep.fasteslap(list)
                if len(list) > 0:
                    if list[0] == h.field11:
                        bestlapms = list[1]
                        isFastestLap = True'''



        ## CarTelemetryDataPacket
        elif h.field6 == 6:
            cartelemetry_time = time.time()*1000 - start_time
            ctp = unpack_cartelemetrydatapacket(telemetry, h.field11)
            list = []

            ## Segítség a listaként érkező adatok feldolgozásához
            '''
            0 – Rear Left (RL)
            1 – Rear Right (RR)
            2 – Front Left (FL)
            3 – Front Right (FR)
            '''

            ctp.item_from_cartelemetrydata(list)
            data_dict_cartelemetry = {
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
            }
            throttle = list[21]
            brake = list[23]
            engineRPM = list[26]
            speed = list[20]
            if lap_distance >= 0:
                current_lap_record.clear()
                current_lap_record.extend([currentLapTimeInMs, int(lap_distance), speed])
                #print(current_lap_record)
                #current_lap_datas.append([currentLapTimeInMs, lap_distance, speed])
                #file.write(str(currentLapTimeInMs) + " " + str(lap_distance) + " " + str(speed) + " " + str(engineRPM) + " " + str(throttle) + " " + str(brake) + " " + str(track_length) + " " + str(bestlapms) + "\n")

            ## MFD Panel Index változásának ellenőrzése
            if ctp.field2 != mfdPanelIndex:
                mfdPanelIndex_isChanged = True
                mfdPanelIndex = ctp.field2
            else:
                mfdPanelIndex_isChanged = False

        ## CarStatusPacket
        elif h.field6 == 7:
            csp = unpack_carstatuspacket(telemetry, h.field11)
            list = []
            csp.item_from_carstatuspacket(list)
            data_dict_carstatus = {
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
               }

        ## CarDamagePacket
        elif h.field6 == 10:
            cdp = unpack_cardamagepacket(telemetry, h.field11)
            list = []
            cdp.item_from_cardamagepacket(list)
            data_dict_cardamage = {
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
            }

        ## SessionHistoryPacket (egyenlőre nem használjuk)
        elif h.field6 == 11:
            shp = unpack_sessionhistorypacket(telemetry, h.field11)

            if shp != 404:
                bestlap.clear()
                shp.get_bestlaptimedata(bestlap, shp.field4)
            else:
                pass
            '''if shp != 404:
                if shp.field4 < 101:
                    list = []
                    shp.lapsofmycar(list)
                    data_dict_sessionhistory = {
                        'bestlapms': list[(shp.field4)],
                    }
                    bestlapms = list[(shp.field4)]
            else:
                pass'''

        ## TyreSetsPacket
        elif h.field6 == 12:
            tsp = unpack_tyresetspacket(telemetry)
            if h.field11 == tsp.field1:
                besttyresetslist.clear()
                tsp.get_tyresetdata(besttyresetslist)

        ##log_fájlba írás
        #log_list.append([currentLapTimeInMs, lap_distance, speed, engineRPM, throttle, brake, track_length, bestlapms])

        #end_time = time.time()*1000
        #print(f"Packet was:{unpacked_packet}, Cost ms: {end_time - start_time}")


### A dict törlések és legjobb kör csekkolása még nincs megoldva
def asd():
    global current_lap_record
    data_dict_bestlap_meters = {}
    data_bestlap_sectors = {}
    data_dict_currentlap_sectors = {}
    data_dict_currentlap_odd = {}
    data_dict_currentlap_even = {}
    global delta
    global bestlapnum
    prev_bestlap = 0
    prev_meter = 0
    global packetType
    global data_dict_delta
    global bestlap


    while True:
        try:
            if packetType == 2:
                if (bool(data_dict_bestlap_meters) or bool(data_bestlap_sectors)) and data_dict_delta[
                    'currentLapTimeInMs'] > 0:
                    print(delta)
                    sector = data_dict_delta['sector']
                    data_dict_currentlap_meters.update(
                        {f'{data_dict_delta['lapDistance']}': data_dict_delta['currentLapTimeInMs']})
                    match sector:
                        case 0:
                            delta = 0.000
                        case 1:
                            delta = data_bestlap_sectors['sector1TimeInMs'] - data_dict_delta['sector1TimeInMs']
                            data_dict_currentlap_sectors.update({'sector1TimeInMs': data_dict_delta['sector1TimeInMs']})
                        case 2:
                            delta = data_bestlap_sectors['sector2TimeInMs'] - data_dict_delta['sector2TimeInMs']
                            data_dict_currentlap_sectors.update({'sector2TimeInMs': data_dict_delta['sector2TimeInMs']})

                    if data_dict_delta['lastLapTime'] == bestlap[0]:
                        data_bestlap_sectors = data_dict_currentlap_sectors



                elif data_dict_delta['currentLapNum'] > 1 and data_dict_delta['currentLapTimeInMs'] > 0 and len(
                        bestlap) > 0:
                    if 'sector2TimeInMs' not in data_bestlap_sectors:
                        data_bestlap_sectors = {
                            'sector1TimeInMs': bestlap[1],
                            'sector2TimeInMs': bestlap[3],
                        }

                else:
                    if data_dict_delta['currentLapTimeInMs'] > 0:
                        data_dict_bestlap_meters.update(
                            {f'{data_dict_delta['lapDistance']}': data_dict_delta['currentLapTimeInMs']})

                        if 'sector1TimeInMs' in data_dict_delta:
                            data_bestlap_sectors.update({
                                'sector1TimeInMs': data_dict_delta['sector1TimeInMs'],
                            })
                        if 'sector2TimeInMs' in data_dict_delta:
                            data_bestlap_sectors.update({
                                'sector2TimeInMs': data_dict_delta['sector2TimeInMs'],
                            })
        except Exception as e:
            print(f"Error in flying_delta_calculation: {e}")
            break



def log():
    global track_length
    global tyresetslist
    global bestlapmillisecpermetertodeltacalc
    global data_dict_main
    global mfdPanelIndex_isChanged
    global mfdPanelIndex
    global data_dict_sessionhistory
    global data_dict_sessionpacket
    global data_dict_cartelemetry
    global data_dict_cardamage
    global data_dict_carstatus
    global data_dict_lapdata
    global currentLapTimeInMs
    global lap_distance
    global throttle
    global brake
    global engineRPM
    global bestlapms
    global speed


    if 'currentLapTimeInMs' in data_dict_lapdata:
        currentLapTimeInMs= data_dict_lapdata['currentLapTimeInMs']
    if 'trackLength' in data_dict_main:
        track_length = data_dict_main['trackLength']
    if 'lapDistance' in data_dict_lapdata:
        lap_distance = data_dict_lapdata['lapDistance']
    if 'throttle' in data_dict_cartelemetry:
        throttle = data_dict_cartelemetry['throttle']
    if 'brake' in data_dict_cartelemetry:
        brake = data_dict_cartelemetry['brake']
    if 'engineRPM' in data_dict_cartelemetry:
        engineRPM = data_dict_cartelemetry['engineRPM']
    if 'bestlapms' in data_dict_sessionhistory and data_dict_sessionhistory['bestlapms'] != 0:
        bestlapms = data_dict_sessionhistory['bestlapms']
    if 'speed' in data_dict_cartelemetry:
        speed = data_dict_cartelemetry['speed']
    log_list.append([currentLapTimeInMs, lap_distance, speed, engineRPM, throttle, brake, track_length, bestlapms])
    #print(
    #f"currentLapTimeInMs: {currentLapTimeInMs},  lap_distance: {lap_distance}, speed: {speed}, engineRPM: {engineRPM}, throttle: {throttle}, brake: {brake}, track_length: {track_length}, bestlapms: {bestlapms}")

def log_write_out():
    global log_list
    print("log_write_out")
    with open('Bahrain_20perSec.txt', 'w') as file:
        while True:
            for i in log_list:
                print(i)
                for j in i:
                    file.write(str(j) + " ")
                file.write("\n")
                log_list.remove(i)
            time.sleep(100)


def rpm_leds():
    global data_dict_cartelemetry
    MAX_LED_COUNT = 18  # Number of LED pixels.
    LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
    # LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10  # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
    DRS = 0 # DRS is not active
    RPM = 0
    LED_COUNT = 0

    '''strip = Adafruit_NeoPixel(MAX_LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    while True:

        if 'revLightsPercent' in data_dict_cartelemetry:
            LED_COUNT = int(MAX_LED_COUNT * (data_dict_cartelemetry['revLightsPercent']/100))
            RPM = data_dict_cartelemetry['revLightsPercent']

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

        strip.show()'''
        #print(f"led szám: {LED_COUNT}, revLights érték: {RPM} DRS?: {DRS}")




def event_handler():
    global data_dict_main
    sc = SafetyCar(root)
    if data_dict_main['isSafetyCar'] == True and data_dict_main['isSafetyCarProcess'] == False:
        #print("safety car is out")
        sc.create_safetycar_display()
        sc.safetycar_label_update()
        root.after(5000, sc.safetycar_is_processed)
    else:
        #print("no safety car")
        sc.destroy_safetycar_display()

    root.after(5, event_handler)

if __name__ == '__main__':

    udp_thread = threading.Thread(target=udp_server)
    #flying_delta_thread = threading.Thread(target=asd)
    udp_thread.start()
    #flying_delta_thread.start()

    #rpm_thread = threading.Thread(target=rpm_leds)
    #rpm_thread.start()

    #log_write_out_thread = threading.Thread(target=log_write_out)
    #log_write_out_thread.start()

    root = tk.Tk()
    root.title("Steering Wheel Display")
    root.geometry("800x480")

    ## Csak a kijelzőt mutatja, nincs ablakkeret
    #root.overrideredirect(True)

    M = Master(root)
    M.__call__(mfdPanelIndex)
    root.after(5, M.update_mfd)

    # Run the Tkinter main loop
    root.mainloop()