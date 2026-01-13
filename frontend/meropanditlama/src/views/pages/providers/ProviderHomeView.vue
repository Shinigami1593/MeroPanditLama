<template>
  <div class="provider-layout">
    <ProviderNavbar />
    <div class="provider-main">
      <div class="greeting-section">
        <h2 class="greeting-title">Namaste, Pandit Ram</h2>
        <p class="greeting-subtitle">Here is your daily overview.</p>
      </div>

      <div class="content-wrapper">
        <div class="left-section">
          <div class="upcoming-card">
            <div class="card-header">
              <h3>Upcoming Bookings</h3>
              <a href="#" class="view-all">View All</a>
            </div>
            <div class="bookings-list">
              <div v-for="booking in upcomingBookings" :key="booking.id" class="booking-item">
                <div class="booking-info">
                  <h4>{{ booking.service }}</h4>
                  <div class="booking-detail">
                    <i class="bi bi-calendar-event"></i>
                    <span>{{ booking.date }}</span>
                  </div>
                  <div class="booking-detail">
                    <i class="bi bi-person"></i>
                    <span>{{ booking.customer }}</span>
                  </div>
                </div>
                <button class="view-details-btn">View Details</button>
              </div>
            </div>
          </div>
        </div>

        <div class="right-section">
          <div class="availability-card">
            <div class="availability-icon">
              <i class="bi bi-clock"></i>
            </div>
            <h3>Set Availability</h3>
            <p>Manage your calendar for the upcoming month.</p>
            <button class="update-calendar-btn">Update Calendar</button>
          </div>

          <div class="profile-card">
            <div class="profile-header">
              <img src="/images/dummy.png" alt="Profile" class="profile-image">
              <div class="profile-info">
                <h4>Pandit Ram Prasad</h4>
                <a href="#" class="edit-profile-link">Edit Profile</a>
              </div>
            </div>

            <div class="services-section">
              <h5>My Services</h5>
              <div class="services-tags">
                <span class="service-tag">Puja</span>
                <span class="service-tag">Wedding</span>
                <span class="service-tag">Griha Pravesh</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import ProviderNavbar from '../../../components/ProviderNavbar.vue'
import Footer from '../../../components/FooterComponent.vue'

const upcomingBookings = [
  {
    id: 1,
    service: 'Wedding Ceremony',
    date: '25th December 2024',
    customer: 'Anjali Sharma'
  },
  {
    id: 2,
    service: 'Griha Pravesh Puja',
    date: '5th January 2025',
    customer: 'Rohan Thapa'
  }
]
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

.greeting-section {
  margin-bottom: 40px;
}

.greeting-title {
  color: #A0673D;
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 8px 0;
}

.greeting-subtitle {
  color: #666;
  font-size: 16px;
  margin: 0;
}

.content-wrapper {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

.left-section {
  flex: 1;
}

.upcoming-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.card-header h3 {
  color: #333;
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.view-all {
  color: #A0673D;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
}

.bookings-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.booking-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  background: #F9F9F9;
}

.booking-info h4 {
  color: #333;
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.booking-detail {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
  font-size: 14px;
  margin-bottom: 4px;
}

.booking-detail i {
  color: #A0673D;
  font-size: 14px;
}

.view-details-btn {
  background: white;
  border: 1px solid #A0673D;
  color: #A0673D;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  font-family: 'Rubik', sans-serif;
}

.view-details-btn:hover {
  background: #A0673D;
  color: white;
}

.right-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.availability-card {
  background: white;
  border-radius: 12px;
  padding: 32px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.availability-icon {
  font-size: 48px;
  color: #D4A574;
  margin-bottom: 16px;
}

.availability-card h3 {
  color: #333;
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.availability-card p {
  color: #666;
  font-size: 14px;
  margin: 0 0 20px 0;
}

.update-calendar-btn {
  background: #C19A6B;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  font-family: 'Rubik', sans-serif;
  transition: background 0.2s;
}

.update-calendar-btn:hover {
  background: #B08860;
}

.profile-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.profile-header {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.profile-image {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
}

.profile-info h4 {
  color: #333;
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 4px 0;
}

.edit-profile-link {
  color: #A0673D;
  text-decoration: none;
  font-size: 12px;
  font-weight: 500;
}

.edit-profile-link:hover {
  text-decoration: underline;
}

.services-section h5 {
  color: #333;
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 12px 0;
}

.services-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.service-tag {
  background: #F5EDE0;
  color: #A0673D;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

@media (max-width: 1024px) {
  .content-wrapper {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .provider-main {
    padding: 20px;
  }

  .greeting-title {
    font-size: 24px;
  }

  .right-section {
    order: -1;
  }
}
</style>
