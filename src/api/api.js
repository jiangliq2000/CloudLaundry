/**
 * Created by liqiang on 2017/06/13.
 */
import axios from 'axios'

var qs = require('qs');
let base = '127.0.0.1:21000'

//添加一个请求拦截器
axios.interceptors.request.use(config => {
    // 下面会说在什么时候存储 token
    if (sessionStorage.getItem('token')) {   
        config.headers.Authorization = 'JWT ' + sessionStorage.getItem('token');
    }
    return config;
},error =>{
    console.log(error);
    alert("错误的传参", 'fail');
    return Promise.reject(error);
});


//添加一个返回拦截器
axios.interceptors.response.use(res =>{
   //对响应数据做些事
   console.log("response res");
   console.log(res);
   return res;
}, error => {
    console.log("response error");
    console.log(error);
    if (error.response) {
        switch (error.response.status) {
            case 401:
                // 401 清除token信息并跳转到登录页面
                if (sessionStorage.getItem('access-user')){
                    alert("token 已经过期，请重新登录！");
                }else{
                    alert("用户名和密码不对，请重试！");    
                }
                
                console.log('401, clear token and user');
                sessionStorage.removeItem('token');  
                sessionStorage.removeItem('access-user');
                location.href = '/#/login';
        }
    }


    /*
    let errStr = error.toLocaleString();
    if (errStr.indexOf('401') >= 0){
      // 401 说明 token 验证失败
      // 可以直接跳转到登录页面，重新登录获取 token
      if (sessionStorage.getItem('access-user')){
         sessionStorage.removeItem('access-user');   
      }
      if (sessionStorage.getItem('token')){

         sessionStorage.removeItem('token');  
      }
      alert("用户名和密码不对，请重试！");
      location.href = '/login';
      //this.$router.push({ path: '/login' });
    } else {
       // do something
       return error;
    }
    */
    // 返回 response 里的错误信息
    //return Promise.reject(error.response.data);
    return Promise.reject(error);

});


//export const requestLogin = params => { return axios.post(`${base}/login`, qs.stringify(params)).then(res => res.data) }
export const requestLogin = params => { return axios.post(`${base}/login`, params) }

// ------ admin part

//axios.defaults.headers.common['Authorization'] = 'jwt ' + sessionStorage.getItem('token');
export const reqGetUserList = params => {  return axios.get(`${base}/user/list`, { params: params }) }

export const reqDeleteUser = params => { return axios.get(`${base}/user/delete`, { params: params }) }

export const reqBatchDeleteUser = params => { return axios.get(`${base}/user/batchdelete`, { params: params }) }

export const reqEditUser = params => { return axios.get(`${base}/user/edit`, { params: params }) }

export const reqAddUser = params => { return axios.get(`${base}/user/add`, { params: params }) }


//  ----- user part
export const reqaChangePwd = params => { return axios.get(`${base}/user/changepwd`, { params: params }) }

export const reqSaveUserProfile = params => { return axios.post(`${base}/user/profile`, params).then(res => res.data) }

export const reqGetDevidByUser = params => { return axios.get(`${base}/config/user/devid`, { params: params }) }

export const reqGetPumpCfg = params => { return axios.get(`${base}/config/devid/pump/query`, { params: params }) }

export const reqEditPumpCfg = params => { return axios.get(`${base}/config/devid/pump/edit`, { params: params }) }

export const reqGetWashCfg = params => { return axios.get(`${base}/config/devid/wash/query`, { params: params }) }

export const reqEditWashCfg = params => { return axios.get(`${base}/config/devid/wash/edit`, { params: params }) }

export const reqGetFormulaCfg = params => { return axios.get(`${base}/config/devid/formula/query`, { params: params }) }

export const reqEditFormulaCfg = params => { return axios.get(`${base}/config/devid/formula/edit`, { params: params }) }

export const reqGetDevidComms = params => { return axios.get(`${base}/config/devidcomms/query`, {params: params})}

export const reqEditDevidComms = params => { return axios.get(`${base}/config/devidcomms/edit`, {params: params})}

export const reqDeleteDevidComms = params => { return axios.get(`${base}/config/devidcomms/delete`, { params: params }) }

export const reqGetStats = params => { return axios.get(`${base}/data/query/date`, {params: params})}

export const reqDownloadStats = params => { return window.open(base + '/data/download/'+ params.filename + params.condition)}
