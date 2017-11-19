# -*- coding:utf-8 -*-  
__author__ = 'liqiang'

from struct import pack as pk

rawSyncdata = "02 01 18 00 09 00 01 09 00 00 00 00 01 00 02 00 00 00 02 00 00 e1 07 04 13 15 04 03 01 a1 03"

class syncQuery(object):
    def __init__(self):
        self.head = 0x02
        self.type = 0x01
        self.len = 0x18
        self.devid = 0x09010009
        self.model = 0x00000000
        self.hwVer = 0x00020001
        self.fwVer = 0x00020000
        self.lang = 0x0
        self.year = 0x07e1
        self.month = 0x04
        self.day = 0x16
        self.hour = 0x15
        self.minute = 0x04
        self.second = 0x03
        self.crc = 0xa101
        self.etx = 0x03

    def groupNetData(self):
        data = ''
        data += pk('B', self.head)
        data += pk('B', self.type)
        data += pk('<H', self.len)
        data += pk('<I', self.devid)
        data += pk('<I', self.model)
        data += pk('<I', self.hwVer)
        data += pk('<I', self.fwVer)
        data += pk('B', self.lang)
        data += pk('<H', self.year)
        data += pk('B', self.month)
        data += pk('B', self.day)
        data += pk('B',self.hour)
        data += pk('B', self.minute)
        data += pk('B', self.second)
        data += pk('<H', self.crc)
        data += pk('B',self.etx)

        return data



rawReportData = "02 02 36 00 09 00 01 09 00 00 03 02 00 00 06 00 \
                 02 02 e1 07 04 17 10 39 32 e1 07 04 17 10 3a 0f \
                 08 00 00 05 00 01 0a 00 02 0f 00 03 14 00 04 19 \
                 00 05 1e 00 06 23 00 07 28 00 1e ab 03"

class  WashStep(object):
    def __init__(self, month=4, day=1, devId=0x09010009, washId=1):
        data = pk('B' ,0x02)
        data += pk('B', 0X02)
        data += pk('<H', 0x0036)
        data += pk('<I', devId)
        data += pk('<H', washId)
        data += pk('<I', 0x00000203)
        data += pk('<H', 0x0006)
        data += pk('B', 0x02)
        data += pk('B', 0x02)
        data += pk('<H', 0x07e1)
        data += pk('B', month)
        data += pk('B', day)
        data += pk('B', 0x10)
        data += pk('B', 0x39)
        data += pk('B', 0x32)
        data += pk('<H', 0x07e1)
        data += pk('B', month)
        data += pk('B', day)
        data += pk('B', 0x10)
        data += pk('B', 0x3a)
        data += pk('B', 0x0f)
        data += pk('<H', 0x0008)

        for i in range(8):
            data += pk('B', i)
            data += pk('<H', 0x0005*(i+1))

        data += pk('<H', 0xab14)
        data += pk('B', 0x03)
         
        self.data = data   

    def groupNetData(self):
        return self.data



rawRptPumpCfg = "02 03 1e 00 09 00 01 09 08 00 00 0a 00 01 0a 00 \
                 02 0a 00 03 0a 00 04 0a 00 05 0a 00 06 0a 00 07 \
                 0a 00 d1 b8 03 "

class RptPumpCfg(object):
    def __init__(self):
        data = pk('B' ,0x02)
        data += pk('B', 0X03)
        data += pk('<H', 0x001e)
        data += pk('<I', 0x0901000a)
        data += pk('<H', 0x0008)

        for i in range(8):
            data += pk('B', i)
            data += pk('<H', 0x000a)

        data += pk('<H', 0xd1b8)
        data += pk('B', 0x03)
         
        self.data = data   

    def groupNetData(self):
        return self.data


class RptValveCfg(object):
    def __init__(self):
        data = pk('B' ,0x02)
        data += pk('B', 0X05)
        data += pk('<H', 0x0036)# length
        data += pk('<I', 0x0901000a)
        data += pk('<H', 0x0008)

        for i in range(8):
            data += pk('B', i)
            data += pk('<H', 0x000a+i)
            data += pk('B', i)
            data += pk('<H', 0x000a+i)

        data += pk('<H', 0xd1b8)
        data += pk('B', 0x03)
         
        self.data = data   

    def groupNetData(self):
        return self.data        

class RptFormulaCfg(object):
    def __init__(self):
        data = pk('B' ,0x02)
        data += pk('B', 0X07)
        data += pk('<H', 0x0cec)# length
        data += pk('<I', 0x0901000a)
        data += pk('<H', 0x0002)
        data += pk('<H', 20)

        for i in range(20):
            # formula type
            data += pk('B', i)
            for j in range(4):
                #step
                data += pk('B', 1) # prio
                for h in range(8):
                    # pump
                    data += pk('B', h) # pump type
                    data += pk('<H', h) # open
                    data += pk('<H', h) # volume

        data += pk('<H', 0xd1b8)
        data += pk('B', 0x03)
         
        self.data = data   
        print "data len is"
        print len(data)

    def groupNetData(self):
        return self.data                