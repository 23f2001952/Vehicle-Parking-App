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
    <div class ="navbar navbar-expand-lg navbar-light bg-light d-flex justify-content-between">
        <span>
            <a @click="router.push('/')">ParkingPoint</a>
        </span>
        <span v-if="auth.loggedIn === true && auth.role === 'admin'">
            <a @click="router.push('/dashboard/admin')">Dashboard</a>
        </span>
        <span v-if="auth.loggedIn === true && auth.role === 'user'">
            <a @click="router.push('/dashboard/user')">Dashboard</a>
        </span>
        <span v-if='auth.loggedIn === true'>
            <a @click='logout'>Logout</a>
        </span>
        <span v-else class="d-flex gap-2">
            <span>
                <a @click="router.push('/login')">Login</a>
            </span>
            <span>
                <a @click="router.push('/register')">Register</a>
            </span>
        </span>

    </div>
</template>