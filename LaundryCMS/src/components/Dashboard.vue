<template>
  <el-row class="warp">
    <el-menu theme="dark" :default-active="$route.path" class="el-menu-demo" mode="horizontal" router >
      <el-row >
        <el-col :span="20">
           <el-menu-item index="/">@heist</el-menu-item>
        </el-col>
        <el-col :span="4">
           <el-menu-item index="/login">用户登录</el-menu-item>
        </el-col>

      </el-row> 
    </el-menu>

    <el-col :span="24" class="warp-main">
      <section class="chart-container">
        <el-row>
          <el-col :span="12">
            <el-card :body-style="{ padding: '0px' }">
              <img src="../assets/images/heist1.jpg" class="image">
              <div style="padding: 14px;">
                <span>一拖N智能远程分配器系统</span>
              </div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card :body-style="{ padding: '0px' }">
              <img src="../assets/images/heist2.jpg" class="image">
              <div style="padding: 14px;">
                <span>耐腐蚀单项阀</span>
              </div>
            </el-card>
          </el-col>

          <el-col :span="24">
             <div class="carousel-caption">
                 <h4>
                     智能改变生活
                 </h4>
                 <p>
                     海斯特科技从事智能产品开发、生产、销售，为清洁、洗衣、环保等行业提供智能化加料系统，推出远程可监控溯源液体分配器系统，模具成型耐腐蚀精密单向阀，智能化工业控制系统，高灵敏度机器人末端传感器等。
                 </p>
                <h4>
                    梦想创造未来
                </h4>
                <p>
                    坚持科技创新理念、工匠精神，多年为清洁剂厂家提供优质设备和系统服务，终端产品遍布全国星级酒店和规模洗衣工厂，技术实力和专业经验在行业遥遥领先。
                </p>
             </div>
          </el-col>
        </el-row>
      </section>

    </el-col>
  </el-row>
</template>
<style>
  .time {
    font-size: 13px;
    color: #999;
  }

  .bottom {
    margin-top: 13px;
    line-height: 12px;
  }

  .image {
    width: 100%;
    display: block;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }

  .clearfix:after {
    clear: both
  }

  .chart-container {
    width: 100%;
  }
  .chart-container .el-col {
    padding: 30px 20px;
  }
</style>

<script>
  import echarts from 'echarts'

  export default {
    data() {
      return {
        currentDate: new Date(),
        chartColumn: null,
        chartBar: null,
        chartLine: null,
        chartPie: null
      };
    }
  }
</script>
