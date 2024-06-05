<script setup>

</script>

<template>
  <div>
  <el-container style="width: 85%">
    <el-aside style="width: 15%">

    </el-aside>
    <el-main >
      <el-card class="transport-card" v-for="(service, index) in services" :key="index">
        <div slot="header" class="transport-title">{{ service.title }}</div>
        <div class="transport-content">
          <div class="transport-image">
            <img :src="service.image" alt="接送服务图片">
          </div>
          <div class="transport-description">
            <p>{{ service.description }}</p>
            <p v-if="service.drinks">提供饮料：{{ service.drinks }}</p>
            <p>接送车辆：{{ service.vehicle }}</p>
            {{service.price}}元/每次
            <el-button @click="order(service.id)" type="primary">立即预定</el-button>
          </div>
        </div>
      </el-card>
      <el-dialog v-model="Show_book" width="30%">
        <template #default>
          <el-form ref="form" :model="formData" label-width="100px">
            <el-form-item label="接送形式">
              <el-select style="width: 60%" v-model="formData.meet_id">
                <el-option :value="'1'" label="普通接送">
                  普通接送
                </el-option>
                <el-option :value="'2'" label="公务接送">
                  公务接送
                </el-option>
                <el-option :value="'3'" label="豪华接送">
                  豪华接送
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item >
              <el-radio-group v-model="formData.type_select" >

                <el-radio-button :value="送站" label="送站">
                送站
              </el-radio-button>
                <el-radio-button :value="接站" label="接站">
                接站
              </el-radio-button>



              </el-radio-group>
            </el-form-item>
            <el-form-item label="接送时间">
              <el-date-picker type="datetime" value-format="YYYY-MM-DD HH-mm-ss" -format="" v-model="formData.pickupTime" placeholder="请选择接送时间"/>
            </el-form-item>
            <el-form-item label="接送地点">
              <el-input v-model="formData.pickupLocation" style="margin-right: 10%" placeholder="请输入接送地点"></el-input>
            </el-form-item>
          </el-form>
          <el-button type="primary" @click="order_submit()" style="margin-left: 40%;width: 20%">确认提交</el-button>
        </template>
      </el-dialog>
    </el-main>
  </el-container>
  </div>

</template>

<script>
import axios from "axios";
import jpg1 from '../../static/接送/1.jpg'
import jpg2 from '../../static/接送/2.jpg'
import jpg3 from '../../static/接送/3.jpg'
export default {
  name:'order_meet',
  data() {
    return {
      Show_book:false,
      formData: {
        meet_id:1,
        type_select:'送站',
        pickupTime: '', // 接送时间
        pickupLocation: '' // 接送地点
      },
      services: [
        {
          id:'1',
          title: "普通接送",
          description: "我们提供经济实惠的普通接送服务，确保您安全、准时地抵达目的地。无论您是来自哪里，都能享受到舒适的乘车体验。",
          drinks: "免费水和小吃",
          vehicle: "舒适的轿车",
          image: jpg1,
          price:5,
        },
        {
          id:'2',
          title: "公务接送",
          description: "我们的公务接送服务为商务旅行者提供高效、便捷的交通解决方案。我们的专业司机团队会确保您按时到达会议地点或商务活动。",
          drinks: "免费饮料（茶、咖啡等）",
          vehicle: "商务车或豪华轿车",
          image: jpg2,
          price:30,
        },
        {
          id:'3',
          title: "豪华接送",
          description: "豪华接送服务为您提供一流的乘车体验，配备舒适的座椅、高级车辆以及专业司机。无论是商务会议还是休闲旅行，我们都能满足您的高品质需求。",
          drinks: "精选饮品、小吃和香槟",
          vehicle: "豪华轿车或SUV",
          image: jpg3,
          price:200,
        },
      ],
    };
  },
  methods:{
    order(id){
      if(!this.$store.state.is_login){
        this.$message({message:'请先登录',type:'info'})
        return
      }
      this.formData.meet_id = id
      this.Show_book = true
    },
    order_submit(){
      let that=this
      if(this.formData.type_select==='送站'){
        axios.get('/api/add_send_order',{
          params:{
            username:that.$store.state.username,
            password:that.$store.state.password,
            meet_id:that.formData.meet_id,
            meet_time:that.formData.pickupTime,
            location:that.formData.pickupLocation
          }
        }).then(function (res){
          if(res.data.code === '1'){
            that.$message({message:'预定成功',type:'success'})
            that.Show_book = false
          }else {
            that.$message({message:res.data.msg,type:'info'})
          }
        }).catch((err)=>{
          that.$message({message:'预定失败',type:'info'})
        })
      }else {
        axios.get('/api/add_meet_order',{
          params:{
            username:that.$store.state.username,
            password:that.$store.state.password,
            meet_id:that.formData.meet_id,
            meet_time:that.formData.pickupTime,
            location:that.formData.pickupLocation
          }
        }).then(function (res){
          if(res.data.code === '1'){
            that.$message({message:'预定成功',type:'success'})
            that.Show_book = false
          }else {
            that.$message({message:res.data.msg,type:'info'})
          }
        }).catch((err)=>{
          that.$message({message:'预定失败',type:'info'})
        })
      }
    }
  },



}

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

.transport-image img {
  max-width: 300px; /* 设置图片宽度 */
  max-height: 200px;
  margin-right: 20px; /* 图片和描述之间的间距 */
}

.transport-description {
  flex: 1; /* 让描述部分占据剩余空间 */
}

.el-button {
  margin-top: 10px;
}
</style>