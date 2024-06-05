<template>
  <div class="food-container">
    <el-container style="width: 85%">
      <el-header style="margin-left: 10%;margin-bottom: 0px">
        <p style="float: left;margin-left: 15%"> 用户的联系电话: </p>
        <el-input v-model="check_phone" style="float: left;margin-top: 10px;width: 200px;margin-left: 2%" ></el-input>
        <el-button style="float: left;margin-top: 10px;margin-left: 3%" @click="orders = this.all_orders.filter(order => order.phone === check_phone)">查询该用户的订单</el-button>
        <el-button style="float: left;margin-top: 10px;margin-left: 3%" @click="orders = all_orders">所有订单</el-button>
      </el-header>

      <el-main style="margin-left: 15%">
        <el-card class="transport-card" v-for="order in orders" :key="order.order_id">
          <div class="transport-content">
            <div class="transport-description">
              <p><strong>订单类型：</strong>{{ order.meet_type }}({{order.meet_action}})</p>
              <p><strong>真实姓名：</strong>{{ order.real_name }}</p>
              <p><strong>订单id：</strong>{{ order.order_id }}</p>
            </div>
            <div class="transport-description" >
              <p><strong>联系电话：</strong>{{ order.phone }}</p>
              <p><strong>接送地点：</strong>{{ order.meet_location }}</p>
              <p><strong>接送时间：</strong>{{ order.meet_date }}-{{order.meet_time}}</p>
            </div>
            <div class="transport-description" style="margin-left: 10%;text-align: center">

              <div><el-button  disabled type="warning">修改订单</el-button></div>
              <div><el-button disabled type="danger">删除订单</el-button></div>
              <div><el-button @click="finish(order.order_id,order.meet_action)" type="success">完成订单</el-button></div>

            </div>
          </div>
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>


<script>


import axios from "axios";

export default {
  data() {
    return {
      orders: [{}],
    }
  },
  methods: {
    finish(id,action){
      let that = this
      axios.get('/api/Complete_meet_order',{
        params:{
          meet_id:id,
          meet_type:action[0],
          username:that.$store.state.username,
          password:that.$store.state.password,
        }
      }).then(res=>{
        if(res.data.code === '1'){
          that.$message({message:'完成成功',type:'success'})
          location.reload()
        }else{
          that.$message({message:res.data.msg,type:'info'})
        }
      })
    },
    getCurrentDate() {
      let now = new Date();
      let year = now.getFullYear();
      let month = now.getMonth() + 1;
      let day = now.getDate();
      return year + "-" + month + "-" + day;
    }
  },

  mounted() {
    if (this.$store.state.loginType !== '2'){
      this.$router.push('/')
    }
    let that = this
    axios.get('/api/get_meet_orders',{
      params:{
        date:that.getCurrentDate(),
        username:that.$store.state.username,
        password:that.$store.state.password,
      }
    }).then((res)=>{
      if(res.data.code === '1'){
        that.orders = res.data.data
      }else {
        that.$message({message:res.data.msg,type:'info'})
      }
    })
  },


};
</script>

<style scoped>
.transport-services {
  display: flex;
  justify-content: space-between;
}

.transport-card {
  margin-bottom: 20px;
}

.transport-title {
  font-size: 20px;
  font-weight: bold;
}

.transport-content {
  display: flex;
  align-items: center;
}


.transport-description {
  flex: 1; /* 让描述部分占据剩余空间 */
  margin-left: 5%;
}

.el-button {
  margin-top: 10px;
}
</style>
