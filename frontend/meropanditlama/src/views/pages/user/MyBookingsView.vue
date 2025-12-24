<template>
  <div class="app-wrapper">
    <Navbar :isAuthenticated="true" />

    <div class="my-bookings-container">
      <h1>My Booking</h1>

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

      <div class="bookings-content">
        <UpcomingBookings v-if="activeTab === 'upcoming'" />
        <CompletedBookings v-if="activeTab === 'completed'" />
        <CancelledBookings v-if="activeTab === 'cancelled'" />
      </div>
    </div>

    <Footer />
  </div>
</template>

<script setup>

import { ref, onMounted } from 'vue'
import Navbar from '@/components/NavbarComponent.vue'
import Footer from '@/components/FooterComponent.vue'
import UpcomingBookings from '../../../components/booking/UpcomingBooking.vue'
import CompletedBookings from '../../../components/booking/CompletedBooking.vue'
import CancelledBookings from '../../../components/booking/CancelledBooking.vue'

const activeTab = ref('upcoming')
const isAuthenticated = ref(false)

onMounted(() => {
  isAuthenticated.value = localStorage.getItem('isAuthenticated') === 'true'
})
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
