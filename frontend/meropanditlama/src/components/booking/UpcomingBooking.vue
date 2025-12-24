<template>
  <div class="bookings-list">
    <BookingCard
      v-for="booking in upcomingBookings"
      :key="booking.id"
      :booking="booking"
      status="Upcoming"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import BookingCard from './BookingCard.vue'

const upcomingBookings = ref([
  {
    id: 1,
    serviceName: 'Wedding Ceremony',
    panditName: 'Pandit John Doe',
    date: '20th December 2025',
    price: 'NPR 5,100',
    status: 'Confirmed',
    statusColor: '#4CAF50',
    image: '/placeholder.svg?height=80&width=80',
  },
  {
    id: 2,
    serviceName: 'Wedding Ceremony',
    panditName: 'Pandit John Doe',
    date: '25th December 2025',
    price: 'NPR 5,100',
    status: 'Pending',
    statusColor: '#FFC107',
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
