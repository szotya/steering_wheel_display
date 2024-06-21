import rawutil
from EventPacket import *
from SessionPacket import MarshalZone, WeatherForecastSample, SessionPacket
from LapDataPacket import LapData, LapDataPacket
from CarTelemetryDataPacket import CarTelemetryData, CarTelemetryDataPacket
from CarStatusPacket import CarStatusData, CarStatusPacket
from CarDamagePacket import CarDamageData, CarDamagePacket
from SessionHistoryPacket import LapHistoryData, SessionHistoryPacket
from TyreSetsPacket import TyreSetData, TyreSetsPacket
from Header import Header


def unpack_header(header: bytes):
    h=Header()
    # <H means 2byte <B means 1byte <Q means 8byte <f means 4byte
    h.field1 = rawutil.unpack('<H', header[:2])[0]
    h.field2 = rawutil.unpack('<B', header[2:3])[0]
    h.field3 = rawutil.unpack('<B', header[3:4])[0]
    h.field4 = rawutil.unpack('<B', header[4:5])[0]
    h.field5 = rawutil.unpack('<B', header[5:6])[0]
    h.field6 = rawutil.unpack('<B', header[6:7])[0]
    h.field7 = rawutil.unpack('<Q', header[7:15])[0]
    h.field8 = rawutil.unpack('<f', header[15:19])[0]
    h.field9 = rawutil.unpack('<I', header[19:23])[0]
    h.field10 = rawutil.unpack('<I', header[23:27])[0]
    h.field11 = rawutil.unpack('<B', header[27:28])[0]
    h.field12 = rawutil.unpack('<B', header[28:29])[0]
    return h

def unpack_marshalzone(telemetry: bytes):
    mz = MarshalZone()
    mz.field1 = rawutil.unpack('<f', telemetry[:4])[0]
    mz.field2 = rawutil.unpack('<b', telemetry[4:5])[0]
    return mz

def unpack_weatherforecastsample(telemetry: bytes):
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

def unpack_sessionpacket(telemetry: bytes):
    sp = SessionPacket()
    sp.field1 = rawutil.unpack('<B', telemetry[:1])[0]
    sp.field2 = rawutil.unpack('<B', telemetry[1:2])[0]
    sp.field3 = rawutil.unpack('<B', telemetry[2:3])[0]
    sp.field4 = rawutil.unpack('<B', telemetry[3:4])[0]
    sp.field5 = rawutil.unpack('<H', telemetry[4:6])[0]
    sp.field6 = rawutil.unpack('<B', telemetry[6:7])[0]
    sp.field7 = rawutil.unpack('<b', telemetry[7:8])[0]
    sp.field8 = rawutil.unpack('<B', telemetry[8:9])[0]
    sp.field9 = rawutil.unpack('<H', telemetry[9:11])[0]
    sp.field10 = rawutil.unpack('<H', telemetry[11:13])[0]
    sp.field11 = rawutil.unpack('<B', telemetry[13:14])[0]
    sp.field12 = rawutil.unpack('<B', telemetry[14:15])[0]
    sp.field13 = rawutil.unpack('<B', telemetry[15:16])[0]
    sp.field14 = rawutil.unpack('<B', telemetry[16:17])[0]
    sp.field15 = rawutil.unpack('<B', telemetry[17:18])[0]
    sp.field16 = rawutil.unpack('<B', telemetry[18:19])[0]
    offset = 19
    for i in range(sp.field16):
        sp.field17.append(unpack_marshalzone(telemetry[offset:offset+5]))
        offset += 5
    sp.field18 = rawutil.unpack('<B', telemetry[124:125])[0]
    sp.field19 = rawutil.unpack('<B', telemetry[125:126])[0]
    sp.field20 = rawutil.unpack('<B', telemetry[126:127])[0]
    offset = 127
    for i in range(sp.field20):
        sp.field21.append(unpack_weatherforecastsample(telemetry[offset:offset+8]))
        offset += 8
    sp.field22 = rawutil.unpack('<B', telemetry[575:576])[0] #1
    sp.field23 = rawutil.unpack('<B', telemetry[576:577])[0] #1
    sp.field24 = rawutil.unpack('<I', telemetry[577:581])[0] #4
    sp.field25 = rawutil.unpack('<I', telemetry[581:585])[0] #4
    sp.field26 = rawutil.unpack('<I', telemetry[585:589])[0] #4
    sp.field27 = rawutil.unpack('<B', telemetry[589:590])[0] #1
    sp.field28 = rawutil.unpack('<B', telemetry[590:591])[0] #1
    sp.field29 = rawutil.unpack('<B', telemetry[591:592])[0] #1
    sp.field30 = rawutil.unpack('<B', telemetry[592:593])[0] #1
    sp.field31 = rawutil.unpack('<B', telemetry[593:594])[0] #1
    sp.field32 = rawutil.unpack('<B', telemetry[594:595])[0] #1
    sp.field33 = rawutil.unpack('<B', telemetry[595:596])[0] #1
    sp.field34 = rawutil.unpack('<B', telemetry[596:597])[0] #1
    sp.field35 = rawutil.unpack('<B', telemetry[597:598])[0] #1
    sp.field36 = rawutil.unpack('<B', telemetry[598:599])[0] #1
    sp.field37 = rawutil.unpack('<B', telemetry[599:600])[0] #1
    sp.field38 = rawutil.unpack('<B', telemetry[600:601])[0] #1
    sp.field39 = rawutil.unpack('<B', telemetry[601:602])[0] #1
    sp.field40 = rawutil.unpack('<B', telemetry[602:603])[0] #1
    sp.field41 = rawutil.unpack('<I', telemetry[603:607])[0] #4
    sp.field42 = rawutil.unpack('<B', telemetry[607:608])[0] #1
    sp.field43 = rawutil.unpack('<B', telemetry[608:609])[0] #1
    sp.field44 = rawutil.unpack('<B', telemetry[609:610])[0] #1
    sp.field45 = rawutil.unpack('<B', telemetry[610:611])[0] #1
    sp.field46 = rawutil.unpack('<B', telemetry[611:612])[0] #1
    sp.field47 = rawutil.unpack('<B', telemetry[612:613])[0] #1
    sp.field48 = rawutil.unpack('<B', telemetry[613:614])[0] #1
    sp.field49 = rawutil.unpack('<B', telemetry[614:615])[0] #1

    return sp

def unpack_lapdata(telemetry: bytes):
    # <H means 2byte <B means 1byte <Q means 8byte <f means 4byte

    ld = LapData()
    ld.field1 = rawutil.unpack('<I', telemetry[:4])[0]
    ld.field2 = rawutil.unpack('<I', telemetry[4:8])[0]
    ld.field3 = rawutil.unpack('<H', telemetry[8:10])[0]
    ld.field4 = rawutil.unpack('<B', telemetry[10:11])[0]
    ld.field5 = rawutil.unpack('<H', telemetry[11:13])[0]
    ld.field6 = rawutil.unpack('<B', telemetry[13:14])[0]
    ld.field7 = rawutil.unpack('<H', telemetry[14:16])[0]
    ld.field8 = rawutil.unpack('<H', telemetry[16:18])[0]
    ld.field9 = rawutil.unpack('<f', telemetry[18:22])[0]
    ld.field10 = rawutil.unpack('<f', telemetry[22:26])[0]
    ld.field11 = rawutil.unpack('<f', telemetry[26:30])[0]
    ld.field12 = rawutil.unpack('<B', telemetry[30:31])[0]
    ld.field13 = rawutil.unpack('<B', telemetry[31:32])[0]
    ld.field14 = rawutil.unpack('<B', telemetry[32:33])[0]
    ld.field15 = rawutil.unpack('<B', telemetry[33:34])[0]
    ld.field16 = rawutil.unpack('<B', telemetry[34:35])[0]
    ld.field17 = rawutil.unpack('<B', telemetry[35:36])[0]
    ld.field18 = rawutil.unpack('<B', telemetry[36:37])[0]
    ld.field19 = rawutil.unpack('<B', telemetry[37:38])[0]
    ld.field20 = rawutil.unpack('<B', telemetry[38:39])[0]
    ld.field21 = rawutil.unpack('<B', telemetry[39:40])[0]
    ld.field22 = rawutil.unpack('<B', telemetry[40:41])[0]
    ld.field23 = rawutil.unpack('<B', telemetry[41:42])[0]
    ld.field24 = rawutil.unpack('<B', telemetry[42:43])[0]
    ld.field25 = rawutil.unpack('<B', telemetry[43:44])[0]
    ld.field26 = rawutil.unpack('<B', telemetry[44:45])[0]
    ld.field27 = rawutil.unpack('<H', telemetry[45:47])[0]
    ld.field28 = rawutil.unpack('<H', telemetry[47:49])[0]
    ld.field29 = rawutil.unpack('<B', telemetry[49:50])[0]
    return ld

def unpack_lapdatapacket(telemetry: bytes, carIndex):
    ldp = LapDataPacket()
    offset = carIndex * 50
    ldp.field1.append(unpack_lapdata(telemetry[offset:offset+50]))
    ldp.field2 = rawutil.unpack('<B', telemetry[1100:1101])[0]
    ldp.field3 = rawutil.unpack('<B', telemetry[1101:1102])[0]
    return ldp

def unpack_fastestlap(telemetry: bytes):
    fl = FastestLap()
    fl.field1 = rawutil.unpack('<B', telemetry[:1])[0]
    fl.field2 = rawutil.unpack('<I', telemetry[1:5])[0]
    return fl

def unpack_retirement(telemetry: bytes):
    r = Retirement()
    r.field1 = rawutil.unpack('<B', telemetry[0:1])
    return r

def unpack_drsstatus(status: int):
    drs = DRSStatus()
    drs.field1 = status
    return drs

def unpack_team_mate_in_pits(telemetry: bytes):
    tmp = TeamMateInPits()
    tmp.field1 = rawutil.unpack('<B', telemetry[0:1])
    return tmp

def unpack_race_winner(telemetry: bytes):
    rw = RaceWinner()
    rw.field1 = rawutil.unpack('<B', telemetry[0:1])
    return rw

def unpack_penalty(telemetry: bytes):
    p = Penalty()
    p.field1 = rawutil.unpack('<B', telemetry[0:1])
    p.field2 = rawutil.unpack('<B', telemetry[1:2])
    p.field3 = rawutil.unpack('<B', telemetry[2:3])
    p.field4 = rawutil.unpack('<B', telemetry[3:4])
    p.field5 = rawutil.unpack('<B', telemetry[4:5])
    p.field6 = rawutil.unpack('<B', telemetry[5:6])
    p.field7 = rawutil.unpack('<B', telemetry[6:7])
    return p

def unpack_speedtrap(telemetry: bytes):
    st = SpeedTrap()
    st.field1 = rawutil.unpack('<B', telemetry[0:1])
    st.field2 = rawutil.unpack('<f', telemetry[1:5])
    st.field3 = rawutil.unpack('<B', telemetry[5:6])
    st.field4 = rawutil.unpack('<B', telemetry[6:7])
    st.field5 = rawutil.unpack('<B', telemetry[7:8])
    st.field6 = rawutil.unpack('<f', telemetry[8:12])
    return st

def unpack_startlights(telemetry: bytes):
    sl = StartLights()
    sl.field1 = rawutil.unpack('<B', telemetry[0:1])
    return sl

def lightsout():
    lo = LightsOut()
    lo.field1 = 1
    return lo

def unpack_drivethroughpenaltyserved(telemetry: bytes):
    dtps = DriveThroughPenaltyServed()
    dtps.field1 = rawutil.unpack('<B', telemetry[0:1])
    return dtps

def unpack_stopgopenaltyserved(telemetry: bytes):
    sgps = StopGoPenaltyServed()
    sgps.field1 = rawutil.unpack('<B', telemetry[0:1])
    return sgps

def unpack_flashback(telemetry: bytes):
    fb = Flashback()
    fb.field1 = rawutil.unpack('<I', telemetry[0:4])
    fb.field2 = rawutil.unpack('<f', telemetry[4:8])
    return fb

def unpack_button(telemetry: bytes):
    b = Buttons()
    b.field1 = rawutil.unpack('<f', telemetry[0:4])
    return b

def unpack_redflag(telemetry: bytes):
    rf = RedFlag()
    rf.field1 = 1
    return rf

def unpack_overtake(telemetry: bytes):
    o = Overtake()
    o.field1 = rawutil.unpack('<B', telemetry[0:1])
    o.field2 = rawutil.unpack('<B', telemetry[1:2])
    return o

def unpack_eventpacket(telemetry: bytes):
    ep = EventPacket()
    char1 = rawutil.unpack('<c', telemetry[:1])
    char2 = rawutil.unpack('<c', telemetry[1:2])
    char3 = rawutil.unpack('<c', telemetry[2:3])
    char4 = rawutil.unpack('<c', telemetry[3:4])
    bytes_list = char1 + char2 + char3 + char4
    ep.field1 =''.join(b.decode('utf-8') for b in bytes_list)
    if ep.field1 == EventStringCode.FASTEST_LAP.value:
        ep.field2.append(unpack_fastestlap(telemetry[4:]))
    elif ep.field1 == EventStringCode.RETIREMENT.value:
        unpack_retirement(telemetry[4:])
    elif ep.field1 == EventStringCode.DRS_ENABLED.value:
        unpack_drsstatus(1)
    elif ep.field1 == EventStringCode.DRS_DISABLED.value:
        unpack_drsstatus(0)
    elif ep.field1 == EventStringCode.TEAM_MATE_IN_PITS.value:
        unpack_team_mate_in_pits(telemetry[4:])
    elif ep.field1 == EventStringCode.RACE_WINNER.value:
        unpack_race_winner(telemetry[4:])
    elif ep.field1 == EventStringCode.PENALTY.value:
        unpack_penalty(telemetry[4:])
    elif ep.field1 == EventStringCode.SPEED_TRAP.value:
        unpack_speedtrap(telemetry[4:])
    elif ep.field1 == EventStringCode.START_LIGHTS.value:
        unpack_startlights(telemetry[4:])
    elif ep.field1 == EventStringCode.LIGHTS_OUT.value:
        lightsout()
    elif ep.field1 == EventStringCode.DRIVE_THROUGH_SERVED.value:
        unpack_drivethroughpenaltyserved(telemetry[4:])
    elif ep.field1 == EventStringCode.STOP_GO_SERVED.value:
        unpack_stopgopenaltyserved(telemetry[4:])
    elif ep.field1 == EventStringCode.FLASHBACK.value:
        unpack_flashback(telemetry[4:])
    elif ep.field1 == EventStringCode.BUTTON.value:
        unpack_button(telemetry[4:])
    elif ep.field1 == EventStringCode.RED_FLAG.value:
        unpack_redflag(telemetry[4:])
    elif ep.field1 == EventStringCode.OVERTAKE.value:
        unpack_overtake(telemetry[4:])
    return ep

def unpack_cartelemetrydata(telemetry: bytes):
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
    for i in range(4):
        ctd.field11.append(rawutil.unpack('<H', telemetry[offset:offset+2])[0])
        offset += 2
    offset = 30
    for i in range(4):
        ctd.field12.append(rawutil.unpack('<B', telemetry[offset:offset+1])[0])
        offset += 1
    offset = 34
    for i in range(4):
        ctd.field13.append(rawutil.unpack('<B', telemetry[offset:offset+1])[0])
        offset += 1
    ctd.field14 = rawutil.unpack('<H', telemetry[38:40])[0]
    offset = 40
    for i in range(4):
        ctd.field15.append(rawutil.unpack('<f', telemetry[offset:offset+4])[0])
        offset += 4
    offset = 56
    for i in range(4):
        ctd.field16.append(rawutil.unpack('<B', telemetry[offset:offset+1])[0])
        offset += 1

    return ctd

def unpack_cartelemetrydatapacket(telemetry: bytes, carIndex):
    ctdp = CarTelemetryDataPacket()
    offset = carIndex * 60
    ctdp.field1.append(unpack_cartelemetrydata(telemetry[offset:offset+60]))
    ctdp.field2 = rawutil.unpack('<B', telemetry[1320:1321])[0]
    ctdp.field3 = rawutil.unpack('<B', telemetry[1321:1322])[0]
    ctdp.field4 = rawutil.unpack('<b', telemetry[1322:1323])[0]
    return ctdp

def unpack_carstatusdata(telemetry: bytes):
    # <H means 2byte <B means 1byte <Q means 8byte <f means 4byte

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

def unpack_carstatuspacket(telemetry: bytes, carIndex):
    csp = CarStatusPacket()
    offset = carIndex * 55
    car_status_data = unpack_carstatusdata(telemetry[offset:offset + 55])
    csp.field1.append(car_status_data)  # append the CarStatusData object to field1
    return csp

def unpack_cardamagedata(telemetry: bytes):
    cdd = CarDamageData()
    offset = 0
    for i in range(4):
        cdd.field1.append(rawutil.unpack('<I', telemetry[offset:offset+4])[0])
        offset += 4
    offset = 16
    for i in range(4):
        cdd.field2.append(rawutil.unpack('<B', telemetry[offset:offset+1])[0])
        offset += 1
    offset = 20
    for i in range(4):
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

def unpack_cardamagepacket(telemetry: bytes, carIndex):
    cdp = CarDamagePacket()
    offset = carIndex * 42
    cdp.field1.append(unpack_cardamagedata(telemetry[offset:offset+42]))

    return cdp


##### Optimalizálni kell az alábbi két függvényt, mert nagyon lassú a feldolgozási idejük
def unpack_laphistorydata(telemetry: bytes):
    # <H means 2byte <B means 1byte <Q means 8byte <f means 4byte

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

def unpack_sessionhistorypacket(telemetry: bytes, carIndex):
    shp = SessionHistoryPacket()
    id = rawutil.unpack('<B', telemetry[:1])[0]
    if id == carIndex:
        shp.field1 = id
        shp.field2 = rawutil.unpack('<B', telemetry[1:2])[0]
        shp.field3 = rawutil.unpack('<B', telemetry[2:3])[0]
        shp.field4 = rawutil.unpack('<B', telemetry[3:4])[0]
        shp.field5 = rawutil.unpack('<B', telemetry[4:5])[0]
        shp.field6 = rawutil.unpack('<B', telemetry[5:6])[0]
        shp.field7 = rawutil.unpack('<B', telemetry[6:7])[0]
        offset = 7
        for i in range(100):
            shp.field8.append(unpack_laphistorydata(telemetry[offset:offset+14]))
            offset += 14
        return shp
    else:
        return 404

########





def unpack_tyresetdata(telemetry: bytes):
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

def unpack_tyresetspacket(telemetry: bytes):
    tsp = TyreSetsPacket()
    tsp.field1 = rawutil.unpack('<B', telemetry[:1])[0]
    offset = 1
    for i in range(20):
        tsp.field2.append(unpack_tyresetdata(telemetry[offset:offset+10]))
        offset += 10
    tsp.field3 = rawutil.unpack('<B', telemetry[201:202])[0]
    return tsp
