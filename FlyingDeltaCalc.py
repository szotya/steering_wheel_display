from SharedVars import *
import threading

class ThreadControllerByEvent(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.pause_event = threading.Event()
        self.resume_event = threading.Event()
        self.resume_event.set()  # Initially, the thread is not paused.

    def run(self):
        global data_dict_delta

        while True:
            if bool(data_dict_delta):
                FlyingDeltaCalc().resume()
            else:
                FlyingDeltaCalc().pause()




class FlyingDeltaCalc(threading.Thread):
    def __init__(self):
        super().__init__()
        threading.Thread.__init__(self)
        self.pause_event = threading.Event()
        self.resume_event = threading.Event()
        self.resume_event.set()  # Initially, the thread is not paused.

    def run(self):
        print("Delta thread is running")
        flying_delta_calculation()

    def pause(self):
        print("Thread is paused")
        self.pause_event.set()
        self.resume_event.clear()

    def resume(self):
        print("Thread is resumed")
        self.resume_event.set()
        self.pause_event.clear()

def flying_delta_calculation():
    global data_dict_delta
    global delta
    global bestlap
    global packetType
    data_dict_bestlap_meters = {}
    data_bestlap_sectors = {}
    data_dict_currentlap_sectors = {}
    data_dict_currentlap_meters = {}

    while True:
        try:
            if (data_dict_bestlap_meters or data_bestlap_sectors) and data_dict_delta['currentLapTimeInMs'] > 0:
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

                    if 'sector1TimeInMs' in data_dict_delta and data_dict_delta['sector1TimeInMs'] > 0:
                        data_bestlap_sectors.update({
                            'sector1TimeInMs': data_dict_delta['sector1TimeInMs'],
                        })
                    if 'sector2TimeInMs' in data_dict_delta and data_dict_delta['sector2TimeInMs'] > 0:
                        data_bestlap_sectors.update({
                            'sector2TimeInMs': data_dict_delta['sector2TimeInMs'],
                        })

        except Exception as e:
            pass
            #print(f"Error in flying_delta_calculation: {e}")