<template>
  <el-row class="warp">
    <el-col :span="24" class="warp-breadcrum">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }"><b>首页</b></el-breadcrumb-item>
        <el-breadcrumb-item>用户管理</el-breadcrumb-item>
      </el-breadcrumb>
    </el-col>

    <el-col :span="24" class="warp-main">
      <!--工具条-->
      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
        <el-form :inline="true" :model="filters">
          <el-form-item>
            <el-input v-model="filters.username" placeholder="用户名"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" v-on:click="getUsers">查询</el-button>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="showAddDialog">新增</el-button>
          </el-form-item>
        </el-form>
      </el-col>

      <!--列表-->
      <el-table :data="users" highlight-current-row v-loading="listLoading" @selection-change="selsChange"
                style="width: 100%;">
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column type="index" width="60"></el-table-column>
        <el-table-column prop="username" label="用户名" width="130" sortable></el-table-column>
        <el-table-column prop="devId" label="设备号" width="150" sortable></el-table-column>
        <el-table-column prop="password" label="密码" width="100" sortable></el-table-column>
        <el-table-column prop="name" label="姓名" width="100" sortable></el-table-column>
        <el-table-column prop="privilege" label="操作权限" width="120" sortable></el-table-column>
        <el-table-column prop="contact" label="联系方式" width="120" sortable></el-table-column>
        <el-table-column prop="register" label="注册日期" width="120" sortable></el-table-column>
        <el-table-column label="操作" width="150">
          <template scope="scope">
            <el-button size="small" @click="showEditDialog(scope.$index,scope.row)">编辑</el-button>
            <el-button type="danger" @click="delUser(scope.$index,scope.row)" size="small">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!--工具条-->
      <!--
      <el-col :span="24" class="toolbar">
        <el-button type="danger" @click="batchDeleteUser" :disabled="this.sels.length===0">批量删除</el-button>
        <el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="10" :total="total"
                       style="float:right;">
        </el-pagination>
      </el-col>
      -->
      
      <el-dialog title="编辑" v-model="editFormVisible" :close-on-click-modal="false">
        <el-form :model="editForm" label-width="100px" :rules="editFormRules" ref="editForm">
          <el-form-item label="用户名" prop="username" >
            <el-input v-model="editForm.username" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="设备号" prop="devId">
            <el-input v-model="editForm.devId" auto-complete="off"></el-input>
          </el-form-item>          
          <!--
          <el-form-item label="设备号" prop="devId">
            <el-input type="textarea" v-model="editForm.devId" :rows="2"></el-input>
          </el-form-item>          
          -->
          <el-form-item label="密码" prop="password">
            <el-input v-model="editForm.password" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="操作权限" prop="privilege">
            <el-input-number v-model="editForm.privilege" :min="0" :max="2"></el-input-number>
          </el-form-item>

        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="editFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
        </div>
      </el-dialog>

      <!--新增界面-->
      <el-dialog title="新增" v-model="addFormVisible" :close-on-click-modal="false">
        <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
          <el-form-item label="用户名" prop="username" >
            <el-input v-model="addForm.username" @blur="checkUsername" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="设备号" prop="devId">
            <el-input v-model="addForm.devId" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="addForm.password" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="操作权限" prop="privilege">
            <el-input-number v-model="addForm.privilege" :min="0" :max="2"></el-input-number>
          </el-form-item>          
          <el-form-item label="姓名" prop="name">
            <el-input v-model="addForm.name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="联系方式" prop="contact">
            <el-input type="textarea" v-model="addForm.contact" :rows="2"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="addCancel">取消</el-button>
          <el-button type="primary" @click.native="addSubmit" :loading="addLoading">提交</el-button>
        </div>
      </el-dialog>

    </el-col>
  </el-row>
</template>
<script>
  import util from '../../common/util'
  import {reqGetUserList, reqDeleteUser, reqBatchDeleteUser, reqEditUser, reqAddUser} from '../../api/api';

  export default{
    data(){
      /*
      var validateUser = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入用户名'));
        } else if (value === this.existUser) {
          callback(new Error('该用户名已经存在!'));
        } else {
          callback();
        }
      };
      */
      return {
        filters: {
          username: ''
        },
        existUser: '',
        showExist: '',
        users: [],
        total: 0,
        page: 1,
        listLoading: false,
        sels: [], //列表选中列

        //编辑相关数据
        editFormVisible: false,//编辑界面是否显示
        editLoading: false,
        editFormRules: {
          devId: [
            {required: true, message: '请输入设备号', trigger: 'blur'}
          ],
          password: [
            {required: true, message: '请输入密码', trigger: 'blur'}
          ]
        },
        editForm: {
          id: 0,
          username: '',
          devId: '',
          password: '',
          privilege: 2,
          contact: ''
        },

        //新增相关数据
        addFormVisible: false,//新增界面是否显示
        addLoading: false,
        addFormRules: {
          username: [
            {required: true, message: '请输入用户名', trigger: 'blur'},
            //{validator: validateUser, trigger: 'blur'}
          ],
          devId: [
            {required: true, message: '请输入设备号', trigger: 'blur'}
          ],
          password: [
            {required: true, message: '请输入密码', trigger: 'blur'}
          ],
        },
        addForm: {
          username: '',
          devId: '',
          password: '',
          privilege: 2,
          name: '',          
          contact: '',
          register: ''
        }
      }
    },
    methods: {
      checkUsername(){
        let para = {
          username: this.addForm.username
        };

        console.log('>. check if username already exist ');
        console.log(para)

        reqGetUserList(para).then((res) => {
          console.log("res data is");
          console.log(res.data);
                   
          let totals = res.data.totals;
          if (totals !==0 &&  this.addForm.username){
            this.$message({
                  message: '用户已经存在， 请重新输入',
                  type: 'error'
                });
          }
          console.log("exist User is ");
          console.log(this.existUser);
          
        })
      },
      handleCurrentChange(val) {
        this.page = val;
        this.getUsers();
      },
      //获取用户列表
      getUsers() {
        let para = {
          //page: this.page,
          username: this.filters.username
        };

        this.listLoading = true;
        reqGetUserList(para).then((res) => {
                   
          this.total = res.data.total;
          this.users = res.data.Users;
          this.listLoading = false;

        })
      },
      selsChange: function (sels) {
        this.sels = sels;
      },
      //删除
      delUser: function (index, row) {
        this.$confirm('确认删除该记录吗?', '提示', {type: 'warning'}).then(() => {
          this.listLoading = true;
          let para = {username: row.username};
          reqDeleteUser(para).then((res) => {
            this.listLoading = false;
            this.$message({message: '删除成功', type: 'success'});
            this.getUsers();
          }).catch(() => {
                this.listLoading = false;
                console.log("dele failed")
                this.$message({ message: '删除失败',  type: 'error'});
          });
        }).catch(() => {
        });
      },
      //显示编辑界面
      showEditDialog: function (index, row) {
        console.log(">. showEditDialog index:" + index + "  row:" +row)
        this.editFormVisible = true;
        this.editForm = Object.assign({}, row);
      },
      //编辑
      editSubmit: function () {
        this.$refs.editForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.editLoading = true;
              //NProgress.start();
              let para = Object.assign({}, this.editForm);
              //para.publishAt = (!para.publishAt || para.publishAt == '') ? '' : util.formatDate.format(new Date(para.publishAt), 'yyyy-MM-dd');
              reqEditUser(para).then((res) => {
                this.editLoading = false;
                //NProgress.done();
                this.$message({
                  message: '提交成功',
                  type: 'success'
                });
                this.$refs['editForm'].resetFields();
                this.editFormVisible = false;
                this.getUsers();
              }).catch(() => {
                this.editLoading = false;
                console.log("update failed")
                this.$message({
                  message: '更新失败',
                  type: 'error'
                });
              });
            });
          }
        });
      },
      showAddDialog: function () {
        this.addFormVisible = true;
        this.addForm = {
          username: '',
          devId: '',
          password: '',
          privilege: '',
          name: '',
          contact: '',
          register: ''
        };
      },
      //新增
      addSubmit: function () {
        this.$refs.addForm.validate((valid) => {
          if (valid) {
            this.addLoading = true;
            //NProgress.start();
            let para = Object.assign({}, this.addForm);
            para.register = new Date().toLocaleDateString()
           
            reqAddUser(para).then((res) => {
              this.addLoading = false;

              this.$message({ message: '提交成功', type: 'success' });
              this.$refs['addForm'].resetFields();
              this.addFormVisible = false;
              this.getUsers();
            }).catch(() => {
              this.addLoading = false;
              console.log("save failed")
              this.$message({
                message: '提交失败',
                type: 'error'
              });
              this.$refs['addForm'].resetFields();
              this.addFormVisible = false;
              this.getUsers();              

            });
          }
        });
      },
      addCancel: function() {
          this.$refs['addForm'].resetFields();
          this.addFormVisible = false;

      },
      //批量删除
      batchDeleteUser: function () {
        var ids = this.sels.map(item => item.id).toString();
        console.log("select user is ");
        console.log(ids);
        this.$confirm('确认删除选中记录吗？', '提示', {
          type: 'warning'
        }).then(() => {
          this.listLoading = true;
          let para = {ids: ids};
          reqBatchDeleteUser(para).then((res) => {
            this.listLoading = false;
            this.$message({
              message: '删除成功',
              type: 'success'
            });
            this.getUsers();
          });
        }).catch(() => {

        });
      }
    },
    mounted() {
      this.getUsers();
    }
  }
</script>

<style>
  .demo-table-expand label {
    font-weight: bold;
  }
</style>
