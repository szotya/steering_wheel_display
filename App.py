import tkinter as tk
import threading
import socket
import time
from UDPunpack import unpack_header, unpack_eventpacket, unpack_sessionpacket, unpack_lapdatapacket, unpack_cartelemetrydatapacket, unpack_carstatuspacket, unpack_cardamagepacket,unpack_tyresetspacket, unpack_sessionhistorypacket
from PIL import Image as PilImage, ImageTk
from listsandconstants import *


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
bestlapmspermeter = []
mfdPanelIndex_isChanged = False
data_dict_tyresets = {}
data_dict_sessionpacket = {}
data_dict_cardamage = {}
data_dict_cartelemetry = {}
data_dict_carstatus = {}
data_dict_lapdata = {}
data_dict_sessionhistory = {}
data_dict_eventpacket = {}


### IP cím lekérdezése
def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('255.255.255.255', 1))
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
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set the SO_REUSEADDR option to reuse the socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    server_address = (host, port)
    sock.bind(server_address)

    while True:
        data, address = sock.recvfrom(65507)
        # Parse the data
        header = data[:29]
        telemetry = data[29:]
        h = unpack_header(header)

        ## SessionPacket
        if h.field6 == 1:
            sp = unpack_sessionpacket(telemetry)
            data_dict_sessionpacket['sessionType'] = sp.field6
            track_length = sp.field5

            data_dict_sessionpacket = {
                'pitStopWindowIdealLap': sp.field27,
                'pitStopWindowLatestLap': sp.field28,
                'pitStopRejoinPosition': sp.field29,
            }

        ## LapDataPacket
        elif h.field6 == 2:
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

        ## EventPacket (egyenlőre nem használjuk)
        elif h.field6 == 3:
            ep = unpack_eventpacket(telemetry)
            data_dict_eventpacket = {
                'eventStringCode': ep.field1,
            }
            if ep.field1 == "SEND":
                mfdPanelIndex = 6
                mfdPanelIndex_isChanged = True



        ## CarTelemetryDataPacket
        elif h.field6 == 6:
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
            shp = unpack_sessionhistorypacket(telemetry)

        ## TyreSetsPacket
        elif h.field6 == 12:
            tsp = unpack_tyresetspacket(telemetry)
            if h.field11 == tsp.field1:
                besttyresetslist.clear()
                tsp.get_tyresetdata(besttyresetslist)


class ConnectDisplay:
    def __init__(self, root):
        self.root = root

    def create_connect_display(self):
        self.canvas = tk.Canvas(root, height=480, width=800, bg="white", highlightthickness=0)
        self.canvas.pack()

        self.logo = PilImage.open("Full_logo-06.png")
        self.logo_resized = self.logo.resize((460,259))
        self.logo_tk_image = ImageTk.PhotoImage(self.logo_resized)
        self.canvas.create_image(400, 200, image=self.logo_tk_image)

        self.ip = tk.Label(self.root, text=f"IP: {get_my_ip()}", fg="black", bg="white", font=("Formula1", 20, "bold"))
        self.ip.place(x=308, y=370)

        self.port = tk.Label(self.root, text="Port: 20777", fg="black", bg="white", font=("Formula1", 20, "bold"))
        self.port.place(x=333, y=400)

        return self.canvas

    def update_connection_display(self):
        if self.canvas is not None and self.canvas.winfo_exists():
            if "eventStringCode" in data_dict_eventpacket:
                self.ip.destroy()
                self.port.destroy()

            self.root.after(100, self.update_connection_display)

class DefaultDisplay:
    def __init__(self, root):
        self.root = root

    def create_default_display(self):
        self.canvas = tk.Canvas(root, height=480, width=800, bg="white")
        self.canvas.pack()
        self.kmphframe = tk.Frame(self.root, height=100, width=200, bg="black")
        self.kmphframe.place(x=0, y=0)

        self.kmph_label = tk.Label(self.kmphframe, text=f"250", fg="white", bg="black", font=("Formula1", 40, "bold"))
        self.kmph_label.place(relx=0.5, rely=0.35, anchor="center")
        self.kmph_text_label = tk.Label(self.kmphframe, text="KM/H", fg="white", bg="black", font=("Formula1", 20, "bold"))
        self.kmph_text_label.place(relx=0.5, rely=0.7, anchor="center")

        self.laptimeframe = tk.Frame(root, height=100, width=402, bg="black")
        self.laptimeframe.place(x=201, y=0)

        self.laptime_label = tk.Label(self.laptimeframe, text="-:--.---", fg="white", bg="black", font=("Formula1", 58, "bold"))
        self.laptime_label.place(relx=0.5, rely=0.25, anchor="center")

        self.laptime_delta_label = tk.Label(self.laptimeframe, text="-0.000", fg="#00ff00", bg="black", font=("Formula1", 20, "bold"))
        self.laptime_delta_label.place(relx=0.5, rely=0.8, anchor="center")


        self.fuelplusframe = tk.Frame(root, height=100, width=202, bg="black")
        self.fuelplusframe.place(x=604, y=0)

        self.fuelplus_label = tk.Label(self.fuelplusframe, text="3.1", fg="white", bg="black", font=("Formula1", 45, "bold"))
        self.fuelplus_label.place(relx=0.5, rely=0.5, anchor="center")

        self.lapnumframe = tk.Frame(self.root, height=120, width=200, bg="black")
        self.lapnumframe.place(x=0, y=101)

        self.lapnum_label = tk.Label(self.lapnumframe, text="L1", fg="cyan", bg="black", font=("Formula1", 50, "bold"))
        self.lapnum_label.place(relx=0.5, rely=0.5, anchor="center")

        self.lefttyresframe = tk.Frame(self.root, height=119, width=200, bg="black")
        self.lefttyresframe.place(x=0, y=222)

        self.lefttyres_front_label = tk.Label(self.lefttyresframe, text="92°C", fg="#ffdb4d", bg="black",
                                         font=("Formula1", 35, "bold"))
        self.lefttyres_front_label.place(relx=0.5, rely=0.3, anchor="center")
        self.lefttyres_rear_label = tk.Label(self.lefttyresframe, text="94°C", fg="#ffdb4d", bg="black",
                                        font=("Formula1", 35, "bold"))
        self.lefttyres_rear_label.place(relx=0.5, rely=0.7, anchor="center")

        self.gear_frame = tk.Frame(self.root, height=240, width=402, bg="black")
        self.gear_frame.place(x=201, y=101)

        self.gear_label = tk.Label(self.gear_frame, text="8", fg="white", bg="black", font=("Formula1", 120, "bold"))
        self.gear_label.place(relx=0.5, rely=0.5, anchor="center")

        self.placeframe = tk.Frame(self.root, height=120, width=202, bg="black")
        self.placeframe.place(x=604, y=101)

        self.place_label = tk.Label(self.placeframe, text="P7", fg="cyan", bg="black", font=("Formula1", 50, "bold"))
        self.place_label.place(relx=0.5, rely=0.5, anchor="center")

        self.righttyresframe = tk.Frame(self.root, height=119, width=202, bg="black")
        self.righttyresframe.place(x=604, y=222)

        self.righttyres_front_label = tk.Label(self.righttyresframe, text="92°C", fg="#ffdb4d", bg="black",
                                          font=("Formula1", 35, "bold"))
        self.righttyres_front_label.place(relx=0.5, rely=0.3, anchor="center")
        self.righttyres_rear_label = tk.Label(self.righttyresframe, text="94°C", fg="#ffdb4d", bg="black",
                                         font=("Formula1", 35, "bold"))
        self.righttyres_rear_label.place(relx=0.5, rely=0.7, anchor="center")

        self.spaceframe = tk.Frame(self.root, height=40, width=806, bg="black")
        self.spaceframe.place(x=0, y=342)

        self.brakeindicatorframe = tk.Frame(self.root, height=114, width=200, bg="darkred")
        self.brakeindicatorframe.place(x=0, y=382.5)
        child_width_brake = float(0.8 * 200)
        self.brakeindicatorfillframe = tk.Frame(self.root, height=114, width=child_width_brake, bg="red")
        self.brakeindicatorfillframe.place(x=0, y=382.5)

        self.ersindicatorframe = tk.Frame(self.root, height=114, width=402, bg="#cca300")
        self.ersindicatorframe.place(x=201, y=382.5)
        child_width_ers = float(0.82 * 402)
        self.ersindicatorfillframe = tk.Frame(self.root, height=114, width=child_width_ers, bg="#ffff00")
        self.ersindicatorfillframe.place(x=201, y=382.5)
        # anvas.create_text(360, 385, text="82%", fill="black", font=("Formula1", 35, "bold"))
        self.ers_percentage_label = tk.Label(self.root, text="82%", fg="white", bg="black", font=("Formula1", 35, "bold"))
        self.ers_percentage_label.place(in_=self.root, x=360, y=375)

        self.acceleratorindicatorframe = tk.Frame(self.root, height=114, width=202, bg="darkgreen")
        self.acceleratorindicatorframe.place(x=604, y=382.5)
        child_width_accelator = float(0.3 * 202)
        self.acceleratorindicatorfillframe = tk.Frame(self.root, height=114, width=child_width_accelator, bg="#00ff00")
        self.acceleratorindicatorfillframe.place(x=604, y=382.5)

        return self.canvas

    def update_labels(self):
        if self.canvas is not None and self.canvas.winfo_exists():
            global data_dict_cartelemetry
            global data_dict_sessionpacket
            global data_dict_sessionhistory
            global data_dict_carstatus
            global data_dict_lapdata
            if 'speed' in data_dict_cartelemetry:
                self.kmph_label.config(text=f"{data_dict_cartelemetry['speed']}")

            if 'gear' in data_dict_cartelemetry:
                if data_dict_cartelemetry['gear'] == -1:
                    self.gear_label.config(text="R")
                elif data_dict_cartelemetry['gear'] == 0:
                    self.gear_label.config(text="N")
                else:
                    self.gear_label.config(text=f"{data_dict_cartelemetry['gear']}")

            if 'throttle' in data_dict_cartelemetry:
                self.acceleratorindicatorfillframe.config(width=float(data_dict_cartelemetry['throttle'] * 202))

            if 'brake' in data_dict_cartelemetry:
                self.brakeindicatorfillframe.config(width=float(data_dict_cartelemetry['brake'] * 200))

            if 'ersStoreEnergy' in data_dict_carstatus:
                stored_energy_in_percentage = data_dict_carstatus['ersStoreEnergy'] / maximum_energy_storage * 100
                self.ersindicatorfillframe.config(
                    width=float((data_dict_carstatus['ersStoreEnergy'] / maximum_energy_storage) * 402))
                self.ers_percentage_label.config(text=f"{stored_energy_in_percentage:.0f}%", font=("Formula1", 35, "bold"))

            if 'RLTyreInnerTemperature' in data_dict_cartelemetry:
                self.lefttyres_front_label.config(text=f"{data_dict_cartelemetry['FLTyreInnerTemperature']}°C")
                self.lefttyres_rear_label.config(text=f"{data_dict_cartelemetry['RLTyreInnerTemperature']}°C")
                self.righttyres_front_label.config(text=f"{data_dict_cartelemetry['FRTyreInnerTemperature']}°C")
                self.righttyres_rear_label.config(text=f"{data_dict_cartelemetry['RRTyreInnerTemperature']}°C")
            if 'fuelInTank' in data_dict_carstatus:
                self.fuelplus_label.config(text=f"{data_dict_carstatus['fuelRemainingLaps']:.0f}")
            if 'currentLapTimeInMs' in data_dict_lapdata:
                laptime = data_dict_lapdata['currentLapTimeInMs']
                if laptime < 59999:
                    seconds = float(laptime / 1000)
                    self.laptime_label.config(text=f"{seconds:.3f}")
                elif 59999 < laptime and laptime < 69999:
                    minutes = int(laptime / 60000)
                    # seconds = float(laptime - minutes * 60000) / 1000
                    string_representation = str(laptime - minutes * 60000)

                    # Insert decimal point at the appropriate position
                    formatted_string = string_representation[:-3] + '.' + string_representation[-3:]

                    # Convert back to float
                    result = '0' + formatted_string
                    self.laptime_label.config(text=f"{minutes}:{result}")
                else:
                    minutes = int(laptime / 60000)
                    seconds = float(laptime - minutes * 60000) / 1000
                    self.laptime_label.config(text=f"{minutes}:{seconds:.3f}")

                if 'currentLapInvalid' == 1:
                    self.laptime_label.config(fg="red")
                else:
                    self.laptime_label.config(fg="white")

            if 'currentLapNum' in data_dict_lapdata:
                self.lapnum_label.config(text=f"L{data_dict_lapdata['currentLapNum']}")
            if 'carPosition' in data_dict_lapdata:
                self.place_label.config(text=f"P{data_dict_lapdata['carPosition']}")

            self.root.after(5, self.update_labels)
class PitStop:
    def __init__(self, root):
        self.root = root

    def create_pitstop_display(self):
        self.canvas = tk.Canvas(root, height=480, width=800, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.pitwindow_text = tk.Label(self.canvas, text="Pit Window", fg="white", bg="black", font=("Formula1", 30, "bold"))
        self.pitwindow_text.place(x=400, y=20, anchor="center")

        self.pitwindowlaps_text = tk.Label(self.canvas, text="LAP 13 - 17", fg="cyan", bg="black", font=("Formula1", 70, "bold"))
        self.pitwindowlaps_text.place(x=400, y=120, anchor="center")

        self.rejoin_text = tk.Label(self.canvas, text="Pit Now Rejoin Position", fg="white", bg="black", font=("Formula1", 20, "bold"))
        self.rejoin_text.place(x=370, y=170, anchor="center")

        self.rejoinpositon = tk.Label(self.canvas, text="20th", fg="cyan", bg="black",
                                    font=("Formula1", 20, "bold"))
        self.rejoinpositon.place(x=540, y=170, anchor="center")

        self.availablebest_text = tk.Label(self.canvas, text="Available Best Sets", fg="white", bg="black", font=("Formula1", 15, "bold"))
        self.availablebest_text.place(x=110, y=380, anchor="center")

        self.soft_img = PilImage.open('tyres/soft.png')
        self.soft_img_resized = self.soft_img.resize((55, 55))
        # Convert the image to a format Tkinter can use
        self.soft_tk_image = ImageTk.PhotoImage(self.soft_img_resized)
        self.canvas.create_image(50, 430, image=self.soft_tk_image)

        self.soft_newest = tk.Label(self.canvas, text="Used", fg="white", bg="black", font=("Formula1", 25, "bold"))
        self.soft_newest.place(x=80, y=397)
        self.soft_best_percent = tk.Label(self.canvas, text="7%", fg="white", bg="black", font=("Formula1", 20, "bold"))
        self.soft_best_percent.place(x=82, y=427)

        self.medium_img = PilImage.open('tyres/medium.png')
        self.medium_img_resized = self.medium_img.resize((55, 55))
        # Convert the image to a format Tkinter can use
        self.medium_tk_image = ImageTk.PhotoImage(self.medium_img_resized)
        self.canvas.create_image(210, 430, image=self.medium_tk_image)

        self.medium_newest = tk.Label(self.canvas, text="Used", fg="white", bg="black", font=("Formula1", 25, "bold"))
        self.medium_newest.place(x=240, y=397)
        self.medium_best_percent = tk.Label(self.canvas, text="12%", fg="white", bg="black", font=("Formula1", 20, "bold"))
        self.medium_best_percent.place(x=242, y=427)

        self.hard_img = PilImage.open('tyres/hard.png')
        self.hard_img_resized = self.hard_img.resize((55, 55))
        # Convert the image to a format Tkinter can use
        self.hard_tk_image = ImageTk.PhotoImage(self.hard_img_resized)
        self.canvas.create_image(370, 430, image=self.hard_tk_image)

        self.hard_newest = tk.Label(self.canvas, text="New", fg="white", bg="black", font=("Formula1", 25, "bold"))
        self.hard_newest.place(x=400, y=397)
        self.hard_best_percent = tk.Label(self.canvas, text="0%", fg="white", bg="black",
                                            font=("Formula1", 20, "bold"))
        self.hard_best_percent.place(x=402, y=427)

        self.inter_img = PilImage.open('tyres/inter.png')
        self.inter_img_resized = self.inter_img.resize((55, 55))
        # Convert the image to a format Tkinter can use
        self.inter_tk_image = ImageTk.PhotoImage(self.inter_img_resized)
        self.canvas.create_image(520, 430, image=self.inter_tk_image)

        self.inter_newest = tk.Label(self.canvas, text="New", fg="white", bg="black", font=("Formula1", 25, "bold"))
        self.inter_newest.place(x=550, y=397)
        self.inter_best_percent = tk.Label(self.canvas, text="0%", fg="white", bg="black",
                                          font=("Formula1", 20, "bold"))
        self.inter_best_percent.place(x=552, y=427)

        self.wet_img = PilImage.open('tyres/wet.png')
        self.wet_img_resized = self.wet_img.resize((55, 55))
        self.wet_tk_image = ImageTk.PhotoImage(self.wet_img_resized)
        self.canvas.create_image(670, 430, image=self.wet_tk_image)

        self.wet_newest = tk.Label(self.canvas, text="New", fg="white", bg="black", font=("Formula1", 25, "bold"))
        self.wet_newest.place(x=700, y=397)
        self.wet_best_percent = tk.Label(self.canvas, text="0%", fg="white", bg="black",
                                           font=("Formula1", 20, "bold"))
        self.wet_best_percent.place(x=702, y=427)

        return self.canvas

    def update_pitstop_labels(self):
        global besttyresetslist
        global data_dict_sessionpacket
        if self.canvas is not None and self.canvas.winfo_exists():
            if len(besttyresetslist) > 0:
                if data_dict_sessionpacket['pitStopWindowIdealLap'] != 0:
                    self.pitwindowlaps_text.config(text=f"LAP {data_dict_sessionpacket['pitStopWindowIdealLap']} - {data_dict_sessionpacket['pitStopWindowLatestLap']}")
                else:
                    self.pitwindowlaps_text.config(text="N/A")

                if data_dict_sessionpacket['pitStopRejoinPosition'] == 1:
                    self.rejoinpositon.config(text="1st")
                elif data_dict_sessionpacket['pitStopRejoinPosition'] == 2:
                    self.rejoinpositon.config(text="2nd")
                elif data_dict_sessionpacket['pitStopRejoinPosition'] == 3:
                    self.rejoinpositon.config(text="3rd")
                else:
                    self.rejoinpositon.config(text=f"{data_dict_sessionpacket['pitStopRejoinPosition']}th")

                bestsoft = besttyresetslist[0][2]
                self.soft_best_percent.config(text=f"{bestsoft}%")
                if bestsoft == 0:
                    self.soft_newest.config(text="New")
                else:
                    self.soft_newest.config(text="Used")

                bestmedium = besttyresetslist[1][2]
                self.medium_best_percent.config(text=f"{bestmedium}%")
                if bestmedium == 0:
                    self.medium_newest.config(text="New")
                else:
                    self.medium_newest.config(text="Used")

                besthard = besttyresetslist[2][2]
                self.hard_best_percent.config(text=f"{besthard}%")
                if besthard == 0:
                    self.hard_newest.config(text="New")
                else:
                    self.hard_newest.config(text="Used")

                bestinter = besttyresetslist[3][2]
                self.inter_best_percent.config(text=f"{bestinter}%")
                if bestinter == 0:
                    self.inter_newest.config(text="New")
                else:
                    self.inter_newest.config(text="Used")

                bestwet = besttyresetslist[4][2]
                self.wet_best_percent.config(text=f"{bestwet}%")
                if bestwet == 0:
                    self.wet_newest.config(text="New")
                else:
                    self.wet_newest.config(text="Used")

            self.root.after(5, self.update_pitstop_labels)
class CarDamage:
    def __init__(self, root):
        self.root = root

    def create_cardamage_display(self):
        self.canvas = tk.Canvas(root, height=480, width=800, bg="black", highlightthickness=0)
        self.canvas.pack()

        #car siluett img
        self.siluett_img = PilImage.open('car_damage_pngs/siluett.png')
        self.siluett_img_resized = self.siluett_img.resize((115, 196))
        # Convert the image to a format Tkinter can use
        self.siluett_tk_image = ImageTk.PhotoImage(self.siluett_img_resized)
        self.canvas.create_image(400, 150, image=self.siluett_tk_image)

        #front left wing
        self.frontleft_img = PilImage.open('car_damage_pngs/frontleft0.png')
        self.frontleft_img_resized = self.frontleft_img.resize((68, 60))
        # Convert the image to a format Tkinter can use
        self.frontleft_tk_image = ImageTk.PhotoImage(self.frontleft_img_resized)
        self.frontleft = self.canvas.create_image(362.5, 69, image=self.frontleft_tk_image)

        #front right wing
        self.frontright_img = PilImage.open('car_damage_pngs/frontright0.png')
        self.frontright_img_resized = self.frontright_img.resize((68, 60))
        # Convert the image to a format Tkinter can use
        self.frontright_tk_image = ImageTk.PhotoImage(self.frontright_img_resized)
        self.frontright = self.canvas.create_image(438, 69, image=self.frontright_tk_image)

        #front left tyre
        self.frontlefttyre_img = PilImage.open('car_damage_pngs/fronttyre0.png')
        self.frontlefttyre_img_resized = self.frontlefttyre_img.resize((29, 53))
        # Convert the image to a format Tkinter can use
        self.frontlefttyre_tk_image = ImageTk.PhotoImage(self.frontlefttyre_img_resized)
        self.frontlefttyre = self.canvas.create_image(342.5, 130.5, image=self.frontlefttyre_tk_image)

        #front left brake
        self.frontleftbrake_img = PilImage.open('car_damage_pngs/brake0.png')
        self.frontleftbrake_img_resized = self.frontlefttyre_img.resize((10, 19))
        # Convert the image to a format Tkinter can use
        self.frontleftbrake_tk_image = ImageTk.PhotoImage(self.frontleftbrake_img_resized)
        self.frontleftbrake = self.canvas.create_image(364.5, 131, image=self.frontleftbrake_tk_image)

        #front right tyre
        self.frontrighttyre_img = PilImage.open('car_damage_pngs/fronttyre0.png')
        self.frontrighttyre_img_resized = self.frontrighttyre_img.resize((29, 53))
        # Convert the image to a format Tkinter can use
        self.frontrighttyre_tk_image = ImageTk.PhotoImage(self.frontrighttyre_img_resized)
        self.frontrighttyre = self.canvas.create_image(457, 130.5, image=self.frontrighttyre_tk_image)

        # front right brake
        self.frontrightbrake_img = PilImage.open('car_damage_pngs/brake0.png')
        self.frontrightbrake_img_resized = self.frontrighttyre_img.resize((10, 19))
        # Convert the image to a format Tkinter can use
        self.frontrightbrake_tk_image = ImageTk.PhotoImage(self.frontrightbrake_img_resized)
        self.frontrightbrake = self.canvas.create_image(436, 131, image=self.frontrightbrake_tk_image)

        #left floor
        self.leftfloor_img = PilImage.open('car_damage_pngs/floorleft0.png')
        self.leftfloor_img_resized = self.leftfloor_img.resize((45, 182))
        # Convert the image to a format Tkinter can use
        self.leftfloor_tk_image = ImageTk.PhotoImage(self.leftfloor_img_resized)
        self.leftfloor = self.canvas.create_image(363.6, 270, image=self.leftfloor_tk_image)

        # right floor
        self.rightfloor_img = PilImage.open('car_damage_pngs/floorright0.png')
        self.rightfloor_img_resized = self.rightfloor_img.resize((45, 182))
        # Convert the image to a format Tkinter can use
        self.rightfloor_tk_image = ImageTk.PhotoImage(self.rightfloor_img_resized)
        self.rightfloor = self.canvas.create_image(436, 270, image=self.rightfloor_tk_image)

        #left side pod
        self.leftsidepod_img = PilImage.open('car_damage_pngs/sideleft0.png')
        self.leftsidepod_img_resized = self.leftsidepod_img.resize((37, 124))
        # Convert the image to a format Tkinter can use
        self.leftsidepod_tk_image = ImageTk.PhotoImage(self.leftsidepod_img_resized)
        self.leftsidepod = self.canvas.create_image(371, 299, image=self.leftsidepod_tk_image)

        # right side pod
        self.rightsidepod_img = PilImage.open('car_damage_pngs/sideright0.png')
        self.rightsidepod_img_resized = self.rightsidepod_img.resize((37, 124))
        # Convert the image to a format Tkinter can use
        self.rightsidepod_tk_image = ImageTk.PhotoImage(self.rightsidepod_img_resized)
        self.rightsidepod = self.canvas.create_image(428.5, 299.4, image=self.rightsidepod_tk_image)

        #engine
        self.engine_img = PilImage.open('car_damage_pngs/engine0.png')
        self.engine_img_resized = self.engine_img.resize((51, 60))
        # Convert the image to a format Tkinter can use
        self.engine_tk_image = ImageTk.PhotoImage(self.engine_img_resized)
        self.engine = self.canvas.create_image(400, 282, image=self.engine_tk_image)

        #gearbox
        self.gearbox_img = PilImage.open('car_damage_pngs/gear0.png')
        self.gearbox_img_resized = self.gearbox_img.resize((14, 47))
        # Convert the image to a format Tkinter can use
        self.gearbox_tk_image = ImageTk.PhotoImage(self.gearbox_img_resized)
        self.gearbox = self.canvas.create_image(400.5, 338.3, image=self.gearbox_tk_image)

        #diffuser
        self.diffuser_img = PilImage.open('car_damage_pngs/diffuser0.png')
        self.diffuser_img_resized = self.diffuser_img.resize((53, 18))
        # Convert the image to a format Tkinter can use
        self.diffuser_tk_image = ImageTk.PhotoImage(self.diffuser_img_resized)
        self.diffuser = self.canvas.create_image(400, 374, image=self.diffuser_tk_image)

        #rear left tyre
        self.rearlefttyre_img = PilImage.open('car_damage_pngs/reartyre0.png')
        self.rearlefttyre_img_resized = self.rearlefttyre_img.resize((32, 53))
        # Convert the image to a format Tkinter can use
        self.rearlefttyre_tk_image = ImageTk.PhotoImage(self.rearlefttyre_img_resized)
        self.rearlefttyre = self.canvas.create_image(341.5, 372, image=self.rearlefttyre_tk_image)

        # rear left brake
        self.rearleftbrake_img = PilImage.open('car_damage_pngs/brake0.png')
        self.rearleftbrake_img_resized = self.rearlefttyre_img.resize((10, 19))
        # Convert the image to a format Tkinter can use
        self.rearleftbrake_tk_image = ImageTk.PhotoImage(self.rearleftbrake_img_resized)
        self.rearleftbrake = self.canvas.create_image(365.5, 373, image=self.rearleftbrake_tk_image)

        #rear right tyre
        self.rearrighttyre_img = PilImage.open('car_damage_pngs/reartyre0.png')
        self.rearrighttyre_img_resized = self.rearrighttyre_img.resize((32, 53))
        # Convert the image to a format Tkinter can use
        self.rearrighttyre_tk_image = ImageTk.PhotoImage(self.rearrighttyre_img_resized)
        self.rearrighttyre = self.canvas.create_image(459, 371.5, image=self.rearrighttyre_tk_image)

        # rear right brake
        self.rearrightbrake_img = PilImage.open('car_damage_pngs/brake0.png')
        self.rearrightbrake_img_resized = self.rearrighttyre_img.resize((10, 19))
        # Convert the image to a format Tkinter can use
        self.rearrightbrake_tk_image = ImageTk.PhotoImage(self.rearrightbrake_img_resized)
        self.rearrightbrake = self.canvas.create_image(435.3, 373, image=self.rearrightbrake_tk_image)

        # rearwing
        self.rearwing_img = PilImage.open('car_damage_pngs/rear0.png')
        self.rearwing_img_resized = self.rearwing_img.resize((91, 36))
        # Convert the image to a format Tkinter can use
        self.rearwing_tk_image = ImageTk.PhotoImage(self.rearwing_img_resized)
        self.rearwing = self.canvas.create_image(400, 403, image=self.rearwing_tk_image)

        # percent circles
        self.frontleftpercent_img = PilImage.open('car_damage_pngs/circle.png')
        self.frontleftpercent_img_resized = self.frontleftpercent_img.resize((117, 117))
        # Convert the image to a format Tkinter can use
        self.frontleftpercent_tk_image = ImageTk.PhotoImage(self.frontleftpercent_img_resized)
        self.frontleftpercent = self.canvas.create_image(232.5, 129, image=self.frontleftpercent_tk_image)
        self.frontrightpercent = self.canvas.create_image(562, 129, image=self.frontleftpercent_tk_image)
        self.rearleftpercent = self.canvas.create_image(232.5, 370, image=self.frontleftpercent_tk_image)
        self.rearrightpercent = self.canvas.create_image(562, 370, image=self.frontleftpercent_tk_image)

        # front left percent text
        self.fl_percent_label = tk.Label(self.root, text="0%", fg="red", bg="black", font=("Formula1", 25, "bold"))
        self.fl_percent_label.place(x=201.5, y=109.5)

        # front right percent text
        self.fr_percent_label = tk.Label(self.root, text="0%", fg="red", bg="black", font=("Formula1", 25, "bold"))
        self.fr_percent_label.place(x=531, y=109.5)

        # rear left percent text
        self.rl_percent_label = tk.Label(self.root, text="0%", fg="red", bg="black", font=("Formula1", 25, "bold"))
        self.rl_percent_label.place(x=191.5, y=351)

        # rear right percent text
        self.rr_percent_label = tk.Label(self.root, text="0%", fg="red", bg="black", font=("Formula1", 25, "bold"))
        self.rr_percent_label.place(x=521, y=351)

        #ERS indicator
        self.ers_img = PilImage.open('car_damage_pngs/ERS_good.png')
        self.ers_img_resized = self.ers_img.resize((150, 76))
        # Convert the image to a format Tkinter can use
        self.ers_tk_image = ImageTk.PhotoImage(self.ers_img_resized)
        self.ers = self.canvas.create_image(90, 50, image=self.ers_tk_image)

        #DRS indicator
        self.drs_img = PilImage.open('car_damage_pngs/DRS_good.png')
        self.drs_img_resized = self.drs_img.resize((150, 76))
        # Convert the image to a format Tkinter can use
        self.drs_tk_image = ImageTk.PhotoImage(self.drs_img_resized)
        self.drs = self.canvas.create_image(710, 50, image=self.drs_tk_image)

        return self.canvas

    def front_wing_left_damage(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((68, 60))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.frontleft_tk_image = new_tk_image
        self.canvas.itemconfig(self.frontleft, image=new_tk_image)

    def front_wing_right_damage(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((68, 60))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.frontright_tk_image = new_tk_image
        self.canvas.itemconfig(self.frontright, image=new_tk_image)

    def front_left_tyre_damage(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((29, 53))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.frontlefttyre_tk_image = new_tk_image
        self.canvas.itemconfig(self.frontlefttyre, image=new_tk_image)

    def front_right_tyre_damage(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((29, 53))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.frontrighttyre_tk_image = new_tk_image
        self.canvas.itemconfig(self.frontrighttyre, image=new_tk_image)

    def rear_left_tyre_damage(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((29, 53))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.rearlefttyre_tk_image = new_tk_image
        self.canvas.itemconfig(self.rearlefttyre, image=new_tk_image)

    def rear_right_tyre_damage(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((29, 53))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.rearrighttyre_tk_image = new_tk_image
        self.canvas.itemconfig(self.rearrighttyre, image=new_tk_image)

    def front_left_brake_damage(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((10, 19))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.frontleftbrake_tk_image = new_tk_image
        self.canvas.itemconfig(self.frontleftbrake, image=new_tk_image)

    def front_right_brake_damage(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((10, 19))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.frontrightbrake_tk_image = new_tk_image
        self.canvas.itemconfig(self.frontrightbrake, image=new_tk_image)

    def rear_left_brake_damage(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((10, 19))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.rearleftbrake_tk_image = new_tk_image
        self.canvas.itemconfig(self.rearleftbrake, image=new_tk_image)

    def rear_right_brake_damage(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((10, 19))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.rearrightbrake_tk_image = new_tk_image
        self.canvas.itemconfig(self.rearrightbrake, image=new_tk_image)

    def rear_wing_damage(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((91, 36))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.rearwing_tk_image = new_tk_image
        self.canvas.itemconfig(self.rearwing, image=new_tk_image)

    def left_floor_damage(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((45, 182))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.leftfloor_tk_image = new_tk_image
        self.canvas.itemconfig(self.leftfloor, image=new_tk_image)

    def right_floor_damage(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((45, 182))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.rightfloor_tk_image = new_tk_image
        self.canvas.itemconfig(self.rightfloor, image=new_tk_image)

    def left_sidepod_damage(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((37, 124))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.leftsidepod_tk_image = new_tk_image
        self.canvas.itemconfig(self.leftsidepod, image=new_tk_image)

    def right_sidepod_damage(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((37, 124))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.rightsidepod_tk_image = new_tk_image
        self.canvas.itemconfig(self.rightsidepod, image=new_tk_image)

    def engine_damage(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((51, 60))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.engine_tk_image = new_tk_image
        self.canvas.itemconfig(self.engine, image=new_tk_image)

    def gearbox_damage(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((14, 47))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.gearbox_tk_image = new_tk_image
        self.canvas.itemconfig(self.gearbox, image=new_tk_image)

    def diffuser_damage(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((53, 18))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.diffuser_tk_image = new_tk_image
        self.canvas.itemconfig(self.diffuser, image=new_tk_image)

    def ers_update(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((150, 76))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.ers_tk_image = new_tk_image
        self.canvas.itemconfig(self.ers, image=new_tk_image)

    def drs_update(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((150, 76))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.drs_tk_image = new_tk_image
        self.canvas.itemconfig(self.drs, image=new_tk_image)

    def update_damage_display(self):
        if self.canvas is not None and self.canvas.winfo_exists():
            global data_dict_cardamage
            if 'frontLeftWingDamage' in data_dict_cardamage:
                fldamage = int(data_dict_cardamage['frontLeftWingDamage'])
                if fldamage < 10:
                    self.front_wing_left_damage(listoffrontwingleftstatus[0])
                elif fldamage < 20:
                    self.front_wing_left_damage(listoffrontwingleftstatus[1])
                elif fldamage < 30:
                    self.front_wing_left_damage(listoffrontwingleftstatus[2])
                elif fldamage < 40:
                    self.front_wing_left_damage(listoffrontwingleftstatus[3])
                elif fldamage < 50:
                    self.front_wing_left_damage(listoffrontwingleftstatus[4])
                elif fldamage < 60:
                    self.front_wing_left_damage(listoffrontwingleftstatus[5])
                elif fldamage < 70:
                    self.front_wing_left_damage(listoffrontwingleftstatus[6])
                elif fldamage < 80:
                    self.front_wing_left_damage(listoffrontwingleftstatus[7])
                elif fldamage < 90:
                    self.front_wing_left_damage(listoffrontwingleftstatus[8])
                elif fldamage < 100:
                    self.front_wing_left_damage(listoffrontwingleftstatus[9])
                else:
                    self.front_wing_left_damage(listoffrontwingleftstatus[10])

            if 'frontRightWingDamage' in data_dict_cardamage:
                frdamage = int(data_dict_cardamage['frontRightWingDamage'])
                if frdamage < 10:
                    self.front_wing_right_damage(listoffrontwingrightstatus[0])
                elif frdamage < 20:
                    self.front_wing_right_damage(listoffrontwingrightstatus[1])
                elif frdamage < 30:
                    self.front_wing_right_damage(listoffrontwingrightstatus[2])
                elif frdamage < 40:
                    self.front_wing_right_damage(listoffrontwingrightstatus[3])
                elif frdamage < 50:
                    self.front_wing_right_damage(listoffrontwingrightstatus[4])
                elif frdamage < 60:
                    self.front_wing_right_damage(listoffrontwingrightstatus[5])
                elif frdamage < 70:
                    self.front_wing_right_damage(listoffrontwingrightstatus[6])
                elif frdamage < 80:
                    self.front_wing_right_damage(listoffrontwingrightstatus[7])
                elif frdamage < 90:
                    self.front_wing_right_damage(listoffrontwingrightstatus[8])
                elif frdamage < 100:
                    self.front_wing_right_damage(listoffrontwingrightstatus[9])
                else:
                    self.front_wing_right_damage(listoffrontwingrightstatus[10])

            if 'FLTyreDamage' in data_dict_cardamage:
                fltdamage = int(data_dict_cardamage['FLTyreDamage'])
                self.fl_percent_label.config(text=data_dict_cardamage['FLTyreDamage'] + "%")
                if fltdamage < 10:
                    self.fl_percent_label.config(fg="#00ff00")
                    self.fl_percent_label.place(x=211.5, y=109.5)
                    self.front_left_tyre_damage(listoffronttyrestatus[0])
                elif fltdamage < 20:
                    self.fl_percent_label.config(fg="#88f612")
                    self.fl_percent_label.place(x=201.5, y=109.5)
                    self.front_left_tyre_damage(listoffronttyrestatus[1])
                elif fltdamage < 30:
                    self.fl_percent_label.config(fg="#aef317")
                    self.fl_percent_label.place(x=201.5, y=109.5)
                    self.front_left_tyre_damage(listoffronttyrestatus[2])
                elif fltdamage < 40:
                    self.fl_percent_label.config(fg="#cff11b")
                    self.fl_percent_label.place(x=201.5, y=109.5)
                    self.front_left_tyre_damage(listoffronttyrestatus[3])
                elif fltdamage < 50:
                    self.fl_percent_label.config(fg="#ebef1f")
                    self.fl_percent_label.place(x=201.5, y=109.5)
                    self.front_left_tyre_damage(listoffronttyrestatus[4])
                elif fltdamage < 60:
                    self.fl_percent_label.config(fg="#fcee21")
                    self.fl_percent_label.place(x=201.5, y=109.5)
                    self.front_left_tyre_damage(listoffronttyrestatus[5])
                elif fltdamage < 70:
                    self.fl_percent_label.config(fg="#fccc1f")
                    self.fl_percent_label.place(x=201.5, y=109.5)
                    self.front_left_tyre_damage(listoffronttyrestatus[6])
                elif fltdamage < 80:
                    self.fl_percent_label.config(fg="#fda61d")
                    self.fl_percent_label.place(x=201.5, y=109.5)
                    self.front_left_tyre_damage(listoffronttyrestatus[7])
                elif fltdamage < 90:
                    self.fl_percent_label.config(fg="#fd7e1b")
                    self.fl_percent_label.place(x=201.5, y=109.5)
                    self.front_left_tyre_damage(listoffronttyrestatus[8])
                elif fltdamage < 100:
                    self.fl_percent_label.config(fg="#fe5519")
                    self.fl_percent_label.place(x=201.5, y=109.5)
                    self.front_left_tyre_damage(listoffronttyrestatus[9])
                else:
                    self.fl_percent_label.config(fg="#ff0015")
                    self.fl_percent_label.place(x=191.5, y=109.5)
                    self.front_left_tyre_damage(listoffronttyrestatus[10])

            if 'FRTyreDamage' in data_dict_cardamage:
                frtdamage = int(data_dict_cardamage['FRTyreDamage'])
                self.fr_percent_label.config(text= data_dict_cardamage['FRTyreDamage'] + "%")
                if frtdamage < 10:
                    self.fr_percent_label.config(fg="#00ff00")
                    self.fr_percent_label.place(x=541, y=109.5)
                    self.front_right_tyre_damage(listoffronttyrestatus[0])
                elif frtdamage < 20:
                    self.fr_percent_label.config(fg="#88f612")
                    self.fr_percent_label.place(x=531, y=109.5)
                    self.front_right_tyre_damage(listoffronttyrestatus[1])
                elif frtdamage < 30:
                    self.fr_percent_label.config(fg="#aef317")
                    self.fr_percent_label.place(x=531, y=109.5)
                    self.front_right_tyre_damage(listoffronttyrestatus[2])
                elif frtdamage < 40:
                    self.fr_percent_label.config(fg="#cff11b")
                    self.fr_percent_label.place(x=531, y=109.5)
                    self.front_right_tyre_damage(listoffronttyrestatus[3])
                elif frtdamage < 50:
                    self.fr_percent_label.config(fg="#ebef1f")
                    self.fr_percent_label.place(x=531, y=109.5)
                    self.front_right_tyre_damage(listoffronttyrestatus[4])
                elif frtdamage < 60:
                    self.fr_percent_label.config(fg="#fcee21")
                    self.fr_percent_label.place(x=531, y=109.5)
                    self.front_right_tyre_damage(listoffronttyrestatus[5])
                elif frtdamage < 70:
                    self.fr_percent_label.config(fg="#fccc1f")
                    self.fr_percent_label.place(x=531, y=109.5)
                    self.front_right_tyre_damage(listoffronttyrestatus[6])
                elif frtdamage < 80:
                    self.fr_percent_label.config(fg="#fda61d")
                    self.fr_percent_label.place(x=531, y=109.5)
                    self.front_right_tyre_damage(listoffronttyrestatus[7])
                elif frtdamage < 90:
                    self.fr_percent_label.config(fg="#fd7e1b")
                    self.fr_percent_label.place(x=531, y=109.5)
                    self.front_right_tyre_damage(listoffronttyrestatus[8])
                elif frtdamage < 100:
                    self.fr_percent_label.config(fg="#fe5519")
                    self.fr_percent_label.place(x=531, y=109.5)
                    self.front_right_tyre_damage(listoffronttyrestatus[9])
                else:
                    self.fr_percent_label.config(fg="#ff0015")
                    self.fr_percent_label.place(x=521, y=109.5)
                    self.front_right_tyre_damage(listoffronttyrestatus[10])

            if 'RLTyreDamage' in data_dict_cardamage:
                rltdamage = int(data_dict_cardamage['RLTyreDamage'])
                self.rl_percent_label.config(text=data_dict_cardamage['RLTyreDamage'] + "%")
                if rltdamage < 10:
                    self.rl_percent_label.config(fg="#00ff00")
                    self.rl_percent_label.place(x=211.5, y=351)
                    self.rear_left_tyre_damage(listofreartyrestatus[0])
                elif rltdamage < 20:
                    self.rl_percent_label.config(fg="#88f612")
                    self.rl_percent_label.place(x=201.5, y=351)
                    self.rear_left_tyre_damage(listofreartyrestatus[1])
                elif rltdamage < 30:
                    self.rl_percent_label.config(fg="#aef317")
                    self.rl_percent_label.place(x=201.5, y=351)
                    self.rear_left_tyre_damage(listofreartyrestatus[2])
                elif rltdamage < 40:
                    self.rl_percent_label.config(fg="#cff11b")
                    self.rl_percent_label.place(x=201.5, y=351)
                    self.rear_left_tyre_damage(listofreartyrestatus[3])
                elif rltdamage < 50:
                    self.rl_percent_label.config(fg="#ebef1f")
                    self.rl_percent_label.place(x=201.5, y=351)
                    self.rear_left_tyre_damage(listofreartyrestatus[4])
                elif rltdamage < 60:
                    self.rl_percent_label.config(fg="#fcee21")
                    self.rl_percent_label.place(x=201.5, y=351)
                    self.rear_left_tyre_damage(listofreartyrestatus[5])
                elif rltdamage < 70:
                    self.rl_percent_label.config(fg="#fccc1f")
                    self.rl_percent_label.place(x=201.5, y=351)
                    self.rear_left_tyre_damage(listofreartyrestatus[6])
                elif rltdamage < 80:
                    self.rl_percent_label.config(fg="#fda61d")
                    self.rl_percent_label.place(x=201.5, y=351)
                    self.rear_left_tyre_damage(listofreartyrestatus[7])
                elif rltdamage < 90:
                    self.rl_percent_label.config(fg="#fd7e1b")
                    self.rl_percent_label.place(x=201.5, y=351)
                    self.rear_left_tyre_damage(listofreartyrestatus[8])
                elif rltdamage < 100:
                    self.rl_percent_label.config(fg="#fe5519")
                    self.rl_percent_label.place(x=201.5, y=351)
                    self.rear_left_tyre_damage(listofreartyrestatus[9])
                else:
                    self.rl_percent_label.config(fg="#ff0015")
                    self.rl_percent_label.place(x=191.5, y=351)
                    self.rear_left_tyre_damage(listofreartyrestatus[10])

            if 'RRTyreDamage' in data_dict_cardamage:
                rrtdamage = int(data_dict_cardamage['RRTyreDamage'])
                self.rr_percent_label.config(text=data_dict_cardamage['RRTyreDamage'] + "%")
                if rrtdamage < 10:
                    self.rr_percent_label.config(fg="#00ff00")
                    self.rr_percent_label.place(x=541, y=351)
                    self.rear_right_tyre_damage(listofreartyrestatus[0])
                elif rrtdamage < 20:
                    self.rr_percent_label.config(fg="#88f612")
                    self.rr_percent_label.place(x=531, y=351)
                    self.rear_right_tyre_damage(listofreartyrestatus[1])
                elif rrtdamage < 30:
                    self.rr_percent_label.config(fg="#aef317")
                    self.rr_percent_label.place(x=531, y=351)
                    self.rear_right_tyre_damage(listofreartyrestatus[2])
                elif rrtdamage < 40:
                    self.rr_percent_label.config(fg="#cff11b")
                    self.rr_percent_label.place(x=531, y=351)
                    self.rear_right_tyre_damage(listofreartyrestatus[3])
                elif rrtdamage < 50:
                    self.rr_percent_label.config(fg="#ebef1f")
                    self.rr_percent_label.place(x=531, y=351)
                    self.rear_right_tyre_damage(listofreartyrestatus[4])
                elif rrtdamage < 60:
                    self.rr_percent_label.config(fg="#fcee21")
                    self.rr_percent_label.place(x=531, y=351)
                    self.rear_right_tyre_damage(listofreartyrestatus[5])
                elif rrtdamage < 70:
                    self.rr_percent_label.config(fg="#fccc1f")
                    self.rr_percent_label.place(x=531, y=351)
                    self.rear_right_tyre_damage(listofreartyrestatus[6])
                elif rrtdamage < 80:
                    self.rr_percent_label.config(fg="#fda61d")
                    self.rr_percent_label.place(x=531, y=351)
                    self.rear_right_tyre_damage(listofreartyrestatus[7])
                elif rrtdamage < 90:
                    self.rr_percent_label.config(fg="#fd7e1b")
                    self.rr_percent_label.place(x=531, y=351)
                    self.rear_right_tyre_damage(listofreartyrestatus[8])
                elif rrtdamage < 100:
                    self.rr_percent_label.config(fg="#fe5519")
                    self.rr_percent_label.place(x=531, y=351)
                    self.rear_right_tyre_damage(listofreartyrestatus[9])
                else:
                    self.rr_percent_label.config(fg="#ff0015")
                    self.rr_percent_label.place(x=521, y=351)
                    self.rear_right_tyre_damage(listofreartyrestatus[10])

            if 'FLBrakeDamage' in data_dict_cardamage:
                flbdamage = int(data_dict_cardamage['FLBrakeDamage'])
                if flbdamage < 10:
                    self.front_left_brake_damage(listofbrakestatus[0])
                elif flbdamage < 20:
                    self.front_left_brake_damage(listofbrakestatus[1])
                elif flbdamage < 30:
                    self.front_left_brake_damage(listofbrakestatus[2])
                elif flbdamage < 40:
                    self.front_left_brake_damage(listofbrakestatus[3])
                elif flbdamage < 50:
                    self.front_left_brake_damage(listofbrakestatus[4])
                elif flbdamage < 60:
                    self.front_left_brake_damage(listofbrakestatus[5])
                elif flbdamage < 70:
                    self.front_left_brake_damage(listofbrakestatus[6])
                elif flbdamage < 80:
                    self.front_left_brake_damage(listofbrakestatus[7])
                elif flbdamage < 90:
                    self.front_left_brake_damage(listofbrakestatus[8])
                elif flbdamage < 100:
                    self.front_left_brake_damage(listofbrakestatus[9])
                else:
                    self.front_left_brake_damage(listofbrakestatus[10])

            if 'FRBrakeDamage' in data_dict_cardamage:
                frbdamage = int(data_dict_cardamage['FRBrakeDamage'])
                if frbdamage < 10:
                    self.front_right_brake_damage(listofbrakestatus[0])
                elif frbdamage < 20:
                    self.front_right_brake_damage(listofbrakestatus[1])
                elif frbdamage < 30:
                    self.front_right_brake_damage(listofbrakestatus[2])
                elif frbdamage < 40:
                    self.front_right_brake_damage(listofbrakestatus[3])
                elif frbdamage < 50:
                    self.front_right_brake_damage(listofbrakestatus[4])
                elif frbdamage < 60:
                    self.front_right_brake_damage(listofbrakestatus[5])
                elif frbdamage < 70:
                    self.front_right_brake_damage(listofbrakestatus[6])
                elif frbdamage < 80:
                    self.front_right_brake_damage(listofbrakestatus[7])
                elif frbdamage < 90:
                    self.front_right_brake_damage(listofbrakestatus[8])
                elif frbdamage < 100:
                    self.front_right_brake_damage(listofbrakestatus[9])
                else:
                    self.front_right_brake_damage(listofbrakestatus[10])

            if 'RLBrakeDamage' in data_dict_cardamage:
                rlbdamage = int(data_dict_cardamage['RLBrakeDamage'])
                if rlbdamage < 10:
                    self.rear_left_brake_damage(listofbrakestatus[0])
                elif rlbdamage < 20:
                    self.rear_left_brake_damage(listofbrakestatus[1])
                elif rlbdamage < 30:
                    self.rear_left_brake_damage(listofbrakestatus[2])
                elif rlbdamage < 40:
                    self.rear_left_brake_damage(listofbrakestatus[3])
                elif rlbdamage < 50:
                    self.rear_left_brake_damage(listofbrakestatus[4])
                elif rlbdamage < 60:
                    self.rear_left_brake_damage(listofbrakestatus[5])
                elif rlbdamage < 70:
                    self.rear_left_brake_damage(listofbrakestatus[6])
                elif rlbdamage < 80:
                    self.rear_left_brake_damage(listofbrakestatus[7])
                elif rlbdamage < 90:
                    self.rear_left_brake_damage(listofbrakestatus[8])
                elif rlbdamage < 100:
                    self.rear_left_brake_damage(listofbrakestatus[9])
                else:
                    self.rear_left_brake_damage(listofbrakestatus[10])

            if 'RRBrakeDamage' in data_dict_cardamage:
                rrbdamage = int(data_dict_cardamage['RRBrakeDamage'])
                if rrbdamage < 10:
                    self.rear_right_brake_damage(listofbrakestatus[0])
                elif rrbdamage < 20:
                    self.rear_right_brake_damage(listofbrakestatus[1])
                elif rrbdamage < 30:
                    self.rear_right_brake_damage(listofbrakestatus[2])
                elif rrbdamage < 40:
                    self.rear_right_brake_damage(listofbrakestatus[3])
                elif rrbdamage < 50:
                    self.rear_right_brake_damage(listofbrakestatus[4])
                elif rrbdamage < 60:
                    self.rear_right_brake_damage(listofbrakestatus[5])
                elif rrbdamage < 70:
                    self.rear_right_brake_damage(listofbrakestatus[6])
                elif rrbdamage < 80:
                    self.rear_right_brake_damage(listofbrakestatus[7])
                elif rrbdamage < 90:
                    self.rear_right_brake_damage(listofbrakestatus[8])
                elif rrbdamage < 100:
                    self.rear_right_brake_damage(listofbrakestatus[9])
                else:
                    self.rear_right_brake_damage(listofbrakestatus[10])

            if 'rearWingDamage' in data_dict_cardamage:
                rwdamage = int(data_dict_cardamage['rearWingDamage'])
                if rwdamage < 10:
                    self.rear_wing_damage(listofrearwingstatus[0])
                elif rwdamage < 20:
                    self.rear_wing_damage(listofrearwingstatus[1])
                elif rwdamage < 30:
                    self.rear_wing_damage(listofrearwingstatus[2])
                elif rwdamage < 40:
                    self.rear_wing_damage(listofrearwingstatus[3])
                elif rwdamage < 50:
                    self.rear_wing_damage(listofrearwingstatus[4])
                elif rwdamage < 60:
                    self.rear_wing_damage(listofrearwingstatus[5])
                elif rwdamage < 70:
                    self.rear_wing_damage(listofrearwingstatus[6])
                elif rwdamage < 80:
                    self.rear_wing_damage(listofrearwingstatus[7])
                elif rwdamage < 90:
                    self.rear_wing_damage(listofrearwingstatus[8])
                elif rwdamage < 100:
                    self.rear_wing_damage(listofrearwingstatus[9])
                else:
                    self.rear_wing_damage(listofrearwingstatus[10])

            if 'floorDamage' in data_dict_cardamage:
                lfdamage = int(data_dict_cardamage['floorDamage'])
                if lfdamage < 10:
                    self.left_floor_damage(listoffloorleftstatus[0])
                elif lfdamage < 20:
                    self.left_floor_damage(listoffloorleftstatus[1])
                elif lfdamage < 30:
                    self.left_floor_damage(listoffloorleftstatus[2])
                elif lfdamage < 40:
                    self.left_floor_damage(listoffloorleftstatus[3])
                elif lfdamage < 50:
                    self.left_floor_damage(listoffloorleftstatus[4])
                elif lfdamage < 60:
                    self.left_floor_damage(listoffloorleftstatus[5])
                elif lfdamage < 70:
                    self.left_floor_damage(listoffloorleftstatus[6])
                elif lfdamage < 80:
                    self.left_floor_damage(listoffloorleftstatus[7])
                elif lfdamage < 90:
                    self.left_floor_damage(listoffloorleftstatus[8])
                elif lfdamage < 100:
                    self.left_floor_damage(listoffloorleftstatus[9])
                else:
                    self.left_floor_damage(listoffloorleftstatus[10])

            if 'floorDamage' in data_dict_cardamage:
                rfdamage = int(data_dict_cardamage['floorDamage'])
                if rfdamage < 10:
                    self.right_floor_damage(listoffloorrightstatus[0])
                elif rfdamage < 20:
                    self.right_floor_damage(listoffloorrightstatus[1])
                elif rfdamage < 30:
                    self.right_floor_damage(listoffloorrightstatus[2])
                elif rfdamage < 40:
                    self.right_floor_damage(listoffloorrightstatus[3])
                elif rfdamage < 50:
                    self.right_floor_damage(listoffloorrightstatus[4])
                elif rfdamage < 60:
                    self.right_floor_damage(listoffloorrightstatus[5])
                elif rfdamage < 70:
                    self.right_floor_damage(listoffloorrightstatus[6])
                elif rfdamage < 80:
                    self.right_floor_damage(listoffloorrightstatus[7])
                elif rfdamage < 90:
                    self.right_floor_damage(listoffloorrightstatus[8])
                elif rfdamage < 100:
                    self.right_floor_damage(listoffloorrightstatus[9])
                else:
                    self.right_floor_damage(listoffloorrightstatus[10])

            if 'sidepodDamage' in data_dict_cardamage:
                lsddamage = int(data_dict_cardamage['sidepodDamage'])
                if lsddamage < 10:
                    self.left_sidepod_damage(listofsidepodleftstatus[0])
                elif lsddamage < 20:
                    self.left_sidepod_damage(listofsidepodleftstatus[1])
                elif lsddamage < 30:
                    self.left_sidepod_damage(listofsidepodleftstatus[2])
                elif lsddamage < 40:
                    self.left_sidepod_damage(listofsidepodleftstatus[3])
                elif lsddamage < 50:
                    self.left_sidepod_damage(listofsidepodleftstatus[4])
                elif lsddamage < 60:
                    self.left_sidepod_damage(listofsidepodleftstatus[5])
                elif lsddamage < 70:
                    self.left_sidepod_damage(listofsidepodleftstatus[6])
                elif lsddamage < 80:
                    self.left_sidepod_damage(listofsidepodleftstatus[7])
                elif lsddamage < 90:
                    self.left_sidepod_damage(listofsidepodleftstatus[8])
                elif lsddamage < 100:
                    self.left_sidepod_damage(listofsidepodleftstatus[9])
                else:
                    self.left_sidepod_damage(listofsidepodleftstatus[10])

            if 'sidepodDamage' in data_dict_cardamage:
                rsddamage = int(data_dict_cardamage['sidepodDamage'])
                if rsddamage < 10:
                    self.right_sidepod_damage(listofsidepodrightstatus[0])
                elif rsddamage < 20:
                    self.right_sidepod_damage(listofsidepodrightstatus[1])
                elif rsddamage < 30:
                    self.right_sidepod_damage(listofsidepodrightstatus[2])
                elif rsddamage < 40:
                    self.right_sidepod_damage(listofsidepodrightstatus[3])
                elif rsddamage < 50:
                    self.right_sidepod_damage(listofsidepodrightstatus[4])
                elif rsddamage < 60:
                    self.right_sidepod_damage(listofsidepodrightstatus[5])
                elif rsddamage < 70:
                    self.right_sidepod_damage(listofsidepodrightstatus[6])
                elif rsddamage < 80:
                    self.right_sidepod_damage(listofsidepodrightstatus[7])
                elif rsddamage < 90:
                    self.right_sidepod_damage(listofsidepodrightstatus[8])
                elif rsddamage < 100:
                    self.right_sidepod_damage(listofsidepodrightstatus[9])
                else:
                    self.right_sidepod_damage(listofsidepodrightstatus[10])

            if 'engineDamage' in data_dict_cardamage:
                edamage = int(data_dict_cardamage['engineDamage'])
                if edamage < 10:
                    self.engine_damage(listofenginestatus[0])
                elif edamage < 20:
                    self.engine_damage(listofenginestatus[1])
                elif edamage < 30:
                    self.engine_damage(listofenginestatus[2])
                elif edamage < 40:
                    self.engine_damage(listofenginestatus[3])
                elif edamage < 50:
                    self.engine_damage(listofenginestatus[4])
                elif edamage < 60:
                    self.engine_damage(listofenginestatus[5])
                elif edamage < 70:
                    self.engine_damage(listofenginestatus[6])
                elif edamage < 80:
                    self.engine_damage(listofenginestatus[7])
                elif edamage < 90:
                    self.engine_damage(listofenginestatus[8])
                elif edamage < 100:
                    self.engine_damage(listofenginestatus[9])
                else:
                    self.engine_damage(listofenginestatus[10])

            if 'gearBoxDamage' in data_dict_cardamage:
                gdamage = int(data_dict_cardamage['gearBoxDamage'])
                if gdamage < 10:
                    self.gearbox_damage(listofgearboxstatus[0])
                elif gdamage < 20:
                    self.gearbox_damage(listofgearboxstatus[1])
                elif gdamage < 30:
                    self.gearbox_damage(listofgearboxstatus[2])
                elif gdamage < 40:
                    self.gearbox_damage(listofgearboxstatus[3])
                elif gdamage < 50:
                    self.gearbox_damage(listofgearboxstatus[4])
                elif gdamage < 60:
                    self.gearbox_damage(listofgearboxstatus[5])
                elif gdamage < 70:
                    self.gearbox_damage(listofgearboxstatus[6])
                elif gdamage < 80:
                    self.gearbox_damage(listofgearboxstatus[7])
                elif gdamage < 90:
                    self.gearbox_damage(listofgearboxstatus[8])
                elif gdamage < 100:
                    self.gearbox_damage(listofgearboxstatus[9])
                else:
                    self.gearbox_damage(listofgearboxstatus[10])

            if 'diffuserDamage' in data_dict_cardamage:
                ddamage = int(data_dict_cardamage['diffuserDamage'])
                if ddamage < 10:
                    self.diffuser_damage(listofdiffuserstatus[0])
                elif ddamage < 20:
                    self.diffuser_damage(listofdiffuserstatus[1])
                elif ddamage < 30:
                    self.diffuser_damage(listofdiffuserstatus[2])
                elif ddamage < 40:
                    self.diffuser_damage(listofdiffuserstatus[3])
                elif ddamage < 50:
                    self.diffuser_damage(listofdiffuserstatus[4])
                elif ddamage < 60:
                    self.diffuser_damage(listofdiffuserstatus[5])
                elif ddamage < 70:
                    self.diffuser_damage(listofdiffuserstatus[6])
                elif ddamage < 80:
                    self.diffuser_damage(listofdiffuserstatus[7])
                elif ddamage < 90:
                    self.diffuser_damage(listofdiffuserstatus[8])
                elif ddamage < 100:
                    self.diffuser_damage(listofdiffuserstatus[9])
                else:
                    self.diffuser_damage(listofdiffuserstatus[10])

            #### ERS hibát meg kell írni
            if 'ersFault' in data_dict_cardamage:
                ersdamage = int(data_dict_cardamage['ersFault'])
                if ersdamage == 0:
                    self.ers_update('car_damage_pngs/ERS_good.png')
                else:
                    self.ers_update('car_damage_pngs/ERS_fault.png')

            #### DRS hibát meg kell írni
            if 'drsFault' in data_dict_cardamage:
                drsdamage = int(data_dict_cardamage['drsFault'])
                if drsdamage == 0:
                    self.drs_update('car_damage_pngs/DRS_good.png')
                else:
                    self.drs_update('car_damage_pngs/DRS_fault.png')

            self.root.after(5, self.update_damage_display)
class Engine:

    def __init__(self, root):
        self.root = root

    def create_engine_display(self):
        self.canvas = tk.Canvas(root, height=480, width=800, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.es_img = PilImage.open('engine/ES_0.png')
        self.es_tk_image = ImageTk.PhotoImage(self.es_img)
        self.es = self.canvas.create_image(599, 120, image=self.es_tk_image)

        self.mguk_img = PilImage.open('engine/MGU-K_0.png')
        self.mguk_tk_image = ImageTk.PhotoImage(self.mguk_img)
        self.mguk = self.canvas.create_image(486, 213, image=self.mguk_tk_image)

        self.mguh_img = PilImage.open('engine/MGU-H_0.png')
        self.mguh_tk_image = ImageTk.PhotoImage(self.mguh_img)
        self.mguh = self.canvas.create_image(700, 232, image=self.mguh_tk_image)

        self.ice_img = PilImage.open('engine/ICE_0.png')
        self.ice_tk_image = ImageTk.PhotoImage(self.ice_img)
        self.ice = self.canvas.create_image(599, 200, image=self.ice_tk_image)

        self.ce_img = PilImage.open('engine/CE_0.png')
        self.ce_tk_image = ImageTk.PhotoImage(self.ce_img)
        self.ce = self.canvas.create_image(600, 198, image=self.ce_tk_image)

        self.tc_img = PilImage.open('engine/TC_0.png')
        self.tc_tk_image = ImageTk.PhotoImage(self.tc_img)
        self.tc = self.canvas.create_image(599, 316.5, image=self.tc_tk_image)

        self.gearbox_img = PilImage.open('engine/GearBox_0.png')
        self.gearbox_tk_image = ImageTk.PhotoImage(self.gearbox_img)
        self.gearbox = self.canvas.create_image(602, 365, image=self.gearbox_tk_image)

        self.guidelines = PilImage.open('engine/help lines.png')
        self.guidelines_tk_image = ImageTk.PhotoImage(self.guidelines)
        self.canvas.create_image(530, 242, image=self.guidelines_tk_image)


        self.mguh_text = tk.Label(self.root, text="MGU-H", font=("Formula1", 30, "bold"), bg="black", fg="white")
        self.mguh_text.place(x=100, y=60)
        self.mguh_percent_label = tk.Label(self.root, text="22%", font=("Formula1", 30, "bold"), bg="black", fg="#00ff00")
        self.mguh_percent_label.place(x=260, y=60)

        self.es_text = tk.Label(self.root, text="ES", font=("Formula1", 30, "bold"), bg="black", fg="white")
        self.es_text.place(x=180, y=114)
        self.es_percent_label = tk.Label(self.root, text="0%", font=("Formula1", 30, "bold"), bg="black", fg="#00ff00")
        self.es_percent_label.place(x=280, y=114)

        self.ce_text = tk.Label(self.root, text="CE", font=("Formula1", 30, "bold"), bg="black", fg="white")
        self.ce_text.place(x=180, y=169)
        self.ce_percent_label = tk.Label(self.root, text="100%", font=("Formula1", 30, "bold"), bg="black", fg="#00ff00")
        self.ce_percent_label.place(x=230, y=169)

        self.ice_text = tk.Label(self.root, text="ICE", font=("Formula1", 30, "bold"), bg="black", fg="white")
        self.ice_text.place(x=170, y=220)
        self.ice_percent_label = tk.Label(self.root, text="100%", font=("Formula1", 30, "bold"), bg="black", fg="#00ff00")
        self.ice_percent_label.place(x=230, y=220)

        self.mguk_text = tk.Label(self.root, text="MGU-K", font=("Formula1", 30, "bold"), bg="black", fg="white")
        self.mguk_text.place(x=100, y=272)
        self.mguk_percent_label = tk.Label(self.root, text="100%", font=("Formula1", 30, "bold"), bg="black", fg="#00ff00")
        self.mguk_percent_label.place(x=230, y=272)

        self.tc_text = tk.Label(self.root, text="TC", font=("Formula1", 30, "bold"), bg="black", fg="white")
        self.tc_text.place(x=180, y=325)
        self.tc_percent_label = tk.Label(self.root, text="100%", font=("Formula1", 30, "bold"), bg="black", fg="#00ff00")
        self.tc_percent_label.place(x=230, y=325)

        self.gearbox_text = tk.Label(self.root, text="GEARBOX", font=("Formula1", 30, "bold"), bg="black", fg="white")
        self.gearbox_text.place(x=50, y=378)
        self.gearbox_percent_label = tk.Label(self.root, text="100%", font=("Formula1", 30, "bold"), bg="black", fg="#00ff00")
        self.gearbox_percent_label.place(x=230, y=378)

        return self.canvas

    def update_mguh_img(self, image_path):
        new_img = PilImage.open(image_path)
        new_tk_image = ImageTk.PhotoImage(new_img)
        self.canvas.itemconfig(self.mguh, image=new_tk_image)
        self.mguh_tk_image = new_tk_image

    def update_mguk_img(self, image_path):
        new_img = PilImage.open(image_path)
        new_tk_image = ImageTk.PhotoImage(new_img)
        self.canvas.itemconfig(self.mguk, image=new_tk_image)
        self.mguk_tk_image = new_tk_image

    def update_es_img(self, image_path):
        new_img = PilImage.open(image_path)
        new_tk_image = ImageTk.PhotoImage(new_img)
        self.canvas.itemconfig(self.es, image=new_tk_image)
        self.es_tk_image = new_tk_image

    def update_ice_img(self, image_path):
        new_img = PilImage.open(image_path)
        new_tk_image = ImageTk.PhotoImage(new_img)
        self.canvas.itemconfig(self.ice, image=new_tk_image)
        self.ice_tk_image = new_tk_image

    def update_ce_img(self, image_path):
        new_img = PilImage.open(image_path)
        new_tk_image = ImageTk.PhotoImage(new_img)
        self.canvas.itemconfig(self.ce, image=new_tk_image)
        self.ce_tk_image = new_tk_image

    def update_tc_img(self, image_path):
        new_img = PilImage.open(image_path)
        new_tk_image = ImageTk.PhotoImage(new_img)
        self.canvas.itemconfig(self.tc, image=new_tk_image)
        self.tc_tk_image = new_tk_image

    def update_gearbox_img(self, image_path):
        new_img = PilImage.open(image_path)
        new_tk_image = ImageTk.PhotoImage(new_img)
        self.canvas.itemconfig(self.gearbox, image=new_tk_image)
        self.gearbox_tk_image = new_tk_image

    def update_engine_display(self):
        global data_dict_cardamage
        if self.canvas is not None and self.canvas.winfo_exists():
            if 'engineMGUHWear' in data_dict_cardamage:
                mguh = int(data_dict_cardamage['engineMGUHWear'])
                self.mguh_percent_label.config(text=str(data_dict_cardamage['engineMGUHWear'])+ "%")
                if mguh < 10:
                    self.mguh_percent_label.config(fg="#00ff00")
                    self.mguh_percent_label.place(x = 280, y = 60)
                    self.update_mguh_img(listofmguhwear[0])
                elif mguh < 20:
                    self.mguh_percent_label.config(fg="#88f612")
                    self.mguh_percent_label.place(x=260, y=60)
                    self.update_mguh_img(listofmguhwear[1])
                elif mguh < 30:
                    self.mguh_percent_label.config(fg="#aef317")
                    self.mguh_percent_label.place(x=260, y=60)
                    self.update_mguh_img(listofmguhwear[2])
                elif mguh < 40:
                    self.mguh_percent_label.config(fg="#cff11b")
                    self.mguh_percent_label.place(x=260, y=60)
                    self.update_mguh_img(listofmguhwear[3])
                elif mguh < 50:
                    self.mguh_percent_label.config(fg="#ebef1f")
                    self.mguh_percent_label.place(x=260, y=60)
                    self.update_mguh_img(listofmguhwear[4])
                elif mguh < 60:
                    self.mguh_percent_label.config(fg="#fcee21")
                    self.mguh_percent_label.place(x=260, y=60)
                    self.update_mguh_img(listofmguhwear[5])
                elif mguh < 70:
                    self.mguh_percent_label.config(fg="#fccc1f")
                    self.mguh_percent_label.place(x=260, y=60)
                    self.update_mguh_img(listofmguhwear[6])
                elif mguh < 80:
                    self.mguh_percent_label.config(fg="#fda61d")
                    self.mguh_percent_label.place(x=260, y=60)
                    self.update_mguh_img(listofmguhwear[7])
                elif mguh < 90:
                    self.mguh_percent_label.config(fg="#fd7e1b")
                    self.mguh_percent_label.place(x=260, y=60)
                    self.update_mguh_img(listofmguhwear[8])
                elif mguh < 100:
                    self.mguh_percent_label.config(fg="#fe5519")
                    self.mguh_percent_label.place(x=260, y=60)
                    self.update_mguh_img(listofmguhwear[9])
                else:
                    self.mguh_percent_label.config(fg="#ff0015")
                    self.mguh_percent_label.place(x=230, y=60)
                    self.update_mguh_img(listofmguhwear[10])

            if 'engineMGUKWear' in data_dict_cardamage:
                mguk = int(data_dict_cardamage['engineMGUKWear'])
                self.mguk_percent_label.config(text=str(data_dict_cardamage['engineMGUKWear']) + "%")
                if mguk < 10:
                    self.mguk_percent_label.config(fg="#00ff00")
                    self.mguk_percent_label.place(x=280, y=272)
                    self.update_mguk_img(listofmgukwear[0])
                elif mguk < 20:
                    self.mguk_percent_label.config(fg="#88f612")
                    self.mguk_percent_label.place(x=260, y=272)
                    self.update_mguk_img(listofmgukwear[1])
                elif mguk < 30:
                    self.mguk_percent_label.config(fg="#aef317")
                    self.mguk_percent_label.place(x=260, y=272)
                    self.update_mguk_img(listofmgukwear[2])
                elif mguk < 40:
                    self.mguk_percent_label.config(fg="#cff11b")
                    self.mguk_percent_label.place(x=260, y=272)
                    self.update_mguk_img(listofmgukwear[3])
                elif mguk < 50:
                    self.mguh_percent_label.config(fg="#ebef1f")
                    self.mguk_percent_label.place(x=260, y=272)
                    self.update_mguk_img(listofmgukwear[4])
                elif mguk < 60:
                    self.mguk_percent_label.config(fg="#fcee21")
                    self.mguk_percent_label.place(x=260, y=272)
                    self.update_mguk_img(listofmgukwear[5])
                elif mguk < 70:
                    self.mguk_percent_label.config(fg="#fccc1f")
                    self.mguk_percent_label.place(x=260, y=272)
                    self.update_mguk_img(listofmgukwear[6])
                elif mguk < 80:
                    self.mguk_percent_label.config(fg="#fda61d")
                    self.mguk_percent_label.place(x=260, y=272)
                    self.update_mguk_img(listofmgukwear[7])
                elif mguk < 90:
                    self.mguh_percent_label.config(fg="#fd7e1b")
                    self.mguk_percent_label.place(x=260, y=272)
                    self.update_mguk_img(listofmgukwear[8])
                elif mguk < 100:
                    self.mguk_percent_label.config(fg="#fe5519")
                    self.mguk_percent_label.place(x=260, y=272)
                    self.update_mguk_img(listofmgukwear[9])
                else:
                    self.mguk_percent_label.config(fg="#ff0015")
                    self.mguk_percent_label.place(x=230, y=272)
                    self.update_mguk_img(listofmgukwear[10])

            if 'engineESWear' in data_dict_cardamage:
                es = int(data_dict_cardamage['engineESWear'])
                self.es_percent_label.config(text=str(data_dict_cardamage['engineESWear']) + "%")
                if es < 10:
                    self.es_percent_label.config(fg="#00ff00")
                    self.es_percent_label.place(x=280, y=114)
                    self.update_es_img(listofeswear[0])
                elif es < 20:
                    self.es_percent_label.config(fg="#88f612")
                    self.es_percent_label.place(x=260, y=114)
                    self.update_es_img(listofeswear[1])
                elif es < 30:
                    self.es_percent_label.config(fg="#aef317")
                    self.es_percent_label.place(x=260, y=114)
                    self.update_es_img(listofeswear[2])
                elif es < 40:
                    self.es_percent_label.config(fg="#cff11b")
                    self.es_percent_label.place(x=260, y=114)
                    self.update_es_img(listofeswear[3])
                elif es < 50:
                    self.es_percent_label.config(fg="#ebef1f")
                    self.es_percent_label.place(x=260, y=114)
                    self.update_es_img(listofeswear[4])
                elif es < 60:
                    self.es_percent_label.config(fg="#fcee21")
                    self.es_percent_label.place(x=260, y=114)
                    self.update_es_img(listofeswear[5])
                elif es < 70:
                    self.es_percent_label.config(fg="#fccc1f")
                    self.es_percent_label.place(x=260, y=114)
                    self.update_es_img(listofeswear[6])
                elif es < 80:
                    self.es_percent_label.config(fg="#fda61d")
                    self.es_percent_label.place(x=260, y=114)
                    self.update_es_img(listofeswear[7])
                elif es < 90:
                    self.es_percent_label.config(fg="#fd7e1b")
                    self.es_percent_label.place(x=260, y=114)
                    self.update_es_img(listofeswear[8])
                elif es < 100:
                    self.es_percent_label.config(fg="#fe5519")
                    self.es_percent_label.place(x=260, y=114)
                    self.update_es_img(listofeswear[9])
                else:
                    self.es_percent_label.config(fg="#ff0015")
                    self.es_percent_label.place(x=230, y=114)
                    self.update_es_img(listofeswear[10])

            if 'engineICEWear' in data_dict_cardamage:
                ice = int(data_dict_cardamage['engineICEWear'])
                self.ice_percent_label.config(text=str(data_dict_cardamage['engineICEWear']) + "%")
                if ice < 10:
                    self.ice_percent_label.config(fg="#00ff00")
                    self.ice_percent_label.place(x=280, y=220)
                    self.update_ice_img(listoficewear[0])
                elif ice < 20:
                    self.ice_percent_label.config(fg="#88f612")
                    self.ice_percent_label.place(x=260, y=220)
                    self.update_ice_img(listoficewear[1])
                elif ice < 30:
                    self.ice_percent_label.config(fg="#aef317")
                    self.ice_percent_label.place(x=260, y=220)
                    self.update_ice_img(listoficewear[2])
                elif ice < 40:
                    self.ice_percent_label.config(fg="#cff11b")
                    self.ice_percent_label.place(x=260, y=220)
                    self.update_ice_img(listoficewear[3])
                elif ice < 50:
                    self.ice_percent_label.config(fg="#ebef1f")
                    self.ice_percent_label.place(x=260, y=220)
                    self.update_ice_img(listoficewear[4])
                elif ice < 60:
                    self.ice_percent_label.config(fg="#fcee21")
                    self.ice_percent_label.place(x=260, y=220)
                    self.update_ice_img(listoficewear[5])
                elif ice < 70:
                    self.ice_percent_label.config(fg="#fccc1f")
                    self.ice_percent_label.place(x=260, y=220)
                    self.update_ice_img(listoficewear[6])
                elif ice < 80:
                    self.ice_percent_label.config(fg="#fda61d")
                    self.ice_percent_label.place(x=260, y=220)
                    self.update_ice_img(listoficewear[7])
                elif ice < 90:
                    self.ice_percent_label.config(fg="#fd7e1b")
                    self.ice_percent_label.place(x=260, y=220)
                    self.update_ice_img(listoficewear[8])
                elif ice < 100:
                    self.ice_percent_label.config(fg="#fe5519")
                    self.ice_percent_label.place(x=260, y=220)
                    self.update_ice_img(listoficewear[9])
                else:
                    self.ice_percent_label.config(fg="#ff0015")
                    self.ice_percent_label.place(x=230, y=220)
                    self.update_ice_img(listoficewear[10])

            if 'engineCEWear' in data_dict_cardamage:
                ce = int(data_dict_cardamage['engineCEWear'])
                self.ce_percent_label.config(text=str(data_dict_cardamage['engineCEWear']) + "%")
                if ce < 10:
                    self.ce_percent_label.config(fg="#00ff00")
                    self.ce_percent_label.place(x=280, y=169)
                    self.update_ce_img(listofcewear[0])
                elif ce < 20:
                    self.ce_percent_label.config(fg="#88f612")
                    self.ce_percent_label.place(x=260, y=169)
                    self.update_ce_img(listofcewear[1])
                elif ce < 30:
                    self.ce_percent_label.config(fg="#aef317")
                    self.ce_percent_label.place(x=260, y=169)
                    self.update_ce_img(listofcewear[2])
                elif ce < 40:
                    self.ce_percent_label.config(fg="#cff11b")
                    self.ce_percent_label.place(x=260, y=169)
                    self.update_ce_img(listofcewear[3])
                elif ce < 50:
                    self.ce_percent_label.config(fg="#ebef1f")
                    self.ce_percent_label.place(x=260, y=169)
                    self.update_ce_img(listofcewear[4])
                elif ce < 60:
                    self.ce_percent_label.config(fg="#fcee21")
                    self.ce_percent_label.place(x=260, y=169)
                    self.update_ce_img(listofcewear[5])
                elif ce < 70:
                    self.ce_percent_label.config(fg="#fccc1f")
                    self.ce_percent_label.place(x=260, y=169)
                    self.update_ce_img(listofcewear[6])
                elif ce < 80:
                    self.ce_percent_label.config(fg="#fda61d")
                    self.ce_percent_label.place(x=260, y=169)
                    self.update_ce_img(listofcewear[7])
                elif ce < 90:
                    self.ce_percent_label.config(fg="#fd7e1b")
                    self.ce_percent_label.place(x=260, y=169)
                    self.update_ce_img(listofcewear[8])
                elif ce < 100:
                    self.ce_percent_label.config(fg="#fe5519")
                    self.ce_percent_label.place(x=260, y=169)
                    self.update_ce_img(listofcewear[9])
                else:
                    self.ce_percent_label.config(fg="#ff0015")
                    self.ce_percent_label.place(x=230, y=169)
                    self.update_ce_img(listofcewear[10])

            if 'engineTCWear' in data_dict_cardamage:
                tc = int(data_dict_cardamage['engineTCWear'])
                self.tc_percent_label.config(text=str(data_dict_cardamage['engineTCWear']) + "%")
                if tc < 10:
                    self.tc_percent_label.config(fg="#00ff00")
                    self.tc_percent_label.place(x=280, y=325)
                    self.update_tc_img(listoftcwear[0])
                elif tc < 20:
                    self.tc_percent_label.config(fg="#88f612")
                    self.tc_percent_label.place(x=260, y=325)
                    self.update_tc_img(listoftcwear[1])
                elif tc < 30:
                    self.tc_percent_label.config(fg="#aef317")
                    self.tc_percent_label.place(x=260, y=325)
                    self.update_tc_img(listoftcwear[2])
                elif tc < 40:
                    self.tc_percent_label.config(fg="#cff11b")
                    self.tc_percent_label.place(x=260, y=325)
                    self.update_tc_img(listoftcwear[3])
                elif tc < 50:
                    self.tc_percent_label.config(fg="#ebef1f")
                    self.tc_percent_label.place(x=260, y=325)
                    self.update_tc_img(listoftcwear[4])
                elif tc < 60:
                    self.tc_percent_label.config(fg="#fcee21")
                    self.tc_percent_label.place(x=260, y=325)
                    self.update_tc_img(listoftcwear[5])
                elif tc < 70:
                    self.tc_percent_label.config(fg="#fccc1f")
                    self.tc_percent_label.place(x=260, y=325)
                    self.update_tc_img(listoftcwear[6])
                elif tc < 80:
                    self.tc_percent_label.config(fg="#fda61d")
                    self.tc_percent_label.place(x=260, y=325)
                    self.update_tc_img(listoftcwear[7])
                elif tc < 90:
                    self.tc_percent_label.config(fg="#fd7e1b")
                    self.tc_percent_label.place(x=260, y=325)
                    self.update_tc_img(listoftcwear[8])
                elif tc < 100:
                    self.tc_percent_label.config(fg="#fe5519")
                    self.tc_percent_label.place(x=260, y=325)
                    self.update_tc_img(listoftcwear[9])
                else:
                    self.tc_percent_label.config(fg="#ff0015")
                    self.tc_percent_label.place(x=230, y=325)
                    self.update_tc_img(listoftcwear[10])

            if 'gearBoxDamage' in data_dict_cardamage:
                gb = int(data_dict_cardamage['gearBoxDamage'])
                self.gearbox_percent_label.config(text=str(data_dict_cardamage['gearBoxDamage']) + "%")
                if gb < 10:
                    self.gearbox_percent_label.config(fg="#00ff00")
                    self.gearbox_percent_label.place(x=280, y=378)
                    self.update_gearbox_img(listofgearboxwear[0])
                elif gb < 20:
                    self.gearbox_percent_label.config(fg="#88f612")
                    self.gearbox_percent_label.place(x=260, y=378)
                    self.update_gearbox_img(listofgearboxwear[1])
                elif gb < 30:
                    self.gearbox_percent_label.config(fg="#aef317")
                    self.gearbox_percent_label.place(x=260, y=378)
                    self.update_gearbox_img(listofgearboxwear[2])
                elif gb < 40:
                    self.gearbox_percent_label.config(fg="#cff11b")
                    self.gearbox_percent_label.place(x=260, y=378)
                    self.update_gearbox_img(listofgearboxwear[3])
                elif gb < 50:
                    self.gearbox_percent_label.config(fg="#ebef1f")
                    self.gearbox_percent_label.place(x=260, y=378)
                    self.update_gearbox_img(listofgearboxwear[4])
                elif gb < 60:
                    self.gearbox_percent_label.config(fg="#fcee21")
                    self.gearbox_percent_label.place(x=260, y=378)
                    self.update_gearbox_img(listofgearboxwear[5])
                elif gb < 70:
                    self.gearbox_percent_label.config(fg="#fccc1f")
                    self.gearbox_percent_label.place(x=260, y=378)
                    self.update_gearbox_img(listofgearboxwear[6])
                elif gb < 80:
                    self.gearbox_percent_label.config(fg="#fda61d")
                    self.gearbox_percent_label.place(x=260, y=378)
                    self.update_gearbox_img(listofgearboxwear[7])
                elif gb < 90:
                    self.gearbox_percent_label.config(fg="#fd7e1b")
                    self.gearbox_percent_label.place(x=260, y=378)
                    self.update_gearbox_img(listofgearboxwear[8])
                elif gb < 100:
                    self.gearbox_percent_label.config(fg="#fe5519")
                    self.gearbox_percent_label.place(x=260, y=378)
                    self.update_gearbox_img(listofgearboxwear[9])
                else:
                    self.gearbox_percent_label.config(fg="#ff0015")
                    self.gearbox_percent_label.place(x=230, y=378)
                    self.update_gearbox_img(listofgearboxwear[10])

            self.root.after(5, self.update_engine_display)
class CarTemperature:
    def __init__(self, root):
        self.root = root

    def create_cartemp_display(self):
        self.canvas = tk.Canvas(root, height=480, width=800, bg="black",highlightthickness=0)
        self.canvas.pack()

        self.siluett_img = PilImage.open('car_temp_pngs/car_siluett.png')
        self.siluett_img_resized = self.siluett_img.resize((141, 382))
        # Convert the image to a format Tkinter can use
        self.siluett_tk_image = ImageTk.PhotoImage(self.siluett_img_resized)
        self.canvas.create_image(408, 248, image=self.siluett_tk_image)
        # Create a label in the Tkinter window
        #siluett = tk.Label(self.root, image=self.siluett_tk_image, bg="black")
        #siluett.place(x=86, y=35)

        self.img = PilImage.open('car_temp_pngs/good_temp_motor.png')
        self.img_resized = self.img.resize((51, 60))
        # Convert the image to a format Tkinter can use
        self.tk_image = ImageTk.PhotoImage(self.img_resized)
        self.engine = self.canvas.create_image(408, 300, image=self.tk_image)

        self.fl_img = PilImage.open('car_temp_pngs/good_temp_fronttyre.png')
        self.fl_img_resized = self.fl_img.resize((29, 53))
        # Convert the image to a format Tkinter can use
        self.fl_tk_image = ImageTk.PhotoImage(self.fl_img_resized)
        # Create a label in the Tkinter window
        self.frontleft = self.canvas.create_image(351, 147, image=self.fl_tk_image)

        self.fl_brake_img = PilImage.open('car_temp_pngs/good_temp_brake.png')
        self.fl_brake_img_resized = self.fl_brake_img.resize((10, 19))
        # Convert the image to a format Tkinter can use
        self.fl_brake_tk_image = ImageTk.PhotoImage(self.fl_brake_img_resized)
        # Create a label in the Tkinter window
        self.frontleftbrake = self.canvas.create_image(373, 148, image=self.fl_brake_tk_image)

        self.fr_img = PilImage.open('car_temp_pngs/good_temp_fronttyre.png')
        self.fr_img_resized = self.fr_img.resize((29, 53))
        # Convert the image to a format Tkinter can use
        self.fr_tk_image = ImageTk.PhotoImage(self.fr_img_resized)
        # Create a label in the Tkinter window
        self.frontright = self.canvas.create_image(465, 147, image=self.fr_tk_image)

        self.fr_brake_img = PilImage.open('car_temp_pngs/good_temp_brake.png')
        self.fr_brake_img_resized = self.fr_brake_img.resize((10, 19))
        # Convert the image to a format Tkinter can use
        self.fr_brake_tk_image = ImageTk.PhotoImage(self.fr_brake_img_resized)
        # Create a label in the Tkinter window
        self.frontrightbrake =self.canvas.create_image(443, 148, image=self.fr_brake_tk_image)


        self.rl_img = PilImage.open('car_temp_pngs/good_temp_reartyre.png')
        self.rl_img_resized = self.fl_img.resize((32, 53))
        # Convert the image to a format Tkinter can use
        self.rl_tk_image = ImageTk.PhotoImage(self.rl_img_resized)
        # Create a label in the Tkinter window
        self.rearleft = self.canvas.create_image(350, 390, image=self.rl_tk_image)

        self.rl_brake_img = PilImage.open('car_temp_pngs/good_temp_brake.png')
        self.rl_brake_img_resized = self.rl_brake_img.resize((10, 19))
        # Convert the image to a format Tkinter can use
        self.rl_brake_tk_image = ImageTk.PhotoImage(self.rl_brake_img_resized)
        # Create a label in the Tkinter window
        self.rearleftbrake = self.canvas.create_image(373, 391, image=self.rl_brake_tk_image)

        self.rr_img = PilImage.open('car_temp_pngs/good_temp_reartyre.png')
        self.rr_img_resized = self.rr_img.resize((32, 53))
        # Convert the image to a format Tkinter can use
        self.rr_tk_image = ImageTk.PhotoImage(self.rr_img_resized)
        # Create a label in the Tkinter window
        self.rearright = self.canvas.create_image(468, 390, image=self.rr_tk_image)

        self.rr_brake_img = PilImage.open('car_temp_pngs/good_temp_brake.png')
        self.rr_brake_img_resized = self.rr_brake_img.resize((10, 19))
        # Convert the image to a format Tkinter can use
        self.rr_brake_tk_image = ImageTk.PhotoImage(self.rr_brake_img_resized)
        # Create a label in the Tkinter window
        self.rearrightbrake =self.canvas.create_image(444, 391, image=self.rr_brake_tk_image)

        self.fl_symbols_img = PilImage.open('car_temp_pngs/symbol_def.png')
        self.fl_symbols_img_resized = self.fl_symbols_img.resize((29, 101))
        self.fl_symbols_tk_image = ImageTk.PhotoImage(self.fl_symbols_img_resized)
        self.canvas.create_image(290, 148, image=self.fl_symbols_tk_image)

        self.rl_symbols_img = PilImage.open('car_temp_pngs/symbol_def.png')
        self.rl_symbols_img_resized = self.rl_symbols_img.resize((29, 101))
        self.rl_symbols_tk_image = ImageTk.PhotoImage(self.rl_symbols_img_resized)
        self.canvas.create_image(290, 390, image=self.rl_symbols_tk_image)

        self.fr_symbols_img = PilImage.open('car_temp_pngs/symbol_def.png')
        self.fr_symbols_img_resized = self.fr_symbols_img.resize((29, 101))
        self.fr_symbols_tk_image = ImageTk.PhotoImage(self.fr_symbols_img_resized)
        self.canvas.create_image(520, 148, image=self.fr_symbols_tk_image)

        self.rr_symbols_img = PilImage.open('car_temp_pngs/symbol_def.png')
        self.rr_symbols_img_resized = self.rr_symbols_img.resize((29, 101))
        self.rr_symbols_tk_image = ImageTk.PhotoImage(self.rr_symbols_img_resized)
        self.canvas.create_image(520, 390, image=self.rr_symbols_tk_image)

        self.fl_inner_temp_label = tk.Label(self.root, text="92°C", fg="#00ff00", bg="black", font=("Formula1", 20, "bold"))
        self.fl_inner_temp_label.place(x=207, y=88)
        self.fl_outer_temp_label = tk.Label(self.root, text="92°C", fg="#00ff00", bg="black",font=("Formula1", 20, "bold"))
        self.fl_outer_temp_label.place(x=207, y=128)
        self.fl_brake_temp_label = tk.Label(self.root, text="692°C", fg="#00ff00", bg="black",font=("Formula1", 20, "bold"))
        self.fl_brake_temp_label.place(x=197, y=168)

        self.rl_inner_temp_label = tk.Label(self.root, text="92°C", fg="#00ff00", bg="black",font=("Formula1", 20, "bold"))
        self.rl_inner_temp_label.place(x=207, y=330)
        self.rl_outer_temp_label = tk.Label(self.root, text="92°C", fg="#00ff00", bg="black",font=("Formula1", 20, "bold"))
        self.rl_outer_temp_label.place(x=207, y=370)
        self.rl_brake_temp_label = tk.Label(self.root, text="692°C", fg="#00ff00", bg="black",font=("Formula1", 20, "bold"))
        self.rl_brake_temp_label.place(x=197, y=410)

        self.fr_inner_temp_label = tk.Label(self.root, text="92°C", fg="#00ff00", bg="black",font=("Formula1", 20, "bold"))
        self.fr_inner_temp_label.place(x=540, y=88)
        self.fr_outer_temp_label = tk.Label(self.root, text="92°C", fg="#00ff00", bg="black",font=("Formula1", 20, "bold"))
        self.fr_outer_temp_label.place(x=540, y=128)
        self.fr_brake_temp_label = tk.Label(self.root, text="692°C", fg="#00ff00", bg="black",font=("Formula1", 20, "bold"))
        self.fr_brake_temp_label.place(x=540, y=168)

        self.rr_inner_temp_label = tk.Label(self.root, text="92°C", fg="#00ff00", bg="black",font=("Formula1", 20, "bold"))
        self.rr_inner_temp_label.place(x=540, y=330)
        self.rr_outer_temp_label = tk.Label(self.root, text="92°C", fg="#00ff00", bg="black",font=("Formula1", 20, "bold"))
        self.rr_outer_temp_label.place(x=540, y=370)
        self.rr_brake_temp_label = tk.Label(self.root, text="692°C", fg="#00ff00", bg="black",font=("Formula1", 20, "bold"))
        self.rr_brake_temp_label.place(x=540, y=410)

        self.motor_temp_label = tk.Label(self.root, text="102°C", fg="#00ff00", bg="black",font=("Formula1", 30, "bold"), padx=15, pady=2)
        self.motor_temp_label.place(x=410, y=248, anchor="center")

        return self.canvas

    def update_fl_tyre(self,image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((29, 53))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.fl_tk_image = new_tk_image
        self.canvas.itemconfig(self.frontleft, image=new_tk_image)
          # keep a reference to the image

    def update_fr_tyre(self,image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((29, 53))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.canvas.itemconfig(self.frontright, image=new_tk_image)
        self.fr_tk_image = new_tk_image  # keep a reference to the image

    def update_rl_tyre(self,image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((32, 53))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.canvas.itemconfig(self.rearleft, image=new_tk_image)
        self.rl_tk_image = new_tk_image  # keep a reference to the image

    def update_rr_tyre(self,image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((32, 53))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.canvas.itemconfig(self.rearright, image=new_tk_image)
        self.rr_tk_image = new_tk_image  # keep a reference to the image

    def update_fl_brake(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((10, 19))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.canvas.itemconfig(self.frontleftbrake, image=new_tk_image)
        self.fl_brake_tk_image = new_tk_image

    def update_fr_brake(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((10, 19))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.canvas.itemconfig(self.frontrightbrake, image=new_tk_image)
        self.fr_brake_tk_image = new_tk_image

    def update_rl_brake(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((10, 19))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.canvas.itemconfig(self.rearleftbrake, image=new_tk_image)
        self.rl_brake_tk_image = new_tk_image

    def update_rr_brake(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((10, 19))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.canvas.itemconfig(self.rearrightbrake, image=new_tk_image)
        self.rr_brake_tk_image = new_tk_image

    def update_engine(self, image_path):
        new_img = PilImage.open(image_path)
        new_img_resized = new_img.resize((51, 60))
        new_tk_image = ImageTk.PhotoImage(new_img_resized)
        self.canvas.itemconfig(self.engine, image=new_tk_image)
        self.tk_image = new_tk_image

    def update_temp_labels(self):
        if self.canvas is not None and self.canvas.winfo_exists():
            global data_dict_cartelemetry
            if 'FLTyreInnerTemperature' in data_dict_cartelemetry:
                self.fl_inner_temp_label.config(text=f"{data_dict_cartelemetry['FLTyreInnerTemperature']}°C")
                if int(data_dict_cartelemetry['FLTyreInnerTemperature']) <= 70:
                    self.update_fl_tyre(listoffronttyres[0])
                    self.fl_inner_temp_label.config(fg="#00ffff")
                elif int(data_dict_cartelemetry['FLTyreInnerTemperature']) <= 90:
                    self.update_fl_tyre(listoffronttyres[1])
                    self.fl_inner_temp_label.config(fg="#00ffaa")
                elif int(data_dict_cartelemetry['FLTyreInnerTemperature']) <= 105:
                    self.update_fl_tyre(listoffronttyres[2])
                    self.fl_inner_temp_label.config(fg="#00ff00")
                elif int(data_dict_cartelemetry['FLTyreInnerTemperature']) <= 110:
                    self.update_fl_tyre(listoffronttyres[3])
                    self.fl_inner_temp_label.config(fg="#fccc1f")
                elif int(data_dict_cartelemetry['FLTyreInnerTemperature']) > 110:
                    self.update_fl_tyre(listoffronttyres[4])
                    self.fl_inner_temp_label.config(fg="#fe2b17")

            if 'FLTyreSurfaceTemperature' in data_dict_cartelemetry:
                self.fl_outer_temp_label.config(text=f"{data_dict_cartelemetry['FLTyreSurfaceTemperature']}°C")
                if int(data_dict_cartelemetry['FLTyreSurfaceTemperature']) <= 70:
                    self.fl_outer_temp_label.config(fg="#00ffff")
                elif int(data_dict_cartelemetry['FLTyreSurfaceTemperature']) <= 90:
                    self.fl_outer_temp_label.config(fg="#00ffaa")
                elif int(data_dict_cartelemetry['FLTyreSurfaceTemperature']) <= 105:
                    self.fl_outer_temp_label.config(fg="#00ff00")
                elif int(data_dict_cartelemetry['FLTyreSurfaceTemperature']) <= 110:
                    self.fl_outer_temp_label.config(fg="#fccc1f")
                elif int(data_dict_cartelemetry['FLTyreSurfaceTemperature']) > 110:
                    self.fl_outer_temp_label.config(fg="#fe2b17")

            if 'FLBrakeTemperature' in data_dict_cartelemetry:
                self.fl_brake_temp_label.config(text=f"{data_dict_cartelemetry['FLBrakeTemperature']}°C")
                if int(data_dict_cartelemetry['FLBrakeTemperature']) <= 350:
                    self.update_fl_brake(listofbrakes[0])
                    self.fl_brake_temp_label.config(fg="#00ffff")
                elif int(data_dict_cartelemetry['FLBrakeTemperature']) <= 450:
                    self.update_fl_brake(listofbrakes[1])
                    self.fl_brake_temp_label.config(fg="#00ffaa")
                elif int(data_dict_cartelemetry['FLBrakeTemperature']) <= 750:
                    self.update_fl_brake(listofbrakes[2])
                    self.fl_brake_temp_label.config(fg="#00ff00")
                elif int(data_dict_cartelemetry['FLBrakeTemperature']) <= 950:
                    self.update_fl_brake(listofbrakes[3])
                    self.fl_brake_temp_label.config(fg="#fccc1f")
                elif int(data_dict_cartelemetry['FLBrakeTemperature']) > 950:
                    self.update_fl_brake(listofbrakes[4])
                    self.fl_brake_temp_label.config(fg="#fe2b17")

            if 'RLTyreInnerTemperature' in data_dict_cartelemetry:
                self.rl_inner_temp_label.config(text=f"{data_dict_cartelemetry['RLTyreInnerTemperature']}°C")
                if int(data_dict_cartelemetry['RLTyreInnerTemperature']) <= 70:
                    self.update_rl_tyre(listofreartyres[0])
                    self.rl_inner_temp_label.config(fg="#00ffff")
                elif int(data_dict_cartelemetry['RLTyreInnerTemperature']) <= 90:
                    self.update_rl_tyre(listofreartyres[1])
                    self.rl_inner_temp_label.config(fg="#00ffaa")
                elif int(data_dict_cartelemetry['RLTyreInnerTemperature']) <= 105:
                    self.update_rl_tyre(listofreartyres[2])
                    self.rl_inner_temp_label.config(fg="#00ff00")
                elif int(data_dict_cartelemetry['RLTyreInnerTemperature']) <= 110:
                    self.update_rl_tyre(listofreartyres[3])
                    self.rl_inner_temp_label.config(fg="#fccc1f")
                elif int(data_dict_cartelemetry['RLTyreInnerTemperature']) > 110:
                    self.update_rl_tyre(listofreartyres[4])
                    self.rl_inner_temp_label.config(fg="#fe2b17")

            if 'RLTyreSurfaceTemperature' in data_dict_cartelemetry:
                self.rl_outer_temp_label.config(text=f"{data_dict_cartelemetry['RLTyreSurfaceTemperature']}°C")
                if int(data_dict_cartelemetry['RLTyreSurfaceTemperature']) <= 70:
                    self.rl_outer_temp_label.config(fg="#00ffff")
                elif int(data_dict_cartelemetry['RLTyreSurfaceTemperature']) <= 90:
                    self.rl_outer_temp_label.config(fg="#00ffaa")
                elif int(data_dict_cartelemetry['RLTyreSurfaceTemperature']) <= 105:
                    self.rl_outer_temp_label.config(fg="#00ff00")
                elif int(data_dict_cartelemetry['RLTyreSurfaceTemperature']) <= 110:
                    self.rl_outer_temp_label.config(fg="#fccc1f")
                elif int(data_dict_cartelemetry['RLTyreSurfaceTemperature']) > 110:
                    self.rl_outer_temp_label.config(fg="#fe2b17")

            if 'RLBrakeTemperature' in data_dict_cartelemetry:
                self.rl_brake_temp_label.config(text=f"{data_dict_cartelemetry['RLBrakeTemperature']}°C")
                if int(data_dict_cartelemetry['RLBrakeTemperature']) <= 350:
                    self.update_rl_brake(listofbrakes[0])
                    self.rl_brake_temp_label.config(fg="#00ffff")
                elif int(data_dict_cartelemetry['RLBrakeTemperature']) <= 450:
                    self.update_rl_brake(listofbrakes[1])
                    self.rl_brake_temp_label.config(fg="#00ffaa")
                elif int(data_dict_cartelemetry['RLBrakeTemperature']) <= 750:
                    self.update_rl_brake(listofbrakes[2])
                    self.rl_brake_temp_label.config(fg="#00ff00")
                elif int(data_dict_cartelemetry['RLBrakeTemperature']) <= 950:
                    self.update_rl_brake(listofbrakes[3])
                    self.rl_brake_temp_label.config(fg="#fccc1f")
                elif int(data_dict_cartelemetry['RLBrakeTemperature']) > 950:
                    self.update_rl_brake(listofbrakes[4])
                    self.rl_brake_temp_label.config(fg="#fe2b17")

            if 'FRTyreInnerTemperature' in data_dict_cartelemetry:
                self.fr_inner_temp_label.config(text=f"{data_dict_cartelemetry['FRTyreInnerTemperature']}°C")
                if int(data_dict_cartelemetry['FRTyreInnerTemperature']) <= 70:
                    self.update_fr_tyre(listoffronttyres[0])
                    self.fr_inner_temp_label.config(fg="#00ffff")
                elif int(data_dict_cartelemetry['FRTyreInnerTemperature']) <= 90:
                    self.update_fr_tyre(listoffronttyres[1])
                    self.fr_inner_temp_label.config(fg="#00ffaa")
                elif int(data_dict_cartelemetry['FRTyreInnerTemperature']) <= 105:
                    self.update_fr_tyre(listoffronttyres[2])
                    self.fr_inner_temp_label.config(fg="#00ff00")
                elif int(data_dict_cartelemetry['FRTyreInnerTemperature']) <= 110:
                    self.update_fr_tyre(listoffronttyres[3])
                    self.fr_inner_temp_label.config(fg="#fccc1f")
                elif int(data_dict_cartelemetry['FRTyreInnerTemperature']) > 110:
                    self.update_fr_tyre(listoffronttyres[4])
                    self.fr_inner_temp_label.config(fg="#fe2b17")

            if 'FRTyreSurfaceTemperature' in data_dict_cartelemetry:
                self.fr_outer_temp_label.config(text=f"{data_dict_cartelemetry['FRTyreSurfaceTemperature']}°C")
                if int(data_dict_cartelemetry['FRTyreSurfaceTemperature']) <= 70:
                    self.fr_outer_temp_label.config(fg="#00ffff")
                elif int(data_dict_cartelemetry['FRTyreSurfaceTemperature']) <= 90:
                    self.fr_outer_temp_label.config(fg="#00ffaa")
                elif int(data_dict_cartelemetry['FRTyreSurfaceTemperature']) <= 105:
                    self.fr_outer_temp_label.config(fg="#00ff00")
                elif int(data_dict_cartelemetry['FRTyreSurfaceTemperature']) <= 110:
                    self.fr_outer_temp_label.config(fg="#fccc1f")
                elif int(data_dict_cartelemetry['FRTyreSurfaceTemperature']) > 110:
                    self.fr_outer_temp_label.config(fg="#fe2b17")

            if 'FRBrakeTemperature' in data_dict_cartelemetry:
                self.fr_brake_temp_label.config(text=f"{data_dict_cartelemetry['FRBrakeTemperature']}°C")
                if int(data_dict_cartelemetry['FRBrakeTemperature']) <= 350:
                    self.update_fr_brake(listofbrakes[0])
                    self.fr_brake_temp_label.config(fg="#00ffff")
                elif int(data_dict_cartelemetry['FRBrakeTemperature']) <= 450:
                    self.update_fr_brake(listofbrakes[1])
                    self.fr_brake_temp_label.config(fg="#00ffaa")
                elif int(data_dict_cartelemetry['FRBrakeTemperature']) <= 750:
                    self.update_fr_brake(listofbrakes[2])
                    self.fr_brake_temp_label.config(fg="#00ff00")
                elif int(data_dict_cartelemetry['FRBrakeTemperature']) <= 950:
                    self.update_fr_brake(listofbrakes[3])
                    self.fr_brake_temp_label.config(fg="#fccc1f")
                elif int(data_dict_cartelemetry['FRBrakeTemperature']) > 950:
                    self.update_fr_brake(listofbrakes[4])
                    self.fr_brake_temp_label.config(fg="#fe2b17")

            if 'RRTyreInnerTemperature' in data_dict_cartelemetry:
                self.rr_inner_temp_label.config(text=f"{data_dict_cartelemetry['RRTyreInnerTemperature']}°C")
                if int(data_dict_cartelemetry['RRTyreInnerTemperature']) <= 70:
                    self.update_rr_tyre(listofreartyres[0])
                    self.rr_inner_temp_label.config(fg="#00ffff")
                elif int(data_dict_cartelemetry['RRTyreInnerTemperature']) <= 90:
                    self.update_rr_tyre(listofreartyres[1])
                    self.rr_inner_temp_label.config(fg="#00ffaa")
                elif int(data_dict_cartelemetry['RRTyreInnerTemperature']) <= 105:
                    self.update_rr_tyre(listofreartyres[2])
                    self.rr_inner_temp_label.config(fg="#00ff00")
                elif int(data_dict_cartelemetry['RRTyreInnerTemperature']) <= 110:
                    self.update_rr_tyre(listofreartyres[3])
                    self.rr_inner_temp_label.config(fg="#fccc1f")
                elif int(data_dict_cartelemetry['RRTyreInnerTemperature']) > 110:
                    self.update_rr_tyre(listofreartyres[4])
                    self.rr_inner_temp_label.config(fg="#fe2b17")

            if 'RRTyreSurfaceTemperature' in data_dict_cartelemetry:
                self.rr_outer_temp_label.config(text=f"{data_dict_cartelemetry['RRTyreSurfaceTemperature']}°C")
                if int(data_dict_cartelemetry['RRTyreSurfaceTemperature']) <= 70:
                    self.rr_outer_temp_label.config(fg="#00ffff")
                elif int(data_dict_cartelemetry['RRTyreSurfaceTemperature']) <= 90:
                    self.rr_outer_temp_label.config(fg="#00ffaa")
                elif int(data_dict_cartelemetry['RRTyreSurfaceTemperature']) <= 105:
                    self.rr_outer_temp_label.config(fg="#00ff00")
                elif int(data_dict_cartelemetry['RRTyreSurfaceTemperature']) <= 110:
                    self.rr_outer_temp_label.config(fg="#fccc1f")
                elif int(data_dict_cartelemetry['RRTyreSurfaceTemperature']) > 110:
                    self.rr_outer_temp_label.config(fg="#fe2b17")

            if 'RRBrakeTemperature' in data_dict_cartelemetry:
                self.rr_brake_temp_label.config(text=f"{data_dict_cartelemetry['RRBrakeTemperature']}°C")
                if int(data_dict_cartelemetry['RRBrakeTemperature']) <= 350:
                    self.update_rr_brake(listofbrakes[0])
                    self.rr_brake_temp_label.config(fg="#00ffff")
                elif int(data_dict_cartelemetry['RRBrakeTemperature']) <= 450:
                    self.update_rr_brake(listofbrakes[1])
                    self.rr_brake_temp_label.config(fg="#00ffaa")
                elif int(data_dict_cartelemetry['RRBrakeTemperature']) <= 750:
                    self.update_rr_brake(listofbrakes[2])
                    self.rr_brake_temp_label.config(fg="#00ff00")
                elif int(data_dict_cartelemetry['RRBrakeTemperature']) <= 950:
                    self.update_rr_brake(listofbrakes[3])
                    self.rr_brake_temp_label.config(fg="#fccc1f")
                elif int(data_dict_cartelemetry['RRBrakeTemperature']) > 950:
                    self.update_rr_brake(listofbrakes[4])
                    self.rr_brake_temp_label.config(fg="#fe2b17")

            if 'engineTemperature' in data_dict_cartelemetry:
                self.motor_temp_label.config(text=f"{data_dict_cartelemetry['engineTemperature']}°C")
                if int(data_dict_cartelemetry['engineTemperature']) <= 80:
                    self.update_engine(listofengine[0])
                    self.motor_temp_label.config(fg="#00ffff")
                elif int(data_dict_cartelemetry['engineTemperature']) <= 100:
                    self.update_engine(listofengine[1])
                    self.motor_temp_label.config(fg="#00ffaa")
                elif int(data_dict_cartelemetry['engineTemperature']) <= 130:
                    self.update_engine(listofengine[2])
                    self.motor_temp_label.config(fg="#00ff00")
                elif int(data_dict_cartelemetry['engineTemperature']) <= 140:
                    self.update_engine(listofengine[3])
                    self.motor_temp_label.config(fg="#fccc1f")
                elif int(data_dict_cartelemetry['engineTemperature']) > 140:
                    self.update_engine(listofengine[4])
                    self.motor_temp_label.config(fg="#fe2b17")

            self.root.after(5, self.update_temp_labels)

    def destroy(self):
        # Destroy the canvas
        self.canvas.destroy()

## Safety Car (egyelőre nem használjuk)
class SafetyCar:
    def __init__(self, root):
        self.root = root

    def create_safetycar_display(self):
        self.canvas = tk.Canvas(root, height=480, width=800, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.safetycar_label = tk.Label(self.root, text="SAFETY CAR", fg="yellow", bg="black",
                                   font=("Formula1", 60, "bold"))
        self.safetycar_label.place(relx=0.5, rely=0.4, anchor="center")

        self.safetycar_delta_label = tk.Label(self.root, text="+0.000", fg="#00ff00", bg="black",
                                         font=("Formula1", 40, "bold"))
        self.safetycar_delta_label.place(relx=0.5, rely=0.6, anchor="center")

    def destroy_safetycar_display(self):
        #print("destroying safety car display")
        self.canvas.destroy()

    def safetycar_label_update(self):
        global data_dict_lapdata
        global data_dict_main
        if 'safetyCarDelta' in data_dict_lapdata:
            self.safetycar_delta_label.config(text=f"+{data_dict_lapdata['safetyCarDelta']:.3f}")

        self.root.after(5, self.safetycar_label_update)

    def safetycar_is_processed(self):
        global data_dict_main
        data_dict_main['isSafetyCarProcess'] = True

## A megjelenítést kezelő osztály
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
        mfdnum = self.mfdnum

        if mfdnum == 6:
            if self.displayed_canvas is not None:
                self.displayed_canvas.destroy()
            self.displayed_canvas = self.connect.create_connect_display()

        elif mfdnum == 255:
            if self.displayed_canvas is not None:
                self.displayed_canvas.destroy()
            self.displayed_canvas = self.df.create_default_display()
            root.after(5, self.df.update_labels)

        elif mfdnum == 1:
            if self.displayed_canvas is not None:
                self.displayed_canvas.destroy()
            self.displayed_canvas = self.ps.create_pitstop_display()
            root.after(5, self.ps.update_pitstop_labels)

        elif mfdnum == 2:
            if self.displayed_canvas is not None:
                self.displayed_canvas.destroy()
            self.displayed_canvas = self.cd.create_cardamage_display()
            root.after(5, self.cd.update_damage_display)

        elif mfdnum == 3:
            if self.displayed_canvas is not None:
                self.displayed_canvas.destroy()
            self.displayed_canvas = self.ct.create_cartemp_display()
            root.after(5, self.ct.update_temp_labels)

        elif mfdnum == 4:
            if self.displayed_canvas is not None:
                self.displayed_canvas.destroy()
            self.displayed_canvas = self.e.create_engine_display()
            root.after(5, self.e.update_engine_display)

    def update_mfd(self):
        global mfdPanelIndex_isChanged
        global mfdPanelIndex
        self.mfdnum = mfdPanelIndex
        if mfdPanelIndex_isChanged == True:
            self.__call__(self.mfdnum)
            mfdPanelIndex_isChanged = False
        else:
            pass
        self.root.after(5, self.update_mfd)



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

    # Create a new thread for udp_server
    udp_thread = threading.Thread(target=udp_server)
    # Start the new thread
    udp_thread.start()

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
