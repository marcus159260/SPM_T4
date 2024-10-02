import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import StaffRequests from '@/views/StaffRequests.vue'
import TeamScheduleView from '../views/TeamScheduleView.vue';
import ManagerScheduleView from '../views/ManagerScheduleView.vue';
import HRScheduleView from '../views/HRScheduleView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    
    {
      path:"/staffrequests/:staff_id", //change to ownrequest
      name:"staffrequests",
      component:StaffRequests
    },
    {
      path: '/team-schedule',
      name: 'TeamSchedule',
      component: TeamScheduleView
    },
    {
      path: '/manager-schedule',
      name: 'ManagerSchedule',
      component: ManagerScheduleView
    },
    {
      path: '/hr-schedule',
      name: 'HRSchedule',
      component: HRScheduleView

    },
  ]
})

export default router
