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
const Pump = []
for (let i = 0; i < 8; i++) {
  Pump.push(Mock.mock({
    //id: Mock.Random.guid(),
    devid: Mock.Random.string(string(i), 5,5),
    pumps: Mock.Random.string("0123456789", 4,4)
  }))
}




export {Pump}
