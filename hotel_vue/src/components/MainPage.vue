<script setup>
import jpg1 from '../../static/mainPage/走马灯/1.jpg'
import jpg2 from '../../static/mainPage/走马灯/2.jpg'
import jpg3 from '../../static/mainPage/走马灯/3.jpg'
import jpg4 from '../../static/mainPage/走马灯/4.jpg'
import icon1 from '../../static/mainPage/icon/1.png'
import icon2 from '../../static/mainPage/icon/2.png'
import icon3 from '../../static/mainPage/icon/3.png'
import icon4 from '../../static/mainPage/icon/4.png'
</script>
style="width: 100%;"
<template>
  <div>
    <el-carousel indicator-position="outside" height="580px" style="width: 100%;">
      <el-carousel-item  >
        <el-image :src="jpg1" style="width: 100%;"></el-image>
      </el-carousel-item>
      <el-carousel-item >
        <el-image :src="jpg2" style="width: 100%;"></el-image>
      </el-carousel-item>
      <el-carousel-item >
        <el-image :src="jpg3" style="width: 100%;"></el-image>
      </el-carousel-item>
      <el-carousel-item >
        <el-image :src="jpg4" style="width: 100%;"></el-image>
      </el-carousel-item>
    </el-carousel>
    <div   style="width: 100%;background: url('../../static/mainPage/website.png');height: 500px;background-repeat: no-repeat;background-size: 100% 100%;" >
      <div style="width: 40%;float: left;margin-left: 17%;margin-top: 70px">
        <p style="font-size: 35px;font-family: 华文细黑">开启愉快旅程</p>
        <p style="width: 70%">成为温德姆会员，在品味美食、放松度假时，尽享会员专属优惠及畅快的智能应用服务。</p>
        <el-button color="#e3dfb1"  @click="$router.push('/room_order')" style="margin-top: 5%;width: 40%;height: 50px">立即预定</el-button>
      </div>
      <div style="width: 400px;float: left;margin-left: 3%;margin-top: 70px">
        <el-image :src="icon1" style="margin-right: 80px"></el-image>
        <el-image :src="icon2"></el-image>
        <div style="height: 80px">
          <p style="margin-left: 25px;width:70px;float: left;font-family: 华文细黑">赚取住宿</p>
          <p style="margin-left: 95px; float: left;font-family: 华文细黑" >儿童享受免费餐饮</p>
        </div>
        <el-image :src="icon3" style="margin-right: 80px"></el-image>
        <el-image :src="icon4"></el-image>
        <div style="height: 80px">
          <p style="margin-left: 12px;width:100px;float: left;font-family: 华文细黑">手机办理入住</p>
          <p style="margin-left: 92px; float: left;font-family: 华文细黑" >会员专属优惠</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name:'MainPage',
  data(){
    return{
      picture:''
    }
  },
  methods:{
  }

}

</script>

<style scoped>

</style>