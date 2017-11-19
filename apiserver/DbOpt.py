# -*- coding:utf-8 -*-  
__author__ = 'liqiang'


from pymongo import MongoClient
from const import *


class dbIns(object):
    def __init__(self, host='localhost', port=27017, tablename='reportdata'):
        self.client = MongoClient(host, port)
        self.db = self.client[DATABASE]
        self.table = self.db[tablename]

    def query(self, condition={}):
        return self.table.find(condition)

    def save(self, obj_dict, condition):
        if (self.table.find_one(condition)):
            self.update(condition, obj_dict)
        else:
            self.insert(obj_dict)

    def insert(self, obj_list):
        ''' insert records in batch or single'''
        self.table.insert(obj_list)

    def find_one(self, condition={},noKey={"_id":0}):
        return self.table.find_one(condition, noKey)

    def findAll(self, condition={},noKey={"_id":0}):
        return self.table.find(condition, noKey)

    def remove(self, condition={}):
        self.table.remove(condition)

    def update(self, condition, data):
        self.table.update(condition, {'$set':data}, multi=True)

    def close(self):
        self.client.close()
    
    def get_by_id(self, idd):
        return self.table.find_one({'id':idd})

    def get_count(self, condition={}):
        return self.table.find(condition).count()

    def drop_table(self):
        self.table.drop()
    
    def get_all_collection_names(self):
        print self.db.collection_names()


def init_TB_USERS():
    user = dict()
    user['username'] = 'test'
    user[DEVID] = '11111'
    user['password'] = '111111'
    user['name'] = u'111'
    user['contact'] = '1111'
    user['register'] = '2017-08-01'
    db = dbIns(tablename=TB_USER)
    db.insert(user)
    db.close()    

def table_init():
    init_TB_USERS()

def IsExistUser(username):
    """
    if user exist, return name and pwd, otherwise return None
    """
    db = dbIns(tablename=TB_USER)
    record = db.find_one({'username':username},noKey={})
    db.close()
    if record:
        return {'id':record['_id'],'username':username, 'password':record['password']}
    else:
        return None

def GetUserList(cnd):
    db = dbIns(tablename=TB_USER)
    buf = db.findAll(condition=cnd) 
    records = []
    for rec in buf:
        #pwd_context.encrypt(rec['records'])
        records.append(rec)
    db.close()
    return records

def VerifyUser(username):
    db = dbIns(tablename=TB_USER)
    record = db.find_one(condition={'username':username}) 
    db.close()
    if record:
        return record
    else:
        db = dbIns(tablename=TB_DEVIDCOMMS)
        record = db.find_one(condition={DEVID:username}) 
        db.close()    
        return record

def UpdatePwd(username, obj_dict):
    db = dbIns(tablename=TB_USER)
    record = db.find_one(condition={'username':username}) 
    if record:
        db.update({'username':username}, obj_dict)
        db.close()
        return 0
    
    db = dbIns(tablename=TB_DEVIDCOMMS)
    record = db.find_one(condition={DEVID:username}) 
    if record:
        db.update({DEVID:username}, obj_dict)
        db.close()    
        return 0
    
    return 1

def CreateDevidComm(devIdList, flag='create'):    
    db = dbIns(tablename=TB_DEVIDCOMMS)
    for devid in devIdList:
        obj_dict = dict()
        obj_dict[DEVID] = devid
        obj_dict['password'] = devid
        #if flag == 'create':
        #    obj_dict['comment'] = ''
        db.save(obj_dict, {DEVID:devid})
    db.close()
    return 0

def SaveUser(obj_dict):
    """
       return 0, save successful
    """
    db = dbIns(tablename=TB_USER)
    db.insert(obj_dict)
    db.close()
    CreateDevidComm(obj_dict[DEVID].split(','))
    return 0

def UpdateUser(condition, obj_dict):
    db = dbIns(tablename=TB_USER)
    db.update(condition, obj_dict)
    db.close()
    CreateDevidComm(obj_dict[DEVID].split(','), flag='update')
    return 0

def DelUser(condition):
    db = dbIns(tablename=TB_USER)
    db.remove(condition)
    db.close()
    return 0

def GetDevidbyUser(user):
    db = dbIns(tablename=TB_USER)
    record = db.find_one({'username':user})     
    db.close()
    if record:
        devIdList = record[DEVID].split(',')
        return devIdList
    else:
        db = dbIns(tablename=TB_DEVIDCOMMS)
        record = db.find_one(condition={DEVID:user}) 
        db.close()   
        devIdList = []
        devIdList.append(user)
        return devIdList

def GetDevidComms(devList,user=''):
    db = dbIns(tablename=TB_DEVIDCOMMS)
    devComms = []
    if (user == 'heist') or (user == 'superadmin'):
        buf = db.findAll()
    else:
        buf = db.findAll(condition={DEVID:{"$in":devList}})
    for record in buf:
        print record
        devComms.append(record)
    db.close()
    return devComms

def UpdateDevidComms(condition, obj_dict):
    db = dbIns(tablename=TB_DEVIDCOMMS)
    buf = db.update(condition, obj_dict)
    db.close()
    return 0

def DelDevidComms(condition):
    db = dbIns(tablename=TB_DEVIDCOMMS)
    buf = db.remove(condition)
    db.close()
    return 0

def GetPosbyDevid(devid):
    db = dbIns(tablename=TB_DEVIDCOMMS)
    record = db.find_one({DEVID:devid}) 
    db.close()
    pos = ''
    comment2 = ''
    print "devid is ", devid
    print "record is "
    print record
    if record:
        if record.has_key('position'):
            pos = record['position']
        if record.has_key('comment2'):
            comment2 = record['comment2']

    return (pos, comment2) 

def GetDevidPumpCfg(devid):
    db = dbIns(tablename=TB_PUMPCFG)
    pumpList = []
    record = db.find_one({DEVID:devid}) 
    db.close()
    if record:
        pumps = record['pumps']
        for i in range(1,record['pumpnum']+1):
            pumpList.append(pumps['pump%d'%i]['type'])
    return pumpList    

def UpdateDevidPump(devid,pumps):
    db = dbIns(tablename=TB_PUMPCFG)
    record = db.find_one({DEVID:devid}) 
    for i in range(1,len(pumps)+1):
        record['pumps']['pump%d'%i]['type']= pumps['pump%d'%i]
    cnd = {DEVID:devid}
    db.update(cnd, record) 
    db.close()
    return 0

def GetDevidWashCfg(devid):
    db = dbIns(tablename = TB_VALVECFG)
    washList = []  
    record = db.find_one({DEVID:devid})
    db.close()
    if record:
        washs = record['washs']
        for i in range(1,record['washnum']+1):
            wash = dict()
            wash['ins'] = washs['wash%d'%i]['inopen']
            wash['inc'] = washs['wash%d'%i]['inclose']
            wash['outs'] = washs['wash%d'%i]['outopen']
            wash['outc'] = washs['wash%d'%i]['outclose']
            washList.append(wash)

    return washList    

def UpdateDevidWash(devid, wash, washIndex):
    db = dbIns(tablename=TB_VALVECFG)
    cnd = {DEVID:devid}
    record = db.find_one(cnd) 
    record['washs']['wash%d'%washIndex]['inopen'] = wash['wash']['inopen']
    record['washs']['wash%d'%washIndex]['inclose'] = wash['wash']['inclose']
    record['washs']['wash%d'%washIndex]['outopen'] = wash['wash']['outopen']
    record['washs']['wash%d'%washIndex]['outclose'] = wash['wash']['outclose']
    db.update(cnd, record)
    db.close()
    return 0

def GetDevidFormuCfg(devid, washid, formutype):
    db = dbIns(tablename = TB_FORMULACFG)
    formuList = []
    record = db.find_one({DEVID:devid, 'washId':washid})
    db.close()
    if record:
        formula = record['formulas'][formutype]
        for i in range(1,FORMULA_STEP_NUM+1):
            print formula['step%d'%i]
            step = formula['step%d'%i]
            startDict = dict()
            volDict = dict()
            for i in range(1,FORMULA_STEPPUMP_NUM+1):
                volDict['p%d'%i] = step['pump%d'%i]['vol']
                startDict['p%d'%i] = step['pump%d'%i]['open']
            startDict['prio'] =''
            volDict['prio'] = step['prio']
            formuList.append(startDict)
            formuList.append(volDict)
    return formuList

def UpdateDevidFormula(devid, washid, formutype,step,data):
    db = dbIns(tablename = TB_FORMULACFG)
    cnd = {DEVID:devid, 'washId':washid}
    record = db.find_one(cnd)
    prio = record['formulas'][formutype][step]['prio']
    if (len(data) == 8):
        # it mean update open time
        upLabel = 'open'
    else:
        # it mean update vol and prio
        upLabel = 'vol'
        record['formulas'][formutype][step]['prio'] = data.pop(8)
    for i in range(len(data)):
        record['formulas'][formutype][step]['pump%d'%(i+1)][upLabel] = data[i]

    db.update(cnd, record) 
    return 0

def updateNotify(devid, updateType):
    db = dbIns(tablename = TB_NOTIFY)
    cnd = {DEVID:devid}
    db.update(cnd, {updateType:'true'}) 
    return 0

if __name__ == "__main__":
    table_init()
