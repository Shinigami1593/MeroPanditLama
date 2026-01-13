<template>
  <div class="app-wrapper">
    <Navbar :isAuthenticated="true" />
    <div class="my-bookings-container">
      <h1>My Bookings</h1>

      <div class="tabs">
        <button
          @click="activeTab = 'upcoming'"
          :class="{ active: activeTab === 'upcoming' }"
          class="tab-button"
        >
          Upcoming
        </button>
        <button
          @click="activeTab = 'completed'"
          :class="{ active: activeTab === 'completed' }"
          class="tab-button"
        >
          Completed
        </button>
        <button
          @click="activeTab = 'cancelled'"
          :class="{ active: activeTab === 'cancelled' }"
          class="tab-button"
        >
          Cancelled
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <p>Loading bookings...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-message">
        {{ error }}
      </div>

      <!-- Bookings Content -->
      <div v-else class="bookings-content">
        <UpcomingBookings
          v-if="activeTab === 'upcoming'"
          :bookings="upcomingBookings"
          @refresh="loadBookings"
        />
        <CompletedBookings
          v-if="activeTab === 'completed'"
          :bookings="completedBookings"
        />
        <CancelledBookings
          v-if="activeTab === 'cancelled'"
          :bookings="cancelledBookings"
        />
      </div>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Navbar from '@/components/NavbarComponent.vue'
import Footer from '@/components/FooterComponent.vue'
import UpcomingBookings from '../../../components/booking/UpcomingBooking.vue'
import CompletedBookings from '../../../components/booking/CompletedBooking.vue'
import CancelledBookings from '../../../components/booking/CancelledBooking.vue'
import { bookingsAPI } from '@/axios'

const activeTab = ref('upcoming')
const loading = ref(true)
const error = ref('')
const bookings = ref([])

// Computed properties for filtered bookings
const upcomingBookings = computed(() => {
  return bookings.value.filter(b =>
    b.status === 'pending' || b.status === 'confirmed'
  )
})

const completedBookings = computed(() => {
  return bookings.value.filter(b => b.status === 'completed')
})

const cancelledBookings = computed(() => {
  return bookings.value.filter(b => b.status === 'cancelled')
})

// Load bookings on mount
onMounted(() => {
  loadBookings()
})

// Load bookings from backend
const loadBookings = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await bookingsAPI.getBookings()
    console.log('Bookings response:', response.data) // Debug log
    bookings.value = response.data.results || response.data || []
    console.log('Loaded bookings:', bookings.value) // Debug log
  } catch (err) {
    console.error('Error loading bookings:', err)
    error.value = 'Failed to load bookings. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;600;700&display=swap');

.app-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100vw;
}

.my-bookings-container {
  width: 100%;
  flex: 1;
  background-color: #FFF5E1;
  padding: 40px 360px;
  box-sizing: border-box;
}

h1 {
  color: #A0673D;
  font-size: 32px;
  margin-bottom: 30px;
  font-weight: 600;
  font-family: 'Rubik', sans-serif;
}

.tabs {
  display: flex;
  gap: 30px;
  margin-bottom: 40px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 15px;
}

.tab-button {
  background: none;
  border: none;
  color: #999;
  font-size: 14px;
  cursor: pointer;
  padding: 0;
  font-weight: 500;
  transition: color 0.3s;
}

.tab-button.active {
  color: #A0673D;
  border-bottom: 2px solid #A0673D;
  margin-bottom: -17px;
}

.tab-button:hover {
  color: #A0673D;
}

.loading-container {
  text-align: center;
  padding: 60px 20px;
  font-size: 16px;
  color: #666;
}

.error-message {
  max-width: 600px;
  margin: 20px auto;
  padding: 16px 24px;
  background: #fee;
  color: #c33;
  border-radius: 8px;
  text-align: center;
  font-size: 14px;
}

.bookings-content {
  min-height: 400px;
}

@media (max-width: 768px) {
  .my-bookings-container {
    padding: 20px;
  }

  h1 {
    font-size: 24px;
    margin-bottom: 20px;
  }

  .tabs {
    gap: 15px;
  }
}
</style>
