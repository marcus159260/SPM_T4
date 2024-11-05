import { defineStore } from 'pinia';
import axios from 'axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),
  actions: {
    async login(staff_id) {
      try {
        const response = await axios.post(
          `http://127.0.0.1:5000//api/auth/login`,
          { Staff_ID: staff_id },
          { withCredentials: true }
        );
        if (response.data.success) {
          this.user = response.data.user;
          console.log(this.user);
          localStorage.setItem('user', JSON.stringify(this.user));
          return true;
        } else {
          return false;
        }
      } catch (error) {
        console.error('Login error:', error);
        return false;
      }
    },
    async logout() {
      try {
        this.user = null;
        // console.log(this.user);
        localStorage.removeItem('user');
      } catch (error) {
        console.error('Logout error:', error);
      }
    },
  },
});
