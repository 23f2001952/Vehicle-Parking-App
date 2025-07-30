<script setup>
import { defineProps } from 'vue'

const props = defineProps({
    parkingSpot: {
        type: Object,
        required: true
    }
})
</script>

<template>
    <div>
        <p>Spot ID: {{ parkingSpot.id }}</p>
        <p>Status: {{ parkingSpot.status }}</p>
    </div>
</template>