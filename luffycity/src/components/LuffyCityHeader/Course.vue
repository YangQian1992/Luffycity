<template>
  <div class="course_classification">
    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" :router="true">
      <el-menu-item :index="item.path" v-for="(item,index) in course_classification" :key="index">{{item.label}}
      </el-menu-item>
    </el-menu>
    <router-view></router-view>
  </div>
</template>

<script>
  export default {
    name: "Course",
    data() {
      return {
        activeIndex: "1",
        course_classification: [
          {label: "全部", path: "/course/total"},
          {label: "Python", path: "/course/python"},
          {label: "Linux基础", path: "/course/linux"},
          {label: "前端", path: "/course/front_end"},
          {label: "Python进阶", path: "/course/python_advance"},
          {label: "UI", path: "/course/ui"},
          {label: "工具", path: "/course/tool"},
        ]
      }
    }
  }
</script>

<style scoped>
  .course_classification {
    margin-left: 70px;

  }

  .course_classification .el-menu--horizontal {
    border-right: none;
    border-bottom: none;
  }

  .el-menu--horizontal > .el-menu-item {
    float: left;
    height: 60px;
    line-height: 60px;
    margin: 0;
    font-size: 16px;
    border-bottom: none;
    color: #666;
  }

  .el-menu--horizontal .el-menu-item:not(.is-disabled):focus, .el-menu--horizontal .el-menu-item:not(.is-disabled):hover {
    outline: 0;
    color: #00b4e4;
  }
</style>
