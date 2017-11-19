# -*- coding:utf-8 -*-  
__author__ = 'liqiang'

import sys
import logging
import struct
import socket
import time
import gevent
import traceback
from gevent import socket, monkey
import lib.encode as encode
import lib.decode as decode
import lib.DbOpt as DbOpt
from lib.const import *

monkey.patch_all()

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %A %H:%M:%S',
                filename='receiver.log',
                filemode='a+')
"""
logging.debug("debug output")
logging.info("info output")
logging.warninging
logging.
"""

BUFFER_LEN = 4096


def server(port):
    try:
        s = socket.socket()

        rbsize = s.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
        print " send buf is ", rbsize

        s.bind(('0.0.0.0', port))
        s.listen(100)
        logging.info("server is listening")
        while True:
            cli, addr = s.accept()
            logging.info('--- recive connection from : ' + str(addr))
            gevent.spawn(handle_request, (cli, str(addr)))

    except KeyboardInterrupt as e:
        print(e)


def handle_request(connInfo):
    conn = connInfo[0]
    addr = connInfo[1]
    try:
        while True:
            data = conn.recv(BUFFER_LEN)
            print "receive data len is "
            print len(data)
            if not data:
                logging.info("client(" +addr + ") has been closed..")
                conn.close()
                break
            else:
                logging.info('from ' +addr + 'recv :' + repr(data))
                # below just for debug
                with open('rawdata', 'ab+') as f:
                    f.write(data)
                # debug end
                res = handle_data(data)
                logging.info("send " +addr + "data :" + repr(res))
                if res != None:
                    conn.send(res)
    except OSError as e:
        logging.error("client has been closed")
        logging.error(e)

    except Exception , ex:
        logging.error("socket exception print")
        logging.error(ex)
        exstr = traceback.format_exc()
        logging.warning(exstr)

    finally:
        conn.close()


def synQueryHandle(data):
    # format request SyncQuery request
    ins = decode.SyncQueryFrame(data)
    # store to database
    db = DbOpt.dbIns(tablename=TB_SYNCSTATUS)
    db.save(ins.genRecord())
    # generate reply ack
    ackInfo = ins.getEncodeInfo()
    # get system
    d,t = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()).split(" ")
    ackInfo[DATE] = d
    ackInfo[TIME] = t
    # status and type is hard code to 1 and 0
    ackInfo[STATUS] = 1
    ackInfo[CFGTYPE] = 0
    ackIns = encode.SyncQueryAck(ackInfo)
    return ackIns.groupFrame()
   

def rptDataHandle(data):
    # format request SyncQuery request
    ins = decode.WashstepFrame(data)
    # store to database
    logging.debug("rpt data genRecord is")
    logging.debug(ins.genRecord())
    db = DbOpt.dbIns(tablename=TB_REPORT)
    db.save(ins.genRecord())
    # generate reply ack
    ackInfo = ins.getEncodeInfo()
    ackIns = encode.RptAck(ackInfo)
    return ackIns.groupFrame()

def rptPumpCfgHandle(data):
    ins = decode.RptPumpCfgFrame(data)
    # store to database
    logging.debug("rpt PumpCfg genRecord is")
    logging.debug(ins.genRecord())
    db = DbOpt.dbIns(tablename=TB_PUMPCFG)
    db.save(ins.genRecord())
    # generate reply ack
    # generate reply ack
    ackInfo = ins.getEncodeInfo()
    ackIns = encode.RptAck(ackInfo)
    return ackIns.groupFrame()

def rptValveCfgHandle(data):
    ins = decode.ValveCfgFrame(data)
    # store to database
    logging.debug("rpt ValveCfg genRecord is")
    logging.debug(ins.genRecord())
    db = DbOpt.dbIns(tablename=TB_VALVECFG)
    db.save(ins.genRecord())
    # generate reply ack
    ackInfo = ins.getEncodeInfo()
    ackIns = encode.RptAck(ackInfo)
    return ackIns.groupFrame()

def rptFormulaHandle(data):
    ins = decode.FormulaFrame(data)
    # store to database
    logging.debug("rpt Formula genRecord is")
    logging.debug(ins.genRecord())
    db = DbOpt.dbIns(tablename=TB_FORMULACFG)
    db.save(ins.genRecord())
    # generate reply ack
    ackInfo = ins.getEncodeInfo()
    ackIns = encode.RptAck(ackInfo)
    return ackIns.groupFrame()


def getPumpCfgHandle(data):
    pass

def getValveCfgHandle(data):
    pass


def getFormulaHanle(data):
    pass


"""
#global dataHandleFun
dataHandleFun = { 0x1:synQueryHandle, 0x2:rptDataHandle, 0x3:rptPumpCfgHandle, 0x4:getPumpCfgHandle ,
                  0x5:rptValveCfgHandle, 0x6:getValveCfgHandle, 0x7:rptFormulaHandle, 0x8:getFormulaHanle }


def handle_data(data):
    # judge frame type
    fhead, ftype = struct.unpack('BB', data[:2])
    if fhead != 0x2:
        logging.warning("frame head is not right, this is bad frame, discard it ")
        return None
    res = dataHandleFun.get(ftype)(data)
    dec
    return res                  


encSwitch_dict = { 0x1:encode.SyncQueryAck, 0x2:encode.RptAck, 0x3:encode.RptPumpCfgAck, 0x4:encode.GetPumpCfgAck ,
                  0x5:encode.RptValveCfgAck, 0x6:encode.GetValveCfgAck, 0x7:encode.RptFormularAck, 0x8:encode.GetFormularAck }

"""








decSwitch_dict = { 0x1:[decode.SyncQueryFrame, encode.SyncQueryAck , TB_SYNCSTATUS], 0x2:[decode.WashstepFrame,encode.RptAck , TB_REPORT], 0x3:[decode.RptPumpCfgFrame, encode.RptAck, TB_PUMPCFG],
                   0x4:[decode.GetPumpCfgFrame, encode.GetPumpCfgAck, TB_PUMPCFG] , 0x5:[decode.ValveCfgFrame,encode.RptAck,TB_VALVECFG], 0x6:[decode.GetValveCfgFrame,encode.GetValveCfgAck,TB_VALVECFG], 
                   0x7:[decode.FormulaFrame,encode.RptAck,TB_FORMULACFG ], 0x8:[decode.GetFormulaFrame,encode.GetFormularAck,TB_FORMULACFG ] }




def decSwitch(x):
    return decSwitch_dict.get(x, None)



def handle_data(data):
    # judge frame type
    fhead, ftype = struct.unpack('BB', data[:2])
    if fhead != 0x2:
        logging.warning("frame head is not right, this is bad frame, discard it ")
        return None

    frameClass = decSwitch(ftype)
    if frameClass == None:
        logging.warning("frame type is not right, this is bad frame, discard it ")
        return None
    ins = frameClass[0](data)
    
    db = DbOpt.dbIns(tablename=frameClass[2])
    # if frame is report frame, store to database
    if ftype in [1,2,3,5,7]:
        db.save(ins.genRecord())
    else:  # query database
        pass
        
    # generate reply ack
    ackInfo = ins.getEncodeInfo()
    ackIns = frameClass[1](ackInfo)
    return ackIns.groupFrame()


if __name__ == '__main__':
    logging.info("###########################################################")
    logging.info("----------receiver restart at:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "--------------")
    logging.info("###########################################################")
    server(6688)


