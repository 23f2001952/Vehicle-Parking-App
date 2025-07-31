<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { Bar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const userSummary = ref(null);

const barChartData = ref({
  labels: [],
  datasets: [
    {
      label: 'Cost per Parking Lot',
      data: [],
      backgroundColor: '#0d6efd',
      borderColor: '#0a58ca',
      borderWidth: 1
    }
  ]
});

const barChartOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: true,
      position: 'top'
    },
    title: {
      display: true,
      text: 'User Revenue by Parking Lot'
    },
    tooltip: {
      callbacks: {
        label: function (context) {
          return `₹ ${context.raw}`;
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true
    }
  }
};

async function fetchUserSummary() {
  try {
    const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/auth/analytics`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    });

    if (response.status === 200) {
      userSummary.value = response.data.data;

      // Set chart data
      const lotCosts = userSummary.value.lot_costs;
      const labels = Object.keys(lotCosts).map(id => `Lot ${id}`);
      const values = Object.values(lotCosts).map(cost => parseFloat(cost));

      barChartData.value.labels = labels;
      barChartData.value.datasets[0].data = values;
    }
  } catch (error) {
    console.error('Error fetching user summary:', error);
  }
}

fetchUserSummary();
</script>

<template>
  <div class="container mt-5">
    <div v-if="userSummary">
      <div class="card shadow-sm mb-4">
        <div class="card-body">
          <h4 class="card-title">Summary for: <strong>{{ userSummary.username }}</strong></h4>
          <ul class="list-group list-group-flush mt-3">
            <li class="list-group-item"><strong>User ID:</strong> {{ userSummary.user_id }}</li>
            <li class="list-group-item"><strong>Total Bookings:</strong> {{ userSummary.total_bookings }}</li>
            <li class="list-group-item"><strong>Total Cost:</strong> ₹{{ userSummary.total_cost }}</li>
          </ul>
        </div>
      </div>

      <div class="card shadow-sm">
        <div class="card-body">
          <h5 class="card-title mb-3">Parking Lot Revenue Chart</h5>
          <Bar :data="barChartData" :options="barChartOptions" :height="300" />
        </div>
      </div>
    </div>
  </div>
</template>
