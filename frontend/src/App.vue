<script>
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth';
import { computed } from 'vue';

export default {
  name: 'App',
  setup() {
    const authStore = useAuthStore();
    const user = computed(() => authStore.user);

    // Debugging
    console.log('user:', user.value);
    console.log('user.role:', typeof user.value?.role, user.value?.role);

    return {
      user,
    };
  },
};
</script>

<template>
  <header>
    <div class="wrapper">
      <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item">
                <a class="nav-link active" aria-current="page" href="#">
                  <RouterLink to="/">Home</RouterLink>
                </a>
              </li>

              <li class="nav-item">
                <a class="nav-link" href="#">
                  <RouterLink to="/login">Login</RouterLink>
                </a>
              </li>

              <li class="nav-item">
                <a class="nav-link" href="#">
                  <RouterLink to="/my-schedule">My Schedule</RouterLink>
                </a>
              </li>

              <li class="nav-item">
                <a class="nav-link" href="#">
                  <RouterLink to="/team-schedule">My Team Schedule</RouterLink>
                </a>
              </li>

              <li v-if="user && Number(user.role) === 1" class="nav-item">
                <a class="nav-link" href="#">
                  <RouterLink to="/hr-schedule">HR Schedule</RouterLink>
                </a>
              </li>

              <li class="nav-item">
                <a class="nav-link" href="#">
                  <RouterLink to="/staff-requests"> (staff) View own requests</RouterLink>
                </a>
              </li>

              <li class="nav-item">
                <a class="nav-link" href="#">
                  <RouterLink to="/manager-schedule"> (M/D) View staff requests</RouterLink>
                </a>
              </li>

              <li class="nav-item">
                <a class="nav-link" href="#">
                  <button @click="logout">Logout</button>                
                </a>
              </li>
            </ul>
            <form class="d-flex" role="search">
              <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
              <button class="btn btn-outline-success" type="submit">Search</button>
            </form>

            
          </div>
        </div>
      </nav>
    </div>
  </header>



  <RouterView />
</template>