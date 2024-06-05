<template>
  <el-container style="width: 85%">
    <el-aside style="width: 5%"></el-aside>
    <el-main >

      <el-tabs tab-position="left" v-model="activeTab" style="margin-top: 1%;margin-left: 3%">
        <el-tab-pane label="房间订单" name="房间订单">
          <OrderList_room style="margin-left: 3%;margin-top: 0px;margin-right: 5%"
                          v-if="activeTab === '房间订单'"
                          :orders="filteredOrders(activeTab)"
                          @modify="modifyOrder"
                          @delete="deleteOrder"
                          @pay="payOrder" />
        </el-tab-pane>
        <el-tab-pane label="接送订单" name="接送订单">
          <OrderListMeet style="margin-left: 3%;margin-top: 0px;margin-right: 5%"
                         v-if="activeTab === '接送订单'"
                         :orders="filteredOrders(activeTab)"
                         @modify="modifyOrder"
                         @delete="deleteOrder"
                         @pay="payOrder" />
        </el-tab-pane>
        <el-tab-pane label="餐品订单" name="餐品订单">
          <OrderListFood style="margin-left: 3%;margin-top: 0px;margin-right: 5%"
                         v-if="activeTab === '餐品订单'"
                         :orders="filteredOrders(activeTab)"
                         @modify="modifyOrder"
                         @delete="deleteOrder"
                         @pay="payOrder" />
        </el-tab-pane>
      </el-tabs>




    </el-main>
  </el-container>
</template>

<script>
import OrderList_room from './OrderList-room.vue';
import OrderListMeet from "@/components/OrderList-meet.vue";
import OrderListFood from "@/components/OrderList-food.vue";
import axios from "axios";

export default {
  components: { OrderList_room,OrderListMeet,OrderListFood},
  data() {
    return {
      activeTab: '房间订单',
      orders: [
        { id: 1, name: 'Order 1', paid: true },
        { id: 2, name: 'Order 2', paid: false },
        { id: 3, name: 'Order 3', paid: true },
        { id: 4, name: 'Order 4', paid: false }
      ]
    };
  },
  methods: {
    filteredOrders(type) {
      if (type === '房间订单') return this.orders.filter(order => order.order_type === '房间订单');
      if (type === '接送订单') return this.orders.filter(order => (order.order_type === '接站订单' || order.order_type==='送站订单'));
      if (type === '餐品订单') return this.orders.filter(order => order.order_type === '食品订单');
    },
    modifyOrder(order) {
      console.log('Modify order:', order);
      // Add your modify logic here
    },
    deleteOrder(order) {
      console.log('Delete order:', order);
      // Add your delete logic here
    },
    payOrder(order) {
      console.log('Pay order:', order);
      // Add your pay logic here
    }
  },
  mounted() {
    let that = this
    if (this.$store.state.is_login === false){
      this.$router.push('/')
      this.$message({message:'请先登录',type:'info'})
      return
    }

    axios.get('/api/get_user_orders',{
      params:{
        username:that.$store.state.username,
        password:that.$store.state.password
      }
    }).then(function (res){
      if(res.data.code === '1'){
        that.orders = JSON.parse(res.data.data)
        console.log(that.orders)
      }else{
        that.$message({message:res.data.msg,type:'info'})
      }
    }).catch((err)=>{
      that.$message({message:'获取失败',type:'info'})
    })
  }
};
</script>
