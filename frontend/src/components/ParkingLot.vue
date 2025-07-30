<script setup>
import { ref, defineProps } from 'vue'
import axios from 'axios'
import ParkingSpot from './ParkingSpot.vue'

const props = defineProps({
    parkingLot: {
        type: Object,
        required: true
    }
})
console.log("ParkingLot component loaded with data:", props.parkingLot);

async function getParkingLotDetails() {
    try {
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/parking_lot/${props.parkingLot.id}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching parking lot details:', error);
        return null;
    }
}

getParkingLotDetails();
</script>


<template>
    <div class="parking-lot">
        <h3>Location: {{ parkingLot['prime_location_name'] }}</h3>
        <p>Price: {{ parkingLot['price'] }}</p>
        <p>Address: {{ parkingLot['address'] }}</p>
        <p>Number of Spots: {{ parkingLot['number_of_spots'] }}</p>
        <p>Pincode: {{ parkingLot['pincode'] }}</p>
        <div class="parking-spots">
            <ParkingSpot v-for="spot in parkingLot['parking_spots']" :key="spot.id" :parkingSpot="spot" />
        </div>
    </div>
</template>
