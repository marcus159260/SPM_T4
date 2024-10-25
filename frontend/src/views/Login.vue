<template>
  <div class="login-page">
    <form @submit.prevent="handleLogin">
      <div>
        <label>Staff ID:</label>
        <input v-model="staff_id" type="text" required />
      </div>
      <button type="submit">Login</button>
    </form>
    <div v-if="successMessage" class="alert alert-success">
      {{ successMessage }}
    </div>
    <div v-if="errorMessage" class="alert alert-danger">
      {{ errorMessage }}
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
      console.log(success);
      if (!success) {
        errorMessage.value = 'Invalid Staff ID';
        successMessage.value = '';
      } else {
        errorMessage.value = '';
        successMessage.value = 'Login successful!';
        // Redirect to home page after a short delay
        setTimeout(() => {
          router.push('/');
        }, 1000); // 1-second delay to show success message
      }
    };

    return {
      staff_id,
      errorMessage,
      successMessage,
      handleLogin,
    };
  },
}
</script>

<style>
  .alert {
    margin-top: 1em;
    padding: 1em;
    border-radius: 5px;
  }

  .alert-success {
    background-color: #d4edda;
    color: #155724;
  }

  .alert-danger {
    background-color: #f8d7da;
    color: #721c24;
  }
</style>