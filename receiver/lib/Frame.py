import logging
import struct

PUMPLEN = 3
PUMPCFGLEN = 3

def StringToDate(buf):
    year = struct.unpack('<H', buf[:2])
    month = struct.unpack('B', buf[2])
    day = struct.unpack('B', buf[3]) 
    return "%d-%d-%d" %(year, month, day)
    
def StringToTime(buf):
    hour = struct.unpack('B', buf[0])
    minute = struct.unpack('B', buf[1])
    second = struct.unpack('B', buf[2])
    return "%d:%d:%d" %(hour, minute, second)


"""
byte order:  little-endian  <
frame struct

head:    1 byte      0x02           
type:    1 byte      0x01 - 0x08 
len :    2 byte
payload: len byte
crc16:   2 byte               
tail:    1 byte

"""

class Frame():
    def __init__(self, buf, flag='unpack'):
        """
        flag: 'pack'    --- buf will be sent to device
              'unpack'  --- buf is receive from device
        """
        if flag == 'unpack':
            self.head = struct.unpack('B',buf[0])
            self.type = struct.unpack('B',buf[1])
            self.payloadLen = struct.unpack('<H',buf[2:4])
            self.crc = struct.unpack('<H', buf[-3:-1])
        else if flag == 'pack':
            self.head = 

    def printFrame(self):
        pass


"""
SyncQueryFrame payload struct

"""
class SyncQueryFrame(Frame):
    def __init__(self, buf, flag):
        super(SyncQueryFrame, self).__init(buf, flag)
        payloadBuf = buf[3:-3]
        # make sure payload buffer len is equal 24
        self.devId = struct.unpack('<I', payload[:4])
        self.model = struct.unpack('<I', payload[4:8])
        self.hwVer = struct.unpack('<I', payload[8:12])
        self.fwVer = struct.unpack('<I', payload[12:16])
        self.language = struct.unpack('B', payload[16])
        self.dateTime = StringToDate(payload[17:21])
        self.time = StringToTime(payload[21:])

class SyncQueryAckFrame(Frame):
    pass



class WashstepFrame(Frame):
    """
    device report washing step data by this frame
    """
    def __init__(self, buf):
        super(WashstepFrame, self).__init__(buf)
        payloadBuf = buf[3:-3]
        # make sure payload buffer len is equal 24
        self.devId = struct.unpack('<I', payload[:4])
        self.washId = struct.unpack('<H', payload[4:6])
        self.formular = struct.unpack('<H',payload[6:8])
        self.step = struct.unpack('B', payload[8])
        self.prio = struct.unpack('B', payload[9])
        self.startDate = StringToDate(payload[9:13])
        self.startTime = StringToTime(payload[13:16])
        self.endDate = StringToDate(payload[16:20])
        self.endTime = StringToTime(payload[20:23])
        self.pumNum = struct.unpack('<H',payload[23])
        pumData = payload[23:]
        if self.pumNum*PUMPLEN != len(pumData):
            print "there are something wrong for this frame"

        self.pumList = []
        for i in range(0, len(pumData),PUMPLEN):
            self.pumList.append(self.ParsePump(pumData[i:i+PUMPLEN]))

    def ParsePump(self, buf):
        pump = dict()
        pump['type'] = struct.unpack('B', buf[0])
        pump['vol'] = struct.unpack('<H', buf[1:])
        return pump



class PumpCfgFrame(Frame):
    """
    device report washing step data by this frame
    """
    def __init__(self, buf):
        super(PumpCfgFrame, self).__init__(buf)
        payloadBuf = buf[3:-3]
        # make sure payload buffer len is equal 24
        self.devId = struct.unpack('<I', payload[:4])
        self.pumNum = struc.unpack('<H', payload[4:6])

        pumCfgData = payload[6:]
        if self.pumNum*PUMPCFGLEN != len(pumCfgData):
            print "there are something wrong for this PumpConf frame"

        self.pumCfgList = []
        for i in range(0, len(pumCfgData), PUMPCFGLEN):
            self.pumCfgList.append(self.ParsePumpCfg(pumCfgData[i:i+PUMPCFGLEN]))

    def ParsePumpCfg(self, buf):
        pump = dict()
        pump['type'] = struct.unpack('B', buf[0])
        pump['speed'] = struct.unpack('<H', buf[1:])
        return pump      




