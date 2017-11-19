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
DEVFlag = struct.pack('<H',0xdddd)
SEVFlag = struct.pack('<H',0xffff)

def server(port):
    try:
        s = socket.socket()

        s.bind(('0.0.0.0', port))
        s.listen(100)
        logging.info("server is listening")
        while True:
            cli, addr = s.accept()
            logging.info('--- recive connection from : ' + str(addr))
            gevent.spawn(handle_request, (cli, str(addr)))


    except KeyboardInterrupt as e:
        
        print(e)
        sys.exit(1)


def handle_request(connInfo):
    conn = connInfo[0]
    addr = connInfo[1]
    conn.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
    conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 20)
    conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 2)
    try:
        tmpbuf = None
        while True:
            data = conn.recv(BUFFER_LEN)
            logging.info("data len is %d" %len(data))
            if not data:
                logging.info("client(" +addr + ") has been closed..")
                #conn.close()
                break
            # it is not whole frame, need wait next recv 
            tail, = struct.unpack('B', data[-1])  
            if tail != 0x3:
                logging.info('receive data, but not whole frame, need reconstruct')
                if tmpbuf is None:
                    tmpbuf = data[:]
                else:
                    tmpbuf = tmpbuf + data
            # one packet is whole frame
            else:
                if tmpbuf is not None:
                    data = tmpbuf + data
                    tmpbuf = None
                logging.info('from ' +addr + 'recv : %d' %len(data))
                # below just for debug
                # get devid then store data to devid.dat file
                devid, = struct.unpack('<I', data[4:8])
                fname = ("%08x"%devid) + ".dat"
                with open("data/" + fname, 'ab+') as f:
                    f.write(DEVFlag)
                    f.write(data)                    
                # debug end
                res = handle_data(data)                
                if res == None:
                    logging.info("cannot generate response to " +addr + ", will close this connection")
                    break
                else:
                    logging.info("send " +addr + "data :" + repr(res))
                    conn.send(res)
                    with open("data/" + fname, 'ab+') as f:
                        f.write(SEVFlag)
                        f.write(res)
                logging.info("finished to response " +addr )

    except OSError as e:
        logging.error("client has been closed")
        logging.error(e)

    except Exception , ex:
        logging.error("socket exception print")
        logging.error(ex)
        exstr = traceback.format_exc()
        logging.warning(exstr)

    finally:
        logging.info("will close socket for " +addr)
        conn.close()

"""
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
    logging.info("rpt Formula genRecord is")
    logging.info(ins.genRecord())
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








decSwitch_dict = { 0x1:[decode.SyncQueryFrame, encode.SyncQueryAck , TB_NOTIFY, 'devid'], 0x2:[decode.WashstepFrame,encode.RptAck , TB_REPORT, 'devid'], 
                   0x3:[decode.RptPumpCfgFrame, encode.RptAck, TB_PUMPCFG, 'devid'], 0x4:[decode.GetPumpCfgFrame, encode.GetPumpCfgAck, TB_PUMPCFG,'devid'] , 
                   0x5:[decode.ValveCfgFrame,encode.RptAck,TB_VALVECFG,'devid'], 0x6:[decode.GetValveCfgFrame,encode.GetValveCfgAck,TB_VALVECFG,'devid'], 
                   0x7:[decode.FormulaFrame,encode.RptAck,TB_FORMULACFG, 'devid+washid' ], 0x8:[decode.GetFormulaFrame,encode.GetFormularAck,TB_FORMULACFG, 'devid+washid' ],
                   0x10:[decode.DevicePosFrame,encode.RptAck,TB_DEVIDCOMMS,'devid'] }




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
    
    # database operation
    db = DbOpt.dbIns(tablename=frameClass[2])
    queryStr = frameClass[3]
    dbdata = ins.genRecord()
    # judge query condition
    devid = dbdata[DEVID]
    washid = ''
    if len(queryStr.split('+')) == 2:
        washid = dbdata[WASHID]         

    # if frame is report frame, store to database
    if ftype == 0x2:
        logging.info("insert into database(%s), devid=%s,  washid=%s " %(frameClass[2], devid, washid))
        db.insert(dbdata)
        ackInfo = ins.getEncodeInfo()

    elif ftype in [3,5,7]:
        logging.info("save into database(%s), devid=%s,  washid=%s " %(frameClass[2], devid, washid))
        db.save(dbdata, devid, washid)
        # updaate notify table, set updateType to false
        DbOpt.dbIns(tablename=TB_NOTIFY).save({DEVID:devid,frameClass[2]:'false'},devid,'') 
        ackInfo = ins.getEncodeInfo()

    else:  # query database
        logging.info("query database(%s), devid=%s,  washid=%s " %(frameClass[2], devid, washid))
        if washid:
            cnd = {DEVID:devid,WASHID:washid}
        elif devid:
            cnd = {DEVID:devid}
        else:
            cnd = {}

        record = db.query(cnd)
        logging.info("query record is: " + str(record))
        ackInfo = ins.getEncodeInfo(record)
        if ftype in [4,6,8]:
            # after complete with devid sync, updaate notify table, set updateType to false
            DbOpt.dbIns(tablename=TB_NOTIFY).save({DEVID:devid,frameClass[2]:'false'},devid,'') 

        if ftype == 0x1:
            # if devid not register in devidcomms table, insert this record.this
            DbOpt.devidRegister(devid) 
            # query device activedays and return device.
            ackInfo[EXPIRY] = int(DbOpt.GetActiveDays(devid))

        if ftype == 0x10:
            # if it is device position frame, update position to devidcomms table
            DbOpt.devPosUpdate(devid, dbdata) 


    ackIns = frameClass[1](ackInfo)
    db.close()
        
    # generate reply ack
    #ackInfo = ins.getEncodeInfo()
    #ackIns = frameClass[1](ackInfo)
    return ackIns.groupFrame()


if __name__ == '__main__':
    logging.info("###########################################################")
    logging.info("----------receiver restart at:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "--------------")
    logging.info("###########################################################")
    server(6688)


