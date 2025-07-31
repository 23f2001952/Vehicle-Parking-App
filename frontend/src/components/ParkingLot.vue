<script setup>
import { ref, defineProps,defineEmits } from 'vue'
import axios from 'axios'
import ParkingSpot from './ParkingSpot.vue'
import UpdateParkingLot from './UpdateParkingLot.vue'
import { useToast } from 'vue-toast-notification'
import { setToast } from '../toast.js'
import BookParkingSpot from './BookParkingSpot.vue'

const toast = useToast()
setToast(toast)

const role = localStorage.getItem('role')

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL
const props = defineProps({
    parkingLot: {
        type: Object,
        required: true
    }
})

const emit = defineEmits(['update', 'delete'])

const spots = ref([])

const OpenupdateParkingLot = ref(false)
const OpenBookParkingSpot = ref(false)
const availableSpots = ref(0)

async function getavailableSpots() {
    try {
        const response = await axios.get(`${BACKEND_URL}/parking_lot/get_available_spots/${props.parkingLot.id}`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        })
        if (response.status === 200) {
            availableSpots.value = response['data']['AvailableSpots'].length
            console.log("Spots fetched successfully:", availableSpots.value)
        }
    } catch (error) {
        console.error('Error fetching available spots:', error)
    }
}


async function deleteParkingLot(id) {
    try {
        const response = await axios.delete(`${BACKEND_URL}/parking_lot/delete/${id}`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        })
        if (response.status === 200) {
            console.log('Parking Lot deleted successfully:', response.data)
            toast.success('Parking Lot deleted successfully!')
            emit('delete')
        } else {
            console.error('Failed to delete Parking Lot:', response.status)
        }
    } catch (error) {
        console.error('Error deleting parking lot:', error)
    }
}

async function getParkingLotDetails() {
    try {
        const response = await axios.get(`${BACKEND_URL}/parking_lot/get/${props.parkingLot.id}`,{
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });
        if (response.status == 200) {
            spots.value = response.data.spots;
            console.log("Spots fetched successfully:", spots.value);
            getavailableSpots();
        }


        
    } catch (error) {
        console.error('Error fetching parking lot details:', error);
        return null;
    }
}

function handleUpdate() {
    emit('update');
    getParkingLotDetails();
}

getParkingLotDetails();
</script>


<template>
  <div class="card h-100 border border-black bg-white shadow-sm">
    <div class="card-body">
      
      <div class="d-flex justify-content-between borde-bottom border-black align-items-center mb-3 border-bottom pb-2">
        <h5 class="card-title fw-bold mb-0">
          #{{ parkingLot.id }}
        </h5>
        <div>
          <span class="badge border border-black bg-success" v-if="availableSpots !== 0">{{ availableSpots }}/{{ parkingLot.number_of_spots }} Spots Available</span>
          <span class="badge border border-black bg-danger" v-else>No Spots Available</span>
        </div>
        <div>
          <button class="btn btn-outline-warning btn-sm me-2" v-if="role === 'admin'" @click="OpenupdateParkingLot = true">Update</button>
          <button class="btn btn-outline-danger btn-sm" v-if="role === 'admin'" @click="deleteParkingLot(parkingLot.id)">Delete</button>
          <button class="btn btn-outline-info btn-sm" v-if="role === 'user' && availableSpots > 0" @click="OpenBookParkingSpot = true"> Book</button>   
        </div>
      </div>

     <BookParkingSpot v-if="OpenBookParkingSpot" :parkinglot="parkingLot" @close="OpenBookParkingSpot = false" @update="handleUpdate" />    
      <UpdateParkingLot v-if="OpenupdateParkingLot" :parkingLot="parkingLot" @close="OpenupdateParkingLot = false" @update="handleUpdate" />

      <div class="d-flex flex-wrap gap-2 mb-3">
        <ParkingSpot v-for="spot in spots" :key="spot.id" :parkingSpot="spot" />
      </div>

      <ul class="list-unstyled small">
        <li><strong>Price:</strong> ₹{{ parkingLot.price }}</li>
        <li><strong>Address:</strong> {{ parkingLot.address }}</li>
        <li><strong>Spots:</strong> {{ parkingLot.number_of_spots }}</li>
        <li><strong>Pincode:</strong> {{ parkingLot.pincode }}</li>
        <li><strong>Prime Location:</strong> {{ parkingLot.prime_location_name }}</li>
      </ul>

    </div>
  </div>
</template> 
