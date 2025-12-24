<template>
  <div class="bookings-list">
    <BookingCard
      v-for="booking in cancelledBookings"
      :key="booking.id"
      :booking="booking"
      status="Cancelled"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import BookingCard from './BookingCard.vue'

const cancelledBookings = ref([
  {
    id: 5,
    serviceName: 'Upanayana',
    panditName: 'Pandit Dev Singh',
    date: '5th October 2025',
    price: 'NPR 6,000',
    status: 'Cancelled',
    statusColor: '#F44336',
    image: '/placeholder.svg?height=80&width=80',
  },
])
</script>

<style scoped>
.bookings-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}
</style>
