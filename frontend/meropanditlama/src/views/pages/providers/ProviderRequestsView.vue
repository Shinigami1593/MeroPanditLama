<template>
  <div class="provider-layout">
    <ProviderNavbar />
    <div class="provider-main">
      <h2 class="page-title">Booking Requests</h2>
      <p class="page-subtitle">Review and manage booking requests from customers.</p>
      <!-- Placeholder for requests -->
      <div class="requests-list">
        <div class="request-card" v-for="request in requests" :key="request.id">
          <div class="request-header">
            <div class="request-left">
              <img src="/images/dummy.png" alt="Profile" class="user-image">
              <div class="request-info">
                <h3 class="service-name">{{ request.serviceName }}</h3>
                <p class="request-from">Request from <strong>{{ request.userName }}</strong></p>
                <p class="request-date">{{ request.date }}</p>
              </div>
            </div>
            <div class="request-actions">
              <button class="btn-decline" @click="declineRequest(request.id)">Decline</button>
              <button class="btn-accept" @click="acceptRequest(request.id)">Accept</button>
            </div>
          </div>
          <div class="request-note" v-if="request.note">
            <strong>Note from user:</strong> "{{ request.note }}"
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

// Sample booking requests data
const requests = ref([
  {
    id: 1,
    serviceName: 'Wedding Ceremony',
    userName: 'Anjali Sharma',
    date: '25th December 2024',
    userImage: '/placeholder.svg?height=60&width=60',
    note: 'The ceremony will be at Hotel Yak & Yeti. Please be there by 9 AM.'
  },
  {
    id: 2,
    serviceName: 'Griha Pravesh Puja',
    userName: 'Rohan Thapa',
    date: '5th January 2025',
    userImage: '/placeholder.svg?height=60&width=60',
    note: 'This is for our new apartment in Bhaisepati. It\'s a small gathering.'
  },
  {
    id: 3,
    serviceName: 'Satyanarayan Puja',
    userName: 'Sunita Karki',
    date: '12th January 2025',
    userImage: '/placeholder.svg?height=60&width=60',
    note: 'Family gathering at our home. Please confirm the timing.'
  }
])

const acceptRequest = (id) => {
  const index = requests.value.findIndex(r => r.id === id)
  if (index > -1) {
    requests.value.splice(index, 1)
  }
}

const declineRequest = (id) => {
  const index = requests.value.findIndex(r => r.id === id)
  if (index > -1) {
    requests.value.splice(index, 1)
  }
}
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
  color: #333;
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 24px 0;
}

.requests-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.request-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.request-left {
  display: flex;
  gap: 16px;
  flex: 1;
}

.user-image {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
}

.request-info {
  flex: 1;
}

.service-name {
  color: #333;
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 4px 0;
}

.request-from {
  color: #666;
  font-size: 14px;
  margin: 0 0 4px 0;
}

.request-date {
  color: #999;
  font-size: 13px;
  margin: 0;
}

.request-actions {
  display: flex;
  gap: 12px;
}

.btn-decline,
.btn-accept {
  padding: 8px 20px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  font-family: 'Rubik', sans-serif;
  transition: all 0.2s;
}

.btn-decline {
  background: #E53E3E;
  color: white;
}

.btn-decline:hover {
  background: #C53030;
}

.btn-accept {
  background: #38A169;
  color: white;
}

.btn-accept:hover {
  background: #2F8659;
}

.request-note {
  background: #FFFACD;
  padding: 12px 16px;
  border-radius: 6px;
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}

.request-note strong {
  color: #333;
}
</style>
