<script setup>
import { ref } from 'vue'
import axios from 'axios'
import UserDetail from '../components/UserDetail.vue'
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
const users = ref([])
const fullUser = ref(null);
const OpenUserDetail = ref(false);

async function fetchUsers() {
    
    try {
        const response = await axios.get(`${BACKEND_URL}/auth/users`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });
        if (response.status == 200) {
            users.value = response.data.Users;
            console.log('Fetched users successfully:', response.data);
        }
        return response.data;
    } catch (error) {
        console.error('Error fetching users:', error);
        return [];
    }
}

async function getUserDetails(userId) {
    
    try {
        const response = await axios.get(`${BACKEND_URL}/auth/users/${userId}`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });
        if (response.status == 200) {
            fullUser.value = response.data.data;
            console.log('User details fetched successfully:', response.data.data);
        }
    } catch (error) {
        console.error('Error fetching user details:', error);
    }
}
async function handleUserClick(userId) {
    await getUserDetails(userId);
    if (fullUser.value) {
        OpenUserDetail.value = true;
    }
}
fetchUsers();
</script>

<template>
    <div class="container border border-black rounded" style="margin-top: 20px; width: 100%;">
        <h2 class="text-center my-4">Users List</h2>
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Id</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Address</th>
                    <th>Pincode</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in users" :key="user.id">
                    <td @click=" handleUserClick(user.id)" style="cursor: pointer; color: blue;">{{ user.id }}</td>
                    <td>{{ user.username }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.address }}</td>
                    <td>{{ user.pincode }}</td>
                </tr>
            </tbody>
        </table>

        <UserDetail v-if="OpenUserDetail" :user="fullUser" @close="OpenUserDetail = false" />

    </div>
</template>