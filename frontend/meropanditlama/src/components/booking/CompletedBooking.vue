<template>
  <div class="bookings-list">
    <BookingCard
      v-for="booking in completedBookings"
      :key="booking.id"
      :booking="booking"
      status="Completed"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import BookingCard from './BookingCard.vue'

const completedBookings = ref([
  {
    id: 3,
    serviceName: 'Puja',
    panditName: 'Pandit Jane Smith',
    date: '15th November 2025',
    price: 'NPR 3,500',
    status: 'Completed',
    statusColor: '#4CAF50',
    image: '/placeholder.svg?height=80&width=80',
  },
  {
    id: 4,
    serviceName: 'Havan',
    panditName: 'Pandit Ram Kumar',
    date: '10th November 2025',
    price: 'NPR 4,200',
    status: 'Completed',
    statusColor: '#4CAF50',
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
