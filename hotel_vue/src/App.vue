<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HotelImg from '../static/hotel-1.png'
</script>

<template>
  <div class="common-layout" >
    <el-container>
      <el-header>
        <el-menu
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          @select="handleSelect"
          style="background-color: transparent"
      >

        <el-sub-menu index="2">
          <template #title >服务</template>
          <el-menu-item  v-if="this.$store.state.loginType !== '2' && this.$store.state.loginType !== '3'" @click="$router.push('/room_order')" style="height: 50px" index="2-1">房间预定</el-menu-item>
          <el-menu-item v-if="this.$store.state.loginType  !== '2' && this.$store.state.loginType  !== '3'" @click="$router.push('/order_meet')" style="height: 50px" index="2-2">接送服务预定</el-menu-item>
          <el-menu-item v-if="this.$store.state.loginType  !== '2' && this.$store.state.loginType  !== '3'" @click="$router.push('/order_food')" style="height: 50px" index="2-3">送餐服务预定</el-menu-item>
          <el-menu-item v-if="this.$store.state.loginType  !== '2' && this.$store.state.loginType  !== '3'" @click="$router.push('/my_orders')" style="height: 50px" index="2-4">我的订单</el-menu-item>
          <el-menu-item  v-if="this.$store.state.loginType === '2'" @click="$router.push('/check_in')" style="height: 50px" index="2-5">入住登记</el-menu-item>
          <el-menu-item  v-if="this.$store.state.loginType === '2'" @click="$router.push('/check_out')" style="height: 50px" index="2-6">退房登记</el-menu-item>
          <el-menu-item  v-if="this.$store.state.loginType === '2'" @click="$router.push('/finish_order')" style="height: 50px" index="2-7">订单完成</el-menu-item>
          <el-menu-item  v-if="this.$store.state.loginType === '3'" @click="$router.push('/admin')" style="height: 50px" index="2-7">管理员页面</el-menu-item>
        </el-sub-menu>
          <div style="width: 20%;text-align: center;"></div>
          <el-image :src="HotelImg" @click="$router.push('/')" style="width: 40px;cursor: pointer;height: 40px;margin-top: 8px;opacity: 0.5;"></el-image>
          <div style="width: 50px"></div>
          <p style="margin-top:8px;font-size:30px;word-spacing: 30px;cursor: pointer" @click="$router.push('/')">温 德 姆 酒 店</p>
          <div v-if="isLogin==false" style="position: absolute;right: 40px;margin-top: 10px">
            <el-button @click="isShowLogin=true;isShowSignUp=false"  style="text-align: center;margin-top:10px;">登录</el-button>
            <el-button @click="isShowLogin=false;isShowSignUp=true" style="text-align: center;margin-top:10px">注册</el-button>
          </div>
          <div @click="logout()" style="margin-top:20px ;position: absolute;right: 40px;" v-if="isLogin==true">
            <p3 >{{Login_info.username}}，您好</p3>
          </div>

      </el-menu>
      </el-header>
      <el-main> <RouterView />
        <el-dialog v-model="isShowLogin" style="height: 544px;
        width: 400px;opacity: 0.9">
          <br>
          <el-avatar  src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
                      :size="140"
                      style="align-items: center;position: absolute;left: 33%"></el-avatar>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <el-form :rules="rules" :model="Login_info" ref="dataForm">
            <el-form-item prop="username" style="margin-left: 35px;width: 80%;text-align: center;opacity: 0.5">
              <el-input placeholder="username" v-model.trim="Login_info.username" style="height: 45px"
                        ></el-input>
            </el-form-item>
            <el-form-item prop="password" style="margin-left: 35px;margin-top:25px;width: 80%;text-align: center;opacity: 0.5">
              <el-input placeholder="password" type="password" v-model.trim="Login_info.password" label="password" style="height: 45px;"
                        ></el-input>
            </el-form-item>


            <el-button
                @click="Login(username,password)"
                :color="pink"
                style="height: 45px;width: 50%;margin-top: 15px;margin-left: 90px;opacity: 0.5"
            >登录</el-button>
            <el-select
                placeholder="选项"
                v-model="loginType"
                style="opacity: 0.5;width: 20%;margin-top: 30px;margin-left: 35px;margin-right: 0px;border: 0px;flex: auto">
              <el-option :value="1" :label="用户登录">用户登录</el-option>
              <el-option :value="2">服务人员登录</el-option>
              <el-option :value="3">管理员登录</el-option>

            </el-select>
            <p @click="isShowLogin=0;isShowSignUp=1"  style="margin-left: 60px;float: left;margin-top: 33px;">还没有账号，点此注册</p>
          </el-form>

        </el-dialog>
        <el-dialog v-model="isShowSignUp" style="height: 544px;
                   width: 400px;
                   opacity: 0.9"
        >
          <br>
          <el-avatar  src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
                      :size="140"
                      style="align-items: center;position: absolute;left: 33%"></el-avatar>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <el-form :rules="rules" :model="Login_info" ref="form">
            <el-form-item prop="username" style="margin-left: 35px;width: 80%;text-align: center;opacity: 0.5">
              <el-input placeholder="username" v-model.trim="Login_info.username" style="height: 45px"
              ></el-input>
            </el-form-item>
            <el-form-item prop="password" style="margin-left: 35px;margin-top:25px;width: 80%;text-align: center;opacity: 0.5">
              <el-input placeholder="password" type="password" v-model.trim="Login_info.password" label="password" style="height: 45px;"
              ></el-input>
            </el-form-item>
            <el-button
                @click="SignUp(username,password)"
                :color="pink"
                style="height: 45px;width: 50%;margin-top: 25px;margin-left: 85px;opacity: 0.5"
            >注册</el-button>
          </el-form>
        </el-dialog>
      </el-main>
    </el-container>
  </div>

</template>
<script>
import axios from "axios";
import {ElMessageBox} from "element-plus";

export default{
  name:'app',
  data(){
    return {
      isShowLogin:false,
      isShowSignUp:false,
      loginType: '1',
      isLogin:false,
      Login_info:{
        username:'',
        password:'',
      },
      is_correct:false,
      rules:{
        username:[
          {required:true,message:'请输入用户名',trigger:'blur'},
          {min:8,max:15,message:'长度在8到15个字符之间',trigger: 'blur'},
        ],
        password:[
          {required:true,message:'请输入密码',trigger:'blur'},
          {min:8,max:15,message:'长度在8到15个字符之间',trigger: 'blur'},
        ]
      }

    }
  },
  methods:{
    Login(username,password){
      let that = this
      console.log(username,password)
      axios.get('/api/login', {
        params:{
          username:that.Login_info.username,
          password:that.Login_info.password,
          loginType:this.loginType,
        },
      }).then(function (response){
        if(response.data.code == '1'){
          localStorage.setItem('username',that.Login_info.username)
          localStorage.setItem('password',that.Login_info.password)
          localStorage.setItem('loginType',that.loginType)

          that.$store.state.username = that.Login_info.username
          that.$store.state.password = that.Login_info.password
          that.$store.state.loginType = that.loginType
          that.$store.state.is_login = true

          that.isShowLogin = 0
          that.$message({message:'登录成功',type:'success'})
          that.isLogin=true
          console.log(that.$store)
          console.log('登录类型'+that.loginType)
          console.log(that.$store.state.loginType === '2')
          if(that.$store.state.loginType === 2){

          }else if(that.$store.state.loginType === 3){
            that.$router.push('/admin')
          }
          location.reload()
        }else {
          that.$message({message:response.data.msg,type:'error'})
        }
      })
    },
    SignUp(username,password){
      let that = this
      axios.get('/api/signup',{
        params:{
          username:that.Login_info.username,
          password:that.Login_info.password,
        }
      }).then(function (response){
        if(response.data.code == '1'){
          localStorage.setItem('username',that.Login_info.username)
          localStorage.setItem('password',that.Login_info.password)
          that.$store.state.username = that.Login_info.username
          that.$store.state.password = that.Login_info.password
          localStorage.setItem('loginType','1')
          that.$store.state.loginType = '1'
          that.$store.state.is_login = true
          that.isShowSignUp = 0
          that.$message({message:'注册成功',type:'success'})
          that.isLogin=true
        }else {
          that.$message({message:response.data.msg,type:'error'})
        }
      })
    },
    logout(){
      let that = this
      ElMessageBox.confirm(
          '是否要注销?',
          {
            confirmButtonText:'注销',
            cancelButtonText:'取消',
            type:'info'
          }
      ).then(()=>{
        localStorage.clear()
        location.reload()
        that.$store.state.username = ''
        that.$store.state.password = ''
        that.$store.state.loginType = ''
        that.$store.state.is_login = false
      })
    }
  },
  mounted() {
    let  that = this

    axios.get('/api/login',{
      params:{
        username:localStorage.getItem('username'),
        password:localStorage.getItem('password'),
        loginType:localStorage.getItem('loginType'),
      }
    }).then(function (res){
      if( res.data.code === '1'){
        that.Login_info.username = localStorage.getItem('username'),
        that.isLogin = true
        that.$store.state.username = localStorage.getItem('username')
        that.$store.state.password = localStorage.getItem('password')
        that.$store.state.loginType = localStorage.getItem('loginType')
        that.$store.state.is_login = true
      }
    })
  },
}

</script>
<style scoped>

.el-dialog__header {
  padding-top: 10px !important;
  background-color:rgb(255,255,255,0);
  border-radius: 14px 14px  0  0 ;
}
.el-dialog__body {
  border-top: 0 !important;
  background-color: rgba(19, 31, 59, 0);
  color: #FFFFFF;
}
.el-dialog__footer{
  text-align: center;
  background-color: rgba(255,255,255,0);
}
</style>
