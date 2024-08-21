import tkinter as tk
from PIL import Image as PilImage, ImageTk
from App import *
from SharedVars import *
from listsandconstants import *
from imageswap import *

class ConnectDisplay:

    def __init__(self, root):
        self.root = root

    def create_connect_display(self):
        self.canvas = tk.Canvas(self.root, height=480, width=800, bg="white", highlightthickness=0)
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
            global data_dict_sessionpacket

            if 'sessionType' in data_dict_sessionpacket:
                self.ip.config(fg="white")
                self.port.config(fg="white")

            self.root.after(5, self.update_connection_display)
class DefaultDisplay:
    def __init__(self, root):
        self.root = root

    def create_default_display(self):
        self.canvas = tk.Canvas(self.root, height=500, width=800, bg="white")
        self.canvas.pack()
        self.kmphframe = tk.Frame(self.root, height=100, width=200, bg="black")
        self.kmphframe.place(x=0, y=0)

        self.kmph_label = tk.Label(self.kmphframe, text=f"250", fg="white", bg="black", font=("Formula1", 30, "bold"))
        self.kmph_label.place(relx=0.5, rely=0.35, anchor="center")
        self.kmph_text_label = tk.Label(self.kmphframe, text="KM/H", fg="white", bg="black", font=("Formula1", 9, "bold"))
        self.kmph_text_label.place(relx=0.5, rely=0.7, anchor="center")

        self.laptimeframe = tk.Frame(self.root, height=100, width=402, bg="black")
        self.laptimeframe.place(x=201, y=0)

        self.laptime_label = tk.Label(self.laptimeframe, text="-:--.---", fg="white", bg="black", font=("Formula1", 38, "bold"))
        self.laptime_label.place(relx=0.5, rely=0.3, anchor="center")

        self.laptime_delta_label = tk.Label(self.laptimeframe, text="-0.000", fg="#00ff00", bg="black", font=("Formula1", 15, "bold"))
        self.laptime_delta_label.place(relx=0.5, rely=0.8, anchor="center")

        self.pitlimiter_label = tk.Label(self.laptimeframe, text="PIT LIMITER", fg="white", bg="black",font=("Formula1", 40, "bold"))
        self.pitlimiter_label.place(relx=0.5, rely=0.5, anchor="center")

        self.formationlapframe = tk.Frame(self.root, height=100, width=402, bg="black")
        self.formationlapframe.place(x=201, y=0)

        self.formationlap_label = tk.Label(self.formationlapframe, text="FORMATION LAP", fg="white", bg="black",font=("Formula1", 25, "bold"))
        self.formationlap_label.place(relx=0.5, rely=0.5, anchor="center")

        self.fuelplusframe = tk.Frame(self.root, height=100, width=202, bg="black")
        self.fuelplusframe.place(x=604, y=0)

        self.fuelplus_label = tk.Label(self.fuelplusframe, text="3.1l", fg="white", bg="black", font=("Formula1", 30, "bold"))
        self.fuelplus_label.place(relx=0.5, rely=0.4, anchor="center")

        self.fuelpluslaps_label = tk.Label(self.fuelplusframe, text="(+1.2 laps)", fg="#00ff00", bg="black", font=("Formula1", 10, "bold"))
        self.fuelpluslaps_label.place(relx=0.5, rely=0.8, anchor="center")

        self.lapnumframe = tk.Frame(self.root, height=80, width=200, bg="black")
        self.lapnumframe.place(x=0, y=101)

        self.lapnum_label = tk.Label(self.lapnumframe, text="L1", fg="cyan", bg="black", font=("Formula1", 33, "bold"))
        self.lapnum_label.place(relx=0.5, rely=0.5, anchor="center")

        self.lefttyresframe = tk.Frame(self.root, height=79, width=200, bg="black")
        self.lefttyresframe.place(x=0, y=182)

        self.lefttyres_front_label = tk.Label(self.lefttyresframe, text="92°C", fg="#ffdb4d", bg="black",font=("Formula1", 20, "bold"))
        self.lefttyres_front_label.place(relx=0.5, rely=0.3, anchor="center")
        self.lefttyres_rear_label = tk.Label(self.lefttyresframe, text="94°C", fg="#ffdb4d", bg="black",font=("Formula1", 20, "bold"))
        self.lefttyres_rear_label.place(relx=0.5, rely=0.7, anchor="center")

        self.differential_frame = tk.Frame(self.root, height=79, width=200, bg="black")
        self.differential_frame.place(x=0, y=262)

        self.differential_percentage_label = tk.Label(self.differential_frame, text="50%", fg="white", bg="black",font=("Formula1", 25, "bold"))
        self.differential_percentage_label.place(relx=0.5, rely=0.35, anchor="center")

        self.differential_text_label = tk.Label(self.differential_frame, text="DIFFERENTIAL", fg="white", bg="black",font=("Formula1", 9, "bold"))
        self.differential_text_label.place(relx=0.5, rely=0.7, anchor="center")

        self.gear_frame = tk.Frame(self.root, height=240, width=402, bg="black")
        self.gear_frame.place(x=201, y=101)

        self.gear_label = tk.Label(self.gear_frame, text="8", fg="white", bg="black", font=("Formula1", 85, "bold"))
        self.gear_label.place(relx=0.5, rely=0.5, anchor="center")

        self.safetycartext = tk.Label(self.gear_frame, text=f"VIRTUAL\nSAFETY CAR", fg="#ffff00", bg="black",font=("Formula1", 25, "bold"))
        self.safetycartext.place(relx=0.5, rely=0.15, anchor="center")

        self.placeframe = tk.Frame(self.root, height=80, width=202, bg="black")
        self.placeframe.place(x=604, y=101)

        self.place_label = tk.Label(self.placeframe, text="P7", fg="cyan", bg="black", font=("Formula1", 33, "bold"))
        self.place_label.place(relx=0.5, rely=0.5, anchor="center")

        self.righttyresframe = tk.Frame(self.root, height=79, width=202, bg="black")
        self.righttyresframe.place(x=604, y=182)

        self.righttyres_front_label = tk.Label(self.righttyresframe, text="92°C", fg="#ffdb4d", bg="black", font=("Formula1", 20, "bold"))
        self.righttyres_front_label.place(relx=0.5, rely=0.3, anchor="center")
        self.righttyres_rear_label = tk.Label(self.righttyresframe, text="94°C", fg="#ffdb4d", bg="black", font=("Formula1", 20, "bold"))
        self.righttyres_rear_label.place(relx=0.5, rely=0.7, anchor="center")

        self.brake_bias_frame = tk.Frame(self.root, height=79, width=202, bg="black")
        self.brake_bias_frame.place(x=604, y=262)

        self.brake_bias_percentage_label = tk.Label(self.brake_bias_frame, text="56%", fg="white", bg="black", font=("Formula1", 25, "bold"))
        self.brake_bias_percentage_label.place(relx=0.5, rely=0.35, anchor="center")

        self.brake_bias_text_label = tk.Label(self.brake_bias_frame, text="FRONT BRAKE BIAS", fg="white", bg="black", font=("Formula1", 9, "bold"))
        self.brake_bias_text_label.place(relx=0.5, rely=0.7, anchor="center")

        #self.brakeindicatorframe = tk.Frame(self.root, height=114, width=200, bg="darkred")
        #self.brakeindicatorframe.place(x=0, y=382.5)

        self.ers_harvest_25_indicator = tk.Frame(self.root, height=113, width=49, bg="darkred")
        self.ers_harvest_25_indicator.place(x=0, y=382.5)
        self.ers_harvest_50_indicator = tk.Frame(self.root, height=113, width=49, bg="darkred")
        self.ers_harvest_50_indicator.place(x=50, y=382.5)
        self.ers_harvest_75_indicator = tk.Frame(self.root, height=113, width=49, bg="darkred")
        self.ers_harvest_75_indicator.place(x=100, y=382.5)
        self.ers_harvest_100_indicator = tk.Frame(self.root, height=113, width=49, bg="darkred")
        self.ers_harvest_100_indicator.place(x=150, y=382.5)



        child_width_brake = float(0.23 * 200)
        self.ers_harvest_indicatorfillframe = tk.Frame(self.root, height=113, width=child_width_brake, bg="red")
        self.ers_harvest_indicatorfillframe.place(x=0, y=382.5)

        #self.ersindicatorframe = tk.Frame(self.root, height=114, width=402, bg="#cca300")
        #self.ersindicatorframe.place(x=201, y=382.5)

        self.ers_10_indicator = tk.Frame(self.root, height=113, width=39, bg="#cca300")
        self.ers_10_indicator.place(x=201.9, y=382.5)
        self.ers_20_indicator = tk.Frame(self.root, height=113, width=39, bg="#cca300")
        self.ers_20_indicator.place(x=241.9, y=382.5)
        self.ers_30_indicator = tk.Frame(self.root, height=113, width=39, bg="#cca300")
        self.ers_30_indicator.place(x=281.9, y=382.5)
        self.ers_40_indicator = tk.Frame(self.root, height=113, width=39, bg="#cca300")
        self.ers_40_indicator.place(x=321.9, y=382.5)
        self.ers_50_indicator = tk.Frame(self.root, height=113, width=39, bg="#cca300")
        self.ers_50_indicator.place(x=361.9, y=382.5)
        self.ers_60_indicator = tk.Frame(self.root, height=113, width=39, bg="#cca300")
        self.ers_60_indicator.place(x=401.9, y=382.5)
        self.ers_70_indicator = tk.Frame(self.root, height=113, width=39, bg="#cca300")
        self.ers_70_indicator.place(x=442, y=382.5)
        self.ers_80_indicator = tk.Frame(self.root, height=113, width=39, bg="#cca300")
        self.ers_80_indicator.place(x=482.1, y=382.5)
        self.ers_90_indicator = tk.Frame(self.root, height=113, width=39, bg="#cca300")
        self.ers_90_indicator.place(x=522.2, y=382.5)
        self.ers_100_indicator = tk.Frame(self.root, height=113, width=39, bg="#cca300")
        self.ers_100_indicator.place(x=562.3, y=382.5)



        child_width_ers = float(0.82 * 401)
        self.ersindicatorfillframe = tk.Frame(self.root, height=113, width=child_width_ers, bg="#ffff00")
        self.ersindicatorfillframe.place(x=201, y=382.5)
        self.ers_percentage_label = tk.Label(self.root, text="82%", fg="white", bg="black", font=("Formula1", 18, "bold"))
        self.ers_percentage_label.place(in_=self.root, x=360, y=385)

        self.ersframe = tk.Frame(self.root, height=40, width=806, bg="black")
        self.ersframe.place(x=0, y=342)

        self.ers_label = tk.Label(self.ersframe, text="NONE", fg="white", bg="black", font=("Formula1", 15, "bold"))
        self.ers_label.place(relx=0.5, rely=0.45, anchor="center")

        #self.acceleratorindicatorframe = tk.Frame(self.root, height=114, width=202, bg="darkgreen")
        #self.acceleratorindicatorframe.place(x=604, y=382.5)

        self.ers_deploy_25_indicator = tk.Frame(self.root, height=113, width=49, bg="darkgreen")
        self.ers_deploy_25_indicator.place(x=604, y=382.5)
        self.ers_deploy_50_indicator = tk.Frame(self.root, height=113, width=49, bg="darkgreen")
        self.ers_deploy_50_indicator.place(x=654, y=382.5)
        self.ers_deploy_75_indicator = tk.Frame(self.root, height=113, width=49, bg="darkgreen")
        self.ers_deploy_75_indicator.place(x=704, y=382.5)
        self.ers_deploy_100_indicator = tk.Frame(self.root, height=113, width=49, bg="darkgreen")
        self.ers_deploy_100_indicator.place(x=754, y=382.5)


        child_width_accelator = float(0.3 * 202)
        self.ers_deploy_indicatorfillframe = tk.Frame(self.root, height=114, width=child_width_accelator, bg="#00ff00")
        self.ers_deploy_indicatorfillframe.place(x=604, y=382.5)

        return self.canvas

    def update_labels(self):
        if self.canvas is not None and self.canvas.winfo_exists():
            global data_dict_cartelemetry
            global data_dict_sessionpacket
            global data_dict_sessionhistory
            global data_dict_carstatus
            global data_dict_lapdata
            global data_dict_flyingdelta

            if 'onThrottle' in data_dict_carsetup:
                self.differential_percentage_label.config(text=f"{data_dict_carsetup['onThrottle']}%")

            if 'frontBrakeBias' in data_dict_carstatus:
                self.brake_bias_percentage_label.config(text=f"{data_dict_carstatus['frontBrakeBias']}%")

            if 'speedUnit' in data_dict_sessionpacket:
                if data_dict_sessionpacket['speedUnit'] == 0:
                    self.kmph_text_label.config(text="MPH")
                else:
                    self.kmph_text_label.config(text="KM/H")

            if 'speed' in data_dict_cartelemetry:
                self.kmph_label.config(text=f"{data_dict_cartelemetry['speed']}")

            if 'gear' in data_dict_cartelemetry:
                if data_dict_cartelemetry['gear'] == -1:
                    self.gear_label.config(text="R")
                elif data_dict_cartelemetry['gear'] == 0:
                    self.gear_label.config(text="N")
                else:
                    self.gear_label.config(text=f"{data_dict_cartelemetry['gear']}")

            if 'ersDeployedThisLap' in data_dict_carstatus:
                self.ers_deploy_indicatorfillframe.config(width=float((1 - (data_dict_carstatus['ersDeployedThisLap']/maximum_energy_deployed)) * 202))

            if 'ersHarvestedThisLapMGUK' in data_dict_carstatus:
                self.ers_harvest_indicatorfillframe.config(width=float((data_dict_carstatus['ersHarvestedThisLapMGUK'] / maximum_energy_harvested) * 200))

            if 'ersStoreEnergy' in data_dict_carstatus:
                stored_energy_in_percentage = data_dict_carstatus['ersStoreEnergy'] / maximum_energy_storage * 100
                self.ersindicatorfillframe.config(
                    width=float((data_dict_carstatus['ersStoreEnergy'] / maximum_energy_storage) * 402))
                self.ers_percentage_label.config(text=f"{stored_energy_in_percentage:.0f}%", font=("Formula1", 35, "bold"))

            if 'ersDeployMode' in data_dict_carstatus:
                if data_dict_carstatus['ersDeployMode'] == 0:
                    self.ers_label.config(text="NONE")
                    self.ers_label.config(fg="white")
                    self.ers_label.config(bg="black")
                    self.ersframe.config(bg="black")
                elif data_dict_carstatus['ersDeployMode'] == 1:
                    self.ers_label.config(text="MEDIUM")
                    self.ers_label.config(fg="black")
                    self.ers_label.config(bg="#15F522")
                    self.ersframe.config(bg="#15F522")
                elif data_dict_carstatus['ersDeployMode'] == 2:
                    self.ers_label.config(text="HOTLAP")
                    self.ers_label.config(fg="black")
                    self.ers_label.config(bg="#F5F414")
                    self.ersframe.config(bg="#F5F414")
                elif data_dict_carstatus['ersDeployMode'] == 3:
                    self.ers_label.config(text="OVERTAKE")
                    self.ers_label.config(fg="black")
                    self.ers_label.config(bg="#E02900")
                    self.ersframe.config(bg="#E02900")

            if 'RLTyreInnerTemperature' in data_dict_cartelemetry:
                self.lefttyres_front_label.config(text=f"{data_dict_cartelemetry['FLTyreInnerTemperature']}°C")
                self.lefttyres_rear_label.config(text=f"{data_dict_cartelemetry['RLTyreInnerTemperature']}°C")
                self.righttyres_front_label.config(text=f"{data_dict_cartelemetry['FRTyreInnerTemperature']}°C")
                self.righttyres_rear_label.config(text=f"{data_dict_cartelemetry['RRTyreInnerTemperature']}°C")

            if 'fuelInTank' in data_dict_carstatus:
                self.fuelplus_label.config(text=f"{data_dict_carstatus['fuelInTank']:.1f}l")

            if 'fuelRemainingLaps' in data_dict_carstatus:
                if data_dict_carstatus['fuelRemainingLaps'] > 0:
                    self.fuelpluslaps_label.config(text=f"(+{data_dict_carstatus['fuelRemainingLaps']:.2f} laps)")
                    self.fuelpluslaps_label.config(fg="#00ff00")
                else:
                    self.fuelpluslaps_label.config(text=f"(+{data_dict_carstatus['fuelRemainingLaps']:.2f} laps)")
                    self.fuelpluslaps_label.config(fg="red")

            if 'safetyCarStatus' in data_dict_sessionpacket and data_dict_sessionpacket['safetyCarStatus'] == 0:
                self.safetycartext.config(fg="black")
                self.formationlapframe.lower()
                if 'delta' in data_dict_flyingdelta and data_dict_carstatus['pitLimiterStatus'] == 0:
                    flyingdelta = data_dict_flyingdelta['delta']
                    if flyingdelta == -100.000:
                        self.laptime_delta_label.config(text="error", fg="red")
                    elif flyingdelta < 0:
                        self.laptime_delta_label.config(text=f"-{flyingdelta:.3f}",fg="#00ff00")
                    elif flyingdelta == 0.000 or flyingdelta == 1000.000:
                        self.laptime_delta_label.config(text=f"+/-{flyingdelta:.3f}",fg="white")
                    else:
                        self.laptime_delta_label.config(text=f"+{flyingdelta:.3f}",fg="red")

            elif 'safetyCarStatus' in data_dict_sessionpacket and (data_dict_sessionpacket['safetyCarStatus'] == 1 or data_dict_sessionpacket['safetyCarStatus'] == 2):
                self.formationlapframe.lower()
                if data_dict_sessionpacket['safetyCarStatus'] == 1:
                    self.safetycartext.config(text="SAFETY CAR", fg="#ffff00")
                elif data_dict_sessionpacket['safetyCarStatus'] == 2:
                    self.safetycartext.config(text="VIRTUAL\nSAFETY CAR", fg="#ffff00")

                if data_dict_lapdata['safetyCarDelta'] > 0.000:
                    self.laptime_delta_label.config(text=f"+{data_dict_lapdata['safetyCarDelta']:.3f}", fg="#00ff00")
                elif data_dict_lapdata['safetyCarDelta'] < 0.000:
                    self.laptime_delta_label.config(text=f"-{data_dict_lapdata['safetyCarDelta']:.3f}", fg="red")
                else:
                    self.laptime_delta_label.config(text=f"+/-{data_dict_lapdata['safetyCarDelta']:.3f}", fg="white")

            elif 'safetyCarStatus' in data_dict_sessionpacket and data_dict_sessionpacket['safetyCarStatus'] == 3:
                self.safetycartext.config(fg="black")
                self.laptime_delta_label.config(text="0.000", fg="black")
                self.formationlapframe.lift()

            else:
                if 'delta' in data_dict_flyingdelta and data_dict_carstatus['pitLimiterStatus'] == 0:
                    flyingdelta = data_dict_flyingdelta['delta']
                    if flyingdelta == -100.000:
                        self.laptime_delta_label.config(text="error", fg="red")
                    elif flyingdelta < 0:
                        self.laptime_delta_label.config(text=f"-{flyingdelta:.3f}", fg="#00ff00")
                    elif flyingdelta == 0.000 or flyingdelta == 1000.000:
                        self.laptime_delta_label.config(text=f"+/-{flyingdelta:.3f}", fg="white")
                    else:
                        self.laptime_delta_label.config(text=f"+{flyingdelta:.3f}", fg="red")

            if 'pitLimiterStatus' in data_dict_carstatus and data_dict_carstatus['pitLimiterStatus'] == 1:
                self.laptime_label.config(fg="black")
                self.laptime_delta_label.config(fg="black")
                self.pitlimiter_label.config(fg="white")
                self.pitlimiter_label.lift()
            else:
                self.pitlimiter_label.config(fg="black")
                self.pitlimiter_label.lower()

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

            if 'currentLapInvalid' in data_dict_lapdata and data_dict_carstatus['pitLimiterStatus'] == 0:
                if data_dict_lapdata['currentLapInvalid'] == 1:
                    print("Lap Invalid")
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
        self.canvas = tk.Canvas(self.root, height=480, width=800, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.pitwindow_text = tk.Label(self.canvas, text="Pit Window", fg="white", bg="black", font=("Formula1", 25, "bold"))
        self.pitwindow_text.place(x=400, y=25, anchor="center")

        self.pitwindowlaps_text = tk.Label(self.canvas, text="LAP 13 - 17", fg="cyan", bg="black", font=("Formula1", 60, "bold"))
        self.pitwindowlaps_text.place(x=400, y=120, anchor="center")

        self.rejoin_text = tk.Label(self.canvas, text="Pit Now Rejoin Position", fg="white", bg="black", font=("Formula1", 15, "bold"))
        self.rejoin_text.place(x=370, y=170, anchor="center")

        self.rejoinpositon = tk.Label(self.canvas, text="20th", fg="cyan", bg="black",font=("Formula1", 15, "bold"))
        self.rejoinpositon.place(x=540, y=170, anchor="center")

        self.availablebest_text = tk.Label(self.canvas, text="Available Best Sets", fg="white", bg="black", font=("Formula1", 10, "bold"))
        self.availablebest_text.place(x=130, y=380, anchor="center")

        self.soft_img = PilImage.open('tyres/soft.png')
        self.soft_img_resized = self.soft_img.resize((50, 50))
        # Convert the image to a format Tkinter can use
        self.soft_tk_image = ImageTk.PhotoImage(self.soft_img_resized)
        self.canvas.create_image(50, 430, image=self.soft_tk_image)

        self.soft_newest = tk.Label(self.canvas, text="Used", fg="white", bg="black", font=("Formula1", 20, "bold"))
        self.soft_newest.place(x=80, y=397)
        self.soft_best_percent = tk.Label(self.canvas, text="7%", fg="white", bg="black", font=("Formula1", 15, "bold"))
        self.soft_best_percent.place(x=82, y=427)

        self.medium_img = PilImage.open('tyres/medium.png')
        self.medium_img_resized = self.medium_img.resize((50, 50))
        # Convert the image to a format Tkinter can use
        self.medium_tk_image = ImageTk.PhotoImage(self.medium_img_resized)
        self.canvas.create_image(210, 430, image=self.medium_tk_image)

        self.medium_newest = tk.Label(self.canvas, text="Used", fg="white", bg="black", font=("Formula1", 20, "bold"))
        self.medium_newest.place(x=240, y=397)
        self.medium_best_percent = tk.Label(self.canvas, text="12%", fg="white", bg="black", font=("Formula1", 15, "bold"))
        self.medium_best_percent.place(x=242, y=427)

        self.hard_img = PilImage.open('tyres/hard.png')
        self.hard_img_resized = self.hard_img.resize((50, 50))
        # Convert the image to a format Tkinter can use
        self.hard_tk_image = ImageTk.PhotoImage(self.hard_img_resized)
        self.canvas.create_image(370, 430, image=self.hard_tk_image)

        self.hard_newest = tk.Label(self.canvas, text="New", fg="white", bg="black", font=("Formula1", 20, "bold"))
        self.hard_newest.place(x=400, y=397)
        self.hard_best_percent = tk.Label(self.canvas, text="0%", fg="white", bg="black",font=("Formula1", 15, "bold"))
        self.hard_best_percent.place(x=402, y=427)

        self.inter_img = PilImage.open('tyres/inter.png')
        self.inter_img_resized = self.inter_img.resize((50, 50))
        # Convert the image to a format Tkinter can use
        self.inter_tk_image = ImageTk.PhotoImage(self.inter_img_resized)
        self.canvas.create_image(520, 430, image=self.inter_tk_image)

        self.inter_newest = tk.Label(self.canvas, text="New", fg="white", bg="black", font=("Formula1", 20, "bold"))
        self.inter_newest.place(x=550, y=397)
        self.inter_best_percent = tk.Label(self.canvas, text="0%", fg="white", bg="black",font=("Formula1", 15, "bold"))
        self.inter_best_percent.place(x=552, y=427)

        self.wet_img = PilImage.open('tyres/wet.png')
        self.wet_img_resized = self.wet_img.resize((50, 50))
        self.wet_tk_image = ImageTk.PhotoImage(self.wet_img_resized)
        self.canvas.create_image(670, 430, image=self.wet_tk_image)

        self.wet_newest = tk.Label(self.canvas, text="New", fg="white", bg="black", font=("Formula1", 20, "bold"))
        self.wet_newest.place(x=700, y=397)
        self.wet_best_percent = tk.Label(self.canvas, text="0%", fg="white", bg="black",font=("Formula1", 15, "bold"))
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
        self.canvas = tk.Canvas(self.root, height=480, width=800, bg="black", highlightthickness=0)
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
        self.fl_percent_label = tk.Label(self.root, text="0%", fg="red", bg="black", font=("Formula1", 15, "bold"))
        self.fl_percent_label.place(x=201.5, y=109.5)

        # front right percent text
        self.fr_percent_label = tk.Label(self.root, text="0%", fg="red", bg="black", font=("Formula1", 15, "bold"))
        self.fr_percent_label.place(x=531, y=109.5)

        # rear left percent text
        self.rl_percent_label = tk.Label(self.root, text="0%", fg="red", bg="black", font=("Formula1", 15, "bold"))
        self.rl_percent_label.place(x=191.5, y=351)

        # rear right percent text
        self.rr_percent_label = tk.Label(self.root, text="0%", fg="red", bg="black", font=("Formula1", 15, "bold"))
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
    def update_damage_display(self):
        if self.canvas is not None and self.canvas.winfo_exists():
            global data_dict_cardamage
            imgswp = ImageSwapper()
            if 'frontLeftWingDamage' in data_dict_cardamage:
                fldamage = int(data_dict_cardamage['frontLeftWingDamage'])
                if fldamage < 10:
                    #self.front_wing_left_damage(listoffrontwingleftstatus[0])
                    imgswp.swapImages(self.canvas, listoffrontwingleftstatus[0], 68, 60, self.frontleft, self.frontleft_tk_image)
                elif fldamage < 20:
                    #self.front_wing_left_damage(listoffrontwingleftstatus[1])
                    imgswp.swapImages(self.canvas, listoffrontwingleftstatus[1], 68, 60, self.frontleft, self.frontleft_tk_image)
                elif fldamage < 30:
                    #self.front_wing_left_damage(listoffrontwingleftstatus[2])
                    imgswp.swapImages(self.canvas, listoffrontwingleftstatus[2], 68, 60, self.frontleft, self.frontleft_tk_image)
                elif fldamage < 40:
                    #self.front_wing_left_damage(listoffrontwingleftstatus[3])
                    imgswp.swapImages(self.canvas, listoffrontwingleftstatus[3], 68, 60, self.frontleft, self.frontleft_tk_image)
                elif fldamage < 50:
                    #self.front_wing_left_damage(listoffrontwingleftstatus[4])
                    imgswp.swapImages(self.canvas, listoffrontwingleftstatus[4], 68, 60, self.frontleft, self.frontleft_tk_image)
                elif fldamage < 60:
                    #self.front_wing_left_damage(listoffrontwingleftstatus[5])
                    imgswp.swapImages(self.canvas, listoffrontwingleftstatus[5], 68, 60, self.frontleft, self.frontleft_tk_image)
                elif fldamage < 70:
                    #self.front_wing_left_damage(listoffrontwingleftstatus[6])
                    imgswp.swapImages(self.canvas, listoffrontwingleftstatus[6], 68, 60, self.frontleft, self.frontleft_tk_image)
                elif fldamage < 80:
                    #self.front_wing_left_damage(listoffrontwingleftstatus[7])
                    imgswp.swapImages(self.canvas, listoffrontwingleftstatus[7], 68, 60, self.frontleft, self.frontleft_tk_image)
                elif fldamage < 90:
                    #self.front_wing_left_damage(listoffrontwingleftstatus[8])
                    imgswp.swapImages(self.canvas, listoffrontwingleftstatus[8], 68, 60, self.frontleft, self.frontleft_tk_image)
                elif fldamage < 100:
                    #self.front_wing_left_damage(listoffrontwingleftstatus[9])
                    imgswp.swapImages(self.canvas, listoffrontwingleftstatus[9], 68, 60, self.frontleft, self.frontleft_tk_image)
                else:
                    #self.front_wing_left_damage(listoffrontwingleftstatus[10])
                    imgswp.swapImages(self.canvas, listoffrontwingleftstatus[10], 68, 60, self.frontleft, self.frontleft_tk_image)

            if 'frontRightWingDamage' in data_dict_cardamage:
                frdamage = int(data_dict_cardamage['frontRightWingDamage'])
                if frdamage < 10:
                    #self.front_wing_right_damage(listoffrontwingrightstatus[0])
                    imgswp.swapImages(self.canvas, listoffrontwingrightstatus[0], 68, 60, self.frontright, self.frontright_tk_image)
                elif frdamage < 20:
                    #self.front_wing_right_damage(listoffrontwingrightstatus[1])
                    imgswp.swapImages(self.canvas, listoffrontwingrightstatus[1], 68, 60, self.frontright, self.frontright_tk_image)
                elif frdamage < 30:
                    #self.front_wing_right_damage(listoffrontwingrightstatus[2])
                    imgswp.swapImages(self.canvas, listoffrontwingrightstatus[2], 68, 60, self.frontright, self.frontright_tk_image)
                elif frdamage < 40:
                    #self.front_wing_right_damage(listoffrontwingrightstatus[3])
                    imgswp.swapImages(self.canvas, listoffrontwingrightstatus[3], 68, 60, self.frontright, self.frontright_tk_image)
                elif frdamage < 50:
                    #self.front_wing_right_damage(listoffrontwingrightstatus[4])
                    imgswp.swapImages(self.canvas, listoffrontwingrightstatus[4], 68, 60, self.frontright, self.frontright_tk_image)
                elif frdamage < 60:
                    #self.front_wing_right_damage(listoffrontwingrightstatus[5])
                    imgswp.swapImages(self.canvas, listoffrontwingrightstatus[5], 68, 60, self.frontright, self.frontright_tk_image)
                elif frdamage < 70:
                    #self.front_wing_right_damage(listoffrontwingrightstatus[6])
                    imgswp.swapImages(self.canvas, listoffrontwingrightstatus[6], 68, 60, self.frontright, self.frontright_tk_image)
                elif frdamage < 80:
                    #self.front_wing_right_damage(listoffrontwingrightstatus[7])
                    imgswp.swapImages(self.canvas, listoffrontwingrightstatus[7], 68, 60, self.frontright, self.frontright_tk_image)
                elif frdamage < 90:
                    #self.front_wing_right_damage(listoffrontwingrightstatus[8])
                    imgswp.swapImages(self.canvas, listoffrontwingrightstatus[8], 68, 60, self.frontright, self.frontright_tk_image)
                elif frdamage < 100:
                    #self.front_wing_right_damage(listoffrontwingrightstatus[9])
                    imgswp.swapImages(self.canvas, listoffrontwingrightstatus[9], 68, 60, self.frontright, self.frontright_tk_image)
                else:
                    #self.front_wing_right_damage(listoffrontwingrightstatus[10])
                    imgswp.swapImages(self.canvas,listoffrontwingrightstatus[10],68,60,self.frontright, self.frontright_tk_image)

            if 'FLTyreDamage' in data_dict_cardamage:
                fltdamage = int(data_dict_cardamage['FLTyreDamage'])
                self.fl_percent_label.config(text=data_dict_cardamage['FLTyreDamage'] + "%")
                if fltdamage < 10:
                    self.fl_percent_label.config(fg="#00ff00")
                    self.fl_percent_label.place(x=211.5, y=109.5)
                    #self.front_left_tyre_damage(listoffronttyrestatus[0])
                    imgswp.swapImages(self.canvas, listoffronttyrestatus[0], 29, 53, self.frontlefttyre, self.frontlefttyre_tk_image)
                elif fltdamage < 20:
                    self.fl_percent_label.config(fg="#88f612")
                    self.fl_percent_label.place(x=201.5, y=109.5)
                    #self.front_left_tyre_damage(listoffronttyrestatus[1])
                    imgswp.swapImages(self.canvas, listoffronttyrestatus[1], 29, 53, self.frontlefttyre, self.frontlefttyre_tk_image)
                elif fltdamage < 30:
                    self.fl_percent_label.config(fg="#aef317")
                    self.fl_percent_label.place(x=201.5, y=109.5)
                    #self.front_left_tyre_damage(listoffronttyrestatus[2])
                    imgswp.swapImages(self.canvas, listoffronttyrestatus[2], 29, 53, self.frontlefttyre, self.frontlefttyre_tk_image)
                elif fltdamage < 40:
                    self.fl_percent_label.config(fg="#cff11b")
                    self.fl_percent_label.place(x=201.5, y=109.5)
                    #self.front_left_tyre_damage(listoffronttyrestatus[3])
                    imgswp.swapImages(self.canvas, listoffronttyrestatus[3], 29, 53, self.frontlefttyre, self.frontlefttyre_tk_image)
                elif fltdamage < 50:
                    self.fl_percent_label.config(fg="#ebef1f")
                    self.fl_percent_label.place(x=201.5, y=109.5)
                    #self.front_left_tyre_damage(listoffronttyrestatus[4])
                    imgswp.swapImages(self.canvas, listoffronttyrestatus[4], 29, 53, self.frontlefttyre, self.frontlefttyre_tk_image)
                elif fltdamage < 60:
                    self.fl_percent_label.config(fg="#fcee21")
                    self.fl_percent_label.place(x=201.5, y=109.5)
                    #self.front_left_tyre_damage(listoffronttyrestatus[5])
                    imgswp.swapImages(self.canvas, listoffronttyrestatus[5], 29, 53, self.frontlefttyre, self.frontlefttyre_tk_image)
                elif fltdamage < 70:
                    self.fl_percent_label.config(fg="#fccc1f")
                    self.fl_percent_label.place(x=201.5, y=109.5)
                    #self.front_left_tyre_damage(listoffronttyrestatus[6])
                    imgswp.swapImages(self.canvas, listoffronttyrestatus[6], 29, 53, self.frontlefttyre, self.frontlefttyre_tk_image)
                elif fltdamage < 80:
                    self.fl_percent_label.config(fg="#fda61d")
                    self.fl_percent_label.place(x=201.5, y=109.5)
                    #self.front_left_tyre_damage(listoffronttyrestatus[7])
                    imgswp.swapImages(self.canvas, listoffronttyrestatus[7], 29, 53, self.frontlefttyre, self.frontlefttyre_tk_image)
                elif fltdamage < 90:
                    self.fl_percent_label.config(fg="#fd7e1b")
                    self.fl_percent_label.place(x=201.5, y=109.5)
                    #self.front_left_tyre_damage(listoffronttyrestatus[8])
                    imgswp.swapImages(self.canvas, listoffronttyrestatus[8], 29, 53, self.frontlefttyre, self.frontlefttyre_tk_image)
                elif fltdamage < 100:
                    self.fl_percent_label.config(fg="#fe5519")
                    self.fl_percent_label.place(x=201.5, y=109.5)
                    #self.front_left_tyre_damage(listoffronttyrestatus[9])
                    imgswp.swapImages(self.canvas, listoffronttyrestatus[9], 29, 53, self.frontlefttyre, self.frontlefttyre_tk_image)
                else:
                    self.fl_percent_label.config(fg="#ff0015")
                    self.fl_percent_label.place(x=191.5, y=109.5)
                    #self.front_left_tyre_damage(listoffronttyrestatus[10])
                    imgswp.swapImages(self.canvas, listoffronttyrestatus[10], 29, 53, self.frontlefttyre, self.frontlefttyre_tk_image)

            if 'FRTyreDamage' in data_dict_cardamage:
                frtdamage = int(data_dict_cardamage['FRTyreDamage'])
                self.fr_percent_label.config(text= data_dict_cardamage['FRTyreDamage'] + "%")
                if frtdamage < 10:
                    self.fr_percent_label.config(fg="#00ff00")
                    self.fr_percent_label.place(x=541, y=109.5)
                    #self.front_right_tyre_damage(listoffronttyrestatus[0])
                    imgswp.swapImages(self.canvas, listoffronttyrestatus[0], 29, 53, self.frontrighttyre, self.frontrighttyre_tk_image)
                elif frtdamage < 20:
                    self.fr_percent_label.config(fg="#88f612")
                    self.fr_percent_label.place(x=531, y=109.5)
                    #self.front_right_tyre_damage(listoffronttyrestatus[1])
                    imgswp.swapImages(self.canvas, listoffronttyrestatus[1], 29, 53, self.frontrighttyre, self.frontrighttyre_tk_image)
                elif frtdamage < 30:
                    self.fr_percent_label.config(fg="#aef317")
                    self.fr_percent_label.place(x=531, y=109.5)
                    #self.front_right_tyre_damage(listoffronttyrestatus[2])
                    imgswp.swapImages(self.canvas, listoffronttyrestatus[2], 29, 53, self.frontrighttyre, self.frontrighttyre_tk_image)
                elif frtdamage < 40:
                    self.fr_percent_label.config(fg="#cff11b")
                    self.fr_percent_label.place(x=531, y=109.5)
                    #self.front_right_tyre_damage(listoffronttyrestatus[3])
                    imgswp.swapImages(self.canvas, listoffronttyrestatus[3], 29, 53, self.frontrighttyre, self.frontrighttyre_tk_image)
                elif frtdamage < 50:
                    self.fr_percent_label.config(fg="#ebef1f")
                    self.fr_percent_label.place(x=531, y=109.5)
                    #self.front_right_tyre_damage(listoffronttyrestatus[4])
                    imgswp.swapImages(self.canvas, listoffronttyrestatus[4], 29, 53, self.frontrighttyre, self.frontrighttyre_tk_image)
                elif frtdamage < 60:
                    self.fr_percent_label.config(fg="#fcee21")
                    self.fr_percent_label.place(x=531, y=109.5)
                    #self.front_right_tyre_damage(listoffronttyrestatus[5])
                    imgswp.swapImages(self.canvas, listoffronttyrestatus[5], 29, 53, self.frontrighttyre, self.frontrighttyre_tk_image)
                elif frtdamage < 70:
                    self.fr_percent_label.config(fg="#fccc1f")
                    self.fr_percent_label.place(x=531, y=109.5)
                    #self.front_right_tyre_damage(listoffronttyrestatus[6])
                    imgswp.swapImages(self.canvas, listoffronttyrestatus[6], 29, 53, self.frontrighttyre, self.frontrighttyre_tk_image)
                elif frtdamage < 80:
                    self.fr_percent_label.config(fg="#fda61d")
                    self.fr_percent_label.place(x=531, y=109.5)
                    #self.front_right_tyre_damage(listoffronttyrestatus[7])
                    imgswp.swapImages(self.canvas, listoffronttyrestatus[7], 29, 53, self.frontrighttyre, self.frontrighttyre_tk_image)
                elif frtdamage < 90:
                    self.fr_percent_label.config(fg="#fd7e1b")
                    self.fr_percent_label.place(x=531, y=109.5)
                    #self.front_right_tyre_damage(listoffronttyrestatus[8])
                    imgswp.swapImages(self.canvas, listoffronttyrestatus[8], 29, 53, self.frontrighttyre, self.frontrighttyre_tk_image)
                elif frtdamage < 100:
                    self.fr_percent_label.config(fg="#fe5519")
                    self.fr_percent_label.place(x=531, y=109.5)
                    #self.front_right_tyre_damage(listoffronttyrestatus[9])
                    imgswp.swapImages(self.canvas, listoffronttyrestatus[9], 29, 53, self.frontrighttyre, self.frontrighttyre_tk_image)
                else:
                    self.fr_percent_label.config(fg="#ff0015")
                    self.fr_percent_label.place(x=521, y=109.5)
                    #self.front_right_tyre_damage(listoffronttyrestatus[10])
                    imgswp.swapImages(self.canvas, listoffronttyrestatus[10], 29, 53, self.frontrighttyre, self.frontrighttyre_tk_image)

            if 'RLTyreDamage' in data_dict_cardamage:
                rltdamage = int(data_dict_cardamage['RLTyreDamage'])
                self.rl_percent_label.config(text=data_dict_cardamage['RLTyreDamage'] + "%")
                if rltdamage < 10:
                    self.rl_percent_label.config(fg="#00ff00")
                    self.rl_percent_label.place(x=211.5, y=351)
                    #self.rear_left_tyre_damage(listofreartyrestatus[0])
                    imgswp.swapImages(self.canvas, listofreartyrestatus[0], 32, 53, self.rearlefttyre, self.rearlefttyre_tk_image)
                elif rltdamage < 20:
                    self.rl_percent_label.config(fg="#88f612")
                    self.rl_percent_label.place(x=201.5, y=351)
                    #self.rear_left_tyre_damage(listofreartyrestatus[1])
                    imgswp.swapImages(self.canvas, listofreartyrestatus[1], 32, 53, self.rearlefttyre, self.rearlefttyre_tk_image)
                elif rltdamage < 30:
                    self.rl_percent_label.config(fg="#aef317")
                    self.rl_percent_label.place(x=201.5, y=351)
                    #self.rear_left_tyre_damage(listofreartyrestatus[2])
                    imgswp.swapImages(self.canvas, listofreartyrestatus[2], 32, 53, self.rearlefttyre, self.rearlefttyre_tk_image)
                elif rltdamage < 40:
                    self.rl_percent_label.config(fg="#cff11b")
                    self.rl_percent_label.place(x=201.5, y=351)
                    #self.rear_left_tyre_damage(listofreartyrestatus[3])
                    imgswp.swapImages(self.canvas, listofreartyrestatus[3], 32, 53, self.rearlefttyre, self.rearlefttyre_tk_image)
                elif rltdamage < 50:
                    self.rl_percent_label.config(fg="#ebef1f")
                    self.rl_percent_label.place(x=201.5, y=351)
                    #self.rear_left_tyre_damage(listofreartyrestatus[4])
                    imgswp.swapImages(self.canvas, listofreartyrestatus[4], 32, 53, self.rearlefttyre, self.rearlefttyre_tk_image)
                elif rltdamage < 60:
                    self.rl_percent_label.config(fg="#fcee21")
                    self.rl_percent_label.place(x=201.5, y=351)
                    #self.rear_left_tyre_damage(listofreartyrestatus[5])
                    imgswp.swapImages(self.canvas, listofreartyrestatus[5], 32, 53, self.rearlefttyre, self.rearlefttyre_tk_image)
                elif rltdamage < 70:
                    self.rl_percent_label.config(fg="#fccc1f")
                    self.rl_percent_label.place(x=201.5, y=351)
                    #self.rear_left_tyre_damage(listofreartyrestatus[6])
                    imgswp.swapImages(self.canvas, listofreartyrestatus[6], 32, 53, self.rearlefttyre, self.rearlefttyre_tk_image)
                elif rltdamage < 80:
                    self.rl_percent_label.config(fg="#fda61d")
                    self.rl_percent_label.place(x=201.5, y=351)
                    #self.rear_left_tyre_damage(listofreartyrestatus[7])
                    imgswp.swapImages(self.canvas, listofreartyrestatus[7], 32, 53, self.rearlefttyre, self.rearlefttyre_tk_image)
                elif rltdamage < 90:
                    self.rl_percent_label.config(fg="#fd7e1b")
                    self.rl_percent_label.place(x=201.5, y=351)
                    #self.rear_left_tyre_damage(listofreartyrestatus[8])
                    imgswp.swapImages(self.canvas, listofreartyrestatus[8], 32, 53, self.rearlefttyre, self.rearlefttyre_tk_image)
                elif rltdamage < 100:
                    self.rl_percent_label.config(fg="#fe5519")
                    self.rl_percent_label.place(x=201.5, y=351)
                    #self.rear_left_tyre_damage(listofreartyrestatus[9])
                    imgswp.swapImages(self.canvas, listofreartyrestatus[9], 32, 53, self.rearlefttyre, self.rearlefttyre_tk_image)
                else:
                    self.rl_percent_label.config(fg="#ff0015")
                    self.rl_percent_label.place(x=191.5, y=351)
                    #self.rear_left_tyre_damage(listofreartyrestatus[10])
                    imgswp.swapImages(self.canvas, listofreartyrestatus[10], 32, 53, self.rearlefttyre, self.rearlefttyre_tk_image)

            if 'RRTyreDamage' in data_dict_cardamage:
                rrtdamage = int(data_dict_cardamage['RRTyreDamage'])
                self.rr_percent_label.config(text=data_dict_cardamage['RRTyreDamage'] + "%")
                if rrtdamage < 10:
                    self.rr_percent_label.config(fg="#00ff00")
                    self.rr_percent_label.place(x=541, y=351)
                    #self.rear_right_tyre_damage(listofreartyrestatus[0])
                    imgswp.swapImages(self.canvas, listofreartyrestatus[0], 32, 53, self.rearrighttyre, self.rearrighttyre_tk_image)
                elif rrtdamage < 20:
                    self.rr_percent_label.config(fg="#88f612")
                    self.rr_percent_label.place(x=531, y=351)
                    #self.rear_right_tyre_damage(listofreartyrestatus[1])
                    imgswp.swapImages(self.canvas, listofreartyrestatus[1], 32, 53, self.rearrighttyre, self.rearrighttyre_tk_image)
                elif rrtdamage < 30:
                    self.rr_percent_label.config(fg="#aef317")
                    self.rr_percent_label.place(x=531, y=351)
                    #self.rear_right_tyre_damage(listofreartyrestatus[2])
                    imgswp.swapImages(self.canvas, listofreartyrestatus[2], 32, 53, self.rearrighttyre, self.rearrighttyre_tk_image)
                elif rrtdamage < 40:
                    self.rr_percent_label.config(fg="#cff11b")
                    self.rr_percent_label.place(x=531, y=351)
                    #self.rear_right_tyre_damage(listofreartyrestatus[3])
                    imgswp.swapImages(self.canvas, listofreartyrestatus[3], 32, 53, self.rearrighttyre, self.rearrighttyre_tk_image)
                elif rrtdamage < 50:
                    self.rr_percent_label.config(fg="#ebef1f")
                    self.rr_percent_label.place(x=531, y=351)
                    #self.rear_right_tyre_damage(listofreartyrestatus[4])
                    imgswp.swapImages(self.canvas, listofreartyrestatus[4], 32, 53, self.rearrighttyre, self.rearrighttyre_tk_image)
                elif rrtdamage < 60:
                    self.rr_percent_label.config(fg="#fcee21")
                    self.rr_percent_label.place(x=531, y=351)
                    #self.rear_right_tyre_damage(listofreartyrestatus[5])
                    imgswp.swapImages(self.canvas, listofreartyrestatus[5], 32, 53, self.rearrighttyre, self.rearrighttyre_tk_image)
                elif rrtdamage < 70:
                    self.rr_percent_label.config(fg="#fccc1f")
                    self.rr_percent_label.place(x=531, y=351)
                    #self.rear_right_tyre_damage(listofreartyrestatus[6])
                    imgswp.swapImages(self.canvas, listofreartyrestatus[6], 32, 53, self.rearrighttyre, self.rearrighttyre_tk_image)
                elif rrtdamage < 80:
                    self.rr_percent_label.config(fg="#fda61d")
                    self.rr_percent_label.place(x=531, y=351)
                    #self.rear_right_tyre_damage(listofreartyrestatus[7])
                    imgswp.swapImages(self.canvas, listofreartyrestatus[7], 32, 53, self.rearrighttyre, self.rearrighttyre_tk_image)
                elif rrtdamage < 90:
                    self.rr_percent_label.config(fg="#fd7e1b")
                    self.rr_percent_label.place(x=531, y=351)
                    #self.rear_right_tyre_damage(listofreartyrestatus[8])
                    imgswp.swapImages(self.canvas, listofreartyrestatus[8], 32, 53, self.rearrighttyre, self.rearrighttyre_tk_image)
                elif rrtdamage < 100:
                    self.rr_percent_label.config(fg="#fe5519")
                    self.rr_percent_label.place(x=531, y=351)
                    #self.rear_right_tyre_damage(listofreartyrestatus[9])
                    imgswp.swapImages(self.canvas, listofreartyrestatus[9], 32, 53, self.rearrighttyre, self.rearrighttyre_tk_image)
                else:
                    self.rr_percent_label.config(fg="#ff0015")
                    self.rr_percent_label.place(x=521, y=351)
                    #self.rear_right_tyre_damage(listofreartyrestatus[10])
                    imgswp.swapImages(self.canvas, listofreartyrestatus[10], 32, 53, self.rearrighttyre, self.rearrighttyre_tk_image)

            if 'FLBrakeDamage' in data_dict_cardamage:
                flbdamage = int(data_dict_cardamage['FLBrakeDamage'])
                if flbdamage < 10:
                    #self.front_left_brake_damage(listofbrakestatus[0])
                    imgswp.swapImages(self.canvas, listofbrakestatus[0], 10, 19, self.frontleftbrake, self.frontleftbrake_tk_image)
                elif flbdamage < 20:
                    #self.front_left_brake_damage(listofbrakestatus[1])
                    imgswp.swapImages(self.canvas, listofbrakestatus[1], 10, 19, self.frontleftbrake, self.frontleftbrake_tk_image)
                elif flbdamage < 30:
                    #self.front_left_brake_damage(listofbrakestatus[2])
                    imgswp.swapImages(self.canvas, listofbrakestatus[2], 10, 19, self.frontleftbrake, self.frontleftbrake_tk_image)
                elif flbdamage < 40:
                    #self.front_left_brake_damage(listofbrakestatus[3])
                    imgswp.swapImages(self.canvas, listofbrakestatus[3], 10, 19, self.frontleftbrake, self.frontleftbrake_tk_image)
                elif flbdamage < 50:
                    #self.front_left_brake_damage(listofbrakestatus[4])
                    imgswp.swapImages(self.canvas, listofbrakestatus[4], 10, 19, self.frontleftbrake, self.frontleftbrake_tk_image)
                elif flbdamage < 60:
                    #self.front_left_brake_damage(listofbrakestatus[5])
                    imgswp.swapImages(self.canvas, listofbrakestatus[5], 10, 19, self.frontleftbrake, self.frontleftbrake_tk_image)
                elif flbdamage < 70:
                    #self.front_left_brake_damage(listofbrakestatus[6])
                    imgswp.swapImages(self.canvas, listofbrakestatus[6], 10, 19, self.frontleftbrake, self.frontleftbrake_tk_image)
                elif flbdamage < 80:
                    #self.front_left_brake_damage(listofbrakestatus[7])
                    imgswp.swapImages(self.canvas, listofbrakestatus[7], 10, 19, self.frontleftbrake, self.frontleftbrake_tk_image)
                elif flbdamage < 90:
                    #self.front_left_brake_damage(listofbrakestatus[8])
                    imgswp.swapImages(self.canvas, listofbrakestatus[8], 10, 19, self.frontleftbrake, self.frontleftbrake_tk_image)
                elif flbdamage < 100:
                    #self.front_left_brake_damage(listofbrakestatus[9])
                    imgswp.swapImages(self.canvas, listofbrakestatus[9], 10, 19, self.frontleftbrake, self.frontleftbrake_tk_image)
                else:
                    #self.front_left_brake_damage(listofbrakestatus[10])
                    imgswp.swapImages(self.canvas, listofbrakestatus[10], 10, 19, self.frontleftbrake, self.frontleftbrake_tk_image)

            if 'FRBrakeDamage' in data_dict_cardamage:
                frbdamage = int(data_dict_cardamage['FRBrakeDamage'])
                if frbdamage < 10:
                    #self.front_right_brake_damage(listofbrakestatus[0])
                    imgswp.swapImages(self.canvas, listofbrakestatus[0], 10, 19, self.frontrightbrake, self.frontrightbrake_tk_image)
                elif frbdamage < 20:
                    #self.front_right_brake_damage(listofbrakestatus[1])
                    imgswp.swapImages(self.canvas, listofbrakestatus[1], 10, 19, self.frontrightbrake, self.frontrightbrake_tk_image)
                elif frbdamage < 30:
                    #self.front_right_brake_damage(listofbrakestatus[2])
                    imgswp.swapImages(self.canvas, listofbrakestatus[2], 10, 19, self.frontrightbrake, self.frontrightbrake_tk_image)
                elif frbdamage < 40:
                    #self.front_right_brake_damage(listofbrakestatus[3])
                    imgswp.swapImages(self.canvas, listofbrakestatus[3], 10, 19, self.frontrightbrake, self.frontrightbrake_tk_image)
                elif frbdamage < 50:
                    #self.front_right_brake_damage(listofbrakestatus[4])
                    imgswp.swapImages(self.canvas, listofbrakestatus[4], 10, 19, self.frontrightbrake, self.frontrightbrake_tk_image)
                elif frbdamage < 60:
                    #self.front_right_brake_damage(listofbrakestatus[5])
                    imgswp.swapImages(self.canvas, listofbrakestatus[5], 10, 19, self.frontrightbrake, self.frontrightbrake_tk_image)
                elif frbdamage < 70:
                    #self.front_right_brake_damage(listofbrakestatus[6])
                    imgswp.swapImages(self.canvas, listofbrakestatus[6], 10, 19, self.frontrightbrake, self.frontrightbrake_tk_image)
                elif frbdamage < 80:
                    #self.front_right_brake_damage(listofbrakestatus[7])
                    imgswp.swapImages(self.canvas, listofbrakestatus[7], 10, 19, self.frontrightbrake, self.frontrightbrake_tk_image)
                elif frbdamage < 90:
                    #self.front_right_brake_damage(listofbrakestatus[8])
                    imgswp.swapImages(self.canvas, listofbrakestatus[8], 10, 19, self.frontrightbrake, self.frontrightbrake_tk_image)
                elif frbdamage < 100:
                    #self.front_right_brake_damage(listofbrakestatus[9])
                    imgswp.swapImages(self.canvas, listofbrakestatus[9], 10, 19, self.frontrightbrake, self.frontrightbrake_tk_image)
                else:
                    #self.front_right_brake_damage(listofbrakestatus[10])
                    imgswp.swapImages(self.canvas, listofbrakestatus[10], 10, 19, self.frontrightbrake, self.frontrightbrake_tk_image)

            if 'RLBrakeDamage' in data_dict_cardamage:
                rlbdamage = int(data_dict_cardamage['RLBrakeDamage'])
                if rlbdamage < 10:
                    #self.rear_left_brake_damage(listofbrakestatus[0])
                    imgswp.swapImages(self.canvas, listofbrakestatus[0], 10, 19, self.rearleftbrake, self.rearleftbrake_tk_image)
                elif rlbdamage < 20:
                    #self.rear_left_brake_damage(listofbrakestatus[1])
                    imgswp.swapImages(self.canvas, listofbrakestatus[1], 10, 19, self.rearleftbrake, self.rearleftbrake_tk_image)
                elif rlbdamage < 30:
                    #self.rear_left_brake_damage(listofbrakestatus[2])
                    imgswp.swapImages(self.canvas, listofbrakestatus[2], 10, 19, self.rearleftbrake, self.rearleftbrake_tk_image)
                elif rlbdamage < 40:
                    #self.rear_left_brake_damage(listofbrakestatus[3])
                    imgswp.swapImages(self.canvas, listofbrakestatus[3], 10, 19, self.rearleftbrake, self.rearleftbrake_tk_image)
                elif rlbdamage < 50:
                    #self.rear_left_brake_damage(listofbrakestatus[4])
                    imgswp.swapImages(self.canvas, listofbrakestatus[4], 10, 19, self.rearleftbrake, self.rearleftbrake_tk_image)
                elif rlbdamage < 60:
                    #self.rear_left_brake_damage(listofbrakestatus[5])
                    imgswp.swapImages(self.canvas, listofbrakestatus[5], 10, 19, self.rearleftbrake, self.rearleftbrake_tk_image)
                elif rlbdamage < 70:
                    #self.rear_left_brake_damage(listofbrakestatus[6])
                    imgswp.swapImages(self.canvas, listofbrakestatus[6], 10, 19, self.rearleftbrake, self.rearleftbrake_tk_image)
                elif rlbdamage < 80:
                    #self.rear_left_brake_damage(listofbrakestatus[7])
                    imgswp.swapImages(self.canvas, listofbrakestatus[7], 10, 19, self.rearleftbrake, self.rearleftbrake_tk_image)
                elif rlbdamage < 90:
                    #self.rear_left_brake_damage(listofbrakestatus[8])
                    imgswp.swapImages(self.canvas, listofbrakestatus[8], 10, 19, self.rearleftbrake, self.rearleftbrake_tk_image)
                elif rlbdamage < 100:
                    #self.rear_left_brake_damage(listofbrakestatus[9])
                    imgswp.swapImages(self.canvas, listofbrakestatus[9], 10, 19, self.rearleftbrake, self.rearleftbrake_tk_image)
                else:
                    #self.rear_left_brake_damage(listofbrakestatus[10])
                    imgswp.swapImages(self.canvas, listofbrakestatus[10], 10, 19, self.rearleftbrake, self.rearleftbrake_tk_image)

            if 'RRBrakeDamage' in data_dict_cardamage:
                rrbdamage = int(data_dict_cardamage['RRBrakeDamage'])
                if rrbdamage < 10:
                    #self.rear_right_brake_damage(listofbrakestatus[0])
                    imgswp.swapImages(self.canvas, listofbrakestatus[0], 10, 19, self.rearrightbrake, self.rearrightbrake_tk_image)
                elif rrbdamage < 20:
                    #self.rear_right_brake_damage(listofbrakestatus[1])
                    imgswp.swapImages(self.canvas, listofbrakestatus[1], 10, 19, self.rearrightbrake, self.rearrightbrake_tk_image)
                elif rrbdamage < 30:
                    #self.rear_right_brake_damage(listofbrakestatus[2])
                    imgswp.swapImages(self.canvas, listofbrakestatus[2], 10, 19, self.rearrightbrake, self.rearrightbrake_tk_image)
                elif rrbdamage < 40:
                    #self.rear_right_brake_damage(listofbrakestatus[3])
                    imgswp.swapImages(self.canvas, listofbrakestatus[3], 10, 19, self.rearrightbrake, self.rearrightbrake_tk_image)
                elif rrbdamage < 50:
                    #self.rear_right_brake_damage(listofbrakestatus[4])
                    imgswp.swapImages(self.canvas, listofbrakestatus[4], 10, 19, self.rearrightbrake, self.rearrightbrake_tk_image)
                elif rrbdamage < 60:
                    #self.rear_right_brake_damage(listofbrakestatus[5])
                    imgswp.swapImages(self.canvas, listofbrakestatus[5], 10, 19, self.rearrightbrake, self.rearrightbrake_tk_image)
                elif rrbdamage < 70:
                    #self.rear_right_brake_damage(listofbrakestatus[6])
                    imgswp.swapImages(self.canvas, listofbrakestatus[6], 10, 19, self.rearrightbrake, self.rearrightbrake_tk_image)
                elif rrbdamage < 80:
                    #self.rear_right_brake_damage(listofbrakestatus[7])
                    imgswp.swapImages(self.canvas, listofbrakestatus[7], 10, 19, self.rearrightbrake, self.rearrightbrake_tk_image)
                elif rrbdamage < 90:
                    #self.rear_right_brake_damage(listofbrakestatus[8])
                    imgswp.swapImages(self.canvas, listofbrakestatus[8], 10, 19, self.rearrightbrake, self.rearrightbrake_tk_image)
                elif rrbdamage < 100:
                    #self.rear_right_brake_damage(listofbrakestatus[9])
                    imgswp.swapImages(self.canvas, listofbrakestatus[9], 10, 19, self.rearrightbrake, self.rearrightbrake_tk_image)
                else:
                    #self.rear_right_brake_damage(listofbrakestatus[10])
                    imgswp.swapImages(self.canvas, listofbrakestatus[10], 10, 19, self.rearrightbrake, self.rearrightbrake_tk_image)

            if 'rearWingDamage' in data_dict_cardamage:
                rwdamage = int(data_dict_cardamage['rearWingDamage'])
                if rwdamage < 10:
                    #self.rear_wing_damage(listofrearwingstatus[0])
                    imgswp.swapImages(self.canvas, listofrearwingstatus[0], 91, 36, self.rearwing, self.rearwing_tk_image)
                elif rwdamage < 20:
                    #self.rear_wing_damage(listofrearwingstatus[1])
                    imgswp.swapImages(self.canvas, listofrearwingstatus[1], 91, 36, self.rearwing, self.rearwing_tk_image)
                elif rwdamage < 30:
                    #self.rear_wing_damage(listofrearwingstatus[2])
                    imgswp.swapImages(self.canvas, listofrearwingstatus[2], 91, 36, self.rearwing, self.rearwing_tk_image)
                elif rwdamage < 40:
                    #self.rear_wing_damage(listofrearwingstatus[3])
                    imgswp.swapImages(self.canvas, listofrearwingstatus[3], 91, 36, self.rearwing, self.rearwing_tk_image)
                elif rwdamage < 50:
                    #self.rear_wing_damage(listofrearwingstatus[4])
                    imgswp.swapImages(self.canvas, listofrearwingstatus[4], 91, 36, self.rearwing, self.rearwing_tk_image)
                elif rwdamage < 60:
                    #self.rear_wing_damage(listofrearwingstatus[5])
                    imgswp.swapImages(self.canvas, listofrearwingstatus[5], 91, 36, self.rearwing, self.rearwing_tk_image)
                elif rwdamage < 70:
                    #self.rear_wing_damage(listofrearwingstatus[6])
                    imgswp.swapImages(self.canvas, listofrearwingstatus[6], 91, 36, self.rearwing, self.rearwing_tk_image)
                elif rwdamage < 80:
                    #self.rear_wing_damage(listofrearwingstatus[7])
                    imgswp.swapImages(self.canvas, listofrearwingstatus[7], 91, 36, self.rearwing, self.rearwing_tk_image)
                elif rwdamage < 90:
                    #self.rear_wing_damage(listofrearwingstatus[8])
                    imgswp.swapImages(self.canvas, listofrearwingstatus[8], 91, 36, self.rearwing, self.rearwing_tk_image)
                elif rwdamage < 100:
                    #self.rear_wing_damage(listofrearwingstatus[9])
                    imgswp.swapImages(self.canvas, listofrearwingstatus[9], 91, 36, self.rearwing, self.rearwing_tk_image)
                else:
                    #self.rear_wing_damage(listofrearwingstatus[10])
                    imgswp.swapImages(self.canvas, listofrearwingstatus[10], 91, 36, self.rearwing, self.rearwing_tk_image)

            if 'floorDamage' in data_dict_cardamage:
                lfdamage = int(data_dict_cardamage['floorDamage'])
                if lfdamage < 10:
                    #self.left_floor_damage(listoffloorleftstatus[0])
                    imgswp.swapImages(self.canvas, listoffloorleftstatus[0], 45, 182, self.leftfloor, self.leftfloor_tk_image)
                    imgswp.swapImages(self.canvas, listoffloorrightstatus[0], 45, 182, self.rightfloor, self.rightfloor_tk_image)
                elif lfdamage < 20:
                    #self.left_floor_damage(listoffloorleftstatus[1])
                    imgswp.swapImages(self.canvas, listoffloorleftstatus[1], 45, 182, self.leftfloor, self.leftfloor_tk_image)
                    imgswp.swapImages(self.canvas, listoffloorrightstatus[1], 45, 182, self.rightfloor, self.rightfloor_tk_image)
                elif lfdamage < 30:
                    #self.left_floor_damage(listoffloorleftstatus[2])
                    imgswp.swapImages(self.canvas, listoffloorleftstatus[2], 45, 182, self.leftfloor, self.leftfloor_tk_image)
                    imgswp.swapImages(self.canvas, listoffloorrightstatus[2], 45, 182, self.rightfloor, self.rightfloor_tk_image)
                elif lfdamage < 40:
                    #self.left_floor_damage(listoffloorleftstatus[3])
                    imgswp.swapImages(self.canvas, listoffloorleftstatus[3], 45, 182, self.leftfloor, self.leftfloor_tk_image)
                    imgswp.swapImages(self.canvas, listoffloorrightstatus[3], 45, 182, self.rightfloor, self.rightfloor_tk_image)
                elif lfdamage < 50:
                    #self.left_floor_damage(listoffloorleftstatus[4])
                    imgswp.swapImages(self.canvas, listoffloorleftstatus[4], 45, 182, self.leftfloor, self.leftfloor_tk_image)
                    imgswp.swapImages(self.canvas, listoffloorrightstatus[4], 45, 182, self.rightfloor, self.rightfloor_tk_image)
                elif lfdamage < 60:
                    #self.left_floor_damage(listoffloorleftstatus[5])
                    imgswp.swapImages(self.canvas, listoffloorleftstatus[5], 45, 182, self.leftfloor, self.leftfloor_tk_image)
                    imgswp.swapImages(self.canvas, listoffloorrightstatus[5], 45, 182, self.rightfloor, self.rightfloor_tk_image)
                elif lfdamage < 70:
                    #self.left_floor_damage(listoffloorleftstatus[6])
                    imgswp.swapImages(self.canvas, listoffloorleftstatus[6], 45, 182, self.leftfloor, self.leftfloor_tk_image)
                    imgswp.swapImages(self.canvas, listoffloorrightstatus[6], 45, 182, self.rightfloor, self.rightfloor_tk_image)
                elif lfdamage < 80:
                    #self.left_floor_damage(listoffloorleftstatus[7])
                    imgswp.swapImages(self.canvas, listoffloorleftstatus[7], 45, 182, self.leftfloor, self.leftfloor_tk_image)
                    imgswp.swapImages(self.canvas, listoffloorrightstatus[7], 45, 182, self.rightfloor, self.rightfloor_tk_image)
                elif lfdamage < 90:
                    #self.left_floor_damage(listoffloorleftstatus[8])
                    imgswp.swapImages(self.canvas, listoffloorleftstatus[8], 45, 182, self.leftfloor, self.leftfloor_tk_image)
                    imgswp.swapImages(self.canvas, listoffloorrightstatus[8], 45, 182, self.rightfloor, self.rightfloor_tk_image)
                elif lfdamage < 100:
                    #self.left_floor_damage(listoffloorleftstatus[9])
                    imgswp.swapImages(self.canvas, listoffloorleftstatus[9], 45, 182, self.leftfloor, self.leftfloor_tk_image)
                    imgswp.swapImages(self.canvas, listoffloorrightstatus[9], 45, 182, self.rightfloor, self.rightfloor_tk_image)
                else:
                    #self.left_floor_damage(listoffloorleftstatus[10])
                    imgswp.swapImages(self.canvas, listoffloorleftstatus[10], 45, 182, self.leftfloor, self.leftfloor_tk_image)
                    imgswp.swapImages(self.canvas, listoffloorrightstatus[10], 45, 182, self.rightfloor, self.rightfloor_tk_image)

            if 'sidepodDamage' in data_dict_cardamage:
                lsddamage = int(data_dict_cardamage['sidepodDamage'])
                if lsddamage < 10:
                    #self.left_sidepod_damage(listofsidepodleftstatus[0])
                    imgswp.swapImages(self.canvas, listofsidepodleftstatus[0], 37, 124, self.leftsidepod, self.leftsidepod_tk_image)
                    imgswp.swapImages(self.canvas, listofsidepodrightstatus[0], 37, 124, self.rightsidepod, self.rightsidepod_tk_image)
                elif lsddamage < 20:
                    #self.left_sidepod_damage(listofsidepodleftstatus[1])
                    imgswp.swapImages(self.canvas, listofsidepodleftstatus[1], 37, 124, self.leftsidepod, self.leftsidepod_tk_image)
                    imgswp.swapImages(self.canvas, listofsidepodrightstatus[1], 37, 124, self.rightsidepod, self.rightsidepod_tk_image)
                elif lsddamage < 30:
                    #self.left_sidepod_damage(listofsidepodleftstatus[2])
                    imgswp.swapImages(self.canvas, listofsidepodleftstatus[2], 37, 124, self.leftsidepod, self.leftsidepod_tk_image)
                    imgswp.swapImages(self.canvas, listofsidepodrightstatus[2], 37, 124, self.rightsidepod, self.rightsidepod_tk_image)
                elif lsddamage < 40:
                    #self.left_sidepod_damage(listofsidepodleftstatus[3])
                    imgswp.swapImages(self.canvas, listofsidepodleftstatus[3], 37, 124, self.leftsidepod, self.leftsidepod_tk_image)
                    imgswp.swapImages(self.canvas, listofsidepodrightstatus[3], 37, 124, self.rightsidepod, self.rightsidepod_tk_image)
                elif lsddamage < 50:
                    #self.left_sidepod_damage(listofsidepodleftstatus[4])
                    imgswp.swapImages(self.canvas, listofsidepodleftstatus[4], 37, 124, self.leftsidepod, self.leftsidepod_tk_image)
                    imgswp.swapImages(self.canvas, listofsidepodrightstatus[4], 37, 124, self.rightsidepod, self.rightsidepod_tk_image)
                elif lsddamage < 60:
                    #self.left_sidepod_damage(listofsidepodleftstatus[5])
                    imgswp.swapImages(self.canvas, listofsidepodleftstatus[5], 37, 124, self.leftsidepod, self.leftsidepod_tk_image)
                    imgswp.swapImages(self.canvas, listofsidepodrightstatus[5], 37, 124, self.rightsidepod, self.rightsidepod_tk_image)
                elif lsddamage < 70:
                    #self.left_sidepod_damage(listofsidepodleftstatus[6])
                    imgswp.swapImages(self.canvas, listofsidepodleftstatus[6], 37, 124, self.leftsidepod, self.leftsidepod_tk_image)
                    imgswp.swapImages(self.canvas, listofsidepodrightstatus[6], 37, 124, self.rightsidepod, self.rightsidepod_tk_image)
                elif lsddamage < 80:
                    #self.left_sidepod_damage(listofsidepodleftstatus[7])
                    imgswp.swapImages(self.canvas, listofsidepodleftstatus[7], 37, 124, self.leftsidepod, self.leftsidepod_tk_image)
                    imgswp.swapImages(self.canvas, listofsidepodrightstatus[7], 37, 124, self.rightsidepod, self.rightsidepod_tk_image)
                elif lsddamage < 90:
                    #self.left_sidepod_damage(listofsidepodleftstatus[8])
                    imgswp.swapImages(self.canvas, listofsidepodleftstatus[8], 37, 124, self.leftsidepod, self.leftsidepod_tk_image)
                    imgswp.swapImages(self.canvas, listofsidepodrightstatus[8], 37, 124, self.rightsidepod, self.rightsidepod_tk_image)
                elif lsddamage < 100:
                    #self.left_sidepod_damage(listofsidepodleftstatus[9])
                    imgswp.swapImages(self.canvas, listofsidepodleftstatus[9], 37, 124, self.leftsidepod, self.leftsidepod_tk_image)
                    imgswp.swapImages(self.canvas, listofsidepodrightstatus[9], 37, 124, self.rightsidepod, self.rightsidepod_tk_image)
                else:
                    #self.left_sidepod_damage(listofsidepodleftstatus[10])
                    imgswp.swapImages(self.canvas, listofsidepodleftstatus[10], 37, 124, self.leftsidepod, self.leftsidepod_tk_image)
                    imgswp.swapImages(self.canvas, listofsidepodrightstatus[10], 37, 124, self.rightsidepod, self.rightsidepod_tk_image)

            if 'engineDamage' in data_dict_cardamage:
                edamage = int(data_dict_cardamage['engineDamage'])
                if edamage < 10:
                    #self.engine_damage(listofenginestatus[0])
                    imgswp.swapImages(self.canvas, listofenginestatus[0], 51, 60, self.engine, self.engine_tk_image)
                elif edamage < 20:
                    #self.engine_damage(listofenginestatus[1])
                    imgswp.swapImages(self.canvas, listofenginestatus[1], 51, 60, self.engine, self.engine_tk_image)
                elif edamage < 30:
                    #self.engine_damage(listofenginestatus[2])
                    imgswp.swapImages(self.canvas, listofenginestatus[2], 51, 60, self.engine, self.engine_tk_image)
                elif edamage < 40:
                    #self.engine_damage(listofenginestatus[3])
                    imgswp.swapImages(self.canvas, listofenginestatus[3], 51, 60, self.engine, self.engine_tk_image)
                elif edamage < 50:
                    #self.engine_damage(listofenginestatus[4])
                    imgswp.swapImages(self.canvas, listofenginestatus[4], 51, 60, self.engine, self.engine_tk_image)
                elif edamage < 60:
                    #self.engine_damage(listofenginestatus[5])
                    imgswp.swapImages(self.canvas, listofenginestatus[5], 51, 60, self.engine, self.engine_tk_image)
                elif edamage < 70:
                    #self.engine_damage(listofenginestatus[6])
                    imgswp.swapImages(self.canvas, listofenginestatus[6], 51, 60, self.engine, self.engine_tk_image)
                elif edamage < 80:
                    #self.engine_damage(listofenginestatus[7])
                    imgswp.swapImages(self.canvas, listofenginestatus[7], 51, 60, self.engine, self.engine_tk_image)
                elif edamage < 90:
                    #self.engine_damage(listofenginestatus[8])
                    imgswp.swapImages(self.canvas, listofenginestatus[8], 51, 60, self.engine, self.engine_tk_image)
                elif edamage < 100:
                    #self.engine_damage(listofenginestatus[9])
                    imgswp.swapImages(self.canvas, listofenginestatus[9], 51, 60, self.engine, self.engine_tk_image)
                else:
                    #self.engine_damage(listofenginestatus[10])
                    imgswp.swapImages(self.canvas, listofenginestatus[10], 51, 60, self.engine, self.engine_tk_image)

            if 'gearBoxDamage' in data_dict_cardamage:
                gdamage = int(data_dict_cardamage['gearBoxDamage'])
                if gdamage < 10:
                    #self.gearbox_damage(listofgearboxstatus[0])
                    imgswp.swapImages(self.canvas, listofgearboxstatus[0], 14, 47, self.gearbox, self.gearbox_tk_image)
                elif gdamage < 20:
                    #self.gearbox_damage(listofgearboxstatus[1])
                    imgswp.swapImages(self.canvas, listofgearboxstatus[1], 14, 47, self.gearbox, self.gearbox_tk_image)
                elif gdamage < 30:
                    #self.gearbox_damage(listofgearboxstatus[2])
                    imgswp.swapImages(self.canvas, listofgearboxstatus[2], 14, 47, self.gearbox, self.gearbox_tk_image)
                elif gdamage < 40:
                    #self.gearbox_damage(listofgearboxstatus[3])
                    imgswp.swapImages(self.canvas, listofgearboxstatus[3], 14, 47, self.gearbox, self.gearbox_tk_image)
                elif gdamage < 50:
                    #self.gearbox_damage(listofgearboxstatus[4])
                    imgswp.swapImages(self.canvas, listofgearboxstatus[4], 14, 47, self.gearbox, self.gearbox_tk_image)
                elif gdamage < 60:
                    #self.gearbox_damage(listofgearboxstatus[5])
                    imgswp.swapImages(self.canvas, listofgearboxstatus[5], 14, 47, self.gearbox, self.gearbox_tk_image)
                elif gdamage < 70:
                    #self.gearbox_damage(listofgearboxstatus[6])
                    imgswp.swapImages(self.canvas, listofgearboxstatus[6], 14, 47, self.gearbox, self.gearbox_tk_image)
                elif gdamage < 80:
                    #self.gearbox_damage(listofgearboxstatus[7])
                    imgswp.swapImages(self.canvas, listofgearboxstatus[7], 14, 47, self.gearbox, self.gearbox_tk_image)
                elif gdamage < 90:
                    #self.gearbox_damage(listofgearboxstatus[8])
                    imgswp.swapImages(self.canvas, listofgearboxstatus[8], 14, 47, self.gearbox, self.gearbox_tk_image)
                elif gdamage < 100:
                    #self.gearbox_damage(listofgearboxstatus[9])
                    imgswp.swapImages(self.canvas, listofgearboxstatus[9], 14, 47, self.gearbox, self.gearbox_tk_image)
                else:
                    #self.gearbox_damage(listofgearboxstatus[10])
                    imgswp.swapImages(self.canvas, listofgearboxstatus[10], 14, 47, self.gearbox, self.gearbox_tk_image)

            if 'diffuserDamage' in data_dict_cardamage:
                ddamage = int(data_dict_cardamage['diffuserDamage'])
                if ddamage < 10:
                    #self.diffuser_damage(listofdiffuserstatus[0])
                    imgswp.swapImages(self.canvas, listofdiffuserstatus[0], 53, 18, self.diffuser, self.diffuser_tk_image)
                elif ddamage < 20:
                    #self.diffuser_damage(listofdiffuserstatus[1])
                    imgswp.swapImages(self.canvas, listofdiffuserstatus[1], 53, 18, self.diffuser, self.diffuser_tk_image)
                elif ddamage < 30:
                    #self.diffuser_damage(listofdiffuserstatus[2])
                    imgswp.swapImages(self.canvas, listofdiffuserstatus[2], 53, 18, self.diffuser, self.diffuser_tk_image)
                elif ddamage < 40:
                    #self.diffuser_damage(listofdiffuserstatus[3])
                    imgswp.swapImages(self.canvas, listofdiffuserstatus[3], 53, 18, self.diffuser, self.diffuser_tk_image)
                elif ddamage < 50:
                    #self.diffuser_damage(listofdiffuserstatus[4])
                    imgswp.swapImages(self.canvas, listofdiffuserstatus[4], 53, 18, self.diffuser, self.diffuser_tk_image)
                elif ddamage < 60:
                    #self.diffuser_damage(listofdiffuserstatus[5])
                    imgswp.swapImages(self.canvas, listofdiffuserstatus[5], 53, 18, self.diffuser, self.diffuser_tk_image)
                elif ddamage < 70:
                    #self.diffuser_damage(listofdiffuserstatus[6])
                    imgswp.swapImages(self.canvas, listofdiffuserstatus[6], 53, 18, self.diffuser, self.diffuser_tk_image)
                elif ddamage < 80:
                    #self.diffuser_damage(listofdiffuserstatus[7])
                    imgswp.swapImages(self.canvas, listofdiffuserstatus[7], 53, 18, self.diffuser, self.diffuser_tk_image)
                elif ddamage < 90:
                    #self.diffuser_damage(listofdiffuserstatus[8])
                    imgswp.swapImages(self.canvas, listofdiffuserstatus[8], 53, 18, self.diffuser, self.diffuser_tk_image)
                elif ddamage < 100:
                    #self.diffuser_damage(listofdiffuserstatus[9])
                    imgswp.swapImages(self.canvas, listofdiffuserstatus[9], 53, 18, self.diffuser, self.diffuser_tk_image)
                else:
                    #self.diffuser_damage(listofdiffuserstatus[10])
                    imgswp.swapImages(self.canvas, listofdiffuserstatus[10], 53, 18, self.diffuser, self.diffuser_tk_image)

            if 'ersFault' in data_dict_cardamage:
                ersdamage = int(data_dict_cardamage['ersFault'])
                if ersdamage == 0:
                    #self.ers_update('car_damage_pngs/ERS_good.png')
                    imgswp.swapImages(self.canvas, 'car_damage_pngs/ERS_good.png', 150, 76, self.ers, self.ers_tk_image)
                else:
                    #self.ers_update('car_damage_pngs/ERS_fault.png')
                    imgswp.swapImages(self.canvas, 'car_damage_pngs/ERS_fault.png', 150, 76, self.ers, self.ers_tk_image)

            if 'drsFault' in data_dict_cardamage:
                drsdamage = int(data_dict_cardamage['drsFault'])
                if drsdamage == 0:
                    #self.drs_update('car_damage_pngs/DRS_good.png')
                    imgswp.swapImages(self.canvas, 'car_damage_pngs/DRS_good.png', 150, 76, self.drs, self.drs_tk_image)
                else:
                    #self.drs_update('car_damage_pngs/DRS_fault.png')
                    imgswp.swapImages(self.canvas, 'car_damage_pngs/DRS_fault.png', 150, 76, self.drs, self.drs_tk_image)

            self.root.after(5, self.update_damage_display)
class Engine:

    def __init__(self, root):
        self.root = root

    def create_engine_display(self):
        self.canvas = tk.Canvas(self.root, height=480, width=800, bg="black", highlightthickness=0)
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

    def update_engine_display(self):
        global data_dict_cardamage
        imgswp = ImageSwapper()
        if self.canvas is not None and self.canvas.winfo_exists():
            if 'engineMGUHWear' in data_dict_cardamage:
                mguh = int(data_dict_cardamage['engineMGUHWear'])
                self.mguh_percent_label.config(text=str(data_dict_cardamage['engineMGUHWear'])+ "%")
                if mguh < 10:
                    self.mguh_percent_label.config(fg="#00ff00")
                    self.mguh_percent_label.place(x = 280, y = 60)
                    #self.update_mguh_img(listofmguhwear[0])
                    imgswp.swapImageWithoutResize(self.canvas, listofmguhwear[0], self.mguh, self.mguh_tk_image)
                elif mguh < 20:
                    self.mguh_percent_label.config(fg="#88f612")
                    self.mguh_percent_label.place(x=260, y=60)
                    #self.update_mguh_img(listofmguhwear[1])
                    imgswp.swapImageWithoutResize(self.canvas, listofmguhwear[1], self.mguh, self.mguh_tk_image)
                elif mguh < 30:
                    self.mguh_percent_label.config(fg="#aef317")
                    self.mguh_percent_label.place(x=260, y=60)
                    #self.update_mguh_img(listofmguhwear[2])
                    imgswp.swapImageWithoutResize(self.canvas, listofmguhwear[2], self.mguh, self.mguh_tk_image)
                elif mguh < 40:
                    self.mguh_percent_label.config(fg="#cff11b")
                    self.mguh_percent_label.place(x=260, y=60)
                    #self.update_mguh_img(listofmguhwear[3])
                    imgswp.swapImageWithoutResize(self.canvas, listofmguhwear[3], self.mguh, self.mguh_tk_image)
                elif mguh < 50:
                    self.mguh_percent_label.config(fg="#ebef1f")
                    self.mguh_percent_label.place(x=260, y=60)
                    #self.update_mguh_img(listofmguhwear[4])
                    imgswp.swapImageWithoutResize(self.canvas, listofmguhwear[4], self.mguh, self.mguh_tk_image)
                elif mguh < 60:
                    self.mguh_percent_label.config(fg="#fcee21")
                    self.mguh_percent_label.place(x=260, y=60)
                    #self.update_mguh_img(listofmguhwear[5])
                    imgswp.swapImageWithoutResize(self.canvas, listofmguhwear[5], self.mguh, self.mguh_tk_image)
                elif mguh < 70:
                    self.mguh_percent_label.config(fg="#fccc1f")
                    self.mguh_percent_label.place(x=260, y=60)
                    #self.update_mguh_img(listofmguhwear[6])
                    imgswp.swapImageWithoutResize(self.canvas, listofmguhwear[6], self.mguh, self.mguh_tk_image)
                elif mguh < 80:
                    self.mguh_percent_label.config(fg="#fda61d")
                    self.mguh_percent_label.place(x=260, y=60)
                    #self.update_mguh_img(listofmguhwear[7])
                    imgswp.swapImageWithoutResize(self.canvas, listofmguhwear[7], self.mguh, self.mguh_tk_image)
                elif mguh < 90:
                    self.mguh_percent_label.config(fg="#fd7e1b")
                    self.mguh_percent_label.place(x=260, y=60)
                    #self.update_mguh_img(listofmguhwear[8])
                    imgswp.swapImageWithoutResize(self.canvas, listofmguhwear[8], self.mguh, self.mguh_tk_image)
                elif mguh < 100:
                    self.mguh_percent_label.config(fg="#fe5519")
                    self.mguh_percent_label.place(x=260, y=60)
                    #self.update_mguh_img(listofmguhwear[9])
                    imgswp.swapImageWithoutResize(self.canvas, listofmguhwear[9], self.mguh, self.mguh_tk_image)
                else:
                    self.mguh_percent_label.config(fg="#ff0015")
                    self.mguh_percent_label.place(x=230, y=60)
                    #self.update_mguh_img(listofmguhwear[10])
                    imgswp.swapImageWithoutResize(self.canvas, listofmguhwear[10], self.mguh, self.mguh_tk_image)

            if 'engineMGUKWear' in data_dict_cardamage:
                mguk = int(data_dict_cardamage['engineMGUKWear'])
                self.mguk_percent_label.config(text=str(data_dict_cardamage['engineMGUKWear']) + "%")
                if mguk < 10:
                    self.mguk_percent_label.config(fg="#00ff00")
                    self.mguk_percent_label.place(x=280, y=272)
                    #self.update_mguk_img(listofmgukwear[0])
                    imgswp.swapImageWithoutResize(self.canvas, listofmgukwear[0], self.mguk, self.mguk_tk_image)
                elif mguk < 20:
                    self.mguk_percent_label.config(fg="#88f612")
                    self.mguk_percent_label.place(x=260, y=272)
                    #self.update_mguk_img(listofmgukwear[1])
                    imgswp.swapImageWithoutResize(self.canvas, listofmgukwear[1], self.mguk, self.mguk_tk_image)
                elif mguk < 30:
                    self.mguk_percent_label.config(fg="#aef317")
                    self.mguk_percent_label.place(x=260, y=272)
                    #self.update_mguk_img(listofmgukwear[2])
                    imgswp.swapImageWithoutResize(self.canvas, listofmgukwear[2], self.mguk, self.mguk_tk_image)
                elif mguk < 40:
                    self.mguk_percent_label.config(fg="#cff11b")
                    self.mguk_percent_label.place(x=260, y=272)
                    #self.update_mguk_img(listofmgukwear[3])
                    imgswp.swapImageWithoutResize(self.canvas, listofmgukwear[3], self.mguk, self.mguk_tk_image)
                elif mguk < 50:
                    self.mguh_percent_label.config(fg="#ebef1f")
                    self.mguk_percent_label.place(x=260, y=272)
                    #self.update_mguk_img(listofmgukwear[4])
                    imgswp.swapImageWithoutResize(self.canvas, listofmgukwear[4], self.mguk, self.mguk_tk_image)
                elif mguk < 60:
                    self.mguk_percent_label.config(fg="#fcee21")
                    self.mguk_percent_label.place(x=260, y=272)
                    #self.update_mguk_img(listofmgukwear[5])
                    imgswp.swapImageWithoutResize(self.canvas, listofmgukwear[5], self.mguk, self.mguk_tk_image)
                elif mguk < 70:
                    self.mguk_percent_label.config(fg="#fccc1f")
                    self.mguk_percent_label.place(x=260, y=272)
                    #self.update_mguk_img(listofmgukwear[6])
                    imgswp.swapImageWithoutResize(self.canvas, listofmgukwear[6], self.mguk, self.mguk_tk_image)
                elif mguk < 80:
                    self.mguk_percent_label.config(fg="#fda61d")
                    self.mguk_percent_label.place(x=260, y=272)
                    #self.update_mguk_img(listofmgukwear[7])
                    imgswp.swapImageWithoutResize(self.canvas, listofmgukwear[7], self.mguk, self.mguk_tk_image)
                elif mguk < 90:
                    self.mguh_percent_label.config(fg="#fd7e1b")
                    self.mguk_percent_label.place(x=260, y=272)
                    #self.update_mguk_img(listofmgukwear[8])
                    imgswp.swapImageWithoutResize(self.canvas, listofmgukwear[8], self.mguk, self.mguk_tk_image)
                elif mguk < 100:
                    self.mguk_percent_label.config(fg="#fe5519")
                    self.mguk_percent_label.place(x=260, y=272)
                    #self.update_mguk_img(listofmgukwear[9])
                    imgswp.swapImageWithoutResize(self.canvas, listofmgukwear[9], self.mguk, self.mguk_tk_image)
                else:
                    self.mguk_percent_label.config(fg="#ff0015")
                    self.mguk_percent_label.place(x=230, y=272)
                    #self.update_mguk_img(listofmgukwear[10])
                    imgswp.swapImageWithoutResize(self.canvas, listofmgukwear[10], self.mguk, self.mguk_tk_image)

            if 'engineESWear' in data_dict_cardamage:
                es = int(data_dict_cardamage['engineESWear'])
                self.es_percent_label.config(text=str(data_dict_cardamage['engineESWear']) + "%")
                if es < 10:
                    self.es_percent_label.config(fg="#00ff00")
                    self.es_percent_label.place(x=280, y=114)
                    #self.update_es_img(listofeswear[0])
                    imgswp.swapImageWithoutResize(self.canvas, listofeswear[0], self.es, self.es_tk_image)
                elif es < 20:
                    self.es_percent_label.config(fg="#88f612")
                    self.es_percent_label.place(x=260, y=114)
                    #self.update_es_img(listofeswear[1])
                    imgswp.swapImageWithoutResize(self.canvas, listofeswear[1], self.es, self.es_tk_image)
                elif es < 30:
                    self.es_percent_label.config(fg="#aef317")
                    self.es_percent_label.place(x=260, y=114)
                    #self.update_es_img(listofeswear[2])
                    imgswp.swapImageWithoutResize(self.canvas, listofeswear[2], self.es, self.es_tk_image)
                elif es < 40:
                    self.es_percent_label.config(fg="#cff11b")
                    self.es_percent_label.place(x=260, y=114)
                    #self.update_es_img(listofeswear[3])
                    imgswp.swapImageWithoutResize(self.canvas, listofeswear[3], self.es, self.es_tk_image)
                elif es < 50:
                    self.es_percent_label.config(fg="#ebef1f")
                    self.es_percent_label.place(x=260, y=114)
                    #self.update_es_img(listofeswear[4])
                    imgswp.swapImageWithoutResize(self.canvas, listofeswear[4], self.es, self.es_tk_image)
                elif es < 60:
                    self.es_percent_label.config(fg="#fcee21")
                    self.es_percent_label.place(x=260, y=114)
                    #self.update_es_img(listofeswear[5])
                    imgswp.swapImageWithoutResize(self.canvas, listofeswear[5], self.es, self.es_tk_image)
                elif es < 70:
                    self.es_percent_label.config(fg="#fccc1f")
                    self.es_percent_label.place(x=260, y=114)
                    #self.update_es_img(listofeswear[6])
                    imgswp.swapImageWithoutResize(self.canvas, listofeswear[6], self.es, self.es_tk_image)
                elif es < 80:
                    self.es_percent_label.config(fg="#fda61d")
                    self.es_percent_label.place(x=260, y=114)
                    #self.update_es_img(listofeswear[7])
                    imgswp.swapImageWithoutResize(self.canvas, listofeswear[7], self.es, self.es_tk_image)
                elif es < 90:
                    self.es_percent_label.config(fg="#fd7e1b")
                    self.es_percent_label.place(x=260, y=114)
                    #self.update_es_img(listofeswear[8])
                    imgswp.swapImageWithoutResize(self.canvas, listofeswear[8], self.es, self.es_tk_image)
                elif es < 100:
                    self.es_percent_label.config(fg="#fe5519")
                    self.es_percent_label.place(x=260, y=114)
                    #self.update_es_img(listofeswear[9])
                    imgswp.swapImageWithoutResize(self.canvas, listofeswear[9], self.es, self.es_tk_image)
                else:
                    self.es_percent_label.config(fg="#ff0015")
                    self.es_percent_label.place(x=230, y=114)
                    #self.update_es_img(listofeswear[10])
                    imgswp.swapImageWithoutResize(self.canvas, listofeswear[10], self.es, self.es_tk_image)

            if 'engineICEWear' in data_dict_cardamage:
                ice = int(data_dict_cardamage['engineICEWear'])
                self.ice_percent_label.config(text=str(data_dict_cardamage['engineICEWear']) + "%")
                if ice < 10:
                    self.ice_percent_label.config(fg="#00ff00")
                    self.ice_percent_label.place(x=280, y=220)
                    #self.update_ice_img(listoficewear[0])
                    imgswp.swapImageWithoutResize(self.canvas, listoficewear[0], self.ice, self.ice_tk_image)
                elif ice < 20:
                    self.ice_percent_label.config(fg="#88f612")
                    self.ice_percent_label.place(x=260, y=220)
                    #self.update_ice_img(listoficewear[1])
                    imgswp.swapImageWithoutResize(self.canvas, listoficewear[1], self.ice, self.ice_tk_image)
                elif ice < 30:
                    self.ice_percent_label.config(fg="#aef317")
                    self.ice_percent_label.place(x=260, y=220)
                    #self.update_ice_img(listoficewear[2])
                    imgswp.swapImageWithoutResize(self.canvas, listoficewear[2], self.ice, self.ice_tk_image)
                elif ice < 40:
                    self.ice_percent_label.config(fg="#cff11b")
                    self.ice_percent_label.place(x=260, y=220)
                    #self.update_ice_img(listoficewear[3])
                    imgswp.swapImageWithoutResize(self.canvas, listoficewear[3], self.ice, self.ice_tk_image)
                elif ice < 50:
                    self.ice_percent_label.config(fg="#ebef1f")
                    self.ice_percent_label.place(x=260, y=220)
                    #self.update_ice_img(listoficewear[4])
                    imgswp.swapImageWithoutResize(self.canvas, listoficewear[4], self.ice, self.ice_tk_image)
                elif ice < 60:
                    self.ice_percent_label.config(fg="#fcee21")
                    self.ice_percent_label.place(x=260, y=220)
                    #self.update_ice_img(listoficewear[5])
                    imgswp.swapImageWithoutResize(self.canvas, listoficewear[5], self.ice, self.ice_tk_image)
                elif ice < 70:
                    self.ice_percent_label.config(fg="#fccc1f")
                    self.ice_percent_label.place(x=260, y=220)
                    #self.update_ice_img(listoficewear[6])
                    imgswp.swapImageWithoutResize(self.canvas, listoficewear[6], self.ice, self.ice_tk_image)
                elif ice < 80:
                    self.ice_percent_label.config(fg="#fda61d")
                    self.ice_percent_label.place(x=260, y=220)
                    #self.update_ice_img(listoficewear[7])
                    imgswp.swapImageWithoutResize(self.canvas, listoficewear[7], self.ice, self.ice_tk_image)
                elif ice < 90:
                    self.ice_percent_label.config(fg="#fd7e1b")
                    self.ice_percent_label.place(x=260, y=220)
                    #self.update_ice_img(listoficewear[8])
                    imgswp.swapImageWithoutResize(self.canvas, listoficewear[8], self.ice, self.ice_tk_image)
                elif ice < 100:
                    self.ice_percent_label.config(fg="#fe5519")
                    self.ice_percent_label.place(x=260, y=220)
                    #self.update_ice_img(listoficewear[9])
                    imgswp.swapImageWithoutResize(self.canvas, listoficewear[9], self.ice, self.ice_tk_image)
                else:
                    self.ice_percent_label.config(fg="#ff0015")
                    self.ice_percent_label.place(x=230, y=220)
                    #self.update_ice_img(listoficewear[10])
                    imgswp.swapImageWithoutResize(self.canvas, listoficewear[10], self.ice, self.ice_tk_image)

            if 'engineCEWear' in data_dict_cardamage:
                ce = int(data_dict_cardamage['engineCEWear'])
                self.ce_percent_label.config(text=str(data_dict_cardamage['engineCEWear']) + "%")
                if ce < 10:
                    self.ce_percent_label.config(fg="#00ff00")
                    self.ce_percent_label.place(x=280, y=169)
                    #self.update_ce_img(listofcewear[0])
                    imgswp.swapImageWithoutResize(self.canvas, listofcewear[0], self.ce, self.ce_tk_image)
                elif ce < 20:
                    self.ce_percent_label.config(fg="#88f612")
                    self.ce_percent_label.place(x=260, y=169)
                    #self.update_ce_img(listofcewear[1])
                    imgswp.swapImageWithoutResize(self.canvas, listofcewear[1], self.ce, self.ce_tk_image)
                elif ce < 30:
                    self.ce_percent_label.config(fg="#aef317")
                    self.ce_percent_label.place(x=260, y=169)
                    #self.update_ce_img(listofcewear[2])
                    imgswp.swapImageWithoutResize(self.canvas, listofcewear[2], self.ce, self.ce_tk_image)
                elif ce < 40:
                    self.ce_percent_label.config(fg="#cff11b")
                    self.ce_percent_label.place(x=260, y=169)
                    #self.update_ce_img(listofcewear[3])
                    imgswp.swapImageWithoutResize(self.canvas, listofcewear[3], self.ce, self.ce_tk_image)
                elif ce < 50:
                    self.ce_percent_label.config(fg="#ebef1f")
                    self.ce_percent_label.place(x=260, y=169)
                    #self.update_ce_img(listofcewear[4])
                    imgswp.swapImageWithoutResize(self.canvas, listofcewear[4], self.ce, self.ce_tk_image)
                elif ce < 60:
                    self.ce_percent_label.config(fg="#fcee21")
                    self.ce_percent_label.place(x=260, y=169)
                    #self.update_ce_img(listofcewear[5])
                    imgswp.swapImageWithoutResize(self.canvas, listofcewear[5], self.ce, self.ce_tk_image)
                elif ce < 70:
                    self.ce_percent_label.config(fg="#fccc1f")
                    self.ce_percent_label.place(x=260, y=169)
                    #self.update_ce_img(listofcewear[6])
                    imgswp.swapImageWithoutResize(self.canvas, listofcewear[6], self.ce, self.ce_tk_image)
                elif ce < 80:
                    self.ce_percent_label.config(fg="#fda61d")
                    self.ce_percent_label.place(x=260, y=169)
                    #self.update_ce_img(listofcewear[7])
                    imgswp.swapImageWithoutResize(self.canvas, listofcewear[7], self.ce, self.ce_tk_image)
                elif ce < 90:
                    self.ce_percent_label.config(fg="#fd7e1b")
                    self.ce_percent_label.place(x=260, y=169)
                    #self.update_ce_img(listofcewear[8])
                    imgswp.swapImageWithoutResize(self.canvas, listofcewear[8], self.ce, self.ce_tk_image)
                elif ce < 100:
                    self.ce_percent_label.config(fg="#fe5519")
                    self.ce_percent_label.place(x=260, y=169)
                    #self.update_ce_img(listofcewear[9])
                    imgswp.swapImageWithoutResize(self.canvas, listofcewear[9], self.ce, self.ce_tk_image)
                else:
                    self.ce_percent_label.config(fg="#ff0015")
                    self.ce_percent_label.place(x=230, y=169)
                    #self.update_ce_img(listofcewear[10])
                    imgswp.swapImageWithoutResize(self.canvas, listofcewear[10], self.ce, self.ce_tk_image)

            if 'engineTCWear' in data_dict_cardamage:
                tc = int(data_dict_cardamage['engineTCWear'])
                self.tc_percent_label.config(text=str(data_dict_cardamage['engineTCWear']) + "%")
                if tc < 10:
                    self.tc_percent_label.config(fg="#00ff00")
                    self.tc_percent_label.place(x=280, y=325)
                    #self.update_tc_img(listoftcwear[0])
                    imgswp.swapImageWithoutResize(self.canvas, listoftcwear[0], self.tc, self.tc_tk_image)
                elif tc < 20:
                    self.tc_percent_label.config(fg="#88f612")
                    self.tc_percent_label.place(x=260, y=325)
                    #self.update_tc_img(listoftcwear[1])
                    imgswp.swapImageWithoutResize(self.canvas, listoftcwear[1], self.tc, self.tc_tk_image)
                elif tc < 30:
                    self.tc_percent_label.config(fg="#aef317")
                    self.tc_percent_label.place(x=260, y=325)
                    #self.update_tc_img(listoftcwear[2])
                    imgswp.swapImageWithoutResize(self.canvas, listoftcwear[2], self.tc, self.tc_tk_image)
                elif tc < 40:
                    self.tc_percent_label.config(fg="#cff11b")
                    self.tc_percent_label.place(x=260, y=325)
                    #self.update_tc_img(listoftcwear[3])
                    imgswp.swapImageWithoutResize(self.canvas, listoftcwear[3], self.tc, self.tc_tk_image)
                elif tc < 50:
                    self.tc_percent_label.config(fg="#ebef1f")
                    self.tc_percent_label.place(x=260, y=325)
                    #self.update_tc_img(listoftcwear[4])
                    imgswp.swapImageWithoutResize(self.canvas, listoftcwear[4], self.tc, self.tc_tk_image)
                elif tc < 60:
                    self.tc_percent_label.config(fg="#fcee21")
                    self.tc_percent_label.place(x=260, y=325)
                    #self.update_tc_img(listoftcwear[5])
                    imgswp.swapImageWithoutResize(self.canvas, listoftcwear[5], self.tc, self.tc_tk_image)
                elif tc < 70:
                    self.tc_percent_label.config(fg="#fccc1f")
                    self.tc_percent_label.place(x=260, y=325)
                    #self.update_tc_img(listoftcwear[6])
                    imgswp.swapImageWithoutResize(self.canvas, listoftcwear[6], self.tc, self.tc_tk_image)
                elif tc < 80:
                    self.tc_percent_label.config(fg="#fda61d")
                    self.tc_percent_label.place(x=260, y=325)
                    #self.update_tc_img(listoftcwear[7])
                    imgswp.swapImageWithoutResize(self.canvas, listoftcwear[7], self.tc, self.tc_tk_image)
                elif tc < 90:
                    self.tc_percent_label.config(fg="#fd7e1b")
                    self.tc_percent_label.place(x=260, y=325)
                    #self.update_tc_img(listoftcwear[8])
                    imgswp.swapImageWithoutResize(self.canvas, listoftcwear[8], self.tc, self.tc_tk_image)
                elif tc < 100:
                    self.tc_percent_label.config(fg="#fe5519")
                    self.tc_percent_label.place(x=260, y=325)
                    #self.update_tc_img(listoftcwear[9])
                    imgswp.swapImageWithoutResize(self.canvas, listoftcwear[9], self.tc, self.tc_tk_image)
                else:
                    self.tc_percent_label.config(fg="#ff0015")
                    self.tc_percent_label.place(x=230, y=325)
                    #self.update_tc_img(listoftcwear[10])
                    imgswp.swapImageWithoutResize(self.canvas, listoftcwear[10], self.tc, self.tc_tk_image)

            if 'gearBoxDamage' in data_dict_cardamage:
                gb = int(data_dict_cardamage['gearBoxDamage'])
                self.gearbox_percent_label.config(text=str(data_dict_cardamage['gearBoxDamage']) + "%")
                if gb < 10:
                    self.gearbox_percent_label.config(fg="#00ff00")
                    self.gearbox_percent_label.place(x=280, y=378)
                    #self.update_gearbox_img(listofgearboxwear[0])
                    imgswp.swapImageWithoutResize(self.canvas, listofgearboxwear[0], self.gearbox, self.gearbox_tk_image)
                elif gb < 20:
                    self.gearbox_percent_label.config(fg="#88f612")
                    self.gearbox_percent_label.place(x=260, y=378)
                    #self.update_gearbox_img(listofgearboxwear[1])
                    imgswp.swapImageWithoutResize(self.canvas, listofgearboxwear[1], self.gearbox, self.gearbox_tk_image)
                elif gb < 30:
                    self.gearbox_percent_label.config(fg="#aef317")
                    self.gearbox_percent_label.place(x=260, y=378)
                    #self.update_gearbox_img(listofgearboxwear[2])
                    imgswp.swapImageWithoutResize(self.canvas, listofgearboxwear[2], self.gearbox, self.gearbox_tk_image)
                elif gb < 40:
                    self.gearbox_percent_label.config(fg="#cff11b")
                    self.gearbox_percent_label.place(x=260, y=378)
                    #self.update_gearbox_img(listofgearboxwear[3])
                    imgswp.swapImageWithoutResize(self.canvas, listofgearboxwear[3], self.gearbox, self.gearbox_tk_image)
                elif gb < 50:
                    self.gearbox_percent_label.config(fg="#ebef1f")
                    self.gearbox_percent_label.place(x=260, y=378)
                    #self.update_gearbox_img(listofgearboxwear[4])
                    imgswp.swapImageWithoutResize(self.canvas, listofgearboxwear[4], self.gearbox, self.gearbox_tk_image)
                elif gb < 60:
                    self.gearbox_percent_label.config(fg="#fcee21")
                    self.gearbox_percent_label.place(x=260, y=378)
                    #self.update_gearbox_img(listofgearboxwear[5])
                    imgswp.swapImageWithoutResize(self.canvas, listofgearboxwear[5], self.gearbox, self.gearbox_tk_image)
                elif gb < 70:
                    self.gearbox_percent_label.config(fg="#fccc1f")
                    self.gearbox_percent_label.place(x=260, y=378)
                    #self.update_gearbox_img(listofgearboxwear[6])
                    imgswp.swapImageWithoutResize(self.canvas, listofgearboxwear[6], self.gearbox, self.gearbox_tk_image)
                elif gb < 80:
                    self.gearbox_percent_label.config(fg="#fda61d")
                    self.gearbox_percent_label.place(x=260, y=378)
                    #self.update_gearbox_img(listofgearboxwear[7])
                    imgswp.swapImageWithoutResize(self.canvas, listofgearboxwear[7], self.gearbox, self.gearbox_tk_image)
                elif gb < 90:
                    self.gearbox_percent_label.config(fg="#fd7e1b")
                    self.gearbox_percent_label.place(x=260, y=378)
                    #self.update_gearbox_img(listofgearboxwear[8])
                    imgswp.swapImageWithoutResize(self.canvas, listofgearboxwear[8], self.gearbox, self.gearbox_tk_image)
                elif gb < 100:
                    self.gearbox_percent_label.config(fg="#fe5519")
                    self.gearbox_percent_label.place(x=260, y=378)
                    #self.update_gearbox_img(listofgearboxwear[9])
                    imgswp.swapImageWithoutResize(self.canvas, listofgearboxwear[9], self.gearbox, self.gearbox_tk_image)
                else:
                    self.gearbox_percent_label.config(fg="#ff0015")
                    self.gearbox_percent_label.place(x=230, y=378)
                    #self.update_gearbox_img(listofgearboxwear[10])
                    imgswp.swapImageWithoutResize(self.canvas, listofgearboxwear[10], self.gearbox, self.gearbox_tk_image)

            self.root.after(5, self.update_engine_display)
class CarTemperature:
    def __init__(self, root):
        self.root = root

    def create_cartemp_display(self):
        self.canvas = tk.Canvas(self.root, height=480, width=800, bg="black",highlightthickness=0)
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

    def update_temp_labels(self):
        if self.canvas is not None and self.canvas.winfo_exists():
            global data_dict_cartelemetry
            imgswp = ImageSwapper()
            if 'FLTyreInnerTemperature' in data_dict_cartelemetry:
                self.fl_inner_temp_label.config(text=f"{data_dict_cartelemetry['FLTyreInnerTemperature']}°C")
                if int(data_dict_cartelemetry['FLTyreInnerTemperature']) <= 70:
                    #self.update_fl_tyre(listoffronttyres[0])
                    imgswp.swapImages(self.canvas, listoffronttyres[0],29,53,self.frontleft, self.fl_tk_image)
                    self.fl_inner_temp_label.config(fg="#00ffff")
                elif int(data_dict_cartelemetry['FLTyreInnerTemperature']) <= 90:
                    #self.update_fl_tyre(listoffronttyres[1])
                    imgswp.swapImages(self.canvas, listoffronttyres[1], 29, 53, self.frontleft, self.fl_tk_image)
                    self.fl_inner_temp_label.config(fg="#00ffaa")
                elif int(data_dict_cartelemetry['FLTyreInnerTemperature']) <= 105:
                    #self.update_fl_tyre(listoffronttyres[2])
                    imgswp.swapImages(self.canvas, listoffronttyres[2], 29, 53, self.frontleft, self.fl_tk_image)
                    self.fl_inner_temp_label.config(fg="#00ff00")
                elif int(data_dict_cartelemetry['FLTyreInnerTemperature']) <= 110:
                    #self.update_fl_tyre(listoffronttyres[3])
                    imgswp.swapImages(self.canvas, listoffronttyres[3], 29, 53, self.frontleft, self.fl_tk_image)
                    self.fl_inner_temp_label.config(fg="#fccc1f")
                elif int(data_dict_cartelemetry['FLTyreInnerTemperature']) > 110:
                    #self.update_fl_tyre(listoffronttyres[4])
                    imgswp.swapImages(self.canvas, listoffronttyres[4], 29, 53, self.frontleft, self.fl_tk_image)
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
                    #self.update_fl_brake(listofbrakes[0])
                    imgswp.swapImages(self.canvas, listofbrakes[0], 10, 19, self.frontleftbrake, self.fl_brake_tk_image)
                    self.fl_brake_temp_label.config(fg="#00ffff")
                elif int(data_dict_cartelemetry['FLBrakeTemperature']) <= 450:
                    #self.update_fl_brake(listofbrakes[1])
                    imgswp.swapImages(self.canvas, listofbrakes[1], 10, 19, self.frontleftbrake, self.fl_brake_tk_image)
                    self.fl_brake_temp_label.config(fg="#00ffaa")
                elif int(data_dict_cartelemetry['FLBrakeTemperature']) <= 750:
                    #self.update_fl_brake(listofbrakes[2])
                    imgswp.swapImages(self.canvas, listofbrakes[2], 10, 19, self.frontleftbrake, self.fl_brake_tk_image)
                    self.fl_brake_temp_label.config(fg="#00ff00")
                elif int(data_dict_cartelemetry['FLBrakeTemperature']) <= 950:
                    #self.update_fl_brake(listofbrakes[3])
                    imgswp.swapImages(self.canvas, listofbrakes[3], 10, 19, self.frontleftbrake, self.fl_brake_tk_image)
                    self.fl_brake_temp_label.config(fg="#fccc1f")
                elif int(data_dict_cartelemetry['FLBrakeTemperature']) > 950:
                    #self.update_fl_brake(listofbrakes[4])
                    imgswp.swapImages(self.canvas, listofbrakes[4], 10, 19, self.frontleftbrake, self.fl_brake_tk_image)
                    self.fl_brake_temp_label.config(fg="#fe2b17")

            if 'RLTyreInnerTemperature' in data_dict_cartelemetry:
                self.rl_inner_temp_label.config(text=f"{data_dict_cartelemetry['RLTyreInnerTemperature']}°C")
                if int(data_dict_cartelemetry['RLTyreInnerTemperature']) <= 70:
                    #self.update_rl_tyre(listofreartyres[0])
                    imgswp.swapImages(self.canvas, listofreartyres[0], 32, 53, self.rearleft, self.rl_tk_image)
                    self.rl_inner_temp_label.config(fg="#00ffff")
                elif int(data_dict_cartelemetry['RLTyreInnerTemperature']) <= 90:
                    #self.update_rl_tyre(listofreartyres[1])
                    imgswp.swapImages(self.canvas, listofreartyres[1], 32, 53, self.rearleft, self.rl_tk_image)
                    self.rl_inner_temp_label.config(fg="#00ffaa")
                elif int(data_dict_cartelemetry['RLTyreInnerTemperature']) <= 105:
                    #self.update_rl_tyre(listofreartyres[2])
                    imgswp.swapImages(self.canvas, listofreartyres[2], 32, 53, self.rearleft, self.rl_tk_image)
                    self.rl_inner_temp_label.config(fg="#00ff00")
                elif int(data_dict_cartelemetry['RLTyreInnerTemperature']) <= 110:
                    #self.update_rl_tyre(listofreartyres[3])
                    imgswp.swapImages(self.canvas, listofreartyres[3], 32, 53, self.rearleft, self.rl_tk_image)
                    self.rl_inner_temp_label.config(fg="#fccc1f")
                elif int(data_dict_cartelemetry['RLTyreInnerTemperature']) > 110:
                    #self.update_rl_tyre(listofreartyres[4])
                    imgswp.swapImages(self.canvas, listofreartyres[4], 32, 53, self.rearleft, self.rl_tk_image)
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
                    #self.update_rl_brake(listofbrakes[0])
                    imgswp.swapImages(self.canvas, listofbrakes[0], 10, 19, self.rearleftbrake, self.rl_brake_tk_image)
                    self.rl_brake_temp_label.config(fg="#00ffff")
                elif int(data_dict_cartelemetry['RLBrakeTemperature']) <= 450:
                    #self.update_rl_brake(listofbrakes[1])
                    imgswp.swapImages(self.canvas, listofbrakes[1], 10, 19, self.rearleftbrake, self.rl_brake_tk_image)
                    self.rl_brake_temp_label.config(fg="#00ffaa")
                elif int(data_dict_cartelemetry['RLBrakeTemperature']) <= 750:
                    #self.update_rl_brake(listofbrakes[2])
                    imgswp.swapImages(self.canvas, listofbrakes[2], 10, 19, self.rearleftbrake, self.rl_brake_tk_image)
                    self.rl_brake_temp_label.config(fg="#00ff00")
                elif int(data_dict_cartelemetry['RLBrakeTemperature']) <= 950:
                    #self.update_rl_brake(listofbrakes[3])
                    imgswp.swapImages(self.canvas, listofbrakes[3], 10, 19, self.rearleftbrake, self.rl_brake_tk_image)
                    self.rl_brake_temp_label.config(fg="#fccc1f")
                elif int(data_dict_cartelemetry['RLBrakeTemperature']) > 950:
                    #self.update_rl_brake(listofbrakes[4])
                    imgswp.swapImages(self.canvas, listofbrakes[4], 10, 19, self.rearleftbrake, self.rl_brake_tk_image)
                    self.rl_brake_temp_label.config(fg="#fe2b17")

            if 'FRTyreInnerTemperature' in data_dict_cartelemetry:
                self.fr_inner_temp_label.config(text=f"{data_dict_cartelemetry['FRTyreInnerTemperature']}°C")
                if int(data_dict_cartelemetry['FRTyreInnerTemperature']) <= 70:
                    #self.update_fr_tyre(listoffronttyres[0])
                    imgswp.swapImages(self.canvas, listoffronttyres[0], 29, 53, self.frontright, self.fr_tk_image)
                    self.fr_inner_temp_label.config(fg="#00ffff")
                elif int(data_dict_cartelemetry['FRTyreInnerTemperature']) <= 90:
                    #self.update_fr_tyre(listoffronttyres[1])
                    imgswp.swapImages(self.canvas, listoffronttyres[1], 29, 53, self.frontright, self.fr_tk_image)
                    self.fr_inner_temp_label.config(fg="#00ffaa")
                elif int(data_dict_cartelemetry['FRTyreInnerTemperature']) <= 105:
                    #self.update_fr_tyre(listoffronttyres[2])
                    imgswp.swapImages(self.canvas, listoffronttyres[2], 29, 53, self.frontright, self.fr_tk_image)
                    self.fr_inner_temp_label.config(fg="#00ff00")
                elif int(data_dict_cartelemetry['FRTyreInnerTemperature']) <= 110:
                    #self.update_fr_tyre(listoffronttyres[3])
                    imgswp.swapImages(self.canvas, listoffronttyres[3], 29, 53, self.frontright, self.fr_tk_image)
                    self.fr_inner_temp_label.config(fg="#fccc1f")
                elif int(data_dict_cartelemetry['FRTyreInnerTemperature']) > 110:
                    #self.update_fr_tyre(listoffronttyres[4])
                    imgswp.swapImages(self.canvas, listoffronttyres[4], 29, 53, self.frontright, self.fr_tk_image)
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
                    #self.update_fr_brake(listofbrakes[0])
                    imgswp.swapImages(self.canvas, listofbrakes[0], 10, 19, self.frontrightbrake, self.fr_brake_tk_image)
                    self.fr_brake_temp_label.config(fg="#00ffff")
                elif int(data_dict_cartelemetry['FRBrakeTemperature']) <= 450:
                    #self.update_fr_brake(listofbrakes[1])
                    imgswp.swapImages(self.canvas, listofbrakes[1], 10, 19, self.frontrightbrake, self.fr_brake_tk_image)
                    self.fr_brake_temp_label.config(fg="#00ffaa")
                elif int(data_dict_cartelemetry['FRBrakeTemperature']) <= 750:
                    #self.update_fr_brake(listofbrakes[2])
                    imgswp.swapImages(self.canvas, listofbrakes[2], 10, 19, self.frontrightbrake, self.fr_brake_tk_image)
                    self.fr_brake_temp_label.config(fg="#00ff00")
                elif int(data_dict_cartelemetry['FRBrakeTemperature']) <= 950:
                    #self.update_fr_brake(listofbrakes[3])
                    imgswp.swapImages(self.canvas, listofbrakes[3], 10, 19, self.frontrightbrake, self.fr_brake_tk_image)
                    self.fr_brake_temp_label.config(fg="#fccc1f")
                elif int(data_dict_cartelemetry['FRBrakeTemperature']) > 950:
                    #self.update_fr_brake(listofbrakes[4])
                    imgswp.swapImages(self.canvas, listofbrakes[4], 10, 19, self.frontrightbrake, self.fr_brake_tk_image)
                    self.fr_brake_temp_label.config(fg="#fe2b17")

            if 'RRTyreInnerTemperature' in data_dict_cartelemetry:
                self.rr_inner_temp_label.config(text=f"{data_dict_cartelemetry['RRTyreInnerTemperature']}°C")
                if int(data_dict_cartelemetry['RRTyreInnerTemperature']) <= 70:
                    #self.update_rr_tyre(listofreartyres[0])
                    imgswp.swapImages(self.canvas, listofreartyres[0], 32, 53, self.rearright, self.rr_tk_image)
                    self.rr_inner_temp_label.config(fg="#00ffff")
                elif int(data_dict_cartelemetry['RRTyreInnerTemperature']) <= 90:
                    #self.update_rr_tyre(listofreartyres[1])
                    imgswp.swapImages(self.canvas, listofreartyres[1], 32, 53, self.rearright, self.rr_tk_image)
                    self.rr_inner_temp_label.config(fg="#00ffaa")
                elif int(data_dict_cartelemetry['RRTyreInnerTemperature']) <= 105:
                    #self.update_rr_tyre(listofreartyres[2])
                    imgswp.swapImages(self.canvas, listofreartyres[2], 32, 53, self.rearright, self.rr_tk_image)
                    self.rr_inner_temp_label.config(fg="#00ff00")
                elif int(data_dict_cartelemetry['RRTyreInnerTemperature']) <= 110:
                    #self.update_rr_tyre(listofreartyres[3])
                    imgswp.swapImages(self.canvas, listofreartyres[3], 32, 53, self.rearright, self.rr_tk_image)
                    self.rr_inner_temp_label.config(fg="#fccc1f")
                elif int(data_dict_cartelemetry['RRTyreInnerTemperature']) > 110:
                    #self.update_rr_tyre(listofreartyres[4])
                    imgswp.swapImages(self.canvas, listofreartyres[4], 32, 53, self.rearright, self.rr_tk_image)
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
                    #self.update_rr_brake(listofbrakes[0])
                    imgswp.swapImages(self.canvas, listofbrakes[0], 10, 19, self.rearrightbrake, self.rr_brake_tk_image)
                    self.rr_brake_temp_label.config(fg="#00ffff")
                elif int(data_dict_cartelemetry['RRBrakeTemperature']) <= 450:
                    #self.update_rr_brake(listofbrakes[1])
                    imgswp.swapImages(self.canvas, listofbrakes[1], 10, 19, self.rearrightbrake, self.rr_brake_tk_image)
                    self.rr_brake_temp_label.config(fg="#00ffaa")
                elif int(data_dict_cartelemetry['RRBrakeTemperature']) <= 750:
                    #self.update_rr_brake(listofbrakes[2])
                    imgswp.swapImages(self.canvas, listofbrakes[2], 10, 19, self.rearrightbrake, self.rr_brake_tk_image)
                    self.rr_brake_temp_label.config(fg="#00ff00")
                elif int(data_dict_cartelemetry['RRBrakeTemperature']) <= 950:
                    #self.update_rr_brake(listofbrakes[3])
                    imgswp.swapImages(self.canvas, listofbrakes[3], 10, 19, self.rearrightbrake, self.rr_brake_tk_image)
                    self.rr_brake_temp_label.config(fg="#fccc1f")
                elif int(data_dict_cartelemetry['RRBrakeTemperature']) > 950:
                    #self.update_rr_brake(listofbrakes[4])
                    imgswp.swapImages(self.canvas, listofbrakes[4], 10, 19, self.rearrightbrake, self.rr_brake_tk_image)
                    self.rr_brake_temp_label.config(fg="#fe2b17")

            if 'engineTemperature' in data_dict_cartelemetry:
                self.motor_temp_label.config(text=f"{data_dict_cartelemetry['engineTemperature']}°C")
                if int(data_dict_cartelemetry['engineTemperature']) <= 80:
                    #self.update_engine(listofengine[0])
                    imgswp.swapImages(self.canvas, listofengine[0], 51, 60, self.engine, self.tk_image)
                    self.motor_temp_label.config(fg="#00ffff")
                elif int(data_dict_cartelemetry['engineTemperature']) <= 100:
                    #self.update_engine(listofengine[1])
                    imgswp.swapImages(self.canvas, listofengine[1], 51, 60, self.engine, self.tk_image)
                    self.motor_temp_label.config(fg="#00ffaa")
                elif int(data_dict_cartelemetry['engineTemperature']) <= 130:
                    #self.update_engine(listofengine[2])
                    imgswp.swapImages(self.canvas, listofengine[2], 51, 60, self.engine, self.tk_image)
                    self.motor_temp_label.config(fg="#00ff00")
                elif int(data_dict_cartelemetry['engineTemperature']) <= 140:
                    #self.update_engine(listofengine[3])
                    imgswp.swapImages(self.canvas, listofengine[3], 51, 60, self.engine, self.tk_image)
                    self.motor_temp_label.config(fg="#fccc1f")
                elif int(data_dict_cartelemetry['engineTemperature']) > 140:
                    #self.update_engine(listofengine[4])
                    imgswp.swapImages(self.canvas, listofengine[4], 51, 60, self.engine, self.tk_image)
                    self.motor_temp_label.config(fg="#fe2b17")

            self.root.after(5, self.update_temp_labels)

    def destroy(self):
        # Destroy the canvas
        self.canvas.destroy()

