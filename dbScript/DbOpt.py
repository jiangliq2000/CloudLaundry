# -*- coding:utf-8 -*-  
__author__ = 'liqiang'

from pymongo import MongoClient
from const import *

class dbIns(object):
    def __init__(self, host='localhost', port=27017, tablename='reportdata'):
        self.client = MongoClient(host, port)
        self.db = self.client[DATABASE]
        self.table = self.db[tablename]

    def query(self, condition={},noKey={"_id":0}):

        return self.table.find_one(condition, noKey)

    def save(self, obj_dict, devid, washid):
        # first if devid and washid is not null, query database ,then update it
        #condition = {"devId":{"$in":devIdList},"startdate":{"$gte":stime, "$lte":etime}}
        if devid:
            if washid :                
                condition = {DEVID:devid, WASHID:washid}
            else:
                condition = {DEVID:devid}

            if (self.table.find_one(condition)):
                self.update(condition, obj_dict)
            else:
                self.insert(obj_dict)
        else:
            self.insert(obj_dict)

    def insert(self, obj_list):
        ''' insert records in batch or single'''
        self.table.insert(obj_list)

    def find_one(self, condition={},noKey={"_id":0}):
        return self.table.find_one(condition, noKey)

    def findAll(self, condition={}):
        return self.table.find(condition)

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

def devidRegister(devid):
    db = dbIns(tablename=TB_DEVIDCOMMS)
    rec = db.find_one(condition={DEVID:devid})
    if not rec:
        db.insert({DEVID: devid, 'password': devid})
    return 0

def devPosUpdate(devid, obj_dict):
    db = dbIns(tablename=TB_DEVIDCOMMS)
    rec = db.update({DEVID:devid},obj_dict)
    
    return 0

def ShowDevidComm():
    db = dbIns(tablename=TB_DEVIDCOMMS)
    buf = db.findAll() 
    records = []
    for rec in buf:
        records.append(rec)
    db.close()
    print records
    return 0

if __name__ == "__main__":
    #db = dbIns(tablename=TB_DEVIDCOMMS)
    #print db.get_all_collection_names()
    ShowDevidComm()


