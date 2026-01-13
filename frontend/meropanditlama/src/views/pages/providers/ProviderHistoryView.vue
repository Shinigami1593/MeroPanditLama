<template>
  <div class="provider-layout">
    <ProviderNavbar />
    <div class="provider-main">
      <h2 class="page-title">Booking History</h2>
      <p class="page-subtitle">View your past bookings and completed services.</p>
      <!-- Placeholder for history -->
      <div class="tabs">
        <button
          class="tab"
          :class="{ active: activeTab === 'upcoming' }"
          @click="activeTab = 'upcoming'"
        >
          Upcoming
        </button>
        <button
          class="tab"
          :class="{ active: activeTab === 'completed' }"
          @click="activeTab = 'completed'"
        >
          Completed
        </button>
        <button
          class="tab"
          :class="{ active: activeTab === 'cancelled' }"
          @click="activeTab = 'cancelled'"
        >
          Cancelled
        </button>
      </div>

      <div class="bookings-container">
        <div v-if="activeTab === 'upcoming'" class="bookings-list">
          <div v-for="booking in upcomingBookings" :key="booking.id" class="booking-card">
            <div class="booking-content">
              <img src="/images/dummy.png" alt="booking" class="booking-image" />
              <div class="booking-info">
                <h3 class="service-name">{{ booking.serviceName }}</h3>
                <p class="user-info">with {{ booking.name }}</p>
                <p class="booking-date">{{ booking.date }}</p>
              </div>
            </div>
            <div class="booking-actions">
              <span class="status-badge confirmed">{{ booking.status }}</span>
              <span class="price">{{ booking.price }}</span>
              <div class="action-links">
                <a href="#" class="action-link cancel">Cancel Booking</a>
              </div>
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'completed'" class="bookings-list">
          <div v-for="booking in completedBookings" :key="booking.id" class="booking-card">
            <div class="booking-content">
              <img src="/images/dummy.png"  :alt="booking.name" class="booking-image" />
              <div class="booking-info">
                <h3 class="service-name">{{ booking.serviceName }}</h3>
                <p class="user-info">with {{ booking.name }}</p>
                <p class="booking-date">{{ booking.date }}</p>
              </div>
            </div>
            <div class="booking-actions">
              <span class="status-badge completed">{{ booking.status }}</span>
              <span class="price">{{ booking.price }}</span>
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'cancelled'" class="bookings-list">
          <div v-for="booking in cancelledBookings" :key="booking.id" class="booking-card">
            <div class="booking-content">
              <img src="/images/dummy.png" :alt="booking.name" class="booking-image" />
              <div class="booking-info">
                <h3 class="service-name">{{ booking.serviceName }}</h3>
                <p class="user-info">with {{ booking.name }}</p>
                <p class="booking-date">{{ booking.date }}</p>
              </div>
            </div>
            <div class="booking-actions">
              <span class="status-badge cancelled">{{ booking.status }}</span>
              <span class="price">{{ booking.price }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ProviderNavbar from '../../../components/ProviderNavbar.vue'
import Footer from '../../../components/FooterComponent.vue'

const activeTab = ref('upcoming')

const upcomingBookings = ref([
  {
    id: 1,
    serviceName: 'Wedding Ceremony',
    name: 'Anjali Sharma',
    date: '25th December 2024',
    status: 'Confirmed',
    price: 'NPR 5,100',
    image: '/placeholder.svg?height=60&width=60'
  }
])

const completedBookings = ref([
  {
    id: 2,
    serviceName: 'Puja Ceremony',
    name: 'Rohan Thapa',
    date: '10th December 2024',
    status: 'Completed',
    price: 'NPR 3,500',
    image: '/placeholder.svg?height=60&width=60'
  }
])

const cancelledBookings = ref([
  {
    id: 3,
    serviceName: 'Griha Pravesh',
    name: 'Priya Singh',
    date: '5th December 2024',
    status: 'Cancelled',
    price: 'NPR 4,200',
    image: '/placeholder.svg?height=60&width=60'
  }
])
</script>

<style scoped>
* {
  font-family: 'Rubik', sans-serif;
}

.provider-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: #F5EDE0;
  width: 100%;
  box-sizing: border-box;
}

.provider-main {
  flex: 1;
  padding: 40px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}

.page-title {
  color: #1a1a1a;
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 32px 0;
}

.page-subtitle {
  color: #666;
  font-size: 16px;
  margin: 0 0 24px 0;
}

.tabs {
  display: flex;
  gap: 32px;
  border-bottom: 1px solid #ddd;
  margin-bottom: 32px;
}

.tab {
  background: none;
  border: none;
  color: #999;
  font-size: 16px;
  font-weight: 500;
  padding: 12px 0;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.3s;
}

.tab.active {
  color: #1a1a1a;
  border-bottom-color: #A0673D;
}

.tab:hover {
  color: #A0673D;
}

.bookings-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.bookings-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.booking-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.booking-content {
  display: flex;
  gap: 16px;
  align-items: center;
  flex: 1;
}

.booking-image {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
}

.booking-info {
  flex: 1;
}

.service-name {
  color: #1a1a1a;
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.user-info {
  color: #666;
  font-size: 14px;
  margin: 4px 0 0 0;
}

.booking-date {
  color: #999;
  font-size: 13px;
  margin: 4px 0 0 0;
}

.booking-actions {
  display: flex;
  gap: 16px;
  align-items: center;
  justify-content: flex-end;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.confirmed {
  background: #E8F5E9;
  color: #2F711B;
}

.status-badge.completed {
  background: #86ABF2;
  color: #1453DA;
}

.status-badge.cancelled {
  background: #FFE0E0;
  color: #D32F2F;
}

.price {
  color: #A0673D;
  font-weight: 600;
  font-size: 14px;
  min-width: 100px;
  text-align: right;
}

.action-links {
  display: flex;
  gap: 8px;
}

.action-link {
  color: #A0673D;
  text-decoration: none;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.3s;
}

.action-link:hover {
  color: #8B5A2B;
}

.action-link.cancel {
  color: #E53935;
}

.action-link.cancel:hover {
  color: #C62828;
}
</style>
