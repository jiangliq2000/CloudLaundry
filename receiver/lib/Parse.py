import logging
import struct



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
    def __init__(self, buf):
        self.head = struct.unpack('B',buf[0])
        self.type = struct.unpack('B',buf[1])
        self.payloadLen = struct.unpack('<H',buf[2:4])
        self.crc = struct.unpack('<H', buf[-3:-1])

    def printFrame(self):
        pass


"""
SyncQueryFrame payload struct

"""
class SyncQueryFrame(Frame):
    def __init__(self, buf):
        super(SyncQueryFrame, self).__init(buf)
        payloadBuf = buf[3:-3]
        # make sure payload buffer len is equal 24
        self.devId = struct.unpack('<I', payload[:4])
        self.model = struct.unpack('<I', payload[4:8])
        self.hwVer = struct.unpack('<I', payload[8:12])
        self.fwVer = struct.unpack('<I', payload[12:16])
        self.language = struct.unpack('B', payload[16])
        self.year = struct.unpack('<H', payload[17:19])
        self.month = struct.unpack('B', payload[19])
        self.day = struct.unpack('B', payload[20]) 
        self.hour = struct.unpack('B', payload[21])
        self.min = struct.unpack('B', payload[22])
        self.sec = struct.unpack('B', payload[23])

class DataFrame(Frame):
    """
    device report washing step data by this frame
    """
    def __init__(self, buf):
        super(DataFrame, self).__init__(buf)
