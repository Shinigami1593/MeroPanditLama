<template>
  <div class="booking-card">
    <img
      :src="getProviderImage()"
      :alt="booking.provider_name"
      class="booking-image"
    >
    <div class="booking-info">
      <h3>{{ booking.service_name || 'N/A' }}</h3>
      <p class="pandit-name">with {{ booking.provider_name }}</p>
      <p class="booking-date">{{ formatDate(booking.requested_date) }} - {{ getTimeSlotDisplay(booking.time_slot) }}</p>
    </div>
    <div class="booking-status">
      <span :class="['status-badge', `status-${booking.status.toLowerCase()}`]">
        {{ booking.status.charAt(0).toUpperCase() + booking.status.slice(1) }}
      </span>
    </div>
    <div class="booking-actions">
      <button
        v-if="status === 'Upcoming' && booking.can_cancel"
        @click="$emit('cancel', booking.id)"
        class="action-button cancel"
      >
        Cancel Booking
      </button>
      <a
        v-if="booking.provider_phone"
        :href="`tel:${booking.provider_phone}`"
        class="action-button contact"
      >
        Contact Provider
      </a>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  booking: {
    type: Object,
    required: true,
  },
  status: {
    type: String,
    required: true,
  },
})

// eslint-disable-next-line no-unused-vars
const emit = defineEmits(['cancel'])

// Helper function to get full image URL - SAME as landing page
const getImageUrl = (photoPath) => {
  if (!photoPath) return null
  // If it's already a full URL, return it
  if (photoPath.startsWith('http')) return photoPath
  // Otherwise, prepend your backend URL
  return `http://localhost:8000${photoPath}`
}

const getProviderImage = () => {
  // Get the image URL using the same logic as landing page
  const imageUrl = getImageUrl(props.booking.provider_photo)

  // If we have an image URL, return it, otherwise return dummy
  return imageUrl || '/images/dummy.png'
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  const day = date.getDate()
  const suffix = ['th', 'st', 'nd', 'rd']
  const v = day % 100
  const ordinal = day + (suffix[(v - 20) % 10] || suffix[v] || suffix[0])

  return date.toLocaleDateString('en-US', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  }).replace(/\d+/, ordinal)
}

const getTimeSlotDisplay = (slot) => {
  const slots = {
    'morning': 'Morning (8am - 12pm)',
    'afternoon': 'Afternoon (12pm - 4pm)',
    'evening': 'Evening (4pm - 8pm)'
  }
  return slots[slot] || slot
}
</script>

<style scoped>
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

.booking-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-end;
}

.action-button {
  padding: 6px 16px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  font-family: 'Rubik', sans-serif;
  border: none;
  text-decoration: none;
  text-align: center;
  min-width: 120px;
}

.action-button.cancel {
  color: #E74C3C;
  background: white;
  border: 1px solid #E74C3C;
}

.action-button.cancel:hover {
  background: #E74C3C;
  color: white;
}

.action-button.contact {
  color: white;
  background: #A0673D;
}

.action-button.contact:hover {
  background: #8a5733;
}
</style>
