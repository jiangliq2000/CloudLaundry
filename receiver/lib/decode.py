# -*- coding:utf-8 -*-  
__author__ = 'liqiang'

import logging
import struct
from const import *


def isFrameTail(buf):
    tail, = struct.unpack('B', buf)
    if tail == 0x3:
        return True
    else:
        return False

def StringToDate(buf):
    year, = struct.unpack('<H', buf[:2])
    month, = struct.unpack('B', buf[2])
    day, = struct.unpack('B', buf[3]) 
    return "%d-%02d-%02d" %(year, month, day)
    
def StringToTime(buf):
    hour, = struct.unpack('B', buf[0])
    minute, = struct.unpack('B', buf[1])
    second, = struct.unpack('B', buf[2])
    return "%d:%02d:%02d" %(hour, minute, second)


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

class Frame(object):
    def __init__(self, buf):
        self.head, = struct.unpack('B',buf[0])
        self.type, = struct.unpack('B',buf[1])
        self.payloadLen, = struct.unpack('<H',buf[2:4])
        self.crc, = struct.unpack('<H', buf[-3:-1])

    def getHead(self):
        head = dict()
        head['head'] = self.head
        head['type'] = self.type

    def printFrame(self):
        pass


"""
SyncQueryFrame payload struct

"""
class SyncQueryFrame(Frame):
    def __init__(self, buf):
        super(SyncQueryFrame, self).__init__(buf)        
        payload = buf[4:-3]
        # make sure payload buffer len is equal 24
        self.devId, = struct.unpack('<I', payload[:4])
        self.model, = struct.unpack('<I', payload[4:8])
        self.hwVer, = struct.unpack('<I', payload[8:12])
        self.fwVer, = struct.unpack('<I', payload[12:16])
        self.language, = struct.unpack('B', payload[16])
        self.date = StringToDate(payload[17:21])
        self.time = StringToTime(payload[21:])
        self.ackInfo = dict()
        self.ackInfo[DEVID] = self.devId
        self.ackInfo[TYPE] = self.type
        logging.info("parse syncQuery frame complete!")

    def genRecord(self):
        """
        return a json format dict
        """
        record = dict()
        record[DEVID] = "%08x" %self.devId
        record[MODEL] = "%d" %self.model
        record[HWVER] = "%d" %self.hwVer
        record[FWVER] = "%d" %self.fwVer
        record[LANG] = "%d" %self.language
        record[DATE] = self.date
        record[TIME] = self.time
        return record

    def getEncodeInfo(self,record):
        self.ackInfo[RECORD] = record
        return self.ackInfo

class WashstepFrame(Frame):
    """
    device report washing step data by this frame
    """
    def __init__(self, buf):
        super(WashstepFrame, self).__init__(buf)
        payload = buf[4:-3]
        ackInfo = dict()
        # make sure payload buffer len is equal 24
        self.devId, = struct.unpack('<I', payload[:4])
        ackInfo[DEVID] = self.devId
        ackInfo[TYPE] = self.type
        self.washId, = struct.unpack('<H', payload[4:6])
        self.seq, = struct.unpack('<I', payload[6:10])
        self.formular, = struct.unpack('<H',payload[10:12])
        self.step, = struct.unpack('B', payload[12])
        self.prio, = struct.unpack('B', payload[13])
        self.startDate = StringToDate(payload[14:18])
        self.startTime = StringToTime(payload[18:21])
        self.endDate = StringToDate(payload[21:25])
        self.endTime = StringToTime(payload[25:28])
        self.pumNum, = struct.unpack('<H',payload[28:30])
  
        pumData = payload[30:]
        if self.pumNum*PUMP_LEN != len(pumData):
            logging.warning("there are something wrong for this frame")
            ackInfo[STATUS] = 0
        else:
            ackInfo[STATUS] = 1
        self.pumpList = []
        for i in range(0, self.pumNum):
            if i != self.pumNum-1:
                self.pumpList.append(self.ParsePump(pumData[i*PUMPCFG_LEN:(i+1)*PUMP_LEN]))
            else:
                self.pumpList.append(self.ParsePump(pumData[i*PUMPCFG_LEN:]))
        self.ackInfo = ackInfo
        logging.info("parse washStep frame complete!")
        #import pdb
        #pdb.set_trace()


    def ParsePump(self, buf):
        pump = dict()
        pump[TYPE], = struct.unpack('B', buf[0])
        pump[VOL], = struct.unpack('<H', buf[1:])
        return pump

    def getEncodeInfo(self):
        return self.ackInfo 

    def genRecord(self):
        """
        return a json formaHWVERt dict
        """
        record = dict()
        record[DEVID] = "%08x" %self.devId
        record[WASHID] = self.washId
        record[SEQ] = "%d" %self.seq
        record[FORMU] = self.formular
        record[STEP] = "%d" %self.step
        record[PRIO] = "%d" %self.prio
        record[STARTDATE] = self.startDate
        record[STARTTIME] = self.startTime
        record[ENDDATE] = self.endDate
        record[ENDTIME] = self.endTime
        record[PUMPNUM] = self.pumNum
        pumpdict = {'jian-ye':0, 'zhu-ji':0, 'yang-piao':0, 'lv-piao':0, 'rou-ruan-ji':0, 'suan-ji':0, 'shui-chu-li':0,'ru-hua-ji':0}
        for i in range(self.pumNum):
            key = self.pumpList[i][TYPE]
            index = PUMPTYPEDICT[key] 
            pumpdict[index] = self.pumpList[i][VOL]
        record[PUMPS] = pumpdict

        return record


class RptPumpCfgFrame(Frame):
    """
    device report washing step data by this frame
    """
    def __init__(self, buf):
        super(RptPumpCfgFrame, self).__init__(buf)
        payload = buf[4:-3]
        ackInfo = dict()
        # make sure payload buffer len is equal 24
        self.devId, = struct.unpack('<I', payload[:4])
        ackInfo[DEVID] = self.devId
        ackInfo[TYPE] = self.type
        self.pumNum, = struct.unpack('<H', payload[4:6])

        pumCfgData = payload[6:]
        if self.pumNum*PUMPCFG_LEN != len(pumCfgData):
            logging.warning("there are something wrong for this report Pump configure frame")
            ackInfo[STATUS] = 0
        else:
            ackInfo[STATUS] = 1

        self.pumCfgList = []
        for i in range(0, self.pumNum):
            if i != self.pumNum-1:
                self.pumCfgList.append(self.ParsePumpCfg(pumCfgData[i*PUMPCFG_LEN:(i+1)*PUMPCFG_LEN]))
            else:
                self.pumCfgList.append(self.ParsePumpCfg(pumCfgData[i*PUMPCFG_LEN:]))
        
        self.ackInfo = ackInfo
        logging.info("parse RtpPumpCfg frame complete!")

    def ParsePumpCfg(self, buf):
        pump = dict()
        pump[TYPE], = struct.unpack('B', buf[0])
        pump[SPEED], = struct.unpack('<H', buf[1:])
        return pump      

    def genRecord(self):
        """
        return a json formaHWVERt dict
        """
        record = dict()
        record[DEVID] = "%08x" %self.devId
        record[PUMPNUM] = self.pumNum
        # init
        pumpdict = dict()
        for i in range(self.pumNum):
            key = ('pump%d' %(i+1))
            #pumpdict[key] = {TYPE:self.pumCfgList[i][TYPE], SPEED:self.pumCfgList[i][SPEED]}
            pumpdict[key] = self.pumCfgList[i]
        record[PUMPS] = pumpdict

        return record

    def getEncodeInfo(self):
        return self.ackInfo 


class GetPumpCfgFrame(Frame):
    def __init__(self, buf):
        super(GetPumpCfgFrame, self).__init__(buf)
        payload = buf[4:-3]
        ackInfo = dict()
        # make sure payload buffer len is equal 24
        self.devId, = struct.unpack('<I', payload[:4])
        ackInfo[DEVID] = self.devId
        ackInfo[TYPE] = self.type
        self.pumNum, = struct.unpack('<H', payload[4:6])
        self.ackInfo = ackInfo
        logging.info("parse GetPumpCfgFrame frame complete!")    

    def genRecord(self):
        """
        for GetPumpCfgFrame, don't need store data into database, just retrun devid
        """
        record = dict()
        record[DEVID] = "%08x" %self.devId
        record[PUMPNUM] = self.pumNum
        return record        

    def getEncodeInfo(self, record):
        self.ackInfo[RECORD] = record
        return self.ackInfo 


class ValveCfgFrame(Frame):
    def __init__(self, buf):
        super(ValveCfgFrame,self).__init__(buf)
        payload = buf[4:-3]
        ackInfo = dict()
        # make sure payload buffer len is equal 24
        self.devId, = struct.unpack('<I', payload[:4])
        ackInfo[DEVID] = self.devId
        ackInfo[TYPE] = self.type
        self.washNum, = struct.unpack('<H', payload[4:6])
        valveData = payload[6:]

        if self.washNum*VALVE_LEN != len(valveData):
            logging.warning("there are something wrong for this report Valve configure frame")
            ackInfo[STATUS] = 0
        else:
            ackInfo[STATUS] = 1

        self.washList = []
        for i in range(0, self.washNum):
            if (i != self.washNum-1) :
                self.washList.append(self.ParseValve(valveData[i*VALVE_LEN:(i+1)*VALVE_LEN]))
            else:
                self.washList.append(self.ParseValve(valveData[i*VALVE_LEN:]))

        self.ackInfo = ackInfo
        logging.info("parse RtpValveCfg complete!")


    def ParseValve(self, buf):
        wash = dict()
        inputValve = dict()
        outputValve = dict()
        wash[INOPEN], = struct.unpack('<H', buf[0:2])
        wash[INCLOSE], = struct.unpack('<H', buf[2:4])
        wash[OUTOPEN], = struct.unpack('<H', buf[4:6])
        wash[OUTCLOSE], = struct.unpack('<H', buf[6:])
        return wash

    def genRecord(self):
        """
        return a json formaHWVERt dict
        """
        record = dict()
        record[DEVID] = "%08x" %self.devId
        record[WASHNUM] = self.washNum
        # init
        washdict = dict()
        for i in range(self.washNum):
            key = ('wash%d' %(i+1))
            #washdict[key] = {'input':{'open': self.washList[i]['input']['open'] , 'close': self.washList[i]['input']['close']}, 'output':{'open': self.washList[i]['output']['open'], 'close': self.washList[i]['output']['close']}}
            washdict[key] = self.washList[i]
        record[WASHS] = washdict
        return record

    def getEncodeInfo(self):
        return self.ackInfo 


class GetValveCfgFrame(Frame):
    def __init__(self, buf):
        super(GetValveCfgFrame, self).__init__(buf)
        payload = buf[4:-3]
        ackInfo = dict()
        # make sure payload buffer len is equal 24
        self.devId, = struct.unpack('<I', payload[:4])
        ackInfo[DEVID] = self.devId
        ackInfo[TYPE] = self.type
        self.washNum, = struct.unpack('<H', payload[4:6])        
        self.ackInfo = ackInfo
        logging.info("parse GetValveCfgFrame frame complete!") 

    def genRecord(self):
        """
        for GetValveCfgFrame, don't need store data into database, just retrun devid
        """
        record = dict()
        record[DEVID] = "%08x" %self.devId
        record[WASHNUM] = self.washNum
        return record

    def getEncodeInfo(self, record):
        self.ackInfo[RECORD] = record
        return self.ackInfo 



class FormulaFrame(Frame):
    def __init__(self, buf):
        super(FormulaFrame,self).__init__(buf)
        payload = buf[4:-3]
        ackInfo = dict()
        # make sure payload buffer len is equal 24
        self.devId, = struct.unpack('<I', payload[:4])
        ackInfo[DEVID] = self.devId
        ackInfo[TYPE] = self.type
        self.washId, = struct.unpack('<H', payload[4:6])
        self.formuNum, = struct.unpack('<H', payload[6:8])
        formuData = payload[8:]
        if self.formuNum*FORMULA_LEN != len(formuData):
            logging.warning("there are something wrong for this report formuData configure frame")
            ackInfo[STATUS] = 0
        else:
            ackInfo[STATUS] = 1

        self.formuList = []

        for i in range(0, self.formuNum):
            if (i != self.formuNum -1):
                self.formuList.append(self.ParseFormula(formuData[i*FORMULA_LEN:(i+1)*FORMULA_LEN]))
            else:
                self.formuList.append(self.ParseFormula(formuData[-FORMULA_LEN:]))

        self.ackInfo = ackInfo
        logging.info("parse RtpFormulaCfg complete!")

    def ParseFormula(self, buf):
        formula = dict()
        formula['type'], = struct.unpack('B', buf[0])
        fload = buf[1:]
        for i in range(1,FORMULA_STEP_NUM+1):
            if i != FORMULA_STEP_NUM :
                formula['step%s' %i] = self.ParseStep(fload[(i-1)*FORMULA_STEP_LEN:i*FORMULA_STEP_LEN])
            else:
                formula['step%s' %i] = self.ParseStep(fload[-FORMULA_STEP_LEN:])

        return formula

    def ParseStep(self, buf):
        step = dict()
        step['prio'], = struct.unpack('B', buf[0])
        #step['pumps'] = []
        pumps = buf[1:]
 
        for i in range(1, FORMULA_STEPPUMP_NUM+1):
            if  i != FORMULA_STEPPUMP_NUM :
                step[('pump%d' %i)] = self.ParsePump(pumps[(i-1)*FORMULA_PUMP_LEN:i*FORMULA_PUMP_LEN])
            else:
                step[('pump%d' %i)] = self.ParsePump(pumps[-FORMULA_PUMP_LEN:])
        return step


    def ParsePump(self, buf):
        pump = dict()
        pump[TYPE], = struct.unpack('B', buf[0])
        pump[OPEN], = struct.unpack('<H', buf[1:3])
        pump[VOL], = struct.unpack('<H', buf[3:])
        return pump

    def genRecord(self):
        """
        return a json formaHWVERt dict
        """
        record = dict()
        record[DEVID] = "%08x" %self.devId
        record[WASHID] = self.washId
        record[FORMUNUM] = self.formuNum
        # init
        formudict = dict()
        for i in range(self.formuNum):
            key = ('formu%d' %i)
            formudict[key] = self.formuList[i]
        record[FORMULAS] = formudict

        return record

    def getEncodeInfo(self):
        return self.ackInfo 


class GetFormulaFrame(Frame):
    def __init__(self, buf):
        super(GetFormulaFrame, self).__init__(buf)
        payload = buf[4:-3]
        ackInfo = dict()
        # make sure payload buffer len is equal 24
        self.devId, = struct.unpack('<I', payload[:4])
        ackInfo[DEVID] = self.devId
        ackInfo[TYPE] = self.type
        self.washid, = struct.unpack('<H', payload[4:6])        
        self.ackInfo = ackInfo
        logging.info("parse GetFormulaFrame frame complete!")    

    def genRecord(self):
        """
        for GetFormulaFrame, don't need store data into database, just retrun devid
        """
        record = dict()
        record[DEVID] = "%08x" %self.devId
        record[WASHID] = self.washid
        return record        
        
    def getEncodeInfo(self, record):
        self.ackInfo[RECORD] = record
        return self.ackInfo 


class DevicePosFrame(Frame):
    def __init__(self, buf):
        super(DevicePosFrame, self).__init__(buf)
        payload = buf[4:-3]
        # make sure payload buffer len is equal 24
        self.devId, = struct.unpack('<I', payload[:4])
        # lac pos : -20 see doc
        # 
        self.lac, = struct.unpack('<H', payload[-20:-18])
        # ci pos:  -22
        self.ci, = struct.unpack('<H', payload[-18:-16])
        self.ackInfo = dict()
        self.ackInfo[DEVID] = self.devId
        self.ackInfo[TYPE] = self.type
        self.ackInfo[STATUS] = 1
        logging.info("parse DevicePosFrame frame complete!")   

    def genRecord(self):
        """
        return a json formaHWVERt dict
        """
        record = dict()
        record[DEVID] = "%08x" %self.devId
        record[POSITION] = "(%d,%d)" %(self.lac, self.ci)
        return record

    def getEncodeInfo(self, record):
        self.ackInfo[RECORD] = record
        return self.ackInfo 