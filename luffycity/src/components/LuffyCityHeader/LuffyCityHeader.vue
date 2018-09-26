<template>
  <div class="header" style="background-color: yellow">
    <div class="container">
      <div class="left_logo">
        <img src="https://www.luffycity.com/static/img/head-logo.a7cedf3.svg" alt="">
      </div>
      <div class="center_nav">
        <template>
          <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" :router="true">
            <el-menu-item style="height: 80px;line-height: 80px" :index="item.path" :key="index"
                          v-for="(item,index) in header_list">{{item.label}}
            </el-menu-item>
          </el-menu>
        </template>
      </div>
      <div class="right_login_register">
        <router-link to="/login/">登录</router-link>
        <span>|</span>
        <a href="">注册</a>
      </div>
    </div>
  </div>
</template>

<script>
  import Login from '../../components/Login'

  export default {
    name: 'LuffyCityHeader',
    data() {
      return {
        activeIndex: "1",
        header_list: [
          {label: "首页", path: "/home"},
          {label: "免费课程", path: "/course"},
          {label: "轻课", path: "/light-course"},
          {label: "学位课程", path: "/micro"},
          {label: "智能题库", path: "/questionbank"},
          {label: "公开课", path: "/publicclass"},
          {label: "内部材料", path: "/internalmaterials"},
        ]
      }
    },
    methods: {
      logout() {
        this.$store.commit('clearToken');
        this.$router.push({path: '/index'})
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .header {
    width: 100%;
  }

  .el-menu {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 80px;
  }

  .left_logo {
    position: absolute;
    left: 80px;
    top: 20px;
    width: 118px;
    height: 70px;
    z-index: 999;
  }

  .right_login_register {
    width: 100%;
    font-size: 14px;
    color: #7f7f7f;
    text-align: right;
    margin-top: -50px;
    position: absolute;
    margin-left: -95px;
  }
</style>
