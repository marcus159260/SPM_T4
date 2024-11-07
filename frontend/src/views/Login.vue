<template>
  <div class="login-page d-flex justify-content-center align-items-center">
    <div class="card p-4">
      <h3 class="mt-0 mb-4">Login</h3>
      <form @submit.prevent="handleLogin">
        <div class="form-group mb-3">
          <label for="staff_id">Staff ID:</label>
          <input v-model="staff_id" type="text" class="form-control" id="staff_id" required />
        </div>
        <button type="submit" class="btn btn-primary btn-block">Login</button>
      </form>
      <div v-if="successMessage" class="alert alert-success mt-3">
        {{ successMessage }}
      </div>
      <div v-if="errorMessage" class="alert alert-danger mt-3">
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth.js';
import { useRouter } from 'vue-router';

export default {
  name: 'Login',
  setup() {
    const staff_id = ref('');
    const errorMessage = ref('');
    const successMessage = ref('');
    const authStore = useAuthStore();
    const router = useRouter();

    const handleLogin = async () => {
      const success = await authStore.login(staff_id.value);
      if (!success) {
        errorMessage.value = 'Invalid Staff ID';
        successMessage.value = '';
      } else {
        errorMessage.value = '';
        successMessage.value = 'Login successful!';
        // Redirect to home page after a short delay
        setTimeout(() => {
          router.push('/');
        }, 800);
      }
    };

    return {
      staff_id,
      errorMessage,
      successMessage,
      handleLogin,
    };
  },
};
</script>

<style scoped>
.login-page {
  height: 100vh;
  background-color: #f8f9fa;
}

.card {
  width: 100%;
  max-width: 400px;
}
</style>