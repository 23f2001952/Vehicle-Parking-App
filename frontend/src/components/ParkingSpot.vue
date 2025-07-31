<script setup>
import { defineProps,ref } from 'vue'
import ParkingSpotInfo from './ParkingSpotInfo.vue'

const selectedSpot = ref(false)
const role = ref(localStorage.getItem('role'))

const props = defineProps({
    parkingSpot: {
        type: Object,
        required: true
    }
})
</script>

<template>
<div>
  <div
    class="spot-box rounded border border-dark d-flex align-items-center justify-content-center text-black fw-bold"
    :class="parkingSpot.status === 'occupied' ? 'bg-danger' : 'bg-success'"
    :title="`Spot ${parkingSpot.status}`"
  @click="selectedSpot = true"
  >
    
  </div>
  <ParkingSpotInfo v-if="selectedSpot === true && role === 'admin'" :parkingSpot="parkingSpot" @close="selectedSpot = false" />
  </div>
</template>

<style scoped>
.spot-box {
  width: 32px;
  height: 32px;
  font-size: 0.7rem;
}
</style>