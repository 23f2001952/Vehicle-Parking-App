<script setup>
import { ref } from 'vue'
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
import { setToast } from './toast.js'
import { useToast } from 'vue-toast-notification'
const toast = useToast()
setToast(toast)

</script>

<template>
  <div id="app">
    <Navbar/>
    <RouterView/>
    <Footer/>
  </div>
</template>
