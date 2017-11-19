import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Hello from '@/components/Hello'
import Main from '@/components/Main'
import Dashboard from '@/components/Dashboard'

import DevidList from '@/components/data/devidList'
import DateQuery from '@/components/data/dateQuery'
import PumpCfg from '@/components/data/pumpCfg'
import FormulaCfg from '@/components/data/formulaCfg'

import UserList from '@/components/user/list'
import UserChangePwd from '@/components/user/changepwd'
import UserProfile from '@/components/user/profile'

// 懒加载方式，当路由被访问的时候才加载对应组件
const Login = resolve => require(['@/components/Login'], resolve)

Vue.use(Router)

let router = new Router({
// mode: 'history',
  routes: [
    {
      path: '/',
      name: '首页',
      component: Dashboard
    },

    {
      path: '/login',
      name: '登录',
      component: Login
    },
    {
      path: '/auth',
      component: Home,
      name: '系统管理',
      admin: false,
      menuShow: true,
      leaf: true, // 只有一个节点
      iconCls: 'iconfont icon-users', // 图标样式class
      children: [
        {path: '/auth/admin/manage', component: UserList, name: '用户管理', menuShow: true}
      ]
    },

    {
      path: '/auth',
      component: Home,
      name: '数据查询',
      menuShow: true,
      iconCls: 'iconfont icon-books',
      children: [        
        {path: '/auth/query/devid', component: DevidList, name: '设备列表', menuShow: true},
        {path: '/auth/query/date', component: DateQuery, name: '日期查询', menuShow: true}
      ]
    },  

    {
      path: '/auth',
      component: Home,
      name: '配置管理',
      menuShow: true,
      iconCls: 'iconfont icon-books',
      children: [
        {path: '/auth/config/pump', component: PumpCfg, name: '泵阀管理', menuShow: true},
        {path: '/auth/config/formula', component: FormulaCfg, name: '配方管理', menuShow: true}
      ]
    },

    {
      path: '/auth',
      component: Home,
      name: '设置',
      menuShow: true,
      iconCls: 'iconfont icon-setting1',
      children: [
        //{path: '/user/profile', component: UserProfile, name: '个人信息', menuShow: true},
        {path: '/auth/user/changepwd', component: UserChangePwd, name: '修改密码', menuShow: true}
      ]
    }
  ]
})


router.beforeEach((to, from, next) => {
  console.log('to:' + to.path)

  if (to.path.startsWith('/login')) {
    window.sessionStorage.removeItem('access-user')
    next()
  } else if (to.path.startsWith('/auth')){
    let user = JSON.parse(window.sessionStorage.getItem('access-user'))
    console.log('user is:' + user)
    if (!user) {
      next({path: '/login'})
    } else {
      next()
    }
  } else{
      next() 
  }
})

export default router
