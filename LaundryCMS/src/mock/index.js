/**
 * Created by liqjiang on 2017/07/13.
 */
import axios from 'axios'
import MockAdapter from 'axios-mock-adapter'
import {LoginUsers, LoginAdmin, UserDevidComms, Users} from './data/user'
import {UserDevid} from './data/devid'
import {Books} from './data/book'
import {Stats} from './data/stats'
let _Users = Users
let _Books = Books
let _Stats = Stats
let _UsersDevid = UserDevid
let _UserDevidComms = UserDevidComms

export default {

  init () {
    let mock = new MockAdapter(axios)

    // mock success request
    mock.onGet('/success').reply(200, {
      msg: 'success'
    })


    // mock error request
    mock.onGet('/error').reply(500, {
      msg: 'failure'
    })

    // 登录
    mock.onPost('/login').reply(arg => {
      console.log("> mock login reply ");

      let {username, password} = JSON.parse(arg.data)
      console.log("username is:" + username);
      console.log("password is " + password);
      return new Promise((resolve, reject) => {
        let user = null
        setTimeout(() => {
          let hasUser = LoginUsers.some(u => {
            console.log(">. hasUser entry")
            if (u.username === username && u.password === password) {
              user = JSON.parse(JSON.stringify(u))
              delete user.password
              return true
            }
          })

          let hasAdmin = LoginAdmin.some(u => {
            console.log(">. hasAdmin entry")
            console.log("u is: " + u)
            if (u.username === username && u.password === password) {
              user = JSON.parse(JSON.stringify(u))
              delete user.password
              return true
            }
          })

          if (hasUser || hasAdmin) {
            resolve([200, {code: 200, msg: '请求成功', user}])
          } else {
            resolve([200, {code: 500, msg: '账号或密码错误'}])
          }
        }, 1000)
      })
    })

    mock.onPost('/user/profile').reply(function (arg) {
      let {name, email} = JSON.parse(arg.data)
      return new Promise((resolve, reject) => {
        let user = LoginUsers[0]
        user.name = name
        user.email = email
        resolve([200, {code: 200, msg: '请求成功', user}])
      })
    })






////////////////////------------------------   user query part -------------------------------


    // 根据用户名获取设备号

    mock.onGet('/config/user/devid').reply(config => {

      console.log(">. mock index -/user/devid print")
      console.log(_UsersDevid)

      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve([200, {
            //devid: [{value:'111111',label:'11111'},{value:'22222',label:'22222'}]
            devid: ['11111','33333']
            //stats: ""
          }])
        }, 500)
      })
    })


    // 根据用户名获取所有设备号的注释

    mock.onGet('/config/devidcomms/query').reply(config => {

      console.log("/devid/query config param is ");

      let {page, devid} = config.params;

      let mockUsers = _UserDevidComms.filter(user => {
        if (devid && user.devid.indexOf(devid) === -1) return false
        return true
      })

      let total = mockUsers.length
      mockUsers = mockUsers.filter((u, index) => index < 10 * page && index >= 10 * (page - 1))
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve([200, {
            total: total,
            devids: mockUsers
          }])
        }, 500)
      })
    })



    // 根据用户名获取设备号信息

    mock.onGet('/config/devidComms/edit').reply(config => {
      let {devid, comment} = config.params
      _UserDevidComms.some(u => {
        if (u.devid === devid) {
          u.comment = comment
          return true
        }
      })

      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve([200, {
            code: 200,
            msg: '编辑成功'
          }])
        }, 500)
      })
    })


    // 获取统计数据

    mock.onGet('/data/query/date').reply(config => {

      console.log(">. mock index -/query/date print")

      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve([200, {
            stats: _Stats
            //stats: ""
          }])
        }, 500)
      })
    })


//////////////////-------------------------   user config part -----------------------------------------
    // 泵阀配置

    mock.onGet('/config/devid/pump').reply(config => {

      console.log("config is ");
      console.log(config.params);
      let {devid} = config.params;

      if (devid === "11111"){
        var resp = ['0','1','2','3','4','5','6','7']
      }
      else{
        var resp = ['1','7','7','6','4','5','6','7']
      }

      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve([200, {
            pumpcfg: resp
            //stats: ""
          }])
        }, 500)
      })
    })


    // wash配置

    mock.onGet('/config/devid/wash').reply(config => {

      let {devid} = config.params;

      if (devid === "11111"){
        var resp = [{'ins':'9','inc':'2','outs':'5','outc':'4'},{'ins':'6','inc':'2','outs':'3','outc':'4'},{'ins':'3','inc':'2','outs':'3','outc':'4'},{'ins':'1','inc':'2','outs':'3','outc':'4'},
                      {'ins':'7','inc':'2','outs':'3','outc':'4'},{'ins':'8','inc':'2','outs':'3','outc':'4'},{'ins':'2','inc':'2','outs':'3','outc':'4'},{'ins':'1','inc':'2','outs':'3','outc':'4'}]
      }
      else{
        var resp = [{'ins':'1','inc':'1','outs':'5','outc':'4'},{'ins':'1','inc':'2','outs':'3','outc':'4'},{'ins':'1','inc':'2','outs':'3','outc':'4'},{'ins':'1','inc':'2','outs':'3','outc':'4'},
                      {'ins':'1','inc':'2','outs':'3','outc':'4'},{'ins':'1','inc':'2','outs':'3','outc':'4'},{'ins':'1','inc':'2','outs':'3','outc':'4'},{'ins':'1','inc':'2','outs':'3','outc':'4'}]
      }



      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve([200, {
            washcfg: resp
            //stats: ""
          }])
        }, 500)
      })
    })


    // 根据设备号获取配方配置

    mock.onGet('/config/devid/formula').reply(config => {

      console.log(">. mock index /config/devid/formula print")
      console.log()


      var resp = [
        {'pri':'','p1':'2','p2':'1','p3':'3','p4':'4','p5':'5','p6':'6','p7':'5','p8':'8'},
        {'pri':'2','p1':'2','p2':'5','p3':'3','p4':'4','p5':'5','p6':'6','p7':'5','p8':'8'},
        {'pri':'','p1':'2','p2':'9','p3':'3','p4':'4','p5':'5','p6':'6','p7':'5','p8':'8'},
        {'pri':'0','p1':'2','p2':'0','p3':'3','p4':'4','p5':'5','p6':'6','p7':'5','p8':'8'},
        {'pri':'','p1':'2','p2':'9','p3':'3','p4':'4','p5':'5','p6':'6','p7':'5','p8':'8'},
        {'pri':'1','p1':'2','p2':'1','p3':'3','p4':'4','p5':'5','p6':'6','p7':'5','p8':'8'},
        {'pri':'','p1':'2','p2':'3','p3':'3','p4':'4','p5':'5','p6':'6','p7':'5','p8':'8'},
        {'pri':'1','p1':'2','p2':'6','p3':'3','p4':'4','p5':'5','p6':'6','p7':'5','p8':'8'}
      ];

      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve([200, {
            formula: resp
          }])
        }, 500)
      })
    })





////////////// -----------  admin  part  -------------------------------

    // 获取用户列表（分页）
    mock.onGet('/user/list').reply(config => {

      console.log("/user/list config param is ");

      let {page, username} = config.params;

      let mockUsers = _Users.filter(user => {
        if (username && user.username.indexOf(username) === -1) return false
        return true
      })

      let total = mockUsers.length
      mockUsers = mockUsers.filter((u, index) => index < 10 * page && index >= 10 * (page - 1))
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve([200, {
            total: total,
            Users: mockUsers
          }])
        }, 500)
      })
    })

    // 新增用户
    mock.onGet('/user/add').reply(config => {
      let {username, devid, password, name, contact, register} = config.params
      _Users.push({
        username: username,
        devid: devid,
        password: password,
        name: name,
        contact: contact,
        register: register
      })
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve([200, {
            code: 200,
            msg: '新增成功'
          }])
        }, 500)
      })
    })

    // 编辑用户
    mock.onGet('/user/edit').reply(config => {
      let {username, devid, password} = config.params
      _Users.some(u => {
        if (u.username === username) {
          u.devid = devid
          u.password = password
          return true
        }
      })

      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve([200, {
            code: 200,
            msg: '编辑成功'
          }])
        }, 500)
      })
    })

    // 删除用户
    mock.onGet('/user/delete').reply(config => {
      let {username} = config.params
      _Users = _Users.filter(b => b.username !== username)
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve([200, {
            code: 200,
            msg: '删除成功'
          }])
        }, 500)
      })
    })

    // 批量删除用户
    mock.onGet('/user/batchdelete').reply(config => {
      let {ids} = config.params
      ids = ids.split(',')
      _Users = _Users.filter(u => !ids.includes(u.id))
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve([200, {
            code: 200,
            msg: '删除成功'
          }])
        }, 500)
      })
    })

  }

}
