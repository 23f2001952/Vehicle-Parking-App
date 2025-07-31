<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

const history = ref([]);
const showOnlyUnpaid = ref(false);

const filteredHistory = computed(() => {
    if (showOnlyUnpaid.value) {
        return history.value.filter(booking => booking.is_paid === false);
    }
    return history.value;
});

async function fetchBookingHistory() {
    try {
        const response = await axios.get(`${BACKEND_URL}/booking_history/get`,{
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem("access_token")}`
            }
        });
        if (response.status == 200) {
            history.value = response.data.data;
            console.log("Booking history fetched successfully:", history.value);
        }
        
    } catch (error) {
        console.error("Error fetching booking history:", error);
    }
}

async function releaseBooking(booking) {
    try {
        const response = await axios.put(`${BACKEND_URL}/parking_spot/update/${booking.id}`, {}, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem("access_token")}`
            }
        });
        if (response.status === 200) {
            console.log('Booking released successfully:', response.data);
            fetchBookingHistory(); 
        } else {
            console.error('Failed to release booking:', response.status);
        }
    } catch (error) {
        console.error('Error releasing booking:', error);
    }
}

fetchBookingHistory();
</script>

<template>
    <div class="container-fluid border border-black rounded p-4 my-4 bg-white">
        
        <div class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-2 border-black">
            <h3 class="mb-0">Booking History</h3>
            <div class="d-flex gap-2">
                <button 
                    class="btn btn-sm" 
                    :class="showOnlyUnpaid ? 'btn-warning' : 'btn-outline-warning'"
                    @click="showOnlyUnpaid = !showOnlyUnpaid"
                >
                    {{ showOnlyUnpaid ? 'Show All' : 'Show Unpaid Only' }}
                </button>
            </div>
        </div>

        <div v-if="filteredHistory.length === 0" class="text-center text-muted p-4">
            <h5>{{ showOnlyUnpaid ? 'No unpaid bookings found' : 'No bookings found' }}</h5>
            <p>{{ showOnlyUnpaid ? 'All your bookings are paid.' : 'You haven\'t made any bookings yet.' }}</p>
        </div>

        <div v-else class="row g-4">
            <div class="col-12" v-for="booking in filteredHistory" :key="booking.id">
                <div class="card border border-black bg-white shadow-sm">
                    <div class="card-body">
                        
                        <div class="d-flex justify-content-between align-items-center mb-3 border-bottom pb-2">
                            <h5 class="card-title fw-bold mb-0">
                                Booking #{{ booking.id }}
                            </h5>
                            <div class="d-flex gap-2 align-items-center">
                                <button class="btn btn-outline-danger btn-sm" v-if="booking.is_paid === false" @click="releaseBooking(booking)">Release</button>
                                <span class="badge bg-success" v-if="booking.is_paid === true">Paid</span>
                                <span class="badge bg-warning" v-if="booking.is_paid === false">Unpaid</span>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-md-6">
                                <ul class="list-unstyled small">
                                    <li class="mb-2"><strong>Spot ID:</strong> {{ booking.spot_id }}</li>
                                    <li class="mb-2"><strong>Start Time:</strong> {{ new Date(booking.start_time).toLocaleString() }}</li>
                                    <li class="mb-2" v-if="booking.end_time"><strong>End Time:</strong> {{ new Date(booking.end_time).toLocaleString() }}</li>
                                </ul>
                            </div>
                            <div class="col-md-6">
                                <ul class="list-unstyled small">
                                    <li class="mb-2" v-if="booking.end_time"><strong>Duration:</strong> {{ ((new Date(booking.end_time) - new Date(booking.start_time)) / 3600000).toFixed(2) }} hours</li>
                                    <li class="mb-2" v-if="booking.parking_cost"><strong>Total Cost:</strong> ₹{{ booking.parking_cost }}</li>
                                    <li class="mb-2" v-if="booking.vehicle_number"><strong>Vehicle Number:</strong> {{ booking.vehicle_number }}</li>
                                    <li class="mb-2" v-if="booking.location"><strong>Location:</strong> {{ booking.location }}</li>
                                </ul>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </div>
</template>