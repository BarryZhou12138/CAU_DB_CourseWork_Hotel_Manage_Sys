import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:'/',
      name:'MainPage',
      component:()=>import('../components/MainPage.vue')
    },
    {
      path:'/room_order',
      name:'room_order',
      component:()=>import('../components/order_room.vue')
    },
    {
      path:'/admin',
      name:'admin',
      component:()=>import('../components/admin.vue')
    },
    {
      path:'/order_meet',
      name:'order_meet',
      component:()=>import('../components/order_meet.vue')
    },
    {
      path:'/order_food',
      name:'order_food',
      component:()=>import('../components/order_food.vue')
    },
    {
      path:'/my_orders',
      name:'my_orders',
      component:()=>import('../components/OrderTabs.vue')
    },
    {
      path:'/check_in',
      name:'check_in',
      component:()=>import('../components/check_in.vue')
    },
    {
      path:'/check_out',
      name:'check_out',
      component:()=>import('../components/check_out.vue')
    },
    {
      path:'/finish_order',
      name:'finish_order',
      component:()=>import('../components/finish_order.vue')
    },


  ]
})

export default router
