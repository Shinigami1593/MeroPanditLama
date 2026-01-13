<template>
  <div class="provider-layout">
    <ProviderNavbar />
    <div class="provider-main">
      <h2 class="page-title">Manage Your Availability</h2>
      <p class="page-subtitle">Click on dates to mark them as available, unavailable, or booked.</p>

      <div class="availability-container">
        <!-- Calendar Section -->
        <div class="calendar-section">
          <div class="calendar-header">
            <button class="nav-btn" @click="previousMonth">&lt;</button>
            <h3 class="month-year">{{ monthYear }}</h3>
            <button class="nav-btn" @click="nextMonth">&gt;</button>
          </div>

          <div class="calendar">
            <div class="weekdays">
              <div class="weekday">Sun</div>
              <div class="weekday">Mon</div>
              <div class="weekday">Tue</div>
              <div class="weekday">Wed</div>
              <div class="weekday">Thu</div>
              <div class="weekday">Fri</div>
              <div class="weekday">Sat</div>
            </div>

            <div class="days">
              <div
                v-for="day in calendarDays"
                :key="day.date"
                @click="selectDate(day.date)"
                :class="['day', { empty: !day.date }, getDateStatusClass(day.date)]"
              >
                {{ day.date ? day.date.split('-')[2].replace(/^0/, '') : ''}}
              </div>
            </div>
          </div>
        </div>

        <!-- Legend and Time Slots Section -->
        <div class="sidebar">
          <!-- Legend -->
          <div class="legend-card">
            <h4>Legend</h4>
            <div class="legend-item">
              <div class="legend-color available"></div>
              <span>Available</span>
            </div>
            <div class="legend-item">
              <div class="legend-color booked"></div>
              <span>Booked</span>
            </div>
            <div class="legend-item">
              <div class="legend-color unavailable"></div>
              <span>Unavailable</span>
            </div>
          </div>

          <!-- Time Slots -->
          <div class="time-slots-card">
            <h4>Set Time Slots for {{ selectedDateFormatted }}</h4>
            <div class="time-slot">
              <input
                type="checkbox"
                v-model="timeSlots.morning"
                id="morning"
              >
              <label for="morning">Morning (8am - 12pm)</label>
            </div>
            <div class="time-slot">
              <input
                type="checkbox"
                v-model="timeSlots.afternoon"
                id="afternoon"
              >
              <label for="afternoon">Afternoon (12pm - 4pm)</label>
            </div>
            <div class="time-slot">
              <input
                type="checkbox"
                v-model="timeSlots.evening"
                id="evening"
              >
              <label for="evening">Evening (4pm - 8pm)</label>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ProviderNavbar from '../../../components/ProviderNavbar.vue'
import Footer from '../../../components/FooterComponent.vue'


const currentDate = ref(new Date())
const selectedDate = ref(null)
const dateStatuses = ref({})
const timeSlots = ref({
  morning: false,
  afternoon: false,
  evening: false
})

const monthYear = computed(() => {
  const month = currentDate.value.toLocaleString('default', { month: 'long' })
  const year = currentDate.value.getFullYear()
  return `${month} ${year}`
})

const selectedDateFormatted = computed(() => {
  if (!selectedDate.value) return 'Select a date'
  const date = new Date(selectedDate.value)
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
})

const calendarDays = computed(() => {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth()

  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)
  const daysInMonth = lastDay.getDate()
  const startingDayOfWeek = firstDay.getDay()

  const days = []

  // Empty slots before first day
  for (let i = 0; i < startingDayOfWeek; i++) {
    days.push({ date: null })
  }

  // Days of month
  for (let i = 1; i <= daysInMonth; i++) {
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`
    days.push({ date: dateStr })
  }

  return days
})

const previousMonth = () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() - 1)
}

const nextMonth = () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() + 1)
}

const selectDate = (date) => {
  if (date) {
    selectedDate.value = date
  }
}

const getDateStatusClass = (date) => {
  if (!date) return ''
  return dateStatuses.value[date] || 'default'
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
  font-weight: 600;
  margin: 0 0 8px 0;
}

.page-subtitle {
  color: #666;
  font-size: 14px;
  margin: 0 0 32px 0;
}

.availability-container {
  display: flex;
  gap: 24px;
}

.calendar-section {
  flex: 1;
  background: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.nav-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #333;
  padding: 8px 12px;
  font-weight: 600;
}

.nav-btn:hover {
  color: #A0673D;
}

.month-year {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.calendar {
  width: 100%;
}

.weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
  margin-bottom: 12px;
}

.weekday {
  text-align: center;
  font-weight: 600;
  color: #666;
  font-size: 12px;
  padding: 8px 0;
}

.days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
}

.day {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  border: 2px solid transparent;
  background: white;
  color: #333;
  transition: all 0.2s;
}

.day:not(.empty):hover {
  border-color: #A0673D;
}

.day.empty {
  cursor: default;
  background: transparent;
}

.day.available {
  background: #FFFBEA;
  border-color: #FFD166;
}

.day.booked {
  background: #FFE4E6;
  border-color: #FF6B7A;
}

.day.unavailable {
  background: #E5E7EB;
  color: #999;
}

.sidebar {
  width: 320px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.legend-card,
.time-slots-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.legend-card h4,
.time-slots-card h4 {
  color: #333;
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 16px 0;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 3px;
}

.legend-color.available {
  background: #FFFBEA;
  border: 2px solid #FFD166;
}

.legend-color.booked {
  background: #FFE4E6;
  border: 2px solid #FF6B7A;
}

.legend-color.unavailable {
  background: #E5E7EB;
}

.legend-item span {
  font-size: 14px;
  color: #666;
}

.time-slot {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.time-slot input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
  accent-color: #A0673D;
}

.time-slot label {
  font-size: 14px;
  color: #333;
  cursor: pointer;
}
</style>
