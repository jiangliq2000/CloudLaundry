<template>
  <el-row class="warp">
    <el-col :span="24" class="warp-breadcrum">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }"><b>首页</b></el-breadcrumb-item>
        <el-breadcrumb-item>设置</el-breadcrumb-item>
        <el-breadcrumb-item>修改密码</el-breadcrumb-item>
      </el-breadcrumb>
    </el-col>

    <el-col :span="24" class="warp-main">
      <el-form ref="form" :model="form" label-width="120px">
        <el-form-item label="原密码">
          <el-input v-model="form.oldPwd"></el-input>
        </el-form-item>
        <el-form-item label="新密码">
          <el-input v-model="form.newPwd"></el-input>
        </el-form-item>
        <el-form-item label="确认新密码">
          <el-input v-model="form.confirmPwd"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="default" @click="onSubmit">提交</el-button>
        </el-form-item>
      </el-form>
    </el-col>
  </el-row>
</template>
<script>
  import { reqaChangePwd} from '../../api/api';     
  export default{

    data(){
      return {
        form: {
          oldPwd: '',
          newPwd: '',
          confirmPwd: ''
        }
      }
    },
    methods:{
      onSubmit() {
        //this.$message({message:"此功能暂时未开发",duration:1500});
        if (this.form.newPwd !== this.form.confirmPwd) {
           this.$message({message: '两次输入的新密码不一致，请重新输入', type: 'error'});
        }
        else{
          let userInfo = sessionStorage.getItem('access-user');

          if (userInfo) {
             userInfo = JSON.parse(userInfo);
          }
          let para = {
            username: userInfo,
            oldpwd: this.form.oldPwd,
            newpwd: this.form.newPwd
          }
  
          reqaChangePwd(para).then((res) => {

            console.log("update pasword");

            this.$message({message: res.data.msg, type: 'success'});
  
          }).catch(() => {
           
            console.log("update failed")

            this.$message({message: '更新失败', type: 'error'});
        });
      }
    }
   }
  }
</script>
