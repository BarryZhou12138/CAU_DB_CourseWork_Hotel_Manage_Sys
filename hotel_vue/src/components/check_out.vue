<template>

  <div class="food-container">
    <el-container style="width: 85%">
      <el-header style="margin-left: 10%;margin-bottom: 0px">
        <p style="float: left;margin-left: 15%"> <strong>今日要退房的房间订单</strong> </p>
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


              <div><el-button @click="openChangeRoomDialog(order)" type="danger">更换房间</el-button></div>
              <div><el-button @click="openCheckOutDialog(order)" type="success">退房</el-button></div>
              <div><el-button @click="queryUser(order.phone)" type="primary">查询用户信息</el-button></div>
              <div><el-button @click="open_update(order)" type="warning">修改退房日期</el-button></div>
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
    <el-dialog title="修改退房时间" v-model="show_update" style="width: 25%;text-align: center" >
      <el-form :model="update_form">
        <el-form-item label="新的退房日期" >
        <el-date-picker v-model="update_form.new_checkout_date"  value-format="YYYY-MM-DD" type="date" placeholder="选择新的退房日期"></el-date-picker>
      </el-form-item>
        <el-form-item label="订单编号" >
          <el-input v-model="update_form.order_id"></el-input>
        </el-form-item>

      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="show_update = false">取消</el-button>
        <el-button type="primary" @click="commit_update">确认修改</el-button>
      </div>
    </el-dialog>
    <el-dialog title="换房操作" v-model="showChangeRoomDialog" style="text-align: center;width: 30%">
      <el-form :model="changeRoomForm">
        <el-form-item label="订单编号" >
          <el-input v-model="changeRoomForm.order_id"></el-input>
        </el-form-item>
        <el-form-item label="新的房间编号" >
          <el-select v-model="changeRoomForm.new_room_id">
            <el-option v-for="room in rooms" :key="room[0]" :value="room[0]" :label="room[0]">{{room[0]}}</el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="showChangeRoomDialog = false">取消</el-button>
        <el-button type="primary" @click="commitChangeRoom">确认换房</el-button>
      </div>
    </el-dialog>
    <el-dialog title="退房登记" v-model="showCheckOutDialog"  style="width: 30%;text-align: center">
      <el-form :model="checkOutForm">
        <el-form-item label="退房日期" >
        <el-date-picker v-model="checkOutForm.checkout_date" type="date" placeholder="选择退房日期"></el-date-picker>
      </el-form-item>
        <el-form-item label="订单编号" >
          <el-input v-model="checkOutForm.order_id"></el-input>
        </el-form-item>

        <el-form-item label="损坏费用" >
          <el-input v-model="checkOutForm.damage_fee" type="number"></el-input>
        </el-form-item>
        <el-form-item label="损坏情况描述" >
          <el-input v-model="checkOutForm.damage_description"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="showCheckOutDialog = false">取消</el-button>
        <el-button type="primary"  @click="commitCheckOut">确认退房</el-button>
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
      showCheckOutDialog: false,
      checkOutForm: {
        username: 'staff123', // 假设服务员的用户名
        password: 'staffpwd', // 假设服务员的密码
        order_id: '',
        checkout_date: '',
        damage_fee: 0.0,
        damage_description: '无'
      },
      showChangeRoomDialog: false,
      rooms:[],
      changeRoomForm: {
        username: 'staff123', // 假设服务员的用户名
        password: 'staffpwd', // 假设服务员的密码
        order_id: '',
        new_room_id: ''
      },
      is_showUserImf:false,
      orders: [{}],
      show_update: false,
      update_form: {
        username: 'staff123', // 假设服务员的用户名
        password: 'staffpwd', // 假设服务员的密码
        order_id: '',
        new_checkout_date: ''
      },
    }
  },
  methods: {
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
      console.log(`删除订单: ${orderId}`);
    },
    getCurrentDate() {
      let now = new Date();
      let year = now.getFullYear();
      let month = now.getMonth() + 1;
      let day = now.getDate();
      return year + "-" + month + "-" + day;
    },
    open_update(order) {
      this.show_update = true;
      this.update_form.order_id = order.order_id
      this.update_form.new_checkout_date = order.check_out
    },
    commit_update() {
      const params = {
        username:this.$store.state.username,
        password:this.$store.state.password,
        order_id: this.update_form.order_id,
        new_checkout_date: this.update_form.new_checkout_date
      };
      let that = this
      axios.get('/api/update_checkout_time', { params })
          .then(response => {
            const res = response.data;
            if (res.code === '1') {
              that.$message({message:'修改成功',type:'success'})
              this.show_update = false;
            } else {
              that.$message({message:res.msg,type:'info'})
            }
          })
          .catch(error => {
            ElMessage.error('退房时间修改失败');
          });
    },
    openChangeRoomDialog(order) {
      this.showChangeRoomDialog = true;
      this.changeRoomForm.order_id = order.order_id
      let that = this
      axios.get('/api/get_available_rooms',{
        params:{
          username:that.$store.state.username,
          password:that.$store.state.password,
          room_id: order.room_id,
        }
      }).then(response => {
        const res = response.data;
        if (res.code === '1') {
          that.rooms = res.data
        } else {
          ElMessage.error(res.msg);
        }
      })
          .catch(error => {
            ElMessage.error('换房失败');
          });
    },
    commitChangeRoom() {
      const params = {
        username: this.changeRoomForm.username,
        password: this.changeRoomForm.password,
        order_id: this.changeRoomForm.order_id,
        new_room_id: this.changeRoomForm.new_room_id
      };

      axios.get('api/change_room', { params })
          .then(response => {
            const res = response.data;
            if (res.code === '1') {

              ElMessage.success(res.msg);
              this.showChangeRoomDialog = false;
            } else {
              ElMessage.error(res.msg);
            }
          })
          .catch(error => {
            ElMessage.error('换房失败');
          });
    },
    openCheckOutDialog(order) {
      this.showCheckOutDialog = true;
      this.checkOutForm.checkout_date = this.getCurrentDate()
      this.checkOutForm.order_id = order.order_id
    },
    commitCheckOut() {
      const params = {
        username:this.$store.state.username,
        password:this.$store.state.password,
        checkout_date: this.checkOutForm.checkout_date,
        damage_fee: this.checkOutForm.damage_fee,
        damage_description: this.checkOutForm.damage_description,
        order_id: this.checkOutForm.order_id
      };
      let that = this
      axios.get('api/check_out', { params })
          .then(response => {
            const res = response.data;
            if (res.code === '1') {
              this.showCheckOutDialog = false;
              let cost = parseInt(res.data)
              let condition = '支付'
              if(cost<0){
                condition = '退款'
              }
              that.$messageBox({message:('需'+condition+':'+Math.abs(cost)+'元'),type:'info'})
            } else {
              ElMessage.error(res.msg);
            }
          })
          .catch(error => {
            ElMessage.error('退房登记失败');
          });
    },
  },

  mounted() {
    if (this.$store.state.loginType !== '2'){
      this.$router.push('/')
    }
    let that = this
    axios.get('/api/get_checkout_orders',{
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
