<script setup>
import axios from 'axios'
import {ref} from 'vue'
import {useRouter} from 'vue-router' 
import {auth} from '../auth.js'
 
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

const username = ref('');
const password = ref('');
const access_token = ref('');
const role = ref('');
const router = useRouter();
const login_error = ref('')
const loggedIn = ref(false)

function routeRegister()
{
    router.push('/register');
}

async function submit()
{
    try{
        const response = await axios.post(`${BACKEND_URL}/auth/login`,
            {
                username : username.value,
                password : password.value
            },
            {
                headers:{
                    'Content-Type':'application/json'
                    }
            }
        );
        console.log(response);
        if(response['status'] === 200)
        {
            access_token.value = response['data']['access_token'];
            role.value = response['data']['role']
            loggedIn.value = true
            localStorage.setItem("access_token",access_token.value);
            auth.login(role.value);
            if(role.value == 'admin')   
            {
                router.push('/dashboard/admin');
            }
            else if(role.value == 'user')
            {
                router.push('/dashboard/user');
            }
            else
            {
                 router.push('/');
                 console.log("Unknown Role!!");
            }
        }

    }
    catch (error) {
    login_error.value = error.response.data;
    console.error('Login failed:', error.response.data || error.message)
  }

    
}

</script>

<template>
    <div class="container">
        <div class="card border border-black mx-auto mt-5" style="width: 30rem;">
            <div class="card-header border-bottom border-dark">
                <h2 class="fs-3 text-center">Login </h2>
                <div v-if='loggedIn==false'>
                    {{ login_error }}
                </div>
            </div>
            <div class = "card-body">
            <form @submit.prevent='submit' class="py-3">
                <div class="mb-3">

                    <label>
                        Enter Username:
                    </label>
                    <input type="text" v-model="username" class="form-control" placeholder="Enter Username" name="username">
                </div>
                <div class="form-group">
                    <label>
                        Enter Password:
                    </label>
                    <input type="password" v-model="password" class="form-control" placeholder="Enter Password" name="password">
                </div>
                <button type="submit" class="btn btn-primary mt-3">Login</button>
            </form>

            </div>
           
            <div class="card-footer text-center">
                <p>Don't have an account? <a @click.prevent="routeRegister" class="text-primary"><u>Register</u></a></p>
            </div>
        </div>
    </div>
    
</template>