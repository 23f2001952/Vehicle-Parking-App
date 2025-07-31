<script setup>
import {ref,defineEmits} from 'vue';
import axios from 'axios';
import {useToast} from 'vue-toast-notification';
import {setToast} from '../toast.js';


const toast = useToast();
setToast(toast);


const emit = defineEmits(['close', 'parkingLotAdded']);
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

const number_of_spots = ref(0);
const prime_location_name = ref('');
const pincode = ref('');
const address = ref('');
const price = ref(0);

function resetForm() {
    number_of_spots.value = 0;
    prime_location_name.value = '';
    pincode.value = '';
    address.value = '';
    price.value = 0;
}

async function addParkingLot() {
    const parkingLotData = {
        number_of_spots: number_of_spots.value,
        prime_location_name: prime_location_name.value,
        pincode: pincode.value,
        address: address.value,
        price: price.value
    };

    try{
        const response = await axios.post(`${BACKEND_URL}/parking_lot/add`, parkingLotData, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
    });
        if (response.status === 201) {
            console.log('Parking Lot added successfully:', response.data);
            toast.success('Parking Lot added successfully!');
            resetForm();
            emit('close');
            emit('parkingLotAdded', response.data);
        } else {
            console.error('Failed to add Parking Lot:', response.status);
            toast.error('Failed to add Parking Lot');
        }
        
    } catch (error) {
        console.error('Error adding Parking Lot:', error);
    }


    console.log('Adding Parking Lot:', parkingLotData);


}

</script>

// ...existing code...
<template>
    <div class="position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center" style="background-color: rgba(0,0,0,0.5); z-index: 1050;">
        <div class="bg-white rounded shadow-lg border" style="width: 90%; max-width: 500px;">
            
            <div class="d-flex justify-content-between align-items-center p-3 border-bottom bg-light rounded-top">
                <h5 class="mb-0 fw-bold">Add Parking Lot</h5>
                <div>
                    <button class="btn btn-outline-secondary btn-sm me-2" @click="resetForm">Reset</button>
                    <button class="btn btn-outline-dark btn-sm" @click="$emit('close')">Close</button>
                </div>
            </div>
            
            <div class="p-4">
                <form @submit.prevent="addParkingLot">
                    
                    <div class="mb-3">
                        <label class="form-label fw-semibold">Prime Location Name:</label>
                        <input 
                            type="text" 
                            class="form-control" 
                            v-model="prime_location_name"
                            placeholder="Enter Prime Location Name"
                            required
                        >
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label fw-semibold">Address:</label>
                        <input 
                            type="text" 
                            class="form-control" 
                            v-model="address"
                            placeholder="Enter Address"
                            required
                        >
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label fw-semibold">Pincode:</label>
                        <input 
                            type="text" 
                            class="form-control" 
                            v-model="pincode"
                            placeholder="Enter Pincode"
                            required
                        >
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label fw-semibold">Price (₹):</label>
                        <input 
                            type="number" 
                            class="form-control" 
                            v-model="price"
                            placeholder="Enter Price"
                            min="0"
                            step="0.01"
                            required
                        >
                    </div>
                    
                    <div class="mb-4">
                        <label class="form-label fw-semibold">Number of Spots:</label>
                        <input 
                            type="number" 
                            class="form-control" 
                            v-model="number_of_spots"
                            placeholder="Enter Number of Spots"
                            min="1"
                            required
                        >
                    </div>

                    <div class="d-flex justify-content-end gap-2 pt-3 border-top">
                        <button type="button" class="btn btn-secondary" @click="resetForm">Reset</button>
                        <button type="submit" class="btn btn-primary">Add Parking Lot</button>
                    </div>
                    
                </form>
            </div>
        </div>
    </div>
</template>