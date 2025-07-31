<script setup>
import {ref} from 'vue'
import ParkingLotContainer from './ParkingLotContainer.vue'
import BookingManager from './BookingManager.vue'

const activeTab = ref('parking-lots');
</script>

<template>
    <div class="container-fluid border border-black rounded mt-3">
        

        <ul class="nav nav-tabs nav-fill mb-0">
            <li class="nav-item">
                <button 
                    class="nav-link fw-bold border-0 text-dark" 
                    :class="activeTab === 'parking-lots' ? 'active bg-dark text-white' : 'bg-light'"
                    @click="activeTab = 'parking-lots'"
                >
                    Find Parking
                </button>
            </li>   
            <li class="nav-item">
                <button 
                    class="nav-link fw-bold border-0 text-dark" 
                    :class="activeTab === 'bookings' ? 'active bg-dark text-white' : 'bg-light'"
                    @click="activeTab = 'bookings'"
                >
                    My Bookings
                </button>
            </li>
            
        </ul>

        <div class="tab-content">
            <div class="tab-pane" :class="{ 'show active': activeTab === 'bookings' }">
                <BookingManager v-if="activeTab === 'bookings'" />
            </div>
            <div class="tab-pane" :class="{ 'show active': activeTab === 'parking-lots' }">
                <ParkingLotContainer v-if="activeTab === 'parking-lots'" />
            </div>
        </div>
        
    </div>
</template>