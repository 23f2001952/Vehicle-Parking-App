<script setup>
import axios from 'axios'
import { ref, defineProps, defineEmits } from 'vue'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

const props = defineProps({
    parkingSpot: {
        type: Object,
        required: true
    }
})

const emit = defineEmits(['close']);
const spotId = ref(props.parkingSpot.id)
const spotDetails = ref(null)
const history = ref([])

async function getSpotDetails() {
    try {
        const response = await axios.get(`${BACKEND_URL}/parking_spot/get/${spotId.value}`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        })
        if (response.status === 200) {
            spotDetails.value = response.data; // Fixed: remove .response, just use response.data
            history.value = response.data.booking_history;
            console.log('Spot details fetched successfully:', response.data);
        }
    } catch (error) {
        console.error('Error fetching spot details:', error);
    }
}

getSpotDetails();

function closeInfo() {
    emit('close');
}
</script>

<template>
    <div class="position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center" style="background-color: rgba(0,0,0,0.5); z-index: 1050;">
        <div class="bg-white rounded shadow-lg border" style="width: 90%; max-width: 600px;">
            
            <div class="d-flex justify-content-between align-items-center p-3 border-bottom bg-light rounded-top">
                <h5 class="mb-0 fw-bold">Parking Spot #{{ spotId }}</h5>
                <button class="btn btn-outline-dark btn-sm" @click="closeInfo">Close</button>
            </div>
            <div class="p-4" v-if="spotDetails">
                <div class="row mb-4">
                    <div class="col-md-6">
                        <h6 class="fw-bold mb-3">Location Details</h6>
                        <ul class="list-unstyled">
                            <li class="mb-2"><strong>Prime Location:</strong> {{ spotDetails.prime_location_name }}</li>
                            <li class="mb-2"><strong>Address:</strong> {{ spotDetails.address }}</li>
                            <li class="mb-2"><strong>Pincode:</strong> {{ spotDetails.pincode }}</li>
                        </ul>
                    </div>
                    <div class="col-md-6">
                        <h6 class="fw-bold mb-3">Spot Details</h6>
                        <ul class="list-unstyled">
                            <li class="mb-2"><strong>Price:</strong> ₹{{ spotDetails.price }}/hour</li>
                            <li class="mb-2"><strong>Status:</strong> 
                                <span class="badge" :class="spotDetails.status === 'occupied' ? 'bg-danger' : 'bg-success'">
                                    {{ spotDetails.status }}
                                </span>
                            </li>
                            <li class="mb-2"><strong>Lot ID:</strong> {{ spotDetails.lot_id }}</li>
                        </ul>
                    </div>
                </div>

                <div v-if="history && history.length > 0">
                    <h6 class="fw-bold mb-3 border-top pt-3">Booking History</h6>
                    <div class="table-responsive" style="max-height: 200px; overflow-y: auto;">
                        <table class="table table-sm table-striped">
                            <thead class="table-dark">
                                <tr>
                                    <th>Booking ID</th>
                                    <th>Vehicle</th>
                                    <th>Start Time</th>
                                    <th>End Time</th>
                                    <th>Cost</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="booking in history" :key="booking.id">
                                    <td>#{{ booking.id }}</td>
                                    <td>{{ booking.vehicle_number }}</td>
                                    <td>{{ new Date(booking.start_time).toLocaleString() }}</td>
                                    <td>{{ booking.end_time ? new Date(booking.end_time).toLocaleString() : 'Active' }}</td>
                                    <td>{{ booking.parking_cost ? '₹' + booking.parking_cost : '-' }}</td>
                                    <td>
                                        <span class="badge" :class="booking.is_paid ? 'bg-success' : 'bg-warning'">
                                            {{ booking.is_paid ? 'Paid' : 'Unpaid' }}
                                        </span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div v-else-if="history && history.length === 0" class="text-center text-muted border-top pt-3">
                    <p>No booking history available for this spot.</p>
                </div>
            </div>

            <div v-else class="p-4 text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">Loading spot details...</p>
            </div>
        </div>
    </div>
</template>