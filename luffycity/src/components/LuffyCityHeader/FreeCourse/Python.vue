<template>
  <div>
    <section v-for="item in courseList" @click="my_click">
      <div class="head"><img src="../../../assets/sketch-small.576677d.png" alt="" class="bacimg"> <b class="mask" id="mask" style="background: #56CBC4"></b>
        <p>{{item.course_name}}</p>
      </div>
      <div class="content"><p class="p1">{{item.course_overview}}</p>
        <div class="div1">
          <div class="div2"><img
            src="data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iMTFweCIgaGVpZ2h0PSIxMnB4IiB2aWV3Qm94PSIwIDAgMTEgMTIiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+CiAgICA8IS0tIEdlbmVyYXRvcjogU2tldGNoIDQ4LjIgKDQ3MzI3KSAtIGh0dHA6Ly93d3cuYm9oZW1pYW5jb2RpbmcuY29tL3NrZXRjaCAtLT4KICAgIDx0aXRsZT5TaGFwZTwvdGl0bGU+CiAgICA8ZGVzYz5DcmVhdGVkIHdpdGggU2tldGNoLjwvZGVzYz4KICAgIDxkZWZzPjwvZGVmcz4KICAgIDxnIGlkPSJSZWN0YW5nbGUtMiIgc3Ryb2tlPSJub25lIiBzdHJva2Utd2lkdGg9IjEiIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTE3LjAwMDAwMCwgLTkxLjAwMDAwMCkiPgogICAgICAgIDxnIGlkPSLkuKrkurrkuK3lv4MiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDE3LjAwMDAwMCwgOTEuMDAwMDAwKSIgZmlsbD0iIzlCOUI5QiIgZmlsbC1ydWxlPSJub256ZXJvIj4KICAgICAgICAgICAgPHBhdGggZD0iTTYuNzU4MjMwODEsNi42MjU2MzEwOCBMNC4yNDEzMzM5Miw2LjYyNTYzMTA4IEMxLjkwMjMxNTc1LDYuNjI1NjMxMDggMCw4LjQxNDM0Nzg0IDAsMTAuNjEzNjY4OSBMMCwxMC44NTAyOTE3IEMwLDEyIDEuODcxODkwNjUsMTIgNC4yNDEzMzM5MiwxMiBMNi43NTgyNDUzMiwxMiBDOS4wMzQ0NTQ2MSwxMiAxMSwxMiAxMSwxMC44NTAyOTE3IEwxMSwxMC42MTM2Njg5IEMxMSw4LjQxNDc3MDM2IDkuMDk3MTkwOTUsNi42MjU2MzEwOCA2Ljc1ODIzMDgxLDYuNjI1NjMxMDggWiBNNS4zNzQwNDEyNiw2LjMyMTI0MjAyIEM3LjIyNjIxNDM2LDYuMzIxMjQyMDIgOC43MzMxOTI0Nyw0LjkwMzU2Mjg4IDguNzMzMTkyNDcsMy4xNjA2Mjc4MiBDOC43MzMxOTI0NywxLjQxNzc3NDU0IDcuMjI2MjE0MzYsMCA1LjM3NDA0MTI2LDAgQzMuNTIxOTI2MiwwIDIuMDE0ODAzLDEuNDE4MDc0MzkgMi4wMTQ4MDMsMy4xNjA2OTU5NyBDMi4wMTQ4MDMsNC45MDMxODEyNSAzLjUyMTkyNjIsNi4zMjEyNDIwMiA1LjM3NDA0MTI2LDYuMzIxMjQyMDIgWiIgaWQ9IlNoYXBlIj48L3BhdGg+CiAgICAgICAgPC9nPgogICAgPC9nPgo8L3N2Zz4K"
            alt="">
            <span class="span1">{{item.number_of_students_studied}}</span>
            <span class="span2">{{item.course_difficulty}}</span>
          </div>
          <div class="div3"><span class="span4">￥9.9</span></div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
  export default {
    name: "Python",
    data() {
      return {
        'courseList': ''
      }
    },
    mounted() {
      let that = this;
      this.$axios.request({
        url: 'http://127.0.0.1:8000/python_course/',
        method: 'get',
      }).then(function (data) {
        that.courseList = data.data;
      })
    },
    methods:{
      my_click:function () {
        this.$axios.request({
          url:'',
          method:'get'
        }).then(function (data) {
          console.log(data.data);
        })
      }
    }
  }
</script>

<style scoped>
  section {
    position: relative;
    width: 288px;
    margin-right: 16px;
    margin-bottom: 30px;
    background-color: #fff;
    border-radius: 2px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, .05);
    transition: all .2s linear;
    display: inline-block;
  }

  section .head {
    width: 100%;
    height: 144px;
    position: relative;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    justify-content: space-around;
  }

  section .head .bacimg {
    width: 100%;
    height: 100%;
    position: absolute;
    left: 0;
    top: 0;
  }

  img {
    vertical-align: middle;
    border: 0;
  }

  section .head b {
    width: 100%;
    height: 100%;
    position: absolute;
    left: 0;
    top: 0;
    opacity: .9;
  }

  b, strong {
    font-weight: 700;
  }

  section .head p {
    width: 100%;
    height: 100%;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    justify-content: space-around;
    z-index: 1;
    font-size: 24px;
    color: #fff;
    text-align: center;
    position: absolute;
    left: 0;
    top: 0;
    letter-spacing: .54px;
    padding: 0 20px;
    margin: 0;
    box-sizing: border-box;
  }

  section .content {
    width: 100%;
    height: 148px;
    padding-top: 30px;
    padding-left: 0;
    padding-right: 0;
    background: #fff;
    box-shadow: 0 2px 6px 0 #e8e8e8;
  }

  section .content .p1 {
    width: 100%;
    height: 40px;
    font-size: 14px;
    color: #666;
    cursor: pointer;
    letter-spacing: .6px;
    margin-bottom: 20px;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
  }

  section .content .div1 {
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    -ms-flex-pack: justify;
    justify-content: space-between;
  }

  section .content .div1 img {
    width: 11px;
    height: 12px;
  }

  section .content .div1 .div2 span {
    font-size: 13px;
    color: #666;
    letter-spacing: .29px;
  }

  section .content .div1 .span1 {
    margin-left: 5px;
    margin-right: 5px;
  }

  section .content .div1 span {
    display: inline-block;
  }

  section .content .div1 .div3 .span4 {
    font-size: 14px;
    color: #fa6240;
    letter-spacing: .32px;
  }

  section:hover {
    box-shadow: 0 8px 15px rgba(0, 0, 0, .15);
    transform: translate3d(0, -3px, 0);
  }

  section .content .p1:hover {
    color: #00b4e4;
  }
</style>

