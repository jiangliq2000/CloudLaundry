# -*- coding:utf-8 -*-  
__author__ = 'liqiang'

import socket
import struct
import testEncode


HOST = 'localhost'
PORT = 6690


def testSyncQuery(s):
    ins = testEncode.syncQuery()
    data = ins.groupNetData()
    print "syncQuery Frame on network is:"
    print repr(data)
    print "send sync data to server"
    s.sendall(data)
    data = s.recv(1024)
    print('received', repr(data))

def testWashStep(s):
    devId = 0x09010009;
    month = 3
    for i in range(1,20):
        ins = testEncode.WashStep(month, i, devId+i%3, i%8)
        data = ins.groupNetData()
        print "WashStep frame on network is:"
        print repr(data)
        print "send WashStep data to server"
        s.sendall(data)
        data = s.recv(1024)
        print('received', repr(data))

def testRptPumpCfg(s):
    ins = testEncode.RptPumpCfg()
    data = ins.groupNetData()
    print "RptPumpCfg frame on network is:"
    print repr(data)
    print "send RptPumpCfg data to server"
    s.sendall(data)
    data = s.recv(1024)
    print('received', repr(data))    


def testRptValveCfg(s):
    ins = testEncode.RptValveCfg()
    data = ins.groupNetData()
    print "RptValveCfg frame on network is:"
    print repr(data)
    print "send RptValveCfg data to server"
    s.sendall(data)
    data = s.recv(1024)
    print('received', repr(data))    


def testRptFormulaCfg(s):
    ins = testEncode.RptFormulaCfg()
    data = ins.groupNetData()

    print "RptFormulaCfg frame on network is:"
    #print repr(data)
    print "the len is ", len(data)

    try:
        print "send RptFormulaCfg data to server"
        s.sendall(data)

        print "finish to send"
        data = s.recv(1024)
        print('received', repr(data))        
    except Exception, e:
        print "throw a exception"
        print e



def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    bsize = s.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    print "send buf size is ", bsize
    s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
    s.connect((HOST, PORT))    
    #testSyncQuery(s)
    #testWashStep(s)
    #testRptPumpCfg(s)
    #testRptValveCfg(s)
    testRptFormulaCfg(s)


    s.close()

"""
while True:
    msg = syncData
    s.sendall(msg)

    data = s.recv(1024)
    print('received', repr(data))
"""
    




if __name__ == '__main__':
    main()







