<template>
  <el-row class="warp">
    <el-col :span="24" class="warp-breadcrum">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }"><b>首页</b></el-breadcrumb-item>
        <el-breadcrumb-item>数据查询</el-breadcrumb-item>
        <el-breadcrumb-item>日期查询</el-breadcrumb-item>
      </el-breadcrumb>
    </el-col>
 
    <el-col :span="24" class="warp-main">
      <!--工具条-->
      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
        <el-form :inline="true" :model="form" >
          <el-form-item label="起始时间">
            <el-date-picker type="date" placeholder="选择日期" v-model="form.starttime" @change="sdateChanged" :picker-options="pickerOptions0" ></el-date-picker>
          </el-form-item>          
          <el-form-item label="结束时间">
            <el-date-picker type="date" placeholder="选择日期" v-model="form.endtime" @change="edateChanged" :picker-options="pickerOptions0" ></el-date-picker>
          </el-form-item>       
          <el-form-item>
            <el-button type="primary" v-on:click="getStats" icon="search">查询</el-button>
          </el-form-item>
        </el-form>
      </el-col>
    
    <el-alert  title="该时间段内未查询到任何数据"  type="warning" v-if="nodatashow">
    </el-alert>

    <!-- 每台设备统计 -->
    <el-card class="box-card" v-for="stats in statsObj">
      <div slot="header" class="clearfix">
        <span style="line-height: 36px;">设备号：{{stats.devId}}   </span>
        <el-button  type="primary" @click="downloads(stats.devId)">下载明细</el-button>
        <span style="line-height: 36px;"> 位置: {{stats.position}}   </span>
         <span style="line-height: 36px;">备注：{{stats.comment2}}  </span>
      </div>    
      <!--车数统计-->
      <el-table :data="stats.wash" style="width: 100%" >
        <el-table-column prop="wash0" label="总车数" width="80" header-align="center" align="center">
        </el-table-column>      
      </el-table>
      <el-table :data="stats.wash" style="width: 100%" >
        <el-table-column prop="wash1" label="1号车数" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="wash2" label="2号车数" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="wash3" label="3号车数" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="wash4" label="4号车数" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="wash5" label="5号车数" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="wash6" label="6号车数" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="wash7" label="7号车数" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="wash8" label="8号车数" width="80" header-align="center" align="center">
        </el-table-column>     
      </el-table>
      <!--药剂统计-->
      <el-table :data="stats.drug" style="width: 100%" >
        <el-table-column prop="drug1" label="药剂1" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="drug2" label="药剂2" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="drug3" label="药剂3" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="drug4" label="药剂4" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="drug5" label="药剂5" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="drug6" label="药剂6" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="drug7" label="药剂7" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="drug8" label="药剂8" width="80" header-align="center" align="center">
        </el-table-column>
      </el-table>
      <!--配方统计-->
      <el-table :data="stats.formula" style="width: 100%" >
        <el-table-column prop="fm1" label="配方1" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm2" label="配方2" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm3" label="配方3" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm4" label="配方4" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm5" label="配方5" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm6" label="配方6" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm7" label="配方7" width="80" header-align="center" align="center">
        </el-table-column>
      </el-table>
      <el-table :data="stats.formula" style="width: 100%" >
        <el-table-column prop="fm8" label="配方8" width="80" header-align="center" align="center">
        </el-table-column>      
        <el-table-column prop="fm9" label="配方9" width="80" header-align="center" align="center">
        </el-table-column>     
        <el-table-column prop="fm10" label="配方10" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm11" label="配方11" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm12" label="配方12" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm13" label="配方13" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm14" label="配方14" width="80" header-align="center" align="center">
        </el-table-column>
      </el-table>
      <el-table :data="stats.formula" style="width: 100%" >
        <el-table-column prop="fm15" label="配方15" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm16" label="配方16" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm17" label="配方17" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm18" label="配方18" width="80" header-align="center" align="center">
        </el-table-column>   
        <el-table-column prop="fm19" label="配方19" width="80" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm20" label="配方20" width="80" header-align="center" align="center">
        </el-table-column>
      </el-table>

    </el-card>
    </el-col>
  </el-row>
</template>
<script>
  import util from '../../common/util'
  import {reqGetStats, reqDownloadStats } from '../../api/api';


  export default{
    data(){
      return {
        form: {
          starttime: "",
          endtime: ""
        },
        pickerOptions0: {
          disabledDate(time) {
            return (time.getTime() > Date.now());
          }
        },
        statsObj: {},
        listLoading: false,
        nodatashow: false,
        showDownLoad: false
      }
    },
    methods: {
      //获取统计数据
      getStats() {
        this.nodatashow = false;
        console.log(">. dateQuery getStatas")
        var userInfo = sessionStorage.getItem('access-user')
        console.log("username is: " + userInfo)

        if (userInfo) {
          var username = JSON.parse(userInfo);
        }

        let st = this.form.starttime;
        let et = this.form.endtime;
        let stdt = new Date(st.replace("-","/"));
        let etdt = new Date(et.replace("-","/"));
        let iDays = parseInt(Math.abs(stdt - etdt)/1000/60/60/24);
        console.log(iDays);
        console.log((iDays>31));
        if ((username != 'heist') && (iDays > 31 )){
          alert("查询时间长度不能超过1个月, 请重新输入");
          return ;
        }

        let para = {
          user: username,
          starttime: this.form.starttime,
          endtime: this.form.endtime
        };    
        this.listLoading = true;
        reqGetStats(para).then((res) => {          
          if (res.data && res.data.length!==0 ) {
            console.log("will show download detail");
            this.statsObj = res.data
            this.showDownLoad = true
          } else {
            this.nodatashow = true
          }         
          this.listLoading = false;
        })
        .catch((error) => {
           console.log("download error")
           console.log(error)
        });
      },

      sdateChanged(val){
        console.log("time change");
        console.log(val);
        this.form.starttime = val;
        this.showDownLoad = false;   
        this.statsObj = {} 
      },
      edateChanged(val){
        console.log("time change");
        console.log(val);
        this.form.endtime = val;
        this.showDownLoad = false;   
        this.statsObj = {} 
      },

      //下载详细数据
      downloads(devId) {
        console.log("> dataQuery. download....")
        console.log(devId);

        let params = {}
        let stime =  this.form.starttime;
        let etime =  this.form.endtime;        
        let filename = devId +'_'+ stime +"_" +  etime + '.csv';
        
        params['filename'] = filename;
        params['condition'] = "?devId=" + devId + "&starttime=" + stime + "&endtime=" + etime ;

        reqDownloadStats(params);
        //window.open("http://127.0.0.1:10000/data/download/"+filename + "?user=admin&starttime=2017-02-28&endtime=2017-07-18");
      }
    },
    mounted() {
      console.log("> dataQuery mounted called")
      let d = new Date();
      console.log(d);
      console.log(d.getFullYear());
      console.log(d.getMonth() + 1);
      console.log(d.getDate());
      this.form.starttime = d.getFullYear() + "-" + (d.getMonth()+1) + "-" + d.getDate();
      this.form.endtime = d.getFullYear() + "-" + (d.getMonth()+1) + "-" + d.getDate();
    }
  }
</script>

<style>
  .demo-table-expand label {
    font-weight: bold;
  }
</style>
