<script setup>
import {
  Check,
  Delete,
  Edit,
  Message,
  Search,
  Star,
} from '@element-plus/icons-vue'
</script>

<template>
  <div>
    <div style="margin-left: 20%;margin-top: 1%">
      <p style="display: inline-block;margin-right: 2%">选择展示表单</p>
      <div style="display: inline-block">
        <el-button @click="show_room()">房间表</el-button>
        <el-button @click="show_room_type()">房型表</el-button>
        <el-button @click="show_user()">用户表</el-button>
        <el-button type="primary" :icon="Edit" circle @click="show_add = true"/>
        <el-button type="danger" @click="show_delete = true" :icon="Delete" circle />
      </div>

    </div>

    <div style="margin-left: 15%;width: 70%">
      <el-table v-if="show_table === '房间表'" :data="mounted_data" >
        <el-table-column label="房间号" :prop="'房间号'" width="100px"></el-table-column>
        <el-table-column label="房型号" :prop="'房型号'"  width="100px"></el-table-column>
        <el-table-column label="房间状态" :prop="'房间状态'"  width="100px"></el-table-column>
      </el-table>

      <el-table v-if="show_table === '房型表'" :data="mounted_data" >
        <el-table-column label="房型号" :prop="'房型号'"></el-table-column>
        <el-table-column label="房型类别" :prop="'房型类别'"></el-table-column>
        <el-table-column label="房型价格" :prop="'房型价格'"></el-table-column>
        <el-table-column label="房型数量" :prop="'房型数量'"></el-table-column>
        <el-table-column label="面积" :prop="'面积'"></el-table-column>
        <el-table-column label="床" :prop="'床'" width="200px"></el-table-column>
        <el-table-column label="每日打扫" :prop="'每日打扫'"></el-table-column>
        <el-table-column label="牙刷" :prop="'牙刷'"></el-table-column>
        <el-table-column label="牙膏" :prop="'牙膏'"></el-table-column>
        <el-table-column label="沐浴露" :prop="'沐浴露'"></el-table-column>
        <el-table-column label="洗发水" :prop="'洗发水'"></el-table-column>
        <el-table-column label="免费wifi" :prop="'免费wifi'"></el-table-column>
        <el-table-column label="电视" :prop="'电视'"></el-table-column>
        <el-table-column label="毛巾" :prop="'毛巾'"></el-table-column>
        <el-table-column label="私人卫浴" :prop="'私人卫浴'"></el-table-column>
        <el-table-column label="吹风机" :prop="'吹风机'"></el-table-column>
        <el-table-column label="房型介绍" :prop="'房型介绍'" width="200px"></el-table-column>
      </el-table>

      <el-table v-if="show_table === '用户表'" :data="mounted_data">
          <el-table-column label="用户ID" :prop="'用户ID'" width="200px"></el-table-column>
          <el-table-column label="用户名" :prop="'用户名'" width="200px"></el-table-column>
          <el-table-column label="姓名" :prop="'姓名'" ></el-table-column>
          <el-table-column label="证件号码" :prop="'证件号码'" width="200px"></el-table-column>
          <el-table-column label="年龄" :prop="'年龄'"></el-table-column>
          <el-table-column label="证件类型" :prop="'证件类型'" ></el-table-column>
          <el-table-column label="性别" :prop="'性别'"></el-table-column>
          <el-table-column label="联系电话" :prop="'联系电话'" width="200px"></el-table-column>
          <el-table-column label="邮箱" :prop="'邮箱'" width="200px"></el-table-column>
      </el-table>




    </div>
    <el-dialog v-model="show_delete" width="30%">
      <p>请输入删除的{{show_table[0]}}{{show_table[1]}}id</p>
      <el-input style="width: 70%;" v-model="delete_value"></el-input>
      <el-button style="margin-left: 3%" @click="delete_item()">删除</el-button>
    </el-dialog>
    <el-dialog v-model="show_add" width="30%">
      <p>请输入新增的数据</p>
      <p>格式 "值1","值2","值3"</p>
      <el-input style="width: 70%;" v-model="add_value"></el-input>
      <el-button style="margin-left: 3%" @click="add_item()">增加</el-button>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name:'admin',
  data(){
    return{
      room_type_table:[],
      room_table:[],
      user_table:[],
      order_table:[],
      sql:'',
      mounted_data:{},
      show_table:'',
      show_delete:false,
      show_insert:false,
      delete_value:'',
      show_add:false,
      add_value:'',
    }
  },
  mounted() {
    let  that = this
    axios.get('/api/login',{
      params:{
        username:localStorage.getItem('username'),
        password:localStorage.getItem('password'),
        loginType:'3',
      }
    }).then(function (res){
      if( res.data.code === '0' ){
        that.$router.push('/')
      }
    })
  },
  methods:{
    show_room(){
      let sql = "select * from 房间表"
      let that = this
      axios.get('/api/admin_db_operations',{
        params:{
          username:that.$store.state.username,
          password:that.$store.state.password,
          sql:sql
        }
      }).then((res)=>{
        if(res.data.code === '1') {
          console.log('success')
          that.room_table = []
          res.data.data.forEach(element => {
            that.room_table.push({
              '房间号': element[0],
              '房型号': element[1],
              '房间状态': element[2],
            })
          })
        }else {
          that.$message({message:res.data.msg,type:'error'})
        }
      }).then(res=>{
        that.mounted_data = this.room_table
        that.show_table = '房间表'
      })

    },
    show_room_type(){
      let sql = "select * from 房型表"
      let that = this
      axios.get('/api/admin_db_operations',{
        params:{
          username:that.$store.state.username,
          password:that.$store.state.password,
          sql:sql
        }
      }).then((res)=>{
        if(res.data.code === '1') {
          console.log('success')
          that.room_type_table = []
          res.data.data.forEach(element => {
            that.room_type_table.push({
              '房型号': element[0],
              '房型类别': element[1],
              '房型价格': element[2],
              '房型数量': element[3],
              '面积': element[4],
              '床': element[5],
              '每日打扫': element[6],
              '牙刷': element[7],
              '牙膏': element[8],
              '沐浴露': element[9],
              '洗发水': element[10],
              '免费wifi': element[11],
              '电视': element[12],
              '毛巾': element[13],
              '私人卫浴': element[14],
              '吹风机': element[15],
              '房型介绍': element[16],
            })
          })
        }else {
          that.$message({message:res.data.msg,type:'error'})
        }
      }).then(res=>{
        that.mounted_data = this.room_type_table
        that.show_table = '房型表'
      })
    },
    show_user(){
      let sql = "select * from 用户表"
      let that = this
      axios.get('/api/admin_db_operations',{
        params:{
          username:that.$store.state.username,
          password:that.$store.state.password,
          sql:sql
        }
      }).then((res)=>{
        if(res.data.code === '1') {
          console.log('success')
          that.user_table = []
          res.data.data.forEach(element => {
            that.user_table.push({
              '用户ID': element[0],
              '用户名': element[1],
              '姓名': element[2],
              '证件号码': element[3],
              '年龄': element[4],
              '证件类型': element[5],
              '性别': element[6],
              '联系电话': element[7],
              '邮箱': element[8],
            })
          })
        }else {
          that.$message({message:res.data.msg,type:'error'})
        }
      }).then(res=>{
        that.mounted_data = this.user_table
        that.show_table = '用户表'
      })

    },
    show_order(){
      let sql = "select * from 订单表"
      let that = this
      axios.get('/api/admin_db_operations',{
        params:{
          username:that.$store.state.username,
          password:that.$store.state.password,
          sql:sql
        }
      }).then((res)=>{
        if(res.data.code === '1') {
          console.log('success')
          that.order_table = []
          res.data.data.forEach(element => {
            that.order_table.push({
              '订单编号': element[0],
              '用户ID': element[1],
              '房型号': element[2],
              '证件号码': element[3],
              '预计入住日期': element[4],
              '预计离开日期': element[5],
              '预计住宿费用': element[6],
              '定金支付状态': element[7],
            })
          })
        }else {
          that.$message({message:res.data.msg,type:'error'})
        }
      }).then(res=>{
        that.mounted_data = this.order_table
        that.show_table = '订单表'
      })

    },
    delete_item(){
      let sql
      if(this.show_table === '房型表'){
        sql = "delete from 房型表 where 房型号="+this.delete_value
      }else if(this.show_table === '房间表'){
        sql = "delete from 房间表 where 房间号="+this.delete_value
      }else if(this.show_table === '用户表'){
        sql = "delete from 用户表 where 用户ID='"+this.delete_value+"'"
      }else {
        return
      }

      let that = this
      axios.get('/api/admin_db_operations',{
        params:{
          username:that.$store.state.username,
          password:that.$store.state.password,
          sql:sql
        }
      }).then((res)=>{
        if(res.data.code === '1') {
          location.reload()
          that.$message({message:'删除成功',type:'success'})
        }else {
          that.$message({message:res.data.msg,type:'error'})
        }
      })
    },
    add_item(){
      let sql
      if(this.show_table === '房型表'){
        sql = "insert into 房型表 value("+this.add_value+")"
      }else if(this.show_table === '房间表'){
        sql = "insert into 房间表 value("+this.add_value+")"
      }else if(this.show_table === '用户表'){
        sql = "insert into 用户表 value("+this.add_value+")"
      }else {
        return
      }

      let that = this
      axios.get('/api/admin_db_operations',{
        params:{
          username:that.$store.state.username,
          password:that.$store.state.password,
          sql:sql
        }
      }).then((res)=>{
        if(res.data.code === '1') {
          location.reload()
          that.$message({message:'添加成功',type:'success'})
        }else {
          that.$message({message:res.data.msg,type:'error'})
        }
      })
    }
  }
}
</script>

<style scoped>

</style>