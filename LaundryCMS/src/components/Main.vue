<template>
  
  <h3> hello, world </h3>

</template>

<script>
  import { bus } from '../bus.js'
  export default {
    name: 'Main',
    created(){
      bus.$on('setUserName', (text) => {
        this.sysUserName = text;
      })
    },
    data () {
      return {
        sysUserName: '',
        sysUserAvatar: '',
        items: {"1":"hello,world", "2":"hello, heist"},
        collapsed: false,
      }
    },
    methods: {
      logout(){
        var _this = this;
        this.$confirm('确认退出吗?', '提示', {
          //type: 'warning'
        }).then(() => {
          sessionStorage.removeItem('access-user');
          _this.$router.push('/');
        }).catch(() => {

        });
      }
    },
    mounted() {
      var user = sessionStorage.getItem('access-user');
      console.log("> mounted print ")
      if (user) {
        user = JSON.parse(user);
        this.sysUserName = user.name || '';
      }
    }
  }


</script>
<style>
  .el-carousel__item h3 {
    color: #475669;
    font-size: 18px;
    opacity: 0.75;
    line-height: 300px;
    margin: 0;
  }
  
  .el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
  }
  
  .el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
  }
</style>
