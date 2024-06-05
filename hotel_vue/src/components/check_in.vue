<template>

  <div class="food-container">
    <el-container style="width: 85%">
      <el-header style="margin-left: 10%;margin-bottom: 0px">
        <p style="float: left;margin-left: 15%"> <strong>今日要入住的房间订单</strong> </p>
        <p style="float: left;margin-left: 3%"> 用户的联系电话: </p>
        <el-input v-model="check_phone" style="float: left;margin-top: 10px;width: 200px;margin-left: 2%" ></el-input>
        <el-button style="float: left;margin-top: 10px;margin-left: 3%" @click="orders = this.all_orders.filter(order => order.phone === check_phone)">查询该用户的订单</el-button>
        <el-button style="float: left;margin-top: 10px;margin-left: 3%" @click="orders = all_orders">所有订单</el-button>
      </el-header>
      <el-main style="margin-left: 15%">
        <el-card class="transport-card" v-for="order in orders" :key="order.order_id">
          <div class="transport-content">
            <div class="transport-description">
              <p><strong>房间类型：</strong>{{ order.room_type }}</p>
              <p><strong>用户真实姓名：</strong>{{ order.real_name }}</p>
              <p><strong>订单id：</strong>{{ order.order_id }}</p>
            </div>
            <div class="transport-description" >
              <p><strong>联系电话：</strong>{{ order.phone }}</p>
              <p><strong>入住日期：</strong>{{ order.check_in }}</p>
              <p><strong>退房日期：</strong>{{ order.check_out }}</p>
            </div>
            <div class="transport-description" style="margin-left: 10%;text-align: center">

              <div><el-button @click="openUpdate(order)" type="warning">修改订单</el-button></div>
              <div><el-button @click="deleteOrder(order.order_id)" type="danger">删除订单</el-button></div>
              <div><el-button @click="openDialog(order.order_id,order.real_name,order.room_id)" type="success">入住</el-button></div>
              <div><el-button @click="queryUser(order.phone)" type="primary">查询用户信息</el-button></div>
            </div>
          </div>
        </el-card>
      </el-main>
    </el-container>
    <el-dialog v-model="is_showUserImf" style="width:45%;">
      <div class="transport-content">
        <div class="transport-description">
          <p style="font-size: 20px"><strong>用户名：</strong>{{User_Imf[0][1]}}</p>
          <p style="font-size: 20px"><strong>证件类型：</strong>{{User_Imf[0][5]}}</p>
          <p style="font-size: 20px"><strong>证件号：</strong><br> <br>{{User_Imf[0][3]}}</p>



        </div>
        <div class="transport-description">
          <p style="font-size: 20px"><strong>真实姓名：</strong>{{User_Imf[0][2]}}</p>
          <p style="font-size: 20px"><strong>性别：</strong>{{User_Imf[0][6]}}</p>
          <p style="font-size: 20px"><strong>手机号：</strong>{{User_Imf[0][7]}}</p>
          <p style="font-size: 20px"><strong>邮箱：</strong>{{User_Imf[0][8]}}</p>
        </div>
      </div>
    </el-dialog>
    <el-dialog title="入住登记" v-model="dialogVisible" width="50%" style="width: 30%;text-align: center;" >
      <el-form :model="form">
        <el-form-item label="入住日期" >
          <el-date-picker v-model="form.check_in_date" type="date" placeholder="选择入住日期"></el-date-picker>
        </el-form-item>
        <el-form-item label="房间号码">
          <el-select v-model="form.room_id" >
            <el-option v-for="room in rooms" :key="room[0]" :label="room[0]" :value="room[0]">
            {{room[0]}}
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="真实姓名" >
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="证件号码" >
          <el-input v-model="form.id_number"></el-input>
        </el-form-item>
        <el-form-item label="入住押金" >
          <el-input v-model="form.deposit" type="number"></el-input>
        </el-form-item>
        <el-form-item label="预计退房日期" >
          <el-date-picker v-model="form.expected_check_out_date" value-format="YYYY-MM-DD" type="date" placeholder="选择预计退房日期"></el-date-picker>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="checkIn()">确认入住</el-button>
      </div>
    </el-dialog>
    <el-dialog title="更改订单" v-model="show_update" width="50%" style="text-align: center;width: 30%">
      <el-form :model="update_form">

        <el-form-item label="入住日期" >
          <el-date-picker v-model="update_form.check_in" value-format="YYYY-MM-DD" type="date" placeholder="选择入住日期"></el-date-picker>
        </el-form-item>
        <el-form-item label="退房日期" >
          <el-date-picker v-model="update_form.check_out" value-format="YYYY-MM-DD" type="date" placeholder="选择退房日期"></el-date-picker>
        </el-form-item>
        <el-form-item label="入住房型" >
          <el-select v-model="update_form.new_room_type">
            <el-option v-for="room in all_rooms" :value="room.room_type" :label="room.room_type">{{room.room_type}}</el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="订单编号" >
          <el-input v-model="update_form.order_id"></el-input>
        </el-form-item>

      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="show_update = false">取消</el-button>
        <el-button type="primary" @click="updateOrder">确认更改</el-button>
      </div>
    </el-dialog>
  </div>
</template>


<script>


import axios from "axios";
import {ElMessage} from "element-plus";

export default {
  data() {
    return {
      show_update:false,
      all_rooms:[],
      update_form: {
        username: 'staff123', // 假设服务员的用户名
        password: 'staffpwd', // 假设服务员的密码
        order_id: '',
        check_in: '',
        check_out: '',
        new_room_type: ''
      },
      is_showUserImf:false,
      dialogVisible: false,
      is_showCheck_In:false,
      User_Imf:[],
      check_phone:'',
      orders: [{}],
      all_orders:[{}],
      rooms:[],
      form: {
        order_id: 'RO123456789', // 假设的订单编号
        room_id: '',
        id_number: '',
        name: '',
        check_in_date: new Date(),
        deposit: 200.00,
        expected_check_out_date: ''
      }

    }
  },
  methods: {
    openUpdate(order) {
      this.show_update = true;
      this.update_form.check_in = order.check_in
      this.update_form.check_out = order.check_out
      this.update_form.order_id = order.order_id
    },
    updateOrder() {
      const params = {
        username:this.$store.state.username,
        password:this.$store.state.password,
        order_id: this.update_form.order_id,
        check_in: this.update_form.check_in,
        check_out: this.update_form.check_out,
        new_room_type: this.update_form.new_room_type
      };

      axios.get('/api/update_order_by_staff', { params })
          .then(response => {
            const res = response.data;
            if (res.code === '1') {
              ElMessage.success(res.msg);
              location.reload()
              this.show_update = false;
            } else {
              ElMessage.error(res.msg);
            }
          })
          .catch(error => {
            ElMessage.error('订单更改失败');
          });
    },
    openDialog(id,real_name,room_id) {
      console.log(id)
      this.dialogVisible = true;
      this.form.order_id = id
      this.form.name = real_name
      let that = this
      axios.get('/api/get_available_rooms',{
        params:{
          username:that.$store.state.username,
          password:that.$store.state.password,
          room_id:room_id
        }
      }).then((res)=>{
        if(res.data.code === '1'){
          that.rooms = res.data.data
        }else{
          that.$message({message:res.data.msg,type:'error'})
        }
      }).catch((err)=>{
        that.$message({message:'查询失败',type:'error'})
      })
    },
    queryUser(phone) {
      // 查询用户信息逻辑
      let that = this
      axios.get('/api/get_user_info_by_phone',{
        params:{
          username:that.$store.state.username,
          password:that.$store.state.password,
          phone:phone,
        }
      }).then(function (res){
        if(res.data.code === '1'){
          that.User_Imf = res.data.data
          that.is_showUserImf = true
        }else {
          that.$message({message:res.data.msg,type:'error'})
        }
      }).catch((err)=>{
        that.$message({message:'查询失败',type:'error'})
      })
    },
    editOrder(orderId) {
      // 修改订单逻辑
      console.log(`修改订单: ${orderId}`);
    },
    deleteOrder(orderId) {
      // 删除订单逻辑
      let that = this
      that.$messageBox.confirm(
          '删除订单会删除相关接送订单和餐食订单，是否删除？',
          'Warning',
          {
            confirmButtonText: '删除',
            cancelButtonText: '取消',
            type: 'warning',
          }
      ).then(() => {

        axios.get('/api/delete_order_by_staff',{
          params:{
            username:that.$store.state.username,
            password:that.$store.state.password,
            orderId:orderId,
          }
        }).then(function (res){
          if(res.data.code === '1'){
            that.$message({message:'删除成功，已经支付的金额会原路返回',type:'success'})
            location.reload()
          }else {
            that.$message({message:res.data.msg,type:'error'})
          }
        }).catch((err)=>{
          that.$message({message:'删除失败',type:'error'})
        })
      })


    },
    checkIn() {
      const params = {
        username:this.$store.state.username,
        password:this.$store.state.password,
        order_id:this.form.order_id,
        room_id: this.form.room_id,
        id_number: this.form.id_number,
        name: this.form.name,
        check_in_date: this.getCurrentDate(),
        deposit: this.form.deposit,
        expected_check_out_date: this.form.expected_check_out_date
      };
      let that = this
      axios.get('api/check_in', { params })
          .then(res => {
            if (res.data.code === '1') {
              that.$message({message:'入住成功',type:'success'})
              this.dialogVisible = false;
              location.reload()
            } else {
              that.$message({message:res.data.msg,type:'error'})
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
    axios.get('/api/get_checkin_orders',{
      params:{
        date:that.getCurrentDate(),
        username:that.$store.state.username,
        password:that.$store.state.password,
      }
    }).then((res)=>{
      if(res.data.code === '1'){
        that.orders = res.data.data
        that.all_orders = res.data.data
      }else {
        that.$message({message:res.data.msg,type:'info'})
      }
    })
    axios.get('/api/get_room_Imf').then(res=>{
      if(res.data.code === '1'){
        that.all_rooms = res.data.data
      }
    })
  }
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
