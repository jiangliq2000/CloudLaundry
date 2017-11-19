/**
 * Created by jerry on 2017/4/13.
 */
import Mock from 'mockjs'
const LoginUsers = [
  {
    id: 1,
    username: 'admin',
    password: '123456',
    email: 'jerry9022@qq.com',
    name: '风车车'
  }
]

const LoginAdmin = [
   {
    id: 1,
    username: 'heist',
    password: '111111',
    email: 'heist@qq.com',
    name: 'heist'     
   }
]


const UserDevid =  {
      user: 'admin',
      devid: [{value:'111111',label:'11111'},{value:'22222',label:'22222'}]
}



// devid.table
const UserDevidComms =  []
for (let i = 0; i < 3; i++) {
  UserDevidComms.push(Mock.mock({
    devid: Mock.Random.string("0123456789abcdefg", 5,5),
    comment: Mock.Random.string("abcdefg", 9,9)
  }))
}
UserDevidComms.push({devid:'11111', comment:'shanghai'})
UserDevidComms.push({devid:'22222', comment:'zhejiang'})




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
const Users = []
for (let i = 0; i < 15; i++) {
  Users.push(Mock.mock({
    //id: Mock.Random.guid(),
    username: Mock.Random.string("abcdefghijklmnopqrstuvwxyz",4, 6),
    devid: Mock.Random.string("0123456789abcdefg", 8,8),
    password: Mock.Random.string("0123456789abcdefg", 6,9),
    name: Mock.Random.cname(),
    contact: String(Mock.Random.integer(133000,133999)),
    register: Mock.Random.date()
  }))
}
Users.push({username:'admin',devid:'11111,22222',password:'123456',name:'张三',contact:'13305781234',register:'2017.07.09'});


export {LoginUsers, LoginAdmin, UserDevid,UserDevidComms, Users}
