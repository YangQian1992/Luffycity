<template>
  <div>
    <el-carousel indicator-position="outside" height="450px">
      <el-carousel-item v-for="item in img_list" :key="item">
        <img :src="item" alt="" style="height: 450px; width: 100%">
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script>
  export default {
    name: "HomeBanner",
    data() {
      return {
        img_list: [
          require("../../assets/banner/home-banner1.png"),
          require("../../assets/banner/home-banner2.png"),
          require("../../assets/banner/home-banner3.png"),
          require("../../assets/banner/home-banner4.png"),
          require("../../assets/banner/home-banner5.png"),
        ]
      }
    },
  }
</script>

<style scoped></style>
