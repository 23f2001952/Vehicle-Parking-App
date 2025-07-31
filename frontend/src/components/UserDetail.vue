<script setup>
import { ref, defineProps, defineEmits } from 'vue'

const props = defineProps({
    user: {
        type: Object,
        required: true
    }
})
console.log(props.user)
const userId = ref(props.user.id)
const username = ref(props.user.username)
const email = ref(props.user.email)
const address = ref(props.user.address || '')
const pincode = ref(props.user.pincode || '')
const BookingHistory = ref(props.user.history || [])    

const emit = defineEmits(['close'])

function closeInfo() {
    emit('close')
}
</script>

<template>
    <div class="position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center" style="background-color: rgba(0,0,0,0.5); z-index: 1050;">
        <div class="bg-white rounded shadow-lg border" style="width: 90%; max-width: 600px;">
            
            <div class="d-flex justify-content-between align-items-center p-3 border-bottom bg-light rounded-top">
                <h5 class="mb-0 fw-bold">User #{{ userId }}</h5>
                <button class="btn btn-outline-dark btn-sm" @click="closeInfo">Close</button>
            </div>
            <div class="p-4" >
                <div class="row mb-4">
                    <div class="col-md-6">
                        <h6 class="fw-bold mb-3">User Details</h6>
                        <ul class="list-unstyled">
                            <li class="mb-2"><strong>Username:</strong> {{ username }}</li>
                            <li class="mb-2"><strong>Email:</strong> {{ email }}</li>
                            <li class="mb-2"><strong>Address:</strong> {{ address }}</li>
                            <li class="mb-2"><strong>Pincode:</strong> {{ pincode }}</li>
                        </ul>
                    </div>
                </div>

                <div v-if="BookingHistory && BookingHistory.length > 0">
                    <h6 class="fw-bold mb-3 border-top pt-3">Booking History</h6>
                    <div class="table-responsive" style="max-height: 200px; overflow-y: auto;">
                        <table class="table table-sm table-striped ">
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
                                <tr v-for="booking in BookingHistory" :key="booking.id">
                                    <td>#{{booking.id }}</td>
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

                <div v-else-if="BookingHistory && BookingHistory.length === 0" class="text-center text-muted border-top pt-3">
                    <p>No booking history available for this spot.</p>
                </div>
            </div>
        </div>
    </div>
</template>