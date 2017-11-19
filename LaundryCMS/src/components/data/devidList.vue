<template>
  <el-row class="warp">
    <el-col :span="24" class="warp-breadcrum">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }"><b>首页</b></el-breadcrumb-item>
        <el-breadcrumb-item>设备列表</el-breadcrumb-item>
      </el-breadcrumb>
    </el-col>

    <el-col :span="24" class="warp-main">
        <!--工具条-->
        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
          <el-form :inline="true" :model="filters">
            <el-form-item>
              <el-input v-model="filters.devId" placeholder="设备号" style="min-width: 240px;"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="getDevid">查询</el-button>
            </el-form-item>
          </el-form>
        </el-col>

      <!--列表-->
      <el-table :data="devids" highlight-current-row v-loading="loading" style="width: 100%;">
        <el-table-column type="index" width="60">
        </el-table-column>
        <el-table-column prop="devId" label="设备号" width="120" sortable>
        </el-table-column>
        <el-table-column prop="password" label="密码" width="120" sortable>
        </el-table-column>
        <el-table-column prop="position" label="位置" width="150" sortable>
        </el-table-column>        
        <el-table-column prop="comment" label="备注" v-if="adminDisplay" sortable>
        </el-table-column> 
        <el-table-column prop="expiry" label="有效期" v-if="adminDisplay" sortable>
        </el-table-column>         
        <el-table-column prop="comment2" label="备注2" sortable>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template scope="scope">
            <el-button size="small" @click="showEditDialog(scope.$index,scope.row)">编辑</el-button>
            <el-button type="danger" @click="delDevid(scope.$index,scope.row)" size="small" v-if="adminDisplay" >删除</el-button>
          </template>
        </el-table-column>        
      </el-table>

      <el-dialog title="编辑" v-model="editFormVisible" :close-on-click-modal="false">
        <el-form :model="editForm" label-width="100px"  ref="editForm">
          <el-form-item label="设备号" prop="devId" >
            <el-input v-model="editForm.devId" auto-complete="off" :disabled="true"></el-input>
          </el-form-item>       
          <el-form-item label="密码" prop="password">
            <el-input v-model="editForm.password" auto-complete="off"></el-input>
          </el-form-item>   
          <el-form-item label="位置" prop="position">
            <el-input v-model="editForm.position" auto-complete="off" :disabled="true"></el-input>
          </el-form-item>             
          <el-form-item label="备注" prop="comment" v-if="adminDisplay" >
            <el-input v-model="editForm.comment" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="有效期" prop="expiry" v-if="adminDisplay" >
            <el-input v-model="editForm.expiry" auto-complete="off"></el-input>
          </el-form-item>          
          <el-form-item label="备注2" prop="comment2">
            <el-input v-model="editForm.comment2" auto-complete="off"></el-input>
          </el-form-item>

        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="editFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
        </div>
      </el-dialog>

    </el-col>
  </el-row>
</template>

<script>
  import { reqGetDevidComms,reqEditDevidComms,reqDeleteDevidComms } from '../../api/api';

  export default {
    data() {
      return {
        filters: {devId: ''},
        loading: false,
        adminDisplay: false,
        devids: [],
        total: 0,
        page: 1,
        listLoading: false,
        sels: [], //列表选中列

        //编辑相关数据
        editFormVisible: false,//编辑界面是否显示
        editLoading: false,
        editForm: {
          id: 0,
          devId: '',
          password: '',
          position: '',
          comment: '',
          expiry: '',
          comment2: ''
        },
      }
    },
    methods: {
      handleCurrentChange(val) {
        this.page = val;
        this.getDevid();
      },
      //获取当期用户设备号
      getDevid() {
        var userInfo = sessionStorage.getItem('access-user');


        if (userInfo) {
          userInfo = JSON.parse(userInfo);
          if (userInfo == 'test') {
            this.adminDisplay = true
          }
        }

        let para = {
          page: this.page,
          devId: this.filters.devId,
          username: userInfo
        };
        
        reqGetDevidComms(para).then((res) => {
          console.log("devid list GetDevidByUser: ")
          console.log(res.data)
          this.devids = res.data;
          let devs = res.data;
          //console.log(this.devids);
          console.log("output devs");
          console.log(devs);
          //this.books = res.data.books;
          this.listLoading = false;
          //NProgress.done();
        })        
      },
      selsChange: function (sels) {
        this.sels = sels;
      },
      //显示编辑界面
      showEditDialog: function (index, row) {
        console.log(">. showEditDialog index:" + index + "  row:" +row)
        this.editFormVisible = true;
        this.editForm = Object.assign({}, row);
      },
      //删除
      delDevid: function (index, row) {
        this.$confirm('确认删除该记录吗?', '提示', {type: 'warning'}).then(() => {
          this.listLoading = true;
          let para = {devId: row.devId};
          reqDeleteDevidComms(para).then((res) => {
            this.listLoading = false;
            this.$message({message: '删除成功', type: 'success'});
            this.getDevid();
          }).catch(() => {
                this.listLoading = false;
                console.log("dele failed")
                this.$message({ message: '删除失败',  type: 'error'});
          });
        }).catch(() => {
        });
      },      
      //编辑
      editSubmit: function () {
        this.$refs.editForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.editLoading = true;
              //NProgress.start();
              let para = Object.assign({}, this.editForm);
              console.log("para is");
              console.log(para);

              reqEditDevidComms(para).then((res) => {
                this.editLoading = false;
                //NProgress.done();
                this.$message({
                  message: '提交成功',
                  type: 'success'
                });
                this.$refs['editForm'].resetFields();
                this.editFormVisible = false;
                this.getDevid();
              }).catch(() => {
              this.editLoading = false;
              console.log("save failed")
              this.$message({
                message: '提交失败',
                type: 'error'
              });

            });
            });
          }
        });
      }
    },
    mounted() {
      this.getDevid();
    }
  }
</script>

<style scoped>

</style>
