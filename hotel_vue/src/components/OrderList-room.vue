<template>
  <div>
    <el-card v-for="order in orders" style="margin-bottom: 2%">
      <div style="display: flex;">
        <img :src="'/api/get_room_picture?id='+order.room_id" alt="room image" style="width: 150px; height: 150px; margin-right: 20px;">
        <div style="width: 30%">
          <h3>{{ order.room_type }} (订单编号：{{order.room_order_id}})</h3>
          <p>预计入住时间: {{ order.check_in }}</p>
          <p>预计退房时间: {{ order.check_out }}</p>
        </div>
        <div style="flex-grow: 1;">
          <h3>房型介绍</h3>
          <p>{{ order.room_intro ? order.room_intro : "无房型介绍" }}</p>
          <p>预计住宿金额：{{order. deposit}}</p>
        </div>
        <div>
          <el-button @click="openDialog(order)" type="primary">更改</el-button>
          <el-button @click="handleDelete(order)" type="danger">删除</el-button>
          <el-button
              @click="handlePay(order)"
              :disabled="order.支付状态 === '已支付'"
              type="success">
            支付
          </el-button>
        </div>
      </div>
    </el-card>
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
  props: {
    orders: {
      type: Array,
      required: true
    }
  },
  data(){
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
      }
    }
  },
  methods:{
    openDialog(order) {
      this.show_update = true;
      this.update_form.check_in = order.check_in
      this.update_form.check_out = order.check_out
      this.update_form.order_id = order.room_order_id
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

      axios.get('/api/update_order_by_user', { params })
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
    formatDate(date) {
      const d = new Date(date);
      const month = '' + (d.getMonth() + 1);
      const day = '' + d.getDate();
      const year = d.getFullYear();

      return [year, month.padStart(2, '0'), day.padStart(2, '0')].join('-');
    },
    handlePay(order){
      let that = this
      axios.get('/api/pay_order',{
        params:{
          username:that.$store.state.username,
          password:that.$store.state.password,
          order_id:order.room_order_id,
        }
      }).then((res)=>{
        if(res.data.code === '1'){
          order.支付状态 = '已支付'
          that.$message({message:'成功支付',type:'success'})
        }else {
          that.$message({message:res.data.msg,type:'info'})
        }
      }).catch(err=>{
        that.$message({message:'支付失败',type:'info'})
      })
    },
    handleDelete(order){
      let that = this
      that.$messageBox.confirm(
          '删除订单会删除相关接送订单和餐食订单，是否删除？如果您删除订单的时间距离入住时间小于24小时，将会扣除50元手续费',
          'Warning',
          {
            confirmButtonText: '删除',
            cancelButtonText: '取消',
            type: 'warning',
          }
      ).then(() => {
            axios.get('/api/remove_order',{
              params:{
                username:that.$store.state.username,
                password:that.$store.state.password,
                order_id:order.room_order_id,
              }
            }).then((res)=>{
              if(res.data.code === '1'){
                that.$message({message:'删除成功,已支付的金额将原路退回',type:'success'})
                location.reload()
              }else {
                that.$message({message:res.data.msg,type:'info'})
              }
            }).catch(err=>{
              that.$message({message:'删除失败',type:'info'})
            })
          })
          .catch(() => {
          })

    },
  },
  mounted() {
    let that = this
    axios.get('/api/get_room_Imf').then(res=>{
      if(res.data.code === '1'){
        that.all_rooms = res.data.data
      }
    })
  }
};
</script>
