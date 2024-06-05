<template>
  <div class="food-container">
    <el-container style="width: 85%">
      <el-aside style="width: 5%">
      </el-aside>
      <el-main >
        <el-tabs v-model="activeTab" tab-position="left">
          <el-tab-pane label="早餐预定" name="breakfast">
            <div class="food-list" style="width: 100%" >
              <el-card class="food-card" v-for="dish in getDishesByType('早餐')" :key="dish.dish_id" style="width: 100%">
                <div slot="header" class="food-title">{{ dish.dish_name }}</div>
                <div class="food-content">
                  <img :src="'api/get_dish_picture?dish_id=' + dish.dish_id" alt="food image" class="food-image">
                  <div class="food-details">
                    <p><strong>类型：</strong>{{ dish.dish_type }} </p>
                    <p><strong>价格：</strong>￥{{ dish.dish_price }}</p>
                    <p><strong>口味：</strong>{{ dish.dish_taste }}</p>
                    <p><strong>介绍：</strong>{{ dish.date_intro }}</p>
                    <el-button type="primary" style="float: left" @click="openReserveDialog(dish.dish_id)">预定</el-button>
                  </div>
                </div>
              </el-card>
            </div>
          </el-tab-pane>
          <el-tab-pane label="午餐预定" name="lunch">
            <div class="food-list" style="width: 100%">
              <el-card class="food-card" v-for="dish in getDishesByType('午餐')" :key="dish.dish_id" style="width: 100%">
                <div slot="header" class="food-title">{{ dish.dish_name }}</div>
                <div class="food-content">
                  <img :src="'api/get_dish_picture?dish_id=' + dish.dish_id" alt="food image" class="food-image">
                  <div class="food-details">
                    <p><strong>类型：</strong>{{ dish.dish_type }}</p>
                    <p><strong>价格：</strong>￥{{ dish.dish_price }}</p>
                    <p><strong>口味：</strong>{{ dish.dish_taste }}</p>
                    <p><strong>介绍：</strong>{{ dish.date_intro }}</p>
                    <el-button type="primary" @click="openReserveDialog(dish.dish_id)">预定</el-button>
                  </div>
                </div>
              </el-card>
            </div>
          </el-tab-pane>
          <el-tab-pane label="晚餐预定" name="dinner">
            <div class="food-list" style="width: 100%">
              <el-card class="food-card" v-for="dish in getDishesByType('晚餐')" :key="dish.dish_id" style="width: 100%">
                <div slot="header" class="food-title">{{ dish.dish_name }}</div>
                <div class="food-content">
                  <img :src="'api/get_dish_picture?dish_id=' + dish.dish_id" alt="food image" class="food-image">
                  <div class="food-details">
                    <p><strong>类型：</strong>{{ dish.dish_type }}</p>
                    <p><strong>价格：</strong>￥{{ dish.dish_price }}</p>
                    <p><strong>口味：</strong>{{ dish.dish_taste }}</p>
                    <p><strong>介绍：</strong>{{ dish.date_intro }}</p>
                    <el-button type="primary" style="width: 40%;" @click="openReserveDialog(dish.dish_id)">预定</el-button>
                  </div>
                </div>
              </el-card>
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-main>
    </el-container>
    <el-dialog v-model="dialogVisible"  width="30%">
      <el-form ref="reserveForm" :model="reserveForm" style="margin-top: 3%;margin-left: 5%;margin-right: 5%">
        <el-form-item label="选择菜品" >
          <el-select v-model="reserveForm.dish_id" placeholder="请选择菜品">
            <el-option v-for="dish in dishes" :key="dish.dish_id" :label="dish.dish_name" :value="dish.dish_id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="菜品数量">
          <el-input v-model="reserveForm.quantity" type="number"></el-input>
        </el-form-item>
        <el-form-item label="上菜时间">
          <el-date-picker value-format="YYYY-MM-DD HH-mm-ss"  v-model="reserveForm.date" type="datetime" placeholder="选择时间"></el-date-picker>
        </el-form-item>
        <el-form-item label="菜品口味">
          <el-select v-model="taste" placeholder="请选择菜品">
            <el-option label="微辣" value="微辣">微辣</el-option>
            <el-option label="中辣" value="中辣">中辣</el-option>
            <el-option label="重辣" value="重辣">重辣</el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <el-button type="primary" @click="submitReservation" style="margin-left: 40%;width: 20%">提交</el-button>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      activeTab: 'breakfast',
      dialogVisible: false,
      taste:'微辣',
      reserveForm: {
        dish_id: '',
        quantity: 1,
        date: ''
      },
      dishes: [
        {
          dish_id: "1",
          dish_type: "早餐",
          dish_name: "辣子鸡",
          dish_price: 30,
          dish_taste: "辣",
          date_intro: "辣子鸡是一道经典的川菜，味道麻辣鲜香。",
          image: 'api/get_dish_picture?dish_id=1'
        },
        {
          dish_id: "2",
          dish_type: "午餐",
          dish_name: "宫保鸡丁",
          dish_price: 35,
          dish_taste: "辣",
          date_intro: "宫保鸡丁，酸甜适口，鸡肉滑嫩，是一道经典川菜。",
          image: 'api/get_dish_picture?dish_id=2'
        },
        {
          dish_id: "3",
          dish_type: "晚餐",
          dish_name: "鱼香肉丝",
          dish_price: 40,
          dish_taste: "酸辣",
          date_intro: "鱼香肉丝，以猪肉为主料，酸辣可口，色香味俱全。",
          image: 'api/get_dish_picture?dish_id=3'
        }
      ]
    };
  },
  methods: {
    getDishesByType(type) {
      return this.dishes.filter(dish => dish.dish_type === type);
    },
    openReserveDialog(dish) {
      if (!this.$store.state.is_login){
        this.$message({message:'请先登录',type:'info'})
        return
      }
      this.reserveForm.dish_id = dish.dish_id;
      this.dialogVisible = true;
    },
    submitReservation() {
      this.$refs.reserveForm.validate(valid => {
        if (valid) {
          console.log('提交的预定信息:', this.reserveForm);
        } else {
          console.log('表单验证失败');
        }
      });
      let that = this
      axios.get('/api/add_food_order',{
        params:{
          username:that.$store.state.username,
          password:that.$store.state.password,
          dish_id:that.reserveForm.dish_id,
          dish_time:that.reserveForm.date,
          quantity:that.reserveForm.quantity,
          taste:that.taste
        }
      }).then(function (res){
        if(res.data.code == '1'){
          that.$message({message:'预定成功',type:'success'})
          that.dialogVisible = false
        }else if (res.data.code ==='0'){
          that.$message({message:res.data.msg,type:'info'})
        }
      })
    }
  },
  mounted() {
    let that = this
    axios.get('/api/get_menu').then(function (res){
      if ( res.data.code === '1'){
        that.dishes = res.data.data
      }
    })
  }
};
</script>

<style scoped>
.food-details{
  margin-left: 5%;
}
.food-container {
  margin: 20px;
}

.food-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.food-card {
  width: 100%;
  margin-left: 3%;
  margin-bottom: 2%;
}

.food-title {
  font-size: 24px;
  font-weight: bold;
  text-align: center;
}

.food-content {
  display: flex;
  align-items: center;
  padding: 10px;
}

.el-button {
  align-items: center;
  padding: 10px;
  width: 30%;
}

.food-image {
  width: 300px;
  height: 225px;
  object-fit: cover;
  margin-right: 20px;
}

.food-details {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.food-details p {
  margin: 5px 0;
}

.food-details .el-button {
  margin-top: 10px;
}
</style>