<script setup>

</script>

<template>
  <div>
    <p style="float: left;margin-left: 15%"> 选择入住时间</p>
    <p style="float: left;margin-left: 3%">入住：</p>
    <el-date-picker v-model="check_in_day" style="float: left;margin-top: 10px" value-format="YYYY-MM-DD" ></el-date-picker>
    <p style="float: left;margin-left: 3%"> 退房：</p>
    <el-date-picker v-model="check_out_day" style="float: left;margin-top: 10px" value-format="YYYY-MM-DD"></el-date-picker>
    <el-button style="float: left;margin-top: 10px;margin-left: 3%" @click="search_room()">查询剩余房间</el-button>
    <el-button @click="get_all_room()" style="float: left;margin-top: 10px;margin-left: 3%">查询所有房间</el-button>

    <br>
    <br>
    <br>
    <el-tabs tab-position="left"  style="float: none;margin-top: 20px;margin-left: 5%" class="demo-tabs">
      <el-tab-pane :label="room.room_type" v-for="room in rooms" :key="room.room_id">
        <el-image  :src="'/api/get_room_picture?id='+room.room_id " style="float: left;width: 50%;height: 40%;margin-left: 20px"></el-image>
        <div style="width: 35%;float: left;margin-left: 5%;height:100%">
          <div style="height: 100%" class="room_intro">
            <div>
              <h1 style="" > {{room.room_type}}</h1>
              <li v-text="room.每日打扫+'每日打扫'"></li><br>
              <li> 面积{{room.面积}}平方米</li>
              <li> {{room.床}}</li><br>
            </div>
            <div >
              <h3 > 洗浴</h3>
              <li v-text="room.牙刷+'牙刷'"></li>
              <li v-text="room.牙膏+'牙膏'"></li><br>
              <li v-text="room.沐浴露+'沐浴露'"></li>
              <li v-text="room.洗发水+'洗发水'"></li><br>
              <li v-text="room.毛巾+'毛巾'"></li>
              <li v-text="room.私人卫浴+'私人卫浴'"></li><br>
            </div>

            <h3 style="float: none"> 电子产品</h3>
            <li v-text="room.免费wifi+'免费wifi'"></li><br>
            <li v-text="room.吹风机+'吹风机'"></li>
            <li v-text="room.电视+'电视'"></li><br>
          </div>
          <br>
          <div style="margin-left: 15%;">
            <h1 style="font-size: 32px;color: red;float: left;margin-bottom: 0px">{{room.room_price}}元/天</h1>
            <p style="float: left;margin-top: 40px;margin-left: 5%" v-text="'原价'+parseInt(room.room_price*1.2)+'元/天'"></p><br>
            <el-button @click="book(room)" style="width: 60%;margin-top: 5%;height: 60%;text-align: left;margin-left: 0px ;">立即预定</el-button>
          </div>

          <el-dialog  center v-model="is_showComplete" style="width: 25%;opacity: 0.9">
            <el-form :rules="Complete_rules" label-position="top" ref="form" :model="user_Info" type="flex" style="text-align: center;margin-left: 15%">
              <el-form-item label="真实姓名" prop="name">
                <el-input v-model.trim="user_Info.name" style="width: 60%"></el-input>
              </el-form-item>
              <el-form-item label="性别" prop="sex">
                <el-radio-group v-model.trim="user_Info.sex" style="width: 60%">
                  <el-radio-button value="男">男</el-radio-button>
                  <el-radio-button value="女">女</el-radio-button>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="证件类型" prop="id_type">
                <el-select v-model.trim="user_Info.id_type"  style="width: 60%">
                  <el-option value="身份证">身份证</el-option>
                  <el-option value="护照">护照</el-option>
                  <el-option value="港澳台居住证">港澳台居住证</el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="实际年龄" prop="age">
                <el-input v-model.number="user_Info.age" style="width: 60%"></el-input>
              </el-form-item>
              <el-form-item label="证件号码" prop="id">
                <el-input v-model="user_Info.id" style="width: 80%"></el-input>
              </el-form-item>
              <el-form-item label="联系电话" prop="phone">
                <el-input v-model.trim="user_Info.phone" style="width: 80%"></el-input>
              </el-form-item>
              <el-form-item label="联系邮箱" prop="email">
                <el-input v-model.trim="user_Info.email" style="width: 80%"></el-input>
              </el-form-item>

            </el-form>
            <el-button @click="submit_complete()" style="width: 20%;margin-left: 40%;margin-top: 4%">提交更改</el-button>
          </el-dialog>

          <el-dialog v-model="show_book" style="width: 20%;">

            <template #header="{ close, titleId, titleClass }">
              <div class="my-header" style="text-align: center;margin: 3%">
                <h4 :id="titleId" :class="titleClass" >房间订单</h4>
              </div>
            </template>

            <template #default>
              <div class="my-header" style="text-align: center;margin: 3%">
                <el-form-item label="预定房型" style="width: 80%" >
                  <el-select v-model="select_room_type" >
                    <el-option  style="width: 30%" v-for="room in rooms" :value="room.room_type" :label="room.room_type">{{ room.room_type }}</el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="入住日期" >
                  <el-date-picker v-model="check_in_day" value-format="YYYY-MM-DD"></el-date-picker>
                </el-form-item>
                <el-form-item label="退房日期" >
                  <el-date-picker v-model="check_out_day" value-format="YYYY-MM-DD"></el-date-picker>
                </el-form-item>
                <el-button @click="book_submit()" style="width: 40%;height: 20%">
                  提交订单
                </el-button>
              </div>

            </template>

          </el-dialog>
        </div>

      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import axios from "axios";
import {ElMessage} from "element-plus";

export default {
  name:'room_order',
  data(){
    return{
      rooms:{},
      select_room_type:'',
      is_showComplete:false,
      check_login:false,
      check_Complete:false,
      show_book:false,
      check_in_day:'',
      check_out_day:'',
      user_Info:{
        name:'',
        sex:'男',
        id_type:'身份证',
        age:18,
        id:'',
        phone:'',
        email:''
      },
      Complete_rules:{
        name:[
          {required:true,message:'请输入真实姓名',trigger:'blur'},
          {min:2,max:30,message:'长度在2到30个字符之间',trigger: 'blur'},
        ],
        id_type:[{type:'enum',enum:['身份证','护照','港澳台居住证'],message:'证件类型输入错误',trigger:'change'}],
        age:[
          {required:true,message:'请输入年龄',trigger:'blur'},
          {type:'integer',message:'请输入整数',trigger:'blur'},
        ],
        sex:[
          {type:'enum',enum:['男','女'],message:'请输入整数',trigger:'blur'},
        ],
        id:[
          {required:true,message:'请输入证件号码',trigger:'blur'},
          {min:8,max:18,message:'长度在8到18个字符之间',trigger: 'blur'},
        ],
        phone: [
          {required:true,message:'请输入手机号码',trigger:'blur'},
          {type:'string',message:'请输入有效手机号码',trigger:'blur'},
          {min:8,max:18,message:'长度在8到18个字符之间',trigger: 'blur'},
        ],
        email:[
          {required:true,message:'请输入电子邮箱',trigger:'blur'},
          {type:'email',message:'请输入有效电子邮箱',trigger:'blur'},
        ],

      },
    }
  },
  methods:{
    get_all_room(){
      let that = this
      axios.get(
          'api/get_room_Imf'
      ).then(function (response){
        if(response.data.code==='1'){
          that.rooms = response.data.data
          console.log(that.rooms)
          console.log(response)
        }
      })
    },
    book(room){
      let that = this
      if (!this.$store.state.is_login){
        that.$message('请先登录')
        return
      }
      //检测是否填写身份信息
      axios.get('/api/get_userInf_complete',{
        params:{
          username:this.$store.state.username,
          password:this.$store.state.password,
          loginType:'3'
        }
      }).then(function (res){
        if(res.data.code == '0'){
          that.$message('请先填写真实信息')
          that.is_showComplete = true
        }else if (res.data.code ==='1'){
          that.show_book=true

        }
      })


    },
    search_room(){
      this.rooms = this.rooms.slice(1,8)
      this.$message({message:'查询成功',type:'success'})
    },
    submit_complete(){
      let that = this
      this.$refs.form[0].validate((valid) => {
        if (valid) {
          axios.get('/api/updata_user_Imf',{
            params:{
              username:localStorage.getItem('username'),
              name:that.user_Info.name,
              id_number:that.user_Info.id,
              age:that.user_Info.age,
              id_type:that.user_Info.id_type,
              sex:that.user_Info.sex,
              phone:that.user_Info.phone,
              email:that.user_Info.email,
              password:localStorage.getItem('password')
            }
          }).then(function (res){
            if (res.data.code === '1'){
              that.$message({message:'更改成功',type:'success'})
              that.is_showComplete = false
            }else {
              that.$message({message:res.data.msg,type:'error'})
            }
          }).catch(function (err){
            that.$message('更改失败','error')
          })
        } else {
          this.$message.error('请完善表单相关信息！');
          return false;
        }
      });
    },
    book_submit(){
      let that = this
      axios.get('/api/add_new_order',{
        params:{
          username:that.$store.state.username,
          password:that.$store.state.password,
          room_type:that.select_room_type,
          check_in:that.check_in_day,
          check_out:that.check_out_day,
        }
      }).then(function (res){
        if(res.data.code === '1'){
          that.$message({message:'成功预定，请前往我的订单支付',type:'success'})
          that.show_book = false
        }else {
          that.$message({message:res.data.msg,type:'error'})
        }
      }).catch((err)=>{
        that.$message({message:err,type:'error'})
      })
    }
  },
  beforeMount() {
    let that = this
    axios.get(
        'api/get_room_Imf'
    ).then(function (response){
      if(response.data.code==='1'){
        that.rooms = response.data.data
        console.log(that.rooms)
        console.log(response)
      }
    })
  }

}

</script>

<style scoped>
.room_intro{
  font-family: 华文细黑;
}
li{
  font-size: 100%;
  width: 50%;
  float: left;
}
h3{
}
.el-dialog__wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>