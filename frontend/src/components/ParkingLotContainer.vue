<script setup>
import axios from 'axios'
import { ref,onMounted } from 'vue'
import ParkingLot from './ParkingLot.vue'

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
    <div class="parking-lot-container">
        <h2>Parking Lots</h2>
        <div class="parking-lots">
            <ParkingLot v-for="lot in parkingLots" :key="lot.id" :parkingLot="lot" />
        </div>
    </div>
</template>