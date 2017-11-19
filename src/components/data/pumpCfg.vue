<template>
<el-form ref="form" :model="form" label-width="80px">
  <el-col :span="24" class="warp-breadcrum">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }"><b>首页</b></el-breadcrumb-item>
        <el-breadcrumb-item>泵阀管理</el-breadcrumb-item>
      </el-breadcrumb>
  </el-col>
  <el-row :gutter="20">
  <el-col :span="6">
  <el-form-item label="设备号">
    <el-select v-model="form.devId" placeholder="请选择设备号" @change="devidChanged" >
      <el-option v-for="item in devids" :label="item" :value="item" ></el-option>
    </el-select>
  </el-form-item>
  </el-col>
  </el-row>
  <el-col :span="24" class="warp-breadcrum">
      <P><strong>加料配型</strong></P>
      <!--列表-->
      <el-table :data="pumpData" v-loading="listLoading" style="width: 100%;">
        <el-table-column prop="p1" label="泵1" width="80" header-align="center" align="center"></el-table-column>
        <el-table-column prop="p2" label="泵2" width="80" header-align="center" align="center"></el-table-column>
        <el-table-column prop="p3" label="泵3" width="80" header-align="center" align="center"></el-table-column>
        <el-table-column prop="p4" label="泵4" width="80" header-align="center" align="center"></el-table-column>
        <el-table-column prop="p5" label="泵5" width="80" header-align="center" align="center"></el-table-column>
        <el-table-column prop="p6" label="泵6" width="80" header-align="center" align="center"></el-table-column>
        <el-table-column prop="p7" label="泵7" width="80" header-align="center" align="center"></el-table-column>
        <el-table-column prop="p8" label="泵8" width="80" header-align="center" align="center"></el-table-column>
        <el-table-column label="操作" width="100" header-align="center" align="center">
          <template scope="scope">
            <el-button size="small" @click="showPumpEditDialog(scope.$index,scope.row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
  </el-col> 
      <el-dialog title="编辑" v-model="editPumpFormVisible" :close-on-click-modal="false">
        <el-form :model="editPumpForm" label-width="100px" ref="editPumpForm">
          <el-form-item label="泵1" prop="p1" >
            <el-select v-model="editPumpForm.p1" placeholder="加料类型">
              <el-option v-for="item in arrPumpCfg" :value="item" ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="泵2" prop="p2">
            <el-select v-model="editPumpForm.p2" placeholder="加料类型">
              <el-option v-for="item in arrPumpCfg"  :value="item" ></el-option>
            </el-select>
          </el-form-item>   
          <el-form-item label="泵3" prop="p3">
            <el-select v-model="editPumpForm.p3" placeholder="加料类型">
              <el-option v-for="item in arrPumpCfg" :value="item" ></el-option>
            </el-select>
          </el-form-item>      
          <el-form-item label="泵4" prop="p4">
            <el-select v-model="editPumpForm.p4" placeholder="加料类型">
              <el-option v-for="item in arrPumpCfg" :value="item" ></el-option>
            </el-select>
          </el-form-item>       
          <el-form-item label="泵5" prop="p5">
            <el-select v-model="editPumpForm.p5" placeholder="加料类型">
              <el-option v-for="item in arrPumpCfg"  :value="item" ></el-option>
            </el-select>
          </el-form-item>   
          <el-form-item label="泵6" prop="p6">
            <el-select v-model="editPumpForm.p6" placeholder="加料类型">
              <el-option v-for="item in arrPumpCfg" :value="item" ></el-option>
            </el-select>
          </el-form-item>   
          <el-form-item label="泵7" prop="p7">
            <el-select v-model="editPumpForm.p7" placeholder="加料类型">
              <el-option v-for="item in arrPumpCfg" :value="item" ></el-option>
            </el-select>
          </el-form-item>   
          <el-form-item label="泵8" prop="p8">
            <el-select v-model="editPumpForm.p8" placeholder="加料类型">
              <el-option v-for="item in arrPumpCfg" :value="item" ></el-option>
            </el-select>
          </el-form-item>   
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="editPumpFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="editPumpSubmit" :loading="editPumpLoading">提交</el-button>
        </div>
      </el-dialog>

    <el-col :span="24" class="warp-breadcrum">
      <P><strong>阀门配置</strong></P>
      <!--列表-->
      <el-table :data="washData" highlight-current-row v-loading="listLoading" height="402" style="width: 100%;">
        <caption>阀门配置</caption>
        <el-table-column prop="washNo" label="洗衣机" width="120"></el-table-column>
        <el-table-column label="进水阀" header-align="center">
          <el-table-column prop="inopen" label="开启延时(S)" width="120" header-align="center" align="center">
          </el-table-column>
          <el-table-column prop="inclose" label="关闭延时(S)" width="120" header-align="center" align="center">
          </el-table-column>
        </el-table-column>
        <el-table-column label="出水阀" header-align="center">
          <el-table-column prop="outopen" label="开启延时(S)" width="120" header-align="center" align="center">
          </el-table-column>
          <el-table-column prop="outclose" label="关闭延时(S)" width="120" header-align="center" align="center">
          </el-table-column>        
        </el-table-column>
        <el-table-column label="操作" width="150" header-align="center" align="center">
          <template scope="scope">
            <el-button size="small" @click="showEditDialog(scope.$index,scope.row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-col>

    <el-dialog title="编辑" v-model="editFormVisible" :close-on-click-modal="false">
        <el-form :model="editForm" label-width="100px" ref="editForm">
          <el-form-item label="洗衣机" prop="washNo" >
            <el-input v-model="editForm.washNo" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="进水开启延时" prop="inopen">
            <el-input v-model="editForm.inopen" auto-complete="off"></el-input>
          </el-form-item>       
          <el-form-item label="进水关闭延时" prop="inclose">
            <el-input v-model="editForm.inclose" auto-complete="off"></el-input>
          </el-form-item>      
          <el-form-item label="出水开启延时" prop="outopen">
            <el-input v-model="editForm.outopen" auto-complete="off"></el-input>
          </el-form-item>       
          <el-form-item label="出水关闭延时" prop="outclose">
            <el-input v-model="editForm.outclose" auto-complete="off"></el-input>
          </el-form-item>      
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="editFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
        </div>
    </el-dialog>
</el-form>

</template>
<script>
  import util from '../../common/util'
  import {reqGetPumpCfg, reqEditPumpCfg, reqGetWashCfg, reqEditWashCfg, reqGetDevidByUser} from '../../api/api';

  export default{
    data(){
      return {
        devids: '',
        arrPumpCfg: ['碱液', '助剂','氧漂','氯漂','柔软剂','酸剂','水处理','乳化剂'],
        form: { devId: '', date1: '', date2: '',delivery: false, type: [], resource: '', unwater: true, desc: ''},
        pumpData: [{p1:'',p2:'',p3:'',p4:'',p5:'',p6:'',p7:'',p8:''}],
        washData: [{washNo: "1号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "2号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "3号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "4号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "5号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "6号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "7号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "8号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""}
        ],
        //编辑pump相关数据
        editPumpFormVisible: false,//编辑界面是否显示
        editPumpLoading: false,
        editPumpFormindex: 0,
        editPumpForm: {p1: '', p2: '', p3: '', p4: '', p5: '', p6: '', p7: '', p8: '' },
        //编辑相关数据
        editFormVisible: false,//编辑界面是否显示
        editLoading: false,
        editFormindex: 0,
        editForm: { washNo: '', inopen: '', inclose: '',  outopen: '', outclose: '' },
        listLoading: false
      }
    },
    methods: {
      //获取当期用户设备号
      getDevidByUser() {
        var userInfo = sessionStorage.getItem('access-user');
        if (userInfo) {
          userInfo = JSON.parse(userInfo);
        }
        let para = {
          user: userInfo
        };
        reqGetDevidByUser(para).then((res) => {
          this.devids = res.data;
          this.listLoading = false;
        })        
      },
      // dev change event
      devidChanged: function(){
        this.getPumpCfg();
        this.getWashCfg();
      },
      //获取当前设备泵配置信息
      getPumpCfg() {
        let para = {
          //page: this.page,
          devId: this.form.devId          
        };
        this.listLoading = true;
        // get pump cfg
        reqGetPumpCfg(para).then((res) => {
          let pumpcfg = res.data;
          this.pumpData[0].p1 = this.arrPumpCfg[pumpcfg[0]];
          this.pumpData[0].p2 = this.arrPumpCfg[pumpcfg[1]];
          this.pumpData[0].p3 = this.arrPumpCfg[pumpcfg[2]];
          this.pumpData[0].p4 = this.arrPumpCfg[pumpcfg[3]];
          this.pumpData[0].p5 = this.arrPumpCfg[pumpcfg[4]];
          this.pumpData[0].p6 = this.arrPumpCfg[pumpcfg[5]];
          this.pumpData[0].p7 = this.arrPumpCfg[pumpcfg[6]];
          this.pumpData[0].p8 = this.arrPumpCfg[pumpcfg[7]];
        }).catch(() => {
            this.$message({
              message: '获取当前设备号泵类型信息失败，请联系供货商',
              type: 'warning'
            });
            this.pumpData = [{p1:'',p2:'',p3:'',p4:'',p5:'',p6:'',p7:'',p8:''}];
        });
        this.listLoading = false;
      },
      //获取当前设备wash配置信息
      getWashCfg() {
        let para = {
          //page: this.page,
          devId: this.form.devId          
        };
        this.listLoading = true;
        //need add get wash cfg
        reqGetWashCfg(para).then((res) => {
          let washcfg = res.data;
          for(var i=0; i<this.washData.length; i++ ){
            this.washData[i].inopen = washcfg[i].ins;
            this.washData[i].inclose = washcfg[i].inc;
            this.washData[i].outopen = washcfg[i].outs;
            this.washData[i].outclose = washcfg[i].outc;
          }
        }).catch(() => {
            this.$message({
              message: '获取当前设备号洗衣机信息失败，请联系供货商',
              type: 'warning'
            });
            this.washData=[
                   {washNo: "1号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "2号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "3号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "4号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "5号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "6号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "7号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "8号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""}
            ];
        });
        this.listLoading = false;
      },
      //显示编辑界面
      showPumpEditDialog: function (index, row) {
        this.editPumpFormVisible = true;
        this.editPumpForm = Object.assign({}, row);
        this.editPumpFormindex = index;
      },
      //编辑 pump
      editPumpSubmit: function () {
        this.$refs.editPumpForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.editPumpLoading = true;
              let editpump = Object.assign({}, this.editPumpForm);
              this.pumpData[this.editPumpFormindex].p1 = editpump.p1;
              this.pumpData[this.editPumpFormindex].p2 = editpump.p2;
              this.pumpData[this.editPumpFormindex].p3 = editpump.p3;
              this.pumpData[this.editPumpFormindex].p4 = editpump.p4;
              this.pumpData[this.editPumpFormindex].p5 = editpump.p5;
              this.pumpData[this.editPumpFormindex].p6 = editpump.p6;
              this.pumpData[this.editPumpFormindex].p7 = editpump.p7;
              this.pumpData[this.editPumpFormindex].p8 = editpump.p8;
              // here, need update this data to mongodb            
              let pumps = {};
              pumps['pump1'] = this.arrPumpCfg.indexOf(editpump.p1);
              pumps['pump2'] = this.arrPumpCfg.indexOf(editpump.p2);
              pumps['pump3'] = this.arrPumpCfg.indexOf(editpump.p3);
              pumps['pump4'] = this.arrPumpCfg.indexOf(editpump.p4);
              pumps['pump5'] = this.arrPumpCfg.indexOf(editpump.p5);
              pumps['pump6'] = this.arrPumpCfg.indexOf(editpump.p6);
              pumps['pump7'] = this.arrPumpCfg.indexOf(editpump.p7);
              pumps['pump8'] = this.arrPumpCfg.indexOf(editpump.p8);

              let para = {
                devId: this.form.devId,
                pumps: {pumps}
              };
              reqEditPumpCfg(para).then((res) => {
                this.editPumpLoading = false;
                this.$message({
                  message: '提交成功',
                  type: 'success'
                });
                this.$refs['editPumpForm'].resetFields();
                this.editPumpFormVisible = false;
                this.getPumpCfg();
              }).catch(() => {
                  this.editPumpLoading = false;
                  this.$message({
                      message: '编辑失败，请重新操作',
                      type: 'error'
                  });
                  this.$refs['editPumpForm'].resetFields();
                  this.editPumpFormVisible = false;
                  this.getPumpCfg();
              });

            });
          }
        });
      },

      //显示编辑界面
      showEditDialog: function (index, row) {
        this.editFormVisible = true;
        this.editForm = Object.assign({}, row);
        this.editFormindex = index;
      },
      //编辑 wash
      editSubmit: function () {
        this.$refs.editForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.editLoading = true;
              let editWash = Object.assign({}, this.editForm);
              this.washData[this.editFormindex].inopen = editWash.inopen;
              this.washData[this.editFormindex].inclose = editWash.inclose;
              this.washData[this.editFormindex].outopen = editWash.outopen;
              this.washData[this.editFormindex].outclose = editWash.outclose;
              // here, need update this data to mongodb
              let wash = {};
              let washIndex = this.editFormindex + 1;
              wash['inopen'] = parseInt(editWash.inopen);
              wash['inclose'] = parseInt(editWash.inclose);
              wash['outopen'] = parseInt(editWash.outopen);
              wash['outclose'] = parseInt(editWash.outclose);
              let para = {
                devId: this.form.devId,
                washIndex: washIndex,
                wash: {wash}
              };
              reqEditWashCfg(para).then((res) => {
                this.editLoading = false;
                this.$message({
                  message: '提交成功',
                  type: 'success'
                });
              this.$refs['editForm'].resetFields();
              this.editFormVisible = false;
                this.getWashCfg();
              }).catch(() => {
                  this.editLoading = false;
                  this.$message({
                      message: '编辑洗衣机阀门配置失败，请重新操作',
                      type: 'error'
                  });
                  this.$refs['editForm'].resetFields();
                   this.editFormVisible = false;
                  this.getWashCfg();
              });
              this.editLoading = false;
                this.$message({
                  message: '提交成功',
                  type: 'success'
                });
              this.$refs['editForm'].resetFields();
              this.editFormVisible = false;
            });
          }
        });
      },
      onSubmit() {
        console.log('submit!');
      },
      handleClick(tab, event) {
        console.log(tab, event);
      }
    },
    mounted() {
      this.getDevidByUser();
    }
  }

</script>
<style>
  .demo-table-expand label {
    font-weight: bold;
  }
</style>
