<template>
  <div class="booking-card">
    <img :src="booking.image && !booking.image.includes('placeholder') ? booking.image:'/images/dummy.png'" :alt="booking.panditName" class="booking-image">

    <div class="booking-info">
      <h3>{{ booking.serviceName }}</h3>
      <p class="pandit-name">with {{ booking.panditName }}</p>
      <p class="booking-date">{{ booking.date }}</p>
    </div>

    <div class="booking-status">
      <!-- Updated status badge with dynamic color classes -->
      <span :class="['status-badge', `status-${booking.status.toLowerCase()}`]">
        {{ booking.status }}
      </span>
    </div>

    <div class="booking-price">
      <span class="price">{{ booking.price }}</span>
      <!-- <a v-if="status === 'Upcoming'" href="#" class="action-link">Cancel booking</a> -->
      <!-- <a v-if="status === 'Completed'" href="#" class="action-link">Book Again</a> -->
    </div>
  </div>
</template>

<script setup>
defineProps({
  booking: {
    type: Object,
    required: true,
  },
  status: {
    type: String,
    required: true,
  },
})
</script>

<style scoped>
/* Added Rubik font import and global font styling */
@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;600;700&display=swap');

.booking-card {
  display: flex;
  align-items: center;
  gap: 20px;
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  font-family: 'Rubik', sans-serif;
}

.booking-image {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #E8D5C4;
}

.booking-info {
  flex: 1;
}

.booking-info h3 {
  color: #333;
  font-size: 16px;
  margin: 0 0 5px 0;
  font-weight: 600;
  font-family: 'Rubik', sans-serif;
}

.pandit-name {
  color: #666;
  font-size: 13px;
  margin: 0 0 3px 0;
  font-family: 'Rubik', sans-serif;
}

.booking-date {
  color: #999;
  font-size: 12px;
  margin: 0;
  font-family: 'Rubik', sans-serif;
}

.booking-status {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  text-align: center;
  font-family: 'Rubik', sans-serif;
}

/* Added specific status badge colors as per design requirements */
.status-confirmed {
  color: #2F711B;
  background-color: #47C92027;
}

.status-pending {
  color: #B58B00;
  background-color: #d9c42927;
}

.status-completed {
  color: #1453DA;
  background-color: #86ABF227;
}

.status-cancelled {
  color: #DC2626;
  background-color: #FCA5A5;
}

.booking-price {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-end;
}

.price {
  color: #A0673D;
  font-weight: 600;
  font-size: 14px;
  font-family: 'Rubik', sans-serif;
}

.action-link {
  color: #E74C3C;
  text-decoration: none;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.3s;
  font-family: 'Rubik', sans-serif;
}

.action-link:hover {
  color: #C0392B;
}
</style>
