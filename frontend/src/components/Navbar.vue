<script setup>

import {useRouter} from 'vue-router'
import { ref} from 'vue'
import { auth } from '../auth.js'

const router = useRouter();

function logout() {
    auth.logout();
    router.push('/');
}

</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light px-4 border border-black shadow-sm">
    <div class="container-fluid">

      <a class="navbar-brand fw-bold" @click="router.push('/')">🚗 ParkingPoint</a>


      <div class="d-flex align-items-center ms-auto gap-3">

        <template v-if="auth.loggedIn && auth.role === 'admin'">
          <a class="nav-link text-black" @click="router.push('/dashboard/admin')">Dashboard</a>
          <a class="nav-link text-black" @click="router.push('/Users')">Users</a>
            <a class="nav-link text-black" @click="router.push('/Summary')">Summary</a>
        </template>
        <template v-if="auth.loggedIn && auth.role === 'user'">
          <a class="nav-link text-black" @click="router.push('/dashboard/user')">Dashboard</a>
            <a class="nav-link text-black" @click="router.push('/UserSummary')">Summary</a>
        </template>

        <template v-if="auth.loggedIn">
          <a class="btn btn-outline-danger btn-sm" @click="logout">Logout</a>
        </template>


        <template v-else>
          <a class="btn btn-outline-dark btn-sm" @click="router.push('/login')">Login</a>
          <a class="btn btn-dark btn-sm" @click="router.push('/register')">Register</a>
        </template>
      </div>
    </div>
  </nav>
</template>