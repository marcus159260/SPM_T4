<template>
  <div class="home-view">
    <h1>Welcome to WFH Scheduler</h1>
    <p class="intro-text">Manage your work-from-home schedule with ease! Navigate to the different sections based on your role.</p>
    <br>
    <div class="page-links">
      <!-- Link to view own requests (for all users) -->
      <div v-if="user" class="page-link">
        <RouterLink to="/staff-requests" class="link">
          <span class="link-title">View My Requests</span>
          <p class="link-description">Track the status of your requests, create new ones, or cancel existing requests.</p>
        </RouterLink>
      </div>

      <!-- Link to manage staff requests (for managers and directors) -->
      <div v-if="user && (user.role === 1 || user.role === 3)" class="page-link">
        <RouterLink to="/manager-schedule" class="link">
          <span class="link-title">Manage Staff Requests</span>
          <p class="link-description">Managers and Directors can approve, reject, or manage work-from-home requests for their team.</p>
        </RouterLink>
      </div>
      
      <!-- Link to view own schedule (for all users) -->
      <div v-if="user" class="page-link">
        <RouterLink to="/my-schedule" class="link">
          <span class="link-title">View My Schedule</span>
          <p class="link-description">Check your upcoming work-from-home schedule and plan accordingly.</p>
        </RouterLink>
      </div>
      
      <!-- Link to view the team schedule (for all staff) -->
      <div v-if="user" class="page-link">
        <RouterLink to="/team-schedule-staff" class="link">
          <span class="link-title">View Team Schedule</span>
          <p class="link-description">View the work-from-home schedule of your entire team.</p>
        </RouterLink>
      </div>

      <!-- Link to view team schedule (for managers and directors) -->
      <div v-if="user && (user.role === 1 || user.role === 3)" class="page-link">
        <RouterLink to="/team-schedule-manager" class="link">
          <span class="link-title">Team Schedule (Manager/Director)</span>
          <p class="link-description">Managers and Directors can view the schedule of their teams and subordinates.</p>
        </RouterLink>
      </div>
      
      

      <!-- Link to view HR schedule (for HR) -->
      <div v-if="user && user.role === 1" class="page-link">
        <RouterLink to="/hr-schedule" class="link">
          <span class="link-title">View HR Schedule</span>
          <p class="link-description">HR can view the work-from-home schedule of all employees in the company.</p>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script>
  import { computed } from 'vue';
  import { useAuthStore } from '@/stores/auth';
  import { useRouter, RouterLink } from 'vue-router';

  export default {
    name: 'HomeView',
    setup() {
      const authStore = useAuthStore();
      const router = useRouter();
      const user = computed(() => authStore.user);
      console.log(user.role);

      return {
        user, // Make user available in the template
      };
    },
  };
</script>

<style scoped>
.home-view {
  text-align: center;
  padding: 40px;
}

h1 {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 5px;
  margin-top:0px;
}

.intro-text {
  font-size: 18px;
  color: #555;
  margin-bottom: 30px;
  max-width: 700px;
  margin: 0 auto;
  font-weight: normal;
}

.page-links {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  max-width: 900px;
  margin: 0 auto;
}

.page-link {
  background-color: #ffffff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.page-link:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.link {
  text-decoration: none;
  color: #007bff;
  display: block;
}

.link-title {
  font-size: 20px;
  font-weight: bold;
  color: #3e8deb;
}

.link-description {
  font-size: 14px;
  color: #777;
  margin-top: 10px;
}

.page-links a:hover .link-title {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .page-links {
    grid-template-columns: 1fr;
  }
}
</style>
