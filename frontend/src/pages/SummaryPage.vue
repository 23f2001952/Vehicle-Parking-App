<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

// =====================
// Revenue Chart
// =====================
const barChartData = ref({
  labels: [],
  datasets: [
    {
      label: 'Total Revenue per Parking Lot',
      data: [],
      backgroundColor: '#36A2EB',
      borderColor: '#000',
      borderWidth: 1
    }
  ]
});

const barOptions = ref({
  responsive: true,
  plugins: {
    title: {
      display: true,
      text: 'Revenue by Parking Lot'
    },
    legend: {
      display: true,
      position: 'top'
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
});

async function fetchData() {
  try {
    const response = await axios.get(`${BACKEND_URL}/booking_history/analytics`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    });

    if (response.status === 200) {
      const data = response.data.data;
      const revenueMap = {};

      for (const item of data) {
        const lotId = `Lot ${item.lot_id}`;
        const revenue = parseFloat(item.parking_cost || 0);
        if (item.is_paid) {
          revenueMap[lotId] = (revenueMap[lotId] || 0) + revenue;
        }
      }

      barChartData.value = {
        labels: Object.keys(revenueMap),
        datasets: [
          {
            label: 'Total Revenue per Parking Lot',
            data: Object.values(revenueMap),
            backgroundColor: '#36A2EB',
            borderColor: '#000',
            borderWidth: 1
          }
        ]
      };
    }

  } catch (error) {
    console.error('Error fetching analytics:', error);
  }
}

// =====================
// Occupied vs Available Chart
// =====================
const lotsRevenue = ref({});
const occupancyChartData = ref({
  labels: [],
  datasets: []
});

const occupancyChartOptions = ref({
  responsive: true,
  plugins: {
    title: {
      display: true,
      text: 'Occupied vs Available Spots by Parking Lot'
    },
    legend: {
      display: true,
      position: 'top'
    },
    tooltip: {
      callbacks: {
        label: function (context) {
          return `${context.dataset.label}: ${context.raw}`;
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true
    }
  }
});

async function fetchParkingLotAnalytics() {
  try {
    const response = await axios.get(`${BACKEND_URL}/parking_lot/analytics`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    });

    if (response.status === 200) {
      lotsRevenue.value = response.data.data;

      const labels = [];
      const occupied = [];
      const available = [];

      for (const [lotId, stats] of Object.entries(lotsRevenue.value)) {
        labels.push(`Lot ${lotId}`);
        occupied.push(stats.occupied_spots || 0);
        available.push(stats.available_spots || 0);
      }

      occupancyChartData.value = {
        labels,
        datasets: [
          {
            label: 'Occupied Spots',
            data: occupied,
            backgroundColor: '#FF6384'
          },
          {
            label: 'Available Spots',
            data: available,
            backgroundColor: '#36A2EB'
          }
        ]
      };
    }

  } catch (error) {
    console.error('Error fetching parking lot analytics:', error);
  }
}

onMounted(() => {
  fetchData();
  fetchParkingLotAnalytics();
});
</script>

<template>
  <div class="row">
    <!-- Revenue Chart -->
    <div class="col-lg-6 mb-4">
      <div class="card">
        <div class="card-header">
          <h5 class="card-title mb-0">Revenue by Parking Lot</h5>
        </div>
        <div class="card-body">
          <Bar :data="barChartData" :options="barOptions" :height="300" />
        </div>
      </div>
    </div>

    <!-- Occupancy Chart -->
    <div class="col-lg-6 mb-4">
      <div class="card">
        <div class="card-header">
          <h5 class="card-title mb-0">Occupied vs Available Spots</h5>
        </div>
        <div class="card-body">
          <Bar :data="occupancyChartData" :options="occupancyChartOptions" :height="300" />
        </div>
      </div>
    </div>
  </div>
</template>
