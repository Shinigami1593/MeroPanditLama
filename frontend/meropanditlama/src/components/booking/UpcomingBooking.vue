<template>
  <div class="bookings-list">
    <div v-if="bookings.length === 0" class="no-bookings">
      <p>No upcoming bookings</p>
    </div>
    <BookingCard
      v-else
      v-for="booking in bookings"
      :key="booking.id"
      :booking="booking"
      status="Upcoming"
      @cancel="cancelBooking"
    />
  </div>
</template>

<script setup>
// Remove the imports
import BookingCard from './BookingCard.vue'
import { bookingsAPI } from '@/axios'

// eslint-disable-next-line no-unused-vars
const props = defineProps({
  bookings: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['refresh'])

const cancelBooking = async (bookingId) => {
  const reason = prompt('Please provide a reason for cancellation (optional):')

  if (reason === null) return

  try {
    await bookingsAPI.cancelBooking(bookingId, {
      cancellation_reason: reason
    })
    alert('Booking cancelled successfully')
    emit('refresh')
  } catch (err) {
    console.error('Error cancelling booking:', err)
    alert('Failed to cancel booking. Please try again.')
  }
}
</script>

<style scoped>
.bookings-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.no-bookings {
  text-align: center;
  padding: 60px 20px;
  color: #666;
  font-size: 16px;
}
</style>
