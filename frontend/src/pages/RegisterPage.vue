<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { setToast } from '../toast.js'
import { useToast } from 'vue-toast-notification'
import { useRouter } from 'vue-router'

const toast = useToast()
setToast(toast)

const router = useRouter();
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const register_error = ref('');

function resetForm() {
    username.value = '';
    email.value = '';
    password.value = '';
    confirmPassword.value = '';
    register_error.value = '';
}

function routeLogin() {
    router.push('/login');
}

function validateForm() {
    if (!username.value || !email.value || !password.value || !confirmPassword.value) {
        toast.error('All fields are required.');
        return false;
    }
    if (password.value !== confirmPassword.value) {
        toast.error('Passwords do not match.');
        return false;
    }
    return true;
}


async function registerUser() {
    try {
        if (!validateForm()) {
            return;
        }
        const response = await axios.post(`${BACKEND_URL}/auth/register`, {
            username: username.value,
            email: email.value,
            password: password.value,
            confirm_password: confirmPassword.value
        });
        
        if (response.status === 201) {
            console.log('Registration successful:', response.data);
            toast.success('Registration successful!');
            router.push('/login');
        }

    } catch (error) {
        console.error('Registration error:', error);
        register_error.value = error.response.data ;
        toast.error('Registration failed. Please try again.');
    }
};

</script>


<template>
  <div class="container">
    <div class="card border border-black mx-auto mt-5" style="width: 30rem;">
      <div class="card-header border-bottom border-dark">
        <h2 class="fs-3 text-center">Register</h2>
        <div v-if="register_error" class="alert alert-danger mt-2">
          {{ register_error }}
        </div>
      </div>

      <div class="card-body p-3">
        <form class="register-form" @submit.prevent="registerUser">
          <div class="mb-3">
            <label class="form-label">Username</label>
            <input
              v-model="username"
              type="text"
              class="form-control"
              placeholder="Enter username"
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Email</label>
            <input
              v-model="email"
              type="email"
              class="form-control"
              placeholder="Enter email"
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Password</label>
            <input
              v-model="password"
              type="password"
              class="form-control"
              placeholder="Enter password"
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Confirm Password</label>
            <input
              v-model="confirmPassword"
              type="password"
              class="form-control"
              placeholder="Confirm password"
            />
          </div>

          <div class="d-flex justify-space-between ">
            <button type="submit" class="btn btn-primary border px-3">Register</button>
            <button type="reset" @click="resetForm" class="btn btn-secondary border mx-3">Reset</button>
          </div>
        </form>
      </div>

      <div class="card-footer text-center">
        <p>
          Already have an account?
          <router-link to="/login">Login</router-link>
        </p>
      </div>
    </div>
  </div>
</template>
