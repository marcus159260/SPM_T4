<template>
    <header>
      <div class="wrapper">
        <nav class="navbar navbar-expand-lg bg-body-tertiary">
          <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
              <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                  <a class="nav-link active" aria-current="page" href="#">
                    <RouterLink to="/">Home</RouterLink>
                  </a>
                </li>
  
                <li class="nav-item">
                  <a class="nav-link" href="#">
                    <RouterLink to="/my-schedule">My Schedule</RouterLink>
                  </a>
                </li>
  
                <li class="nav-item">
                  <a class="nav-link" href="#">
                    <RouterLink to="/team-schedule-staff">My Team Schedule</RouterLink>
                  </a>
                </li>

                <li v-if="user && (Number(user.role) === 3 || Number(user.role) === 1)" class="nav-item">
                  <a class="nav-link" href="#">
                    <RouterLink to="/team-schedule-manager">(M/D)Team Schedule</RouterLink>
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
  
                <li v-if="user && (Number(user.role) === 1 || Number(user.role) === 3)" class="nav-item">
                  <a class="nav-link" href="#">
                    <RouterLink to="/manager-schedule"> (M/D) View staff requests</RouterLink>
                  </a>
                </li>
  
                <li class="nav-item">
                  <a class="nav-link" href="#">
                    <button class="btn btn-outline-dark" @click="logout">Logout</button>                
                  </a>
                </li>
              </ul>
  
              
            </div>
          </div>
        </nav>
      </div>
    </header>
  </template>
    
    <script>
    import { computed } from 'vue';
    import { useAuthStore } from '@/stores/auth';
    import { useRouter,RouterLink, RouterView } from 'vue-router';
  
    export default {
      name: 'NavBar',
      setup() {
        const authStore = useAuthStore();
        const router = useRouter();
    
        const user = computed(() => authStore.user);
    
        const logout = () => {
          authStore.logout();
          router.push('/login');
        };
    
        return {
          user,
          logout,
        };
      },
    };
    </script>
    
    <style scoped>
      .wrapper {
          width: 100%;
          margin: 0 auto;
      }
  
      .navbar {
        display: flex;
          background-color: #f8f9fa;
      }

      .navbar-nav {
        display: flex;               /* Display list items in a row */
        list-style: none;            /* Remove list-style */
        padding-left: 0;             /* Remove left padding */
        margin-bottom: 0;            /* Remove bottom margin */
        }
  
      .nav-item {
          display: flex;
          margin-right: 1em;
          align-items: center;
          
      }
      
      .nav-link {
          text-decoration: none;
          display: flex;
      }

      a {
        display: block;
        /* padding: 4px; */
        text-decoration: none;
        color: #272757;
    }


      .router-link-active {
        font-weight: bold;
        }
    </style>
    
