<script setup>
import { ref, defineProps, defineEmits } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toast-notification'
import { setToast } from '../toast.js'

const toast = useToast()
setToast(toast)

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

const vehicleNumber = ref('');

const props = defineProps({
    parkinglot: {
        type: Object,
        required: true
    }
})

const emit = defineEmits(['update', 'close'])

function resetForm() {
    vehicleNumber.value = '';
}

async function bookParkingSpot() {
    try {
        const response = await axios.post(`${BACKEND_URL}/parking_spot/book/${props.parkinglot.id}`, {
            "vehicle_number": vehicleNumber.value
        }, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });

        if (response.status === 201) {
            console.log('Parking Spot booked successfully:', response.data);
            toast.success('Parking Spot booked successfully!');
            vehicleNumber.value = '';
            emit('update');
            emit('close');
    
        } else {
            console.error('Failed to book Parking Spot:', response.status);
            toast.error('Failed to book Parking Spot');
        }
    } catch (error) {
        console.error('Error booking parking spot:', error);
    }
}


</script>

<template>
    <div class="position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center" style="background-color: rgba(0,0,0,0.5); z-index: 1050;">
        <div class="bg-white rounded shadow-lg border" style="width: 90%; max-width: 500px;">
            
            <div class="d-flex justify-content-between align-items-center p-3 border-bottom bg-light rounded-top">
                <h5 class="mb-0 fw-bold">Book Parking Spot</h5>
                <div>
                    <button class="btn btn-outline-secondary btn-sm me-2" @click="resetForm">Reset</button>
                    <button class="btn btn-outline-dark btn-sm" @click="$emit('close')">Close</button>
                </div>
            </div>
            <form @submit.prevent="bookParkingSpot">
                <div class="p-4">
                    <div class="mb-3">
                        <label class="form-label fw-semibold">Parking Lot Id:</label>
                        <input type="text" class="form-control" v-model="parkinglot.id" disabled/>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold">Prime Location Name:</label>
                        <input type="text" class="form-control" v-model="parkinglot.prime_location_name" disabled/>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold">Price:</label>
                        <input type="text" class="form-control" v-model="parkinglot.price" disabled/>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold">Vehicle Number:</label>
                        <input type="text" class="form-control" v-model="vehicleNumber" placeholder="Enter Vehicle Number" required />
                    </div>
                    <div class="d-flex justify-content-end gap-2 pt-3 ">
                        <button type="submit" class="btn btn-primary">Book</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>