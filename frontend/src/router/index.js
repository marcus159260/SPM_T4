import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import StaffRequests from '@/views/StaffRequests.vue'
import TeamScheduleViewManager from '../views/TeamScheduleViewManager.vue';
import TeamScheduleViewStaff from '../views/TeamScheduleViewStaff.vue';
import ManagerScheduleView from '../views/ManagerScheduleView.vue';
import HRScheduleView from '../views/HRScheduleView.vue';
import MyScheduleView from '@/views/MyScheduleView.vue';
import Login from '@/views/Login.vue';
import Unauthorised from '@/views/Unauthorised.vue';
import { useAuthStore } from '@/stores/auth';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path:"/staff-requests", //change to ownrequest
      name:"StaffRequests",
      component:StaffRequests,
      meta: { requiresAuth: true }
    },
    {
      path: '/my-schedule',
      name: 'MySchedule',
      component: MyScheduleView,
      meta: { requiresAuth: true }
    },
    {
      path: '/team-schedule-manager',
      name: 'TeamScheduleManager',
      component: TeamScheduleViewManager,
      meta: { requiresAuth: true, requiredRoles: [1,3] },
    },
    {
      path: '/team-schedule-staff',
      name: 'TeamScheduleStaff',
      component: TeamScheduleViewStaff,
      meta: { requiresAuth: true, requiredRoles: [1,2,3] },
    },
    {
      path: '/manager-schedule',
      name: 'ManagerSchedule',
      component: ManagerScheduleView,
      meta: { requiresAuth: true, requiredRoles: [1,3] },
    },
    {
      path: '/hr-schedule',
      name: 'HRSchedule',
      component: HRScheduleView,
      meta: { requiresAuth: true, requiredRoles: [1] },
    },
    {
      path: '/unauthorised',
      name: 'Unauthorised',
      component: Unauthorised
    }    
    
  ]
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  // if (!authStore.user) {
  //   localStorage.getItem('user') ? authStore.user = JSON.parse(localStorage.getItem('user')) : null;

  // }

  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

  if (requiresAuth) {
    if (authStore.user) {
      // Collect requiredRoles from all matched route records
      // const requiredRoles = to.matched.reduce((roles, record) => {
      //   if (record.meta.requiredRoles) {
      //     roles.push(...record.meta.requiredRoles);
      //   }
      //   return roles;
      // }, []);

      const requiredRoles = to.matched[0]?.meta?.requiredRoles || [];

      // console.log('authStore.user.role:', authStore.user.role);
      // console.log(authStore.user.staff_id);
      // console.log('requiredRoles:', requiredRoles);

      // Check if user's role is included in requiredRoles
      if (
        requiredRoles.length > 0 &&
        !requiredRoles.includes(authStore.user.role)
      ) {
        next('/unauthorised');
      } else {
        next();
      }
    } else {
      next('/login');
    }
  } else {
    next();
  }
});


export default router