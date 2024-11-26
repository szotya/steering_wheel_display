from rawutil import unpack
from modules.EventPacket import FastestLap, Retirement, DRSStatus, TeamMateInPits, RaceWinner, Penalty, SpeedTrap, StartLights, LightsOut, DriveThroughPenaltyServed, StopGoPenaltyServed, Flashback, Buttons, RedFlag, Overtake, EventPacket, EventStringCode
from modules.SessionPacket import MarshalZone, WeatherForecastSample, SessionPacket
from modules.LapDataPacket import LapData, LapDataPacket
from modules.CarTelemetryDataPacket import CarTelemetryData, CarTelemetryDataPacket
from modules.CarStatusPacket import CarStatusData, CarStatusPacket
from modules.CarDamagePacket import CarDamageData, CarDamagePacket
from modules.SessionHistoryPacket import LapHistoryData, SessionHistoryPacket
from modules.TyreSetsPacket import TyreSetData, TyreSetsPacket
from modules.CarSetupPacket import CarSetupData, CarSetupPacket
from modules.Header import Header

def unpack_header(header: bytes):
    h=Header()

    # <H means 2byte <B means 1byte <Q means 8byte <f means 4byte
    values = unpack("<H <B <B <B <B <B <Q <f <I <I <B <B", header)
    h.field1  = values[0]
    h.field2  = values[1]
    h.field3  = values[2]
    h.field4  = values[3]
    h.field5  = values[4]
    h.field6  = values[5]
    h.field7  = values[6]
    h.field8  = values[7]
    h.field9  = values[8]
    h.field10 = values[9]
    h.field11 = values[10]
    h.field12 = values[11]

    return h

def unpack_marshalzone(telemetry: bytes):
    mz = MarshalZone()
    values = unpack("<f <b", telemetry)
    
    mz.field1 = values[0]
    mz.field2 = values[1]

    return mz

def unpack_weatherforecastsample(telemetry: bytes):
    wfs = WeatherForecastSample()
    values = unpack("<B <B <B <b <b <b <b <B", telemetry)

    wfs.field1 = values[0]
    wfs.field2 = values[1]
    wfs.field3 = values[2]
    wfs.field4 = values[3]
    wfs.field5 = values[4]
    wfs.field6 = values[5]
    wfs.field7 = values[6]
    wfs.field8 = values[7]

    return wfs

def unpack_sessionpacket(telemetry: bytes):
    sp = SessionPacket()
    values = unpack("<B <B <B <B <H <B <b <B <H <H <B <B <B <B <B <B")

    sp.field1  = values[0]
    sp.field2  = values[1]
    sp.field3  = values[2]
    sp.field4  = values[3]
    sp.field5  = values[4]
    sp.field6  = values[5]
    sp.field7  = values[6]
    sp.field8  = values[7]
    sp.field9  = values[8]
    sp.field10 = values[9]
    sp.field11 = values[10]
    sp.field12 = values[11]
    sp.field13 = values[12]
    sp.field14 = values[13]
    sp.field15 = values[14]
    sp.field16 = values[15]

    offset = 19
    for _ in range(sp.field16):
        sp.field17.append(unpack_marshalzone(telemetry[offset:offset+5]))
        offset += 5
    
    sp.field18 = rawutil.unpack('<B', telemetry[124:125])[0]
    sp.field19 = rawutil.unpack('<B', telemetry[125:126])[0]
    sp.field20 = rawutil.unpack('<B', telemetry[126:127])[0]

    offset = 127
    for _ in range(sp.field20):
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
    ld = LapData()
    values = unpack("<I <I <H <B <H <B <H <H <f <f <f <B <B <B <B <B <B <B <B <B <B <B <B <B <B <B <H <H <B", telemetry)

    ld.field1  = values[0]
    ld.field2  = values[1]
    ld.field3  = values[2]
    ld.field4  = values[3]
    ld.field5  = values[4]
    ld.field6  = values[5]
    ld.field7  = values[6]
    ld.field8  = values[7]
    ld.field9  = values[8]
    ld.field10 = values[9]
    ld.field11 = values[10]
    ld.field12 = values[11]
    ld.field13 = values[12]
    ld.field14 = values[13]
    ld.field15 = values[14]
    ld.field16 = values[15]
    ld.field17 = values[16]
    ld.field18 = values[17]
    ld.field19 = values[18]
    ld.field20 = values[19]
    ld.field21 = values[20]
    ld.field22 = values[21]
    ld.field23 = values[22]
    ld.field24 = values[23]
    ld.field25 = values[24]
    ld.field26 = values[25]
    ld.field27 = values[26]
    ld.field28 = values[27]
    ld.field29 = values[28]

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
    values = unpack("<B <B <B <B <B <B <B", telemetry)

    p.field1 = values[0]
    p.field2 = values[1]
    p.field3 = values[2]
    p.field4 = values[3]
    p.field5 = values[4]
    p.field6 = values[5]
    p.field7 = values[6]

    return p

def unpack_speedtrap(telemetry: bytes):
    st = SpeedTrap()
    values = unpack("<B <f <B <B <B, <f", telemetry)

    st.field1 = values[0]
    st.field2 = values[1]
    st.field3 = values[2]
    st.field4 = values[3]
    st.field5 = values[4]
    st.field6 = values[5]

    return st

def unpack_startlights(telemetry: bytes):
    sl = StartLights()
    value = unpack("<B", telemetry)
    sl.field1 = value[0]

    return sl

def lightsout():
    lo = LightsOut()
    lo.field1 = 1
    return lo

def unpack_drivethroughpenaltyserved(telemetry: bytes):
    dtps = DriveThroughPenaltyServed()
    value = unpack("<B", telemetry)
    dtps.field1 = value

    return dtps

def unpack_stopgopenaltyserved(telemetry: bytes):
    sgps = StopGoPenaltyServed()
    value = unpack("<B", telemetry)
    sgps.field1 = value
    return sgps

def unpack_flashback(telemetry: bytes):
    fb = Flashback()
    values = unpack("<I <f", telemetry)
    fb.field1 = values[0]
    fb.field2 = values[1]

    return fb

def unpack_button(telemetry: bytes):
    b = Buttons()
    values = unpack("<f", telemetry)
    b.field1 = values

    return b

def unpack_redflag():
    rf = RedFlag()
    rf.field1 = 1

    return rf

def unpack_overtake(telemetry: bytes):
    o = Overtake()
    values = unpack("<B <B", telemetry)
    o.field1 = values[0]
    o.field2 = values[1]

    return o

def unpack_eventpacket(telemetry: bytes):
    ep = EventPacket()
    values = unpack("<c <c <c <c", telemetry)

    char1 = values
    char2 = values
    char3 = values
    char4 = values
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
    values = unpack("<H <f <f <f <B <b <H <B <B <H", telemetry)
    ctd.field1  = values[0]
    ctd.field2  = values[1]
    ctd.field3  = values[2]
    ctd.field4  = values[3]
    ctd.field5  = values[4]
    ctd.field6  = values[5]
    ctd.field7  = values[6]
    ctd.field8  = values[7]
    ctd.field9  = values[8]
    ctd.field10 = values[9]

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

def unpack_carsetupdata(telemetry: bytes):
    csdp = CarSetupData()
    values = unpack("<B <B <B <B <f <f <f <f <B <B <B <B <B <B <B <B <f <f <f <f <B <f", telemetry)

    csdp.field1  = values[0]
    csdp.field2  = values[1]
    csdp.field3  = values[2]
    csdp.field4  = values[3]
    csdp.field5  = values[4]
    csdp.field6  = values[5]
    csdp.field7  = values[6]
    csdp.field8  = values[7]
    csdp.field9  = values[8]
    csdp.field10 = values[9]
    csdp.field11 = values[10]
    csdp.field12 = values[11]
    csdp.field13 = values[12]
    csdp.field14 = values[13]
    csdp.field15 = values[14]
    csdp.field16 = values[15]
    csdp.field17 = values[16]
    csdp.field18 = values[17]
    csdp.field19 = values[18]
    csdp.field20 = values[19]
    csdp.field21 = values[20]
    csdp.field22 = values[21]

def unpack_carsetupdatapacket(telemetry: bytes, carIndex):
    csp = CarSetupPacket()
    offset = carIndex * 49
    csp.field1.append(unpack_carsetupdata(telemetry[offset:offset+49]))
    return csp

def unpack_cartelemetrydatapacket(telemetry: bytes, carIndex):
    ctdp = CarTelemetryDataPacket()
    offset = carIndex * 60
    ctdp.field1.append(unpack_cartelemetrydata(telemetry[offset:offset+60]))
    ctdp.field2 = rawutil.unpack('<B', telemetry[1320:1321])[0]
    ctdp.field3 = rawutil.unpack('<B', telemetry[1321:1322])[0]
    ctdp.field4 = rawutil.unpack('<b', telemetry[1322:1323])[0]
    return ctdp

def unpack_carstatusdata(telemetry: bytes):
    csd = CarStatusData()
    values = unpack("<B <B <B <B <B <f <f <f <H <H <B <B <H <B <B <B <B <f <f <f <B <f <f <f <B")

    csd.field1  = values[0]
    csd.field2  = values[1]
    csd.field3  = values[2]
    csd.field4  = values[3]
    csd.field5  = values[4]
    csd.field6  = values[5]
    csd.field7  = values[6]
    csd.field8  = values[7]
    csd.field9  = values[8]
    csd.field10 = values[9]
    csd.field11 = values[10]
    csd.field12 = values[11]
    csd.field13 = values[12]
    csd.field14 = values[13]
    csd.field15 = values[14]
    csd.field16 = values[15]
    csd.field17 = values[16]
    csd.field18 = values[17]
    csd.field19 = values[18]
    csd.field20 = values[19]
    csd.field21 = values[20]
    csd.field22 = values[21]
    csd.field23 = values[22]
    csd.field24 = values[23]
    csd.field25 = values[24]

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
    lhd = LapHistoryData()
    values = unpack("<I <H <B <H <B <H <B <B", telemetry)

    lhd.field1 = values[0]
    lhd.field2 = values[1]
    lhd.field3 = values[2]
    lhd.field4 = values[3]
    lhd.field5 = values[4]
    lhd.field6 = values[5]
    lhd.field7 = values[6]
    lhd.field8 = values[7]

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

def unpack_tyresetdata(telemetry: bytes):
    tsd = TyreSetData()
    values = unpack("<B <B <B <B <B <B <B <H <B", telemetry)
    tsd.field1 = values[0]
    tsd.field2 = values[1]
    tsd.field3 = values[2]
    tsd.field4 = values[3]
    tsd.field5 = values[4]
    tsd.field6 = values[5]
    tsd.field7 = values[6]
    tsd.field8 = values[7]
    tsd.field9 = values[8]
    return tsd

def unpack_tyresetspacket(telemetry: bytes):
    tsp = TyreSetsPacket()
    value = unpack("<B", telemetry)
    tsp.field1 = value

    offset = 1
    for _ in range(20):
        tsp.field2.append(unpack_tyresetdata(telemetry[offset:offset+10]))
        offset += 10
    
    value = unpack("<B", telemetry[201:202])
    tsp.field3 = value
    return tsp
