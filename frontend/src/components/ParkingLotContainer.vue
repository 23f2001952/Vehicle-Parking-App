<script setup>
import axios from 'axios'
import { ref,onMounted } from 'vue'
import ParkingLot from './ParkingLot.vue'
import AddParkingLot from './AddParkingLot.vue'

const add_parkingLot = ref(null);

function OpenaddParkingLot() {
    add_parkingLot.value = true;
}

const role = localStorage.getItem('role')

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;   
const parkingLots = ref([]);
async function get_all_parking_lot()
{
    try{
        const response = await axios.get(`${BACKEND_URL}/parking_lot/get`, 
                {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('access_token') }`
                    }
                }
            );
    
        if (response.status === 200) {
            parkingLots.value = response.data['ParkingLots'] || [];
        } else {
            console.error('Failed to fetch parking lots:', response.status);
        }
        return parkingLots.value;
    }
    catch (error) {
        console.error('Error fetching parking lots:', error);
        return [];
    }
}



    get_all_parking_lot();
</script>

<template>
  <div class="container border border-black rounded p-4 my-4 bg-white">
    
    <div class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-2 border-black">
      <h3 class="mb-0 ">Parking Lots</h3>
      <div class="d-flex gap-2">
        <button class="btn btn-outline-dark btn-sm" v-if="role === 'admin'" @click="OpenaddParkingLot">Add</button>
      </div>
    </div>

    <AddParkingLot v-if="add_parkingLot" @close="add_parkingLot = null" @parkingLotAdded="get_all_parking_lot" />
    <div class="row g-4">
      <div class="col-md-6 col-lg-4" v-for="lot in parkingLots" :key="lot.id">
        <ParkingLot :parkingLot="lot" @update="get_all_parking_lot" @delete="get_all_parking_lot" />
      </div>
    </div>
    
  </div>
</template>