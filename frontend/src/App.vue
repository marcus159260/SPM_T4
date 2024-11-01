<template>
  <div id="app">
    <NavBar v-if="user" />
    <router-view />
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import { computed } from 'vue';
import NavBar from '@/components/Navbar.vue';

export default {
  name: 'App',
  components: {
    NavBar,
  },
  setup() {
    const authStore = useAuthStore();
    const user = computed(() => authStore.user);

    // Debugging
    // console.log('user:', user.value);
    // console.log('user.role:', typeof user.value?.role, user.value?.role);

    return {
      user,
    };
  },
};
</script>