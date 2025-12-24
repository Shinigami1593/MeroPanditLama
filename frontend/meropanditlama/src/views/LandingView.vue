<template>
  <div class="browse-page">
    <Navbar :isAuthenticated="true" />

    <main class="main-content">
      <!-- Welcome Section -->
      <section class="welcome-section">
        <h1 class="welcome-title">Welcome, John Doe</h1>
      </section>

      <!-- Booking Options -->
      <section class="booking-options">
        <div class="booking-card" @click="navigateToBooking('browse')">
          <div class="card-icon">
            <!-- <svg width="60" height="60" viewBox="0 0 60 60" fill="none">
              <path d="M30 5L35 15H25L30 5Z" fill="#AE664A"/>
              <rect x="20" y="15" width="20" height="8" fill="#AE664A"/>
              <path d="M15 23L20 15H40L45 23H15Z" fill="#AE664A"/>
              <rect x="18" y="23" width="24" height="6" fill="#AE664A"/>
              <path d="M12 29L18 23H42L48 29H12Z" fill="#AE664A"/>
              <rect x="15" y="29" width="30" height="8" fill="#AE664A"/>
              <rect x="25" y="37" width="10" height="18" fill="#AE664A"/>
            </svg> -->
          </div>
          <h3 class="card-title">Book Pandit</h3>
          <p class="card-subtitle">For Puja, Weddings, and Rituals</p>
        </div>

        <div class="booking-card" @click="navigateToBooking('browse')">
          <div class="card-icon">
            <!-- <svg width="60" height="60" viewBox="0 0 60 60" fill="none">
              <ellipse cx="30" cy="20" rx="8" ry="6" fill="#AE664A"/>
              <path d="M30 26C25 26 22 28 22 32V40C22 42 24 44 26 44H34C36 44 38 42 38 40V32C38 28 35 26 30 26Z" fill="#AE664A"/>
              <circle cx="30" cy="36" r="4" fill="#F5E6D3"/>
              <rect x="28" y="44" width="4" height="6" fill="#AE664A"/>
            </svg> -->
          </div>
          <h3 class="card-title">Book Lama</h3>
          <p class="card-subtitle">For Puja, Weddings, and Rituals</p>
        </div>
      </section>

      <!-- View All Link -->
      <div class="view-all-container">
        <a href="#" class="view-all-link" @click="navigateToBooking('browse')">View All</a>
      </div>

      <!-- Pandit Profiles Horizontal Scroll -->
      <section class="profiles-section">
        <div class="profiles-scroll">
          <div v-for="pandit in pandits" :key="pandit.id" class="profile-card">
            <div class="profile-image">
              <div class="image-placeholder"></div>
            </div>
            <div class="profile-content">
              <span class="profile-tag">{{ pandit.type }}</span>
              <h3 class="profile-name">{{ pandit.name }}</h3>
              <p class="profile-price">Starts at {{ pandit.price }}</p>
              <button class="view-details-button" @click="viewDetails(pandit.id)">
                View Details
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Footer -->
      <Footer />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '../components/NavbarComponent.vue'
import Footer from '../components/FooterComponent.vue'

const router = useRouter()

// Sample data
const pandits = ref([
  { id: 1, type: 'Pandit', name: 'Pandit John Doe', price: 'NPR 5,300' },
  { id: 2, type: 'Pandit', name: 'Pandit John Doe', price: 'NPR 5,300' },
  { id: 3, type: 'Pandit', name: 'Pandit John Doe', price: 'NPR 5,300' },
  { id: 4, type: 'Pandit', name: 'Pandit John Doe', price: 'NPR 5,300' },
])

const navigateToBooking = (type) => {
  router.push(`/${type}`)
}

const viewDetails = (id) => {
  router.push(`/pandit/${id}`)
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700&display=swap');

* {
  font-family: 'Rubik', sans-serif;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.browse-page {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #FFF5E1;
}

.main-content {
  flex: 1;
  width: 100%;
}

/* Welcome Section */
.welcome-section {
  padding: 60px 40px 40px;
  text-align: center;
  background-color: #FFF5E1;
}

.welcome-title {
  font-size: 32px;
  font-weight: 600;
  color: #ae664a;
}

/* Booking Options */
.booking-options {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px 40px;
  display: flex;
  gap: 24px;
  justify-content: center;
}

.booking-card {
  flex: 1;
  background: white;
  border: 2px solid #e5d5c3;
  border-radius: 16px;
  padding: 32px 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.booking-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(174, 102, 74, 0.15);
  border-color: #ae664a;
}

.card-icon {
  margin-bottom: 16px;
  display: flex;
  justify-content: center;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #ae664a;
  margin-bottom: 8px;
}

.card-subtitle {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

/* View All */
.view-all-container {
  text-align: right;
  padding: 20px 10px;
  max-width: 1200px;
  margin: 0 auto;
}

.view-all-link {
  color: #ae664a;
  text-decoration: none;
  font-weight: 500;
  font-size: 14px;
}

.view-all-link:hover {
  text-decoration: underline;
}

/* Profiles Section */
.profiles-section {
  padding: 0 40px 60px;
  overflow-x: auto;
}

.profiles-scroll {
  display: flex;
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.profile-card {
  flex: 0 0 280px;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.profile-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.profile-image {
  width: 100%;
  height: 160px;
  background: #e5e7eb;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  background:
    linear-gradient(135deg, #f0f0f0 25%, transparent 25%),
    linear-gradient(225deg, #f0f0f0 25%, transparent 25%),
    linear-gradient(45deg, #f0f0f0 25%, transparent 25%),
    linear-gradient(315deg, #f0f0f0 25%, #e0e0e0 25%);
  background-size: 20px 20px;
  background-position:
    0 0,
    10px 0,
    10px -10px,
    0px 10px;
}

.profile-content {
  padding: 20px;
}

.profile-tag {
  display: inline-block;
  background: #f5e6d3;
  color: #ae664a;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 8px;
}

.profile-name {
  font-size: 16px;
  font-weight: 600;
  color: #000;
  margin: 8px 0;
}

.profile-price {
  font-size: 13px;
  color: #666;
  margin-bottom: 16px;
}

.view-details-button {
  width: 100%;
  padding: 10px;
  background: #ae664a;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.view-details-button:hover {
  background: #9a5838;
}
</style>
