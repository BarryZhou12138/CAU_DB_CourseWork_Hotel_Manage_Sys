<script setup>

</script>

<template>
  <div>
    <el-input v-model="sql" @keyup.enter="submit()" style="width: 60%;margin-left: 15%" placeholder="需要执行的sql语句"></el-input>
    <el-button @click="submit()"  style="margin-left: 3%">执行</el-button>
    <p style="margin-left: 15%"> 运行结果:</p>
    <el-input type="textarea" autosize v-model="return_data" style="margin-left: 15%;width: 60%;height: 60%"></el-input>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name:'admin',
  data(){
    return{
      return_data:{},
      sql:''
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
    submit(){
      let that = this
      console.log(this.sql)
      axios.get('/api/admin_db_operations',{
        params:{
          admin:localStorage.getItem('username'),
          password:localStorage.getItem('password'),
          sql:that.sql
        }
      }).then(function (res){
        if(res.data.code === '1'){
          that.return_data = JSON.stringify(res.data,null, '\t')
          console.log('成功'+that.return_data)
        }else{
          that.return_data = JSON.stringify(res.data,null, '\t')
          console.log('失败'+that.return_data)
        }
      })
    }
  }
}
</script>

<style scoped>

</style>