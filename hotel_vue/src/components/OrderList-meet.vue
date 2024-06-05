<script setup>
import jpg1 from '../../static/接送/1.jpg'
import jpg2 from '../../static/接送/2.jpg'
import jpg3 from '../../static/接送/3.jpg'
</script>
<template>
  <div>
    <div v-for="order in orders">
      <el-card  style="margin-bottom: 2%" v-if="order.meet_id==='1'">
        <div style="display: flex;">
          <img :src="jpg1" alt="dish image" style="width: 150px; height: 150px; margin-right: 20px;">
          <div style="flex-grow: 1;">
            <h3>{{ order.order_type }} (订单编号：{{order.meet_order_id}})</h3>
            <p>接送形式: 普通接送</p>
            <p>预定时间: {{ order.meet_time }}</p>
          </div>
          <div style="flex-grow: 1;width: 30%;margin-right: 3%" >
            <br>
            <p>接送地点：{{ order.location }}</p>
          </div>
          <el-button @click="handleEdit(order)" type="primary" :disabled="true">更改</el-button>
          <el-button @click="handleDelete(order)" type="danger" :disabled="true">删除</el-button>
          <el-button :disabled="true">
            支付
          </el-button>
        </div>
      </el-card>
      <el-card  style="margin-bottom: 2%" v-if="order.meet_id==='2'">
        <div style="display: flex;">
          <img :src="jpg2" alt="dish image" style="width: 150px; height: 150px; margin-right: 20px;">
          <div style="flex-grow: 1;">
            <h3>{{ order.order_type }} (订单编号：{{order.meet_order_id}})</h3>
            <p>接送形式: 公务接送</p>
            <p>预定时间: {{ order.meet_time }}</p>
          </div>
          <div style="flex-grow: 1;width: 30%;margin-right: 3%" >
            <br>
            <p>接送地点：{{ order.location }}</p>
          </div>
          <el-button @click="handleEdit(order)" type="primary" :disabled="true">更改</el-button>
          <el-button @click="handleDelete(order)" type="danger" :disabled="true">删除</el-button>
          <el-button :disabled="true">
            支付
          </el-button>
        </div>
      </el-card>
      <el-card  style="margin-bottom: 2%" v-if="order.meet_id==='3'">
        <div style="display: flex;">
          <img :src="jpg3" alt="dish image" style="width: 150px; height: 150px; margin-right: 20px;">
          <div style="flex-grow: 1;">
            <h3>{{ order.order_type }} (订单编号：{{order.meet_order_id}})</h3>
            <p>接送形式: 豪华接送</p>
            <p>预定时间: {{ order.meet_time }}</p>
          </div>
          <div style="flex-grow: 1;width: 30%;margin-right: 3%" >
            <br>
            <p>接送地点：{{ order.location }}</p>
          </div>
          <el-button @click="handleEdit(order)" type="primary" :disabled="true">更改</el-button>
          <el-button @click="handleDelete(order)" type="danger" :disabled="true">删除</el-button>
          <el-button :disabled="true">
            支付
          </el-button>
        </div>
      </el-card>
    </div>
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
