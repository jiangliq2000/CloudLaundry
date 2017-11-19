/**
 * Created by jerry on 2017/4/13.
 */
import Mock from 'mockjs'



const UserDevid =  ['222222','111111']


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

const Users = []
for (let i = 0; i < 5; i++) {
  Users.push(Mock.mock({
    //id: Mock.Random.guid(),
    username: Mock.Random.string("abcdefghijklmnopqrstuvwxyz",6, 8),
    devid: Mock.Random.string("0123456789abcdefg", 8,8),
    password: Mock.Random.string("0123456789abcdefg", 6,9),
    name: Mock.Random.cname(),
    contact: String(Mock.Random.integer(133000,133999)),
    register: Mock.Random.date()
  }))
}


export {UserDevid}
