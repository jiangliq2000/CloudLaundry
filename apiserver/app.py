# -*- coding:utf-8 -*-  
__author__ = 'liqiang'

from flask import Flask, jsonify, request, stream_with_context, Response
from flask import make_response
import json
import logging
from pymongo import MongoClient
from flask_jwt import JWT, jwt_required, current_identity,CONFIG_DEFAULTS
from werkzeug.security import safe_str_cmp
from flask_cors import CORS, cross_origin
import unicodecsv as csv
import codecs
import os
import time
import datetime
import traceback
import DbOpt
from const import *

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

def authenticate(username, password):
    users = DbOpt.VerifyUser(username)
    if users and safe_str_cmp(users['password'].encode('utf-8'), password.encode('utf-8')):
        return User(username, username, password)

def identity(payload):
    username = payload['identity']
    users = DbOpt.VerifyUser(username)
    if users:
        return User(username, username, users['password'])

app = Flask(__name__)
CORS(app)
CONFIG_DEFAULTS['JWT_AUTH_URL_RULE'] = '/login'
CONFIG_DEFAULTS['JWT_EXPIRATION_DELTA'] = datetime.timedelta(seconds=900)
app.debug = True
app.config['SECRET_KEY'] = '!@#hijkl*(,.x1509xm$%'
jwt = JWT(app, authenticate, identity)

YAOJIMap = {'jian-ye':1, 'zhu-ji':2, 'yang-piao':3, 'lv-piao':4,'rou-ruan-ji':5,'suan-ji':6, 'shui-chu-li':7, 'ru-hua-ji':8}
PRIOMap = {0:u'低',1:u'普通',2:u'高',3:u'紧急'}
FORMULAMap = {1:u'白毛巾',2:u'颜色毛巾',3:u'白床单',4:u'颜色床单',5:u'白台布',6:u'颜色台布',7:u'厨衣',8:u'浅制服',9:u'深制服',10:u'新草布', \
              11:u'毛巾回洗',12:u'床单回洗',13:u'台布回洗',14:u'床罩窗帘',15:u'抹布',16:u'自定义1',17:u'自定义2',18:u'自定义3',19:u'自定义4',20:u'自定义5'}
caption = [u'起始时间',u'结束时间',u'设备号',u'洗衣机',u'配方',u'步骤',u'优先级',u'药剂1',u'药剂2',u'药剂3',u'药剂4',u'药剂5',u'药剂6',u'药剂7',u'药剂8']
HEADERS = "Access-Control-Allow-Origin"

def parseParam(alist):
    for (x,y) in alist:
        if x == 'userName':
            user = y
        elif x == 'startdate':
            stime = y
        elif x == 'enddate':
            etime = y
        else:
            print "somethint is wrong"
            user, stime, etimie = (0,0,0)
    return (user, stime, etime)

def calcStats(records):
    stats = dict()
    washList = [0,0,0,0,0,0,0,0,0]
    drugList = [0,0,0,0,0,0,0,0,0]
    formulaList = [0,0,0,0,0,0,0,0,0,0,\
                   0,0,0,0,0,0,0,0,0,0]
    for record in records:
        if record[STEP] == '1':
            washList[record['washId']] += 1
            formulaList[record['formula']-1] += 1
        for k,v in record['pumps'].items():
            drugList[YAOJIMap[k]] += v
    drugList.pop(0)
    washList[0] = sum(washList)
    #  calc wash
    washDict = dict()
    for i in range(len(washList)):
        washDict['wash%d'%i] = washList[i]
    stats['wash'] = []
    stats['wash'].append(washDict)
    # calc drug
    drugDict = dict()
    for i in range(len(drugList)):
        drugDict['drug%d'%(i+1)] = format(float(drugList[i])/float(1000),'.2f')
    stats['drug'] = []
    stats['drug'].append(drugDict)
    #calc formula
    formulaDict = dict()
    for i in range(len(formulaList)):
        formulaDict['fm%d'%(i+1)] = formulaList[i]
    stats["formula"] = []
    stats["formula"].append(formulaDict)
    return stats

def parseRecord(record):
    rList = [0]*15
    rList[0] = record['startdate'] +' ' + record['starttime']
    rList[1] = record['enddate'] + ' ' + record['endtime']
    rList[2] = str(record[DEVID])
    rList[3] = str(record['washId'])
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

# -------------- admin api part
@app.route('/user/list', methods=['GET'])
@jwt_required()
def GetUserList():
    username = request.args.get('username')
    if username:
        cnd = {'username':username}
    else:
        cnd = {}
    users = DbOpt.GetUserList(cnd)
    resp = make_response(json.dumps({'totals':len(users), 'Users':users}))
    resp.headers["Access-Control-Allow-Origin"] = '*'
    return resp

@app.route('/user/delete', methods=['GET'])
@jwt_required()
def GetDeleteUser():
    userRec = dict()
    userRec['username'] = request.args.get('username')
    cdn = {'username':userRec['username']}
    status = DbOpt.DelUser(cdn)
    resp = make_response(jsonify({'msg': u'成功', 'code':200}), 200)
    resp.headers["Access-Control-Allow-Origin"] = '*'
    return resp     	

@app.route('/user/batchdelete/', methods=['GET'])
@jwt_required()
def GetBatchDeleteUser():
    pass			

@app.route('/user/changepwd', methods=['GET'])
@jwt_required()
def ChangePwd():
    username = request.args.get('username')
    oldpwd = request.args.get('oldpwd')
    newpwd = request.args.get('newpwd')
    users = DbOpt.VerifyUser(username)
    if users:
        pwdStore = users['password']
        if oldpwd == pwdStore:
            userRec = dict()
            userRec['password'] = request.args.get('newpwd')
            status = DbOpt.UpdatePwd(username,userRec)
            resp = make_response(jsonify({'msg': u'修改成功', 'code':200}), 200)
        else:
            resp = make_response(jsonify({'msg': u'旧密码验证失败', 'code': 201}), 200)
    else:
        resp = make_response(jsonify({'msg': u'密码更新失败', 'code': 202}), 200)

    resp.headers["Access-Control-Allow-Origin"] = '*'
    return resp

@app.route('/user/edit', methods=['GET'])
@jwt_required()
def EditUser():
    userRec = dict()
    userRec['username'] = request.args.get('username')
    userRec[DEVID] = request.args.get(DEVID).lower()
    userRec['password'] = request.args.get('password')
    userRec['privilege'] = request.args.get('privilege')
    userRec['name'] = request.args.get('name')
    userRec['contact'] = request.args.get('contact')   
    cdn = {'username':userRec['username']}
    status = DbOpt.UpdateUser(cdn,userRec)
    resp = make_response(jsonify({'msg': u'修改成功', 'code':200}), 200)
    resp.headers["Access-Control-Allow-Origin"] = '*'
    return resp    	

	
@app.route('/user/add', methods=['GET'])
@jwt_required()
def AddUser():
    userRec = dict()
    userRec['username'] = request.args.get('username')
    userRec[DEVID] = request.args.get(DEVID).lower()
    userRec['password'] = request.args.get('password')
    userRec['privilege'] = request.args.get('privilege')
    userRec['name'] = request.args.get('name')
    userRec['contact'] = request.args.get('contact')   
    userRec['register'] = request.args.get('register')   
    status = DbOpt.SaveUser(userRec)
    resp = make_response(jsonify({'msg': u'保存成功', 'code':200}), 200)
    resp.headers["Access-Control-Allow-Origin"] = '*'
    return resp    
	
# ---------- user api part	
@app.route('/data/query/date', methods=['GET'])
@jwt_required()
def GetDateStats():
    #(user, stime, etime) = parseParam(request.args.items())
    user = request.args.get('user')
    stime = request.args.get('starttime')
    etime = request.args.get('endtime')
    conn = MongoClient('127.0.0.1', 27017)
    # get deviceId
    devIdList = DbOpt.GetDevidbyUser(user)
    # get all dats according condition
    db_heist = conn['heist']
    tb_heist = db_heist['reportdata']
    totalStats = []
    for devid in devIdList:
        condition = {"devId":devid,"startdate":{"$gte":stime, "$lte":etime}}
        buf = tb_heist.find(condition) 
        result = []
        for x in buf:
            result.append(x)
        if result:
            stats = calcStats(result)
            stats[DEVID] = devid
            pos, comment2 = DbOpt.GetPosbyDevid(devid)
            stats['position'] = pos
            stats['comment2'] = comment2
            totalStats.append(stats)

    conn.close()
    resp = make_response(json.dumps(totalStats))
    resp.headers["Access-Control-Allow-Origin"] = '*'
    return resp


@app.route('/data/download/<filename>', methods=['GET'])
#@jwt_required()
def DownloadFile(filename):   
    devid = request.args.get(DEVID)
    stime = request.args.get('starttime')
    etime = request.args.get('endtime')
    def generate():
        #yield ','.join(caption).encode('GB18030') + '\n'
        yield ','.join(caption).encode('utf-8') + '\n'
        conn = MongoClient('127.0.0.1', 27017)
        condition = {"devId":devid,"startdate":{"$gte":stime, "$lte":etime}}
        db_heist = conn['heist']
        tb_heist = db_heist['reportdata']
        buf = tb_heist.find(condition) 
        result = []
        for x in buf:
            recd = parseRecord(x)
            yield ','.join(recd).encode('utf-8') + '\n'    
        conn.close()
    return Response(generate(), mimetype='text/csv')
    """
    resp =  Response(stream_with_context(result))
    content_disposition = "attachment; filename={}".format(filename)
    resp.headers['Content-Disposition'] = content_disposition
    resp.headers["Access-Control-Allow-Origin"] = '*'

    return resp

    #return (buf)
    """

@app.route('/config/user/devid', methods=['GET'])
@jwt_required()
def GetDevidByUser():
    user = request.args.get('user')
    devList = DbOpt.GetDevidbyUser(user)
    resp = make_response(json.dumps(devList))
    resp.headers["Access-Control-Allow-Origin"] = '*'
    #return (json.dumps(totalStats))
    return resp

@app.route('/config/devid/pump/query', methods=['GET'])
@jwt_required()
def GetDevidPump():
    devid = request.args.get(DEVID)
    pumps = DbOpt.GetDevidPumpCfg(devid)
    if pumps:
        resp = make_response(json.dumps(pumps))
    else:
        resp = make_response(jsonify({'msg': u'failed', 'code':404}), 404)    
    resp.headers["Access-Control-Allow-Origin"] = '*'
    return resp

@app.route('/config/devid/pump/edit', methods=['GET'])
@jwt_required()
def GetEditDevidPump():
    devid = request.args.get(DEVID)
    # json.dumps,  dict --> str
    # json.loads,  str --> dict
    pumps = json.loads(request.args.get('pumps'))
    if DbOpt.UpdateDevidPump(devid, pumps['pumps']):
        # updaate failed
        msg = {'msg': u'更新失败', 'code':500}
    else:
        msg = {'msg': u'保存成功', 'code':200}
        # update successful
        # need updatae notify table(pump update), 前台来同步查询时就知道该表是否更新
        DbOpt.updateNotify(devid, TB_PUMPCFG)
    resp = make_response(jsonify(msg), 200)
    resp.headers["Access-Control-Allow-Origin"] = '*'
    #return (json.dumps(totalStats))
    return resp  


@app.route('/config/devid/wash/query', methods=['GET'])
@jwt_required()
def GetDevidWash():
    devid = request.args.get(DEVID)
    washs = DbOpt.GetDevidWashCfg(devid)
    if washs:
        resp = make_response(json.dumps(washs))
    else:
        resp = make_response(jsonify({'msg': u'failed', 'code':404}), 404)    
    resp.headers["Access-Control-Allow-Origin"] = '*'
    #return (json.dumps(totalStats))
    return resp

@app.route('/config/devid/wash/edit', methods=['GET'])
@jwt_required()
def EditDevidWash():
    devid = request.args.get(DEVID)
    # json.dumps,  dict --> str
    # json.loads,  str --> dict
    wash = json.loads(request.args.get('wash'))
    washIndex = json.loads(request.args.get('washIndex'))    
    if DbOpt.UpdateDevidWash(devid, wash, washIndex):
        # updaate failed
        msg = {'msg': u'更新失败', 'code':500}
    else:
        msg = {'msg': u'保存成功', 'code':200}
        # update successful
        # need updatae notify table(valve update), 前台来同步查询时就知道该表是否更新
        DbOpt.updateNotify(devid, TB_VALVECFG)
    resp = make_response(jsonify(msg), 200)
    resp.headers["Access-Control-Allow-Origin"] = '*'
    return resp  

@app.route('/config/devid/formula/query', methods=['GET'])
@jwt_required()
def GetDevidFormula():
    devid = request.args.get(DEVID)
    washid = request.args.get('washid')
    formula = 'formu' + request.args.get('formula')
    formulaCfg = DbOpt.GetDevidFormuCfg(devid, int(washid), formula)
    resp = make_response(json.dumps(formulaCfg))
    resp.headers["Access-Control-Allow-Origin"] = '*'
    return resp

@app.route('/config/devid/formula/edit', methods=['GET'])
@jwt_required()
def EditDevidFormula():
    devid = request.args.get(DEVID)
    washid = request.args.get('washid')
    formula = 'formu' + request.args.get('formula')
    step = 'step' + request.args.get('stepindex')
    data = json.loads(request.args.get('stepdata'))

    if DbOpt.UpdateDevidFormula(devid, int(washid), formula,step,data['data']):
        # updaate failed
        msg = {'msg': u'更新失败', 'code':500}
    else:
        # update successful
        msg = {'msg': u'保存成功', 'code':200}
        # need updatae notify table(formula update), 前台来同步查询时就知道该表是否更新
        DbOpt.updateNotify(devid, TB_FORMULACFG)

    resp = make_response(jsonify(msg), 200)
    resp.headers["Access-Control-Allow-Origin"] = '*'
    #return (json.dumps(totalStats))
    return resp  

@app.route('/config/devidcomms/query', methods=['GET'])
@jwt_required()
def GetDevidcomms():
    devid = request.args.get(DEVID)
    username = request.args.get('username')
    if devid:
        devidList = []
        devidList.append(devid)
    else:
        # get all devid according to username
        devidList = DbOpt.GetDevidbyUser(username) 

    devidComms = DbOpt.GetDevidComms(devidList,user=username)
    resp = make_response(json.dumps(devidComms))
    resp.headers["Access-Control-Allow-Origin"] = '*'
    return resp
	
@app.route('/config/devidcomms/edit', methods=['GET'])
@jwt_required()
def GetDevidcommsEdit():
    record = dict()
    devid = request.args.get(DEVID)
    if request.args.get('password'):
        record[PASSWORD] = request.args.get('password')
    if request.args.get('position'):
        record[POSITION] = request.args.get('position')
    if request.args.get('comment'):
        record[COMMENT] = request.args.get('comment')
    if request.args.get('expiry'):
        record[EXPIRY] = int(request.args.get('expiry'))
    if request.args.get('comment2'):
        record[COMMENT2] = request.args.get('comment2')

    cnd = {DEVID: record[DEVID]}
    if DbOpt.UpdateDevidComms(cnd, record):
        # updaate failed
        msg = {'msg': u'更新失败', 'code':500}
    else:
        msg = {'msg': u'保存成功', 'code':200}

    resp = make_response(jsonify(msg), 200)
    resp.headers["Access-Control-Allow-Origin"] = '*'
    return resp    

@app.route('/config/devidcomms/delete', methods=['GET'])
@jwt_required()
def GetDevidcommsDel():
    devid = request.args.get(DEVID)
    cnd = {DEVID: devid}
    if DbOpt.DelDevidComms(cnd):
        # updaate failed
        msg = {'msg': u'更新失败', 'code':500}
    else:
        msg = {'msg': u'保存成功', 'code':200}

    resp = make_response(jsonify(msg), 200)
    resp.headers["Access-Control-Allow-Origin"] = '*'
    return resp    

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    handler = logging.FileHandler('apiserver.log')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    print "will start flask app "
    app.logger.info("###########################################################")
    app.logger.info("----------receiver restart at:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "--------------")
    app.logger.info("###########################################################")
    app.run(host="0.0.0.0", port=21000, debug = True)
