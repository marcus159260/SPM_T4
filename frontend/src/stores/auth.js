import { defineStore } from 'pinia';
import axios from 'axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    // isAuthenticated: false,
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),
  actions: {
    // async checkAuth() {
    //   try {
    //     const response = await axios.get('http://127.0.0.1:5000/api/auth/check_auth', {
    //       withCredentials: true,
    //     });
    //     console.log(response.data);
    //     if (response.data.authenticated) {
    //       this.isAuthenticated = true;
    //       this.user = {
    //         staff_id: response.data.staff_id,
    //         role: response.data.role,
    //         position: response.data.position,
    //         department: response.data.department,
    //         staff_fname: response.data.staff_fname,
    //         staff_lname: response.data.staff_lname,
    //         reporting_manager: response.data.reporting_manager,
    //       };
    //       console.log(this.user);
    //     } else {
    //       this.isAuthenticated = false;
    //       this.user = null;
    //     }
    //   } catch (error) {
    //     console.error('Error checking authentication:', error);
    //     this.isAuthenticated = false;
    //     this.user = null;
    //   }
    // },
    async login(staff_id) {
      try {
        const response = await axios.post(
          'http://127.0.0.1:5000/api/auth/login',
          { Staff_ID: staff_id },
          { withCredentials: true }
        );
        if (response.data.success) {
          // await this.checkAuth(); // Update the store state
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
        // await axios.post('http://127.0.0.1:5000/api/auth/logout', {}, { withCredentials: true });
        // this.isAuthenticated = false;
        this.user = null;
        // console.log(this.user);
        localStorage.removeItem('user');
      } catch (error) {
        console.error('Logout error:', error);
      }
    },
  },
});