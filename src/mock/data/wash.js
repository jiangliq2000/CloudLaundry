/**
 * Created by jerry on 2017/4/13.
 */
import Mock from 'mockjs'


/*
const Users = []
for (let i = 0; i < 100; i++) {
  Users.push(Mock.mock({
    id: Mock.Random.guid(),
    name: Mock.Random.cname(),
    addr: Mock.mock('@county(true)'),
    'age|18-60': 1,
    birth: Mock.Random.date(),
    sex: Mock.Random.integer(0, 1)
  }))
}
*/


// user.table 
const Formula = []
for (let i = 0; i < 15; i++) {
  Users.push(Mock.mock({
    //id: Mock.Random.guid(),
    devid: Mock.Random.string("0123456789abcdefg", 8,8),
    washid: Mock.Random.string("0123456789", 4,4),
    formulas: {'fm1':{'type':'baimaojin',''}, 'fm2':{}}

  }))
}

export {Formula}
