<template>
  <div class="booking-card">
    <img
      :src="getProviderImage()"
      :alt="booking.provider_name"
      class="booking-image"
    >
    <div class="booking-info">
      <h3>{{ getServiceName() }}</h3>
      <p class="pandit-name">with {{ booking.provider_name || 'Provider' }}</p>
      <!-- <p class="booking-date">{{ formatDate(booking.requested_datetime) }} - {{ formatTime(booking.requested_datetime) }}</p> -->
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
    </div>
    <div v-if="showConfirmModal" class="modal-overlay" @click="showConfirmModal = false">
      <div class="modal-content" @click.stop>
        <h2>Cancel Booking</h2>
        <div class="modal-buttons">
          <button @click="confirmCancel" class="btn-yes">Yes</button>
          <button @click="showConfirmModal = false" class="btn-no">No</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

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


const emit = defineEmits(['cancel'])
const showConfirmModal = ref(false)

// Get service name from booking object
const getServiceName = () => {
  // Backend returns service as an object with name property
  if (props.booking.service && typeof props.booking.service === 'object') {
    return props.booking.service.name || 'Service'
  }
  // Fallback to service_name if it exists
  return props.booking.service_name || 'Service'
}

// Helper function to get full image URL
const getImageUrl = (photoPath) => {
  if (!photoPath) return null
  if (photoPath.startsWith('http')) return photoPath
  return `http://localhost:8000${photoPath}`
}

const getProviderImage = () => {

  const imageUrl = getImageUrl(props.booking.provider_photo)
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

const confirmCancel = () => {
  showConfirmModal.value = false
  emit('cancel', props.booking.id)
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
  margin: 0 0 3px 0;
  font-family: 'Rubik', sans-serif;
}

.booking-duration {
  color: #A0673D;
  font-size: 12px;
  margin: 0;
  font-family: 'Rubik', sans-serif;
  font-weight: 500;
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
  background-color: #fca5a598;
}

.booking-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-end;
}

.action-button {
  padding: 8px 20px;
  border-radius: 6px;
  font-size: 13px;
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
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  font-family: 'Rubik', sans-serif;
}

.modal-content {
  background: white;
  padding: 40px 50px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  font-family: 'Rubik', sans-serif;
  max-width: 450px;
  width: 90%;
  animation: slideIn 0.3s ease-out;
}

/* Added animation for modal appearance */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.modal-content h2 {
  color: #2C2C2C;
  font-size: 22px;
  margin: 0 0 35px 0;
  font-weight: 600;
}

.modal-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.btn-yes {
  padding: 12px 35px;
  background-color: #A0673D;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
  font-family: 'Rubik', sans-serif;
}

.btn-yes:hover {
  background-color: #8B5530;
}

.btn-no {
  padding: 12px 35px;
  background-color: #E8E8E8;
  color: #333;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
  font-family: 'Rubik', sans-serif;
}

.btn-no:hover {
  background-color: #D8D8D8;
}

@media (max-width: 768px) {
  .booking-card {
    flex-direction: column;
    align-items: flex-start;
  }

  .booking-image {
    width: 60px;
    height: 60px;
  }

  .booking-status {
    width: 100%;
  }

  .booking-actions {
    width: 100%;
    align-items: stretch;
  }

  .action-button {
    width: 100%;
  }
}
</style>
