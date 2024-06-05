<template>
  <div>
    <el-card v-for="order in orders" style="margin-bottom: 2%">
      <div style="display: flex;">
        <img :src="'/api/get_dish_picture?id='+order.dish_id" alt="dish image" style="width: 150px; height: 150px; margin-right: 20px;">
        <div style="flex-grow: 1;">
          <h3>{{ order.dish_name }} (订单编号：{{order.food_order_id}})</h3>
          <p>预定数量: {{ order.quantity }}</p>
          <p>预定时间: {{ order.order_time }}</p>
        </div>
        <div style="flex-grow: 1;width: 30%">
          <h3>菜品介绍</h3>
          <p>{{ order.dish_intro ? order.dish_intro : "无菜品介绍" }}</p>
        </div>
        <el-button @click="handleEdit(order)" type="primary" :disabled="true">更改</el-button>
        <el-button @click="handleDelete(order)" type="danger" :disabled="true">删除</el-button>
        <el-button :disabled="true">
          支付
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  props: {
    orders: {
      type: Array,
      required: true
    }
  }
};
</script>
