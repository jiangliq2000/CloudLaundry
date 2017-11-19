# -*- coding:utf-8 -*- 
__author__ = 'liqiang'

import logging
import time
#import struct
from struct import pack as pk
import CRC16
from const import *


FRAME_HEAD = 0x02
FRAME_TAIL = 0X03
WASHSTEPACK_PAYLOAD_LEN = 0x05

class PayloadLen(object):
    syncQuery = 17
    washStep = 5
    rptPumpCfg = 5

def DateSplit(date):
    """
       date format:  2017-04-21
    """
    year = date[:4]
    month = date[5:7]
    day = date[-2:]
    return (year, month, day)

def encodePayload(ftype, payload):
    tmpbuf = ftype + pk('<H', len(payload))
    tmpbuf += payload
    crc = CRC16.calcString(tmpbuf, CRC16.INITIAL_MODBUS)
    tmpbuf += pk('<H', crc)
    tmpbuf += pk('B', FRAME_TAIL) 
    return tmpbuf

"""
it is json data when get data from mongodb

"""

"""
SyncQueryFrame payload struct


    # get system
    d,t = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()).split(" ")
    ackInfo[DATE] = d
    ackInfo[TIME] = t
    # status and type is hard code to 1 and 0
    ackInfo[STATUS] = 1

"""
class SyncQueryAck(object):
    def __init__(self, data):
        self.ftype = data[TYPE]
        tmpbuf = pk('<I',data[DEVID])
        # get system
        d,t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).split(" ")        
        tmpbuf += self.packDate(d)
        tmpbuf += self.packTime(t)
        # current activedays is hard code: 1000
        # query activedays from database 
        tmpbuf += pk('<I',  data[EXPIRY])        
        if data[RECORD] == None:
            status =0
            cfgtype = 7
        else:
            status = 1
            cfgtype = 0
            # need something exception protect, otherwise will not send sync response to client
            try:
                if data[RECORD][TB_PUMPCFG] == 'true':
                    status = 2
                    cfgtype = cfgtype | 1
                if data[RECORD][TB_VALVECFG] == 'true':
                    status = 2
                    cfgtype = cfgtype | 2
                if data[RECORD][TB_FORMULACFG] == 'true':
                    status = 2
                    cfgtype = cfgtype | 4
            except KeyError,e:
                # if raise exception, notify client sync from server 
                logging.info("----------there are something exception when query configuration for pumpcfg,valvecf,formulacf --------------")
                status = 0
                cfgtype = 7

        tmpbuf += pk('B', status)     
        tmpbuf += pk('B', cfgtype)
        self.payload = tmpbuf


    def packDate(self, data):
        """  
           date format:  2017-04-21
        """
        dateList = data.split("-")
        tmpbuf = pk('<H', int(dateList[0]))
        tmpbuf += pk('B', int(dateList[1]))
        tmpbuf += pk('B', int(dateList[2]))
        return tmpbuf

    def packTime(self, data):
        """  
           date format:  10:20:45
        """
        dateList = data.split(":")
        tmpbuf = pk('B', int(dateList[0]))
        tmpbuf += pk('B', int(dateList[1]))
        tmpbuf += pk('B', int(dateList[2]))
        return tmpbuf

    def groupFrame(self):
        head = pk('B', FRAME_HEAD)
        frameType = pk('B', self.ftype)
        tmpbuf = encodePayload(frameType, self.payload)     
        return (head + tmpbuf)

class Ack(object):
    def __init__(self, data):
        self.ftype = data[TYPE]
        self.tmpbuf = pk('<I', data[DEVID])

    def groupFrame(self):
        head = pk('B', FRAME_HEAD)
        frameType = pk('B', self.ftype)        
        tmpbuf = encodePayload(frameType, self.payload)
        return (head + tmpbuf)    


class RptAck(object):
    """
    device report washing step data by this frame
    """
    def __init__(self, data):
        self.ftype = data[TYPE]
        tmpbuf = pk('<I', data[DEVID])
        tmpbuf += pk('B', data[STATUS])
        self.payload = tmpbuf

    def groupFrame(self):
        head = pk('B', FRAME_HEAD)
        frameType = pk('B', self.ftype)        
        tmpbuf = encodePayload(frameType, self.payload)
        return (head + tmpbuf)

class GetPumpCfgAck(Ack):
    def __init__(self, data):
        super(GetPumpCfgAck, self).__init__(data)         
        self.tmpbuf += self.parseRecord(data[RECORD])
        self.payload = self.tmpbuf

    def parseRecord(self, record):
        pumpNum = record[PUMPNUM]
        pumps = record[PUMPS]
        data = pk('<H', pumpNum)        
      
        for i in range(pumpNum):
            data += pk('B', pumps['pump%d'%(i+1)][TYPE])
            data += pk('<H', pumps['pump%d'%(i+1)][SPEED])

        return data


class GetValveCfgAck(Ack):
    def __init__(self, data):
        super(GetValveCfgAck, self).__init__(data)         
        self.tmpbuf += self.parseRecord(data[RECORD])
        self.payload = self.tmpbuf

    def parseRecord(self, record):
        washNum = record[WASHNUM]
        washs = record[WASHS]
        data = pk('<H', washNum)  
        for i in range(1, washNum+1):
            data += pk('<H', washs['wash%d'%i][INOPEN] )
            data += pk('<H',washs['wash%d'%i][INCLOSE] )
            data += pk('<H', washs['wash%d'%i][OUTOPEN] )
            data += pk('<H', washs['wash%d'%i][OUTCLOSE] )
        return data

class GetFormularAck(Ack):
    def __init__(self, data):
        super(GetFormularAck, self).__init__(data)     
        self.tmpbuf += self.parseRecord(data[RECORD])
        self.payload = self.tmpbuf

    def parseRecord(self, record):
        formunum = record[FORMUNUM]
        formus = record[FORMULAS]
        data = pk('<H', record[WASHID])
        data += pk('<H', formunum)

        for i in range(formunum):
            # formula type
            data += pk('B', formus['formu%d'%i][TYPE])
            for j in range(1,FORMULA_STEP_NUM+1):
                #step
                data += pk('B', formus['formu%d'%i]['step%d'%j][PRIO]) # prio
                for k in range(1,FORMULA_STEPPUMP_NUM+1):
                    # pump                    
                    data += pk('B', formus['formu%d'%i]['step%d'%j]['pump%d'%k][TYPE]) # pump type
                    data += pk('<H', formus['formu%d'%i]['step%d'%j]['pump%d'%k][OPEN]) # open
                    data += pk('<H', formus['formu%d'%i]['step%d'%j]['pump%d'%k][VOL]) # volume

        return data
