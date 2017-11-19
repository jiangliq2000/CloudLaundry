<template>
<div>
  <!-- 设备号/洗衣机号选择 -->
  <el-form ref="devform"  :model="devform" label-width="80px"> 
    <el-col :span="24" class="warp-breadcrum">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }"><b>首页</b></el-breadcrumb-item>
        <el-breadcrumb-item>配方管理</el-breadcrumb-item>
      </el-breadcrumb>
    </el-col>    
    <el-col :span="16">
      <el-form-item label="设备号">
        <el-cascader expand-trigger="hover" :options="options" v-model="devidWash" @change="handleChange">
        </el-cascader>
      </el-form-item>
    </el-col>   
    <el-col :span="15">
      <el-form-item label="配方号">
        <el-radio-group v-model="selecFormula" @change="formulaChanged" >
          <el-radio-button v-for="item in formulas" :label="item" ></el-radio-button>
        </el-radio-group>
      </el-form-item>
    </el-col>
  </el-form>
  <!--列表-->
  <el-table :data="formluaData" highlight-current-row v-loading="listLoading" stripe height="402" style="width: 100%;">
     <el-table-column prop="title" label="洗衣步骤" width="120" header-align="center" align="center">
     </el-table-column>
     <el-table-column prop="prio" label="优先级" width="80" header-align="center" align="center">
     </el-table-column>
     <el-table-column prop="p1" label="泵1" width="60" header-align="center" align="center">
     </el-table-column>
     <el-table-column prop="p2" label="泵2" width="60" header-align="center" align="center">
     </el-table-column>
     <el-table-column prop="p3" label="泵3" width="60" header-align="center" align="center">
     </el-table-column>
     <el-table-column prop="p4" label="泵4" width="60" header-align="center" align="center">
     </el-table-column>     
     <el-table-column prop="p5" label="泵5" width="60" header-align="center" align="center">
     </el-table-column>
     <el-table-column prop="p6" label="泵6" width="60" header-align="center" align="center">
     </el-table-column>
     <el-table-column prop="p7" label="泵7" width="60" header-align="center" align="center">
     </el-table-column>
     <el-table-column prop="p8" label="泵8" width="60" header-align="center" align="center">
     </el-table-column>            
     <el-table-column label="操作" width="80" header-align="center" align="center">
       <template scope="scope">
         <el-button size="small" @click="showEditDialog(scope.$index,scope.row)">编辑</el-button>
       </template>
     </el-table-column>
   </el-table>
  <el-dialog title="编辑" v-model="editFormVisible" :close-on-click-modal="false">
     <el-form :model="editForm" label-width="100px" ref="editForm">
       <el-form-item label="洗衣机" prop="washNo" >
         <el-input v-model="editForm.title" :disabled="true"></el-input>
       </el-form-item>
       <el-form-item label="优先级" prop="prio">
         <el-input v-model="editForm.prio" :disabled="editShowPrio" auto-complete="off"></el-input>
       </el-form-item>       
       <el-form-item label="泵1" prop="inClose">
         <el-input v-model="editForm.p1" auto-complete="off"></el-input>
       </el-form-item>      
       <el-form-item label="泵2" prop="outStart">
         <el-input v-model="editForm.p2" auto-complete="off"></el-input>
       </el-form-item>       
       <el-form-item label="泵3" prop="outClose">
         <el-input v-model="editForm.p3" auto-complete="off"></el-input>
       </el-form-item> 
       <el-form-item label="泵4" prop="inClose">
         <el-input v-model="editForm.p4" auto-complete="off"></el-input>
       </el-form-item>      
       <el-form-item label="泵5" prop="outStart">
         <el-input v-model="editForm.p5" auto-complete="off"></el-input>
       </el-form-item>       
       <el-form-item label="泵6" prop="outClose">
         <el-input v-model="editForm.p6" auto-complete="off"></el-input>
       </el-form-item>  
       <el-form-item label="泵7" prop="inClose">
         <el-input v-model="editForm.p7" auto-complete="off"></el-input>
       </el-form-item>      
       <el-form-item label="泵8" prop="outStart">
         <el-input v-model="editForm.p8" auto-complete="off"></el-input>
       </el-form-item>         
     </el-form>
     <div slot="footer" class="dialog-footer">
       <el-button @click.native="editFormVisible = false">取消</el-button>
       <el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
     </div>
  </el-dialog>
</div>
</template>
<script>
  import util from '../../common/util'
  import {reqGetFormulaCfg, reqEditFormulaCfg, reqGetDevidByUser} from '../../api/api';

  export default{
    data(){
      return {
        options: [ ],
        devidWash: [],
        washs: [{value:'1',label:'1号洗衣机'}, {value:'2',label:'2号洗衣机'}, {value:'3',label:'3号洗衣机'},{value:'4',label:'4号洗衣机'},
                {value:'5',label:'5号洗衣机'}, {value:'6',label:'6号洗衣机'}, {value:'7',label:'7号洗衣机'},{value:'8',label:'8号洗衣机'}
        ],        
        selecFormula: '',
        formulas:[' 配方1 ',' 配方2 ','配方3 ','配方4 ','配方5 ','配方6 ','配方7 ','配方8 ','配方9 ','配方10',
                  '配方11','配方12','配方13','配方14','配方15','配方16','配方17','配方18','配方19','配方20'],
        devform: {devId:''},
        formluaData: [ {title: "步骤1(延时)", prio: "", p1: "", p2: "", p3: "", p4: "" ,p5: "", p6: "", p7: "", p8: "" },
                       {title: "步骤1(剂量)", prio: "", p1: "", p2: "", p3: "", p4: "" ,p5: "", p6: "", p7: "", p8: "" },
                       {title: "步骤2(延时)", prio: "", p1: "", p2: "", p3: "", p4: "" ,p5: "", p6: "", p7: "", p8: "" },
                       {title: "步骤2(剂量)", prio: "", p1: "", p2: "", p3: "", p4: "" ,p5: "", p6: "", p7: "", p8: "" },
                       {title: "步骤3(延时)", prio: "", p1: "", p2: "", p3: "", p4: "" ,p5: "", p6: "", p7: "", p8: "" },
                       {title: "步骤3(剂量)", prio: "", p1: "", p2: "", p3: "", p4: "" ,p5: "", p6: "", p7: "", p8: "" },
                       {title: "步骤4(延时)", prio: "", p1: "", p2: "", p3: "", p4: "" ,p5: "", p6: "", p7: "", p8: "" },
                       {title: "步骤4(剂量)", prio: "", p1: "", p2: "", p3: "", p4: "" ,p5: "", p6: "", p7: "", p8: "" }
        ],
        //编辑相关数据
        editFormVisible: false,//编辑界面是否显示
        editLoading: false,
        editFormindex: 0,
        editShowPrio: false, // 是否让prio 可编辑
        editForm: { title: "", prio: "", p1: "", p2: "", p3: "", p4: "" , p5: "", p6: "", p7: "", p8: "" },
        listLoading: false
      }
    },
    methods: {
      handleChange(value) {
        this.selecFormula='';
        this.formluaData = [ {title: "步骤1(延时)", prio: "", p1: "", p2: "", p3: "", p4: "" ,p5: "", p6: "", p7: "", p8: "" },
                       {title: "步骤1(剂量)", prio: "", p1: "", p2: "", p3: "", p4: "" ,p5: "", p6: "", p7: "", p8: "" },
                       {title: "步骤2(延时)", prio: "", p1: "", p2: "", p3: "", p4: "" ,p5: "", p6: "", p7: "", p8: "" },
                       {title: "步骤2(剂量)", prio: "", p1: "", p2: "", p3: "", p4: "" ,p5: "", p6: "", p7: "", p8: "" },
                       {title: "步骤3(延时)", prio: "", p1: "", p2: "", p3: "", p4: "" ,p5: "", p6: "", p7: "", p8: "" },
                       {title: "步骤3(剂量)", prio: "", p1: "", p2: "", p3: "", p4: "" ,p5: "", p6: "", p7: "", p8: "" },
                       {title: "步骤4(延时)", prio: "", p1: "", p2: "", p3: "", p4: "" ,p5: "", p6: "", p7: "", p8: "" },
                       {title: "步骤4(剂量)", prio: "", p1: "", p2: "", p3: "", p4: "" ,p5: "", p6: "", p7: "", p8: "" }
        ];
      },
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
          var devids = res.data;
          let element = {value:'',label:'',children:this.washs};
          for (var i=0;i<devids.length; i++){
            element.value = devids[i];
            element.label = devids[i];
            let record = Object.assign({}, element);
            this.options.push(record);
          }
          this.listLoading = false;
        })        
      },
      getFormuCfg(devid,washid,formula){
          let para = {
            devId: devid,
            washid: washid,
            formula: formula
          };
          reqGetFormulaCfg(para).then((res) => {
            var fdata = res.data; 
            if (fdata.length === 0){
              this.$message({
              message: '获取当前设备号配方信息失败，请联系供货商',
              type: 'warning'
            });
            }else{
              for(var i=0;i<fdata.length; i++){
                this.formluaData[i].prio = fdata[i].prio;
                this.formluaData[i].p1 = fdata[i].p1;
                this.formluaData[i].p2 = fdata[i].p2;
                this.formluaData[i].p3 = fdata[i].p3;
                this.formluaData[i].p4 = fdata[i].p4;
                this.formluaData[i].p5 = fdata[i].p5;
                this.formluaData[i].p6 = fdata[i].p6;
                this.formluaData[i].p7 = fdata[i].p7;
                this.formluaData[i].p8 = fdata[i].p8;
              }              
              this.listLoading = false;
            }
          }).catch(() => {
            this.$message({
              message: '获取当前设备号配方信息失败，请检查网络',
              type: 'warning'
            });
            this.selecFormula='';
            this.formluaData = [ {title: "步骤1(延时)", prio: "", p1: "", p2: "", p3: "", p4: "" ,p5: "", p6: "", p7: "", p8: "" },
                       {title: "步骤1(剂量)", prio: "", p1: "", p2: "", p3: "", p4: "" ,p5: "", p6: "", p7: "", p8: "" },
                       {title: "步骤2(延时)", prio: "", p1: "", p2: "", p3: "", p4: "" ,p5: "", p6: "", p7: "", p8: "" },
                       {title: "步骤2(剂量)", prio: "", p1: "", p2: "", p3: "", p4: "" ,p5: "", p6: "", p7: "", p8: "" },
                       {title: "步骤3(延时)", prio: "", p1: "", p2: "", p3: "", p4: "" ,p5: "", p6: "", p7: "", p8: "" },
                       {title: "步骤3(剂量)", prio: "", p1: "", p2: "", p3: "", p4: "" ,p5: "", p6: "", p7: "", p8: "" },
                       {title: "步骤4(延时)", prio: "", p1: "", p2: "", p3: "", p4: "" ,p5: "", p6: "", p7: "", p8: "" },
                       {title: "步骤4(剂量)", prio: "", p1: "", p2: "", p3: "", p4: "" ,p5: "", p6: "", p7: "", p8: "" }
            ];
        });  
      },
      formulaChanged: function(){
        if (typeof(this.devidWash[0]) === "undefined"){
          this.$message({
                  message: '请先选择设备号/洗衣机号',
                  type: 'error'
                });
          this.selecFormula = '';
        } else {
          // according to this.selectFormula , change to the real value
          // map: '白毛巾' -> 1
          let formula = this.formulas.indexOf(this.selecFormula);
          let devid = this.devidWash[0];
          let washid = this.devidWash[1];
          this.getFormuCfg(devid,washid,formula);
        }
      },
      //显示编辑界面
      showEditDialog: function (index, row) {
        this.editFormVisible = true;
        this.editForm = Object.assign({}, row);
        this.editFormindex = index;
        if (index%2 === 0){
          this.editShowPrio = true;
        }
        else{
          this.editShowPrio = false;
        }
      },
      //编辑
      editSubmit: function () {
        this.$refs.editForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.editLoading = true;
              let editFormu = Object.assign({}, this.editForm);
              this.formluaData[this.editFormindex].prio = editFormu.prio;
              this.formluaData[this.editFormindex].p1 = editFormu.p1;
              this.formluaData[this.editFormindex].p2 = editFormu.p2;
              this.formluaData[this.editFormindex].p3 = editFormu.p3;
              this.formluaData[this.editFormindex].p4 = editFormu.p4;
              this.formluaData[this.editFormindex].p5 = editFormu.p5;
              this.formluaData[this.editFormindex].p6 = editFormu.p6;
              this.formluaData[this.editFormindex].p7 = editFormu.p7;
              this.formluaData[this.editFormindex].p8 = editFormu.p8;
              // need update data to mongodb
              let formula = this.formulas.indexOf(this.selecFormula);
              let stepindex = parseInt(this.editFormindex/2) + 1;
              let data = [];
              data.push(parseInt(editFormu.p1));
              data.push(parseInt(editFormu.p2));
              data.push(parseInt(editFormu.p3));
              data.push(parseInt(editFormu.p4));
              data.push(parseInt(editFormu.p5));
              data.push(parseInt(editFormu.p6));
              data.push(parseInt(editFormu.p7));
              data.push(parseInt(editFormu.p8));
              if (this.editFormindex%2 !== 0){
                // open time(s)
                data.push(parseInt(editFormu.prio));  
              }     
              let para = {
                devId: this.devidWash[0],
                washid: this.devidWash[1],
                formula: formula,
                stepindex: stepindex,
                stepdata: {data}
              };          
              reqEditFormulaCfg(para).then((res) => {
                this.editLoading = false;
                //NProgress.done();
                this.$message({
                  message: '编辑成功',
                  type: 'success'
                });
                this.$refs['editForm'].resetFields();
                this.editFormVisible = false;
                this.getFormuCfg(this.devidWash[0],this.devidWash[1],this.formulas.indexOf(this.selecFormula));
              }).catch(() => {
                  this.editLoading = false;
                  this.$message({
                      message: '编辑失败，请重新操作',
                      type: 'error'
                  });
                  this.$refs['editForm'].resetFields();
                  this.editFormVisible = false;
                  this.getFormuCfg(this.devidWash[0],this.devidWash[1],this.formulas.indexOf(this.selecFormula));
              });
            });
          }
        });
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
