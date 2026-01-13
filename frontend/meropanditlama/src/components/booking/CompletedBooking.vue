<template>
  <div class="bookings-list">
    <div v-if="bookings.length === 0" class="no-bookings">
      <p>No completed bookings</p>
    </div>
    <BookingCard
      v-else
      v-for="booking in bookings"
      :key="booking.id"
      :booking="booking"
      status="Completed"
    />
  </div>
</template>

<script setup>
// import { defineProps } from 'vue'
import BookingCard from './BookingCard.vue'

// eslint-disable-next-line no-unused-vars
const props = defineProps({
  bookings: {
    type: Array,
    required: true
  }
})
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
