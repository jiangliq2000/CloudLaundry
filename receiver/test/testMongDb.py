# -*- coding:utf-8 -*-  
__author__ = 'liqiang'


import sys
import unicodecsv as csv
import codecs
sys.path.append("..")

import lib.DbOpt as dbOpt



record = {u'washId': 3, u'startdate': u'2017-03-03', u'endtime': u'16:58:15', u'enddate': u'2017-03-03', u'seq': u'515', u'prio': u'2', u'devId': u'09010009', u'step': u'2', u'pumps': {u'rou-ruan-ji': 25, u'zhu-ji': 10, u'jian-ye': 5, u'suan-ji': 30, u'yang-piao': 15, u'lv-piao': 20, u'ru-hua-ji': 40, u'shui-chu-li': 35}, u'starttime': u'16:57:50', u'formula': 6, u'pumpnum': 8}
caption = [u'起始时间',u'结束时间',u'设备号',u'洗衣机',u'配方',u'步骤',u'优先级',u'碱液',u'助剂',u'氧漂',u'氯漂',u'柔软剂',u'酸剂',u'水处理',u'乳化剂']
test = ['中国','测试','你好']

PRIOMap = {0:u'低',1:u'普通',2:u'高',3:u'紧急'}
FORMULAMap = {1:u'白毛巾',2:u'颜色毛巾',3:u'白床单',4:u'颜色床单',5:u'白台布',6:u'颜色台布',7:u'厨衣',8:u'浅制服',9:u'深制服',10:u'新草布', \
              11:u'毛巾回洗',12:u'床单回洗',13:u'台布回洗',14:u'床罩窗帘',15:u'抹布',16:u'自定义1',17:u'自定义2',18:u'自定义3',19:u'自定义4',20:u'自定义5'}

def parseRecord(rec):
    rList = [0]*15
    rList[0] = record['startdate'] +' ' + record['starttime']
    rList[1] = record['enddate'] + ' ' + record['endtime']
    rList[2] = str(record['devId'])
    rList[3] = record['washId']
    rList[4] = FORMULAMap[record['formula']]
    rList[5] = record['step']
    rList[6] = PRIOMap[int(record['prio'])]
    rList[7] = str(record['pumps']['jian-ye'])
    rList[8] = str(record['pumps']['zhu-ji'])
    rList[9] = str(record['pumps']['yang-piao'])
    rList[10] = str(record['pumps']['lv-piao'])
    rList[11] = str(record['pumps']['rou-ruan-ji'])
    rList[12] = str(record['pumps']['suan-ji'])
    rList[13] = str(record['pumps']['shui-chu-li'])
    rList[14] = str(record['pumps']['ru-hua-ji'])

    return rList    

if __name__ == '__main__':

    """
    db = dbOpt.dbIns(tablename='test')
    data = {u'碱液':10, u'助剂':20}
    db.save(dat8a)
    data = db.query({'name':'liqiang'})
    #data = db.query({u'碱液'：10})
    db.close()
    print data

    """
    with open('csvtest.csv','wb') as csvfile:
        csvfile.write(codecs.BOM_UTF8)
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow(caption)
        result = []
        for i in range(10):
            result.append(parseRecord(record))
        writer.writerows(result)
    csvfile.close()
    print "reuslt is: \n"

    print result


    