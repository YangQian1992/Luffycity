<template>
  <div class="footer">
    <div class="container">
      <div>
        <el-menu :default-active="activeIndex" class="el-menu-demo list-inline up_list" mode="horizontal"  :router="true">
          <el-menu-item :index="item.path" class="li_list" v-for="(item,index) in footer_list" :key="index">{{item.label}}</el-menu-item>
        </el-menu>
      </div>
      <div class="down_text">
        <p>Copyright © luffycity.com版权所有 | 京ICP备17072161号-1</p>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "LuffyCityFooter",
    data() {
      return {
        activeIndex:"1",
        footer_list: [
          {label:"关于我们",path:"/about_us"},
          {label:"联系我们",path:"call_us"},
          {label:"商务合作",path:"/business_cooperation"},
          {label:"帮助中心",path:"/help_center"},
          {label:"意见反馈",path:"/feedback"},
          {label:"新手指南",path:"/beginner_guide"},
        ]
      }
    },
  }
</script>

<style scoped>
  .footer {
    width: 100%;
    height: 128px;
    display: -ms-flexbox;
    display: flex;
    text-align: center;
    -ms-flex-align: center;
    align-items: center;
    -ms-flex-pack: center;
    justify-content: center;
    background: #25292e;
    margin-top: auto;
    z-index: 1;
  }

  .footer .container .up_list {
    background: #25292e;
    width: 100%;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-pack: justify;
    justify-content: space-between;
    -ms-flex-align: center;
    align-items: center;
    color: #fff;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .li_list {
    list-style: none;
    width: 14%;
    font-size: 14px;
    cursor: pointer;
  }

  .down_text {
    font-size: 12px;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-pack: center;
    justify-content: center;
    color: #fff;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .el-menu--horizontal{
      border-right: none;
      border-bottom: none;
  }
  .el-menu--horizontal .el-menu-item:not(.is-disabled):focus, .el-menu--horizontal .el-menu-item:not(.is-disabled):hover {
    outline: 0;
    color: #fff;
}
  .el-dropdown-menu__item--divided:before, .el-menu, .el-menu--horizontal>.el-menu-item:not(.is-disabled):focus, .el-menu--horizontal>.el-menu-item:not(.is-disabled):hover, .el-menu--horizontal>.el-submenu .el-submenu__title:hover{
    background: #25292e;
  }

  .el-menu--horizontal>.el-menu-item.is-active {
     border-bottom: none;
}
  .el-menu--horizontal>.el-menu-item{
    border-bottom: none;
  }
</style>
