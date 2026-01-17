<template>
  <div class="detail-page">
    <Navbar />

    <main class="main-content">
      <!-- Success Message -->
      <div v-if="showSuccessMessage" class="success-overlay" @click="closeSuccessMessage">
        <div class="success-modal" @click.stop>
          <div class="success-icon">✓</div>
          <h3 class="success-title">Booking Successful!</h3>
          <p class="success-text">Your booking request has been sent successfully. The provider will review and confirm your booking soon.</p>
          <button @click="closeSuccessMessage" class="success-button">
            Continue
          </button>
        </div>
      </div>

      <div v-if="loading" class="loading-container">
        <p>Loading provider details...</p>
      </div>

      <div v-else-if="error" class="error-message">
        {{ error }}
      </div>

      <div v-else class="content-container">
        <!-- Left Section: Profile Info -->
        <section class="profile-section">
          <div class="profile-header">
            <div class="profile-image">
              <img
                v-if="provider.profilePhoto"
                :src="getImageUrl(provider.profilePhoto)"
                :alt="provider.name"
                class="profile-photo"
              />
              <div v-else class="image-placeholder"></div>
            </div>
            <div class="profile-info">
              <h1 class="profile-name">{{ provider.name }}</h1>
              <p class="profile-location">{{ provider.shortDescription }}</p>
              <p class="profile-address">{{ provider.location }}</p>
              <div class="profile-meta">
                <span v-if="provider.rating" class="meta-item">⭐ {{ provider.rating }}</span>
                <span class="meta-item">{{ provider.experience }} years experience</span>
              </div>
            </div>
          </div>

          <div class="about-section">
            <h2 class="section-title">About {{ provider.name }}</h2>
            <p class="about-text">
              {{ provider.description }}
            </p>
          </div>

          <div class="services-section">
            <h2 class="section-title">Services Offered</h2>
            <div class="service-tags">
              <span v-for="service in provider.services" :key="service.id" class="service-tag">
                {{ service.name }}
              </span>
            </div>
          </div>
        </section>

        <!-- Right Section: Booking Form -->
        <section class="booking-section">
          <div class="booking-card">
            <h2 class="booking-title">Book This Service</h2>
            <p class="booking-price">Starts at NPR {{ provider.priceFormatted }}</p>

            <!-- Auth Warning -->
            <div v-if="!isAuthenticated" class="auth-warning">
              <p>⚠️ Please <router-link to="/login" class="login-link">log in</router-link> to make a booking</p>
            </div>

            <form @submit.prevent="submitBooking" class="booking-form">
              <div class="form-group">
                <label class="form-label">Select Service</label>
                <select v-model="bookingForm.service" class="form-select" required>
                  <option value="">Select a service</option>
                  <option v-for="service in provider.services" :key="service.id" :value="service.id">
                    {{ service.name }}
                  </option>
                </select>
              </div>

              <!-- Calendar -->
              <div class="form-group">
                <label class="form-label">Select Date</label>
                <div class="calendar-container">
                  <div class="calendar-header">
                    <button type="button" @click="previousMonth" class="calendar-nav">‹</button>
                    <span class="calendar-month">{{ currentMonthYear }}</span>
                    <button type="button" @click="nextMonth" class="calendar-nav">›</button>
                  </div>
                  <div class="calendar-grid">
                    <div v-for="day in weekDays" :key="day" class="calendar-day-label">{{ day }}</div>
                    <div
                      v-for="date in calendarDates"
                      :key="date.dateString"
                      :class="[
                        'calendar-date',
                        { 'other-month': date.isOtherMonth },
                        { 'selected': isDateSelected(date.dateString) },
                        { 'disabled': date.isPast }
                      ]"
                      @click="!date.isPast && selectDate(date.dateString)"
                    >
                      {{ date.day }}
                    </div>
                  </div>
                </div>
              </div>

              <!-- Time Slots -->
              <div class="form-group" v-if="bookingForm.date">
                <label class="form-label">Select Time Slot</label>

                <!-- Loading state -->
                <div v-if="loadingSlots" class="slots-loading">
                  <p>Loading available slots...</p>
                </div>

                <!-- No slots available -->
                <div v-else-if="timeSlots.length === 0" class="no-slots-message">
                  <p>⚠️ No available time slots for this date. Please select another date.</p>
                </div>

                <!-- Available slots -->
                <div v-else class="time-slots">
                  <button
                    type="button"
                    v-for="slot in timeSlots"
                    :key="slot.value"
                    :class="['time-slot', { 'selected': bookingForm.timeSlot === slot.value }]"
                    @click="selectTimeSlot(slot.value)"
                  >
                    <span class="slot-label">{{ slot.label }}</span>
                    <span class="slot-time">{{ slot.time }}</span>
                  </button>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Note (optional)</label>
                <textarea
                  v-model="bookingForm.note"
                  class="form-textarea"
                  rows="4"
                  placeholder="Any special requirements..."
                ></textarea>
              </div>

              <button type="submit" class="submit-button" :disabled="!isFormValid || isSubmitting">
                {{ isSubmitting ? 'Sending...' : 'Send Booking Request' }}
              </button>
            </form>
          </div>
        </section>
      </div>

      <!-- Footer -->
      <Footer/>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Navbar from '../../../components/NavbarComponent.vue';
import Footer from '../../../components/FooterComponent.vue';
import { providersAPI, bookingsAPI, getUserData } from '@/axios';

const route = useRoute();
const router = useRouter();

const providerId = ref(route.params.id);
const loading = ref(true);
const error = ref('');
const provider = ref(null);
const showSuccessMessage = ref(false);
const isSubmitting = ref(false);
const loadingSlots = ref(false);
const availableTimeSlots = ref([]);

// Authentication state
const isAuthenticated = ref(false);
const user = ref(null);

// Calendar state
const currentDate = ref(new Date());
const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

// All possible time slots
const allTimeSlots = [
  { value: 'morning', label: 'Morning', time: '8am - 12pm' },
  { value: 'afternoon', label: 'Afternoon', time: '12pm - 4pm' },
  { value: 'evening', label: 'Evening', time: '4pm - 8pm' }
];

const bookingForm = ref({
  service: '',
  date: '',
  timeSlot: '',
  note: ''
});

// Check authentication helper
const checkAuth = () => {
  const token = localStorage.getItem('token');
  return !!token;
};

// Update authentication state
const updateAuthState = () => {
  isAuthenticated.value = checkAuth();
  user.value = getUserData();
  console.log('Auth state updated:', { isAuthenticated: isAuthenticated.value, user: user.value });
};

// Computed property for available time slots based on selected date
const timeSlots = computed(() => {
  return allTimeSlots.filter(slot =>
    availableTimeSlots.value.includes(slot.value)
  );
});

// Watch for date changes and fetch available slots
watch(() => bookingForm.value.date, async (newDate, oldDate) => {
  console.log('📅 Date changed from', oldDate, 'to', newDate);

  if (newDate) {
    await fetchAvailableSlots(newDate);
  } else {
    console.log('Date cleared, resetting slots');
    availableTimeSlots.value = [];
  }
  // Reset time slot when date changes
  bookingForm.value.timeSlot = '';
});

// Watch for route changes to update auth state
router.afterEach(() => {
  updateAuthState();
});

// Fetch available time slots for selected date
const fetchAvailableSlots = async (date) => {
  loadingSlots.value = true;

  console.log('=== FETCHING AVAILABILITY ===');
  console.log('Provider ID:', providerId.value);
  console.log('Date:', date);

  try {
    const response = await providersAPI.getProviderAvailability(providerId.value, date);

    console.log('Full API Response:', response);
    console.log('Response data:', response.data);
    console.log('Available slots from API:', response.data.available_slots);

    availableTimeSlots.value = response.data.available_slots || [];

    console.log('Available slots set to:', availableTimeSlots.value);
    console.log('Filtered time slots:', timeSlots.value);

    if (availableTimeSlots.value.length === 0) {
      console.warn('⚠️ No available slots for this date');
    } else {
      console.log('✅ Found', availableTimeSlots.value.length, 'available slots');
    }
  } catch (err) {
    console.error('❌ Error fetching availability:', err);
    console.error('Error response:', err.response);
    console.error('Error message:', err.message);
    availableTimeSlots.value = [];
  } finally {
    loadingSlots.value = false;
    console.log('=== FETCH COMPLETE ===');
  }
};

// Load provider details
onMounted(async () => {
  updateAuthState(); // Check authentication on mount
  await loadProviderDetails();
});

const loadProviderDetails = async () => {
  loading.value = true;
  error.value = '';

  try {
    const response = await providersAPI.getProviderById(providerId.value);
    const p = response.data;

    provider.value = {
      id: p.id,
      religionType: p.religion_type,
      type: p.religion_type === 'hindu' ? 'Pandit' : 'Lama',
      name: `${p.religion_type === 'hindu' ? 'Pandit' : 'Lama'} ${p.user.first_name} ${p.user.last_name}`,
      shortDescription: p.short_description,
      description: p.short_description,
      location: p.location,
      experience: p.experience_years,
      rating: p.average_rating,
      priceFormatted: parseFloat(p.price_per_service).toLocaleString('en-NP'),
      price: p.price_per_service,
      profilePhoto: p.user.profile_photo,
      services: p.services || []
    };

  } catch (err) {
    console.error('Error loading provider:', err);
    error.value = 'Failed to load provider details. Please try again.';
  } finally {
    loading.value = false;
  }
};

// Calendar computed properties
const currentMonthYear = computed(() => {
  const months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December'];
  return `${months[currentDate.value.getMonth()]} ${currentDate.value.getFullYear()}`;
});

const calendarDates = computed(() => {
  const year = currentDate.value.getFullYear();
  const month = currentDate.value.getMonth();

  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const prevLastDay = new Date(year, month, 0);

  const firstDayOfWeek = firstDay.getDay();
  const lastDate = lastDay.getDate();
  const prevLastDate = prevLastDay.getDate();

  const dates = [];
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  // Previous month dates
  for (let i = firstDayOfWeek - 1; i >= 0; i--) {
    const day = prevLastDate - i;
    const date = new Date(year, month - 1, day);
    dates.push({
      day,
      dateString: formatDate(date),
      isOtherMonth: true,
      isPast: date < today
    });
  }

  // Current month dates
  for (let day = 1; day <= lastDate; day++) {
    const date = new Date(year, month, day);
    dates.push({
      day,
      dateString: formatDate(date),
      isOtherMonth: false,
      isPast: date < today
    });
  }

  // Next month dates
  const remainingDays = 42 - dates.length;
  for (let day = 1; day <= remainingDays; day++) {
    const date = new Date(year, month + 1, day);
    dates.push({
      day,
      dateString: formatDate(date),
      isOtherMonth: true,
      isPast: false
    });
  }

  return dates;
});

// Calendar methods
const formatDate = (date) => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

const isDateSelected = (dateString) => {
  return bookingForm.value.date === dateString;
};

const selectDate = (dateString) => {
  bookingForm.value.date = dateString;
};

const selectTimeSlot = (slot) => {
  bookingForm.value.timeSlot = slot;
};

const previousMonth = () => {
  currentDate.value = new Date(
    currentDate.value.getFullYear(),
    currentDate.value.getMonth() - 1,
    1
  );
};

const nextMonth = () => {
  currentDate.value = new Date(
    currentDate.value.getFullYear(),
    currentDate.value.getMonth() + 1,
    1
  );
};

// Form validation
const isFormValid = computed(() => {
  return bookingForm.value.service &&
         bookingForm.value.date &&
         bookingForm.value.timeSlot;
});

// Helper function
const getImageUrl = (photoPath) => {
  if (!photoPath) return null;
  if (photoPath.startsWith('http')) return photoPath;
  return `http://localhost:8000${photoPath}`;
};

// Submit booking
const submitBooking = async () => {
  if (!isFormValid.value) return;

  // Check authentication first
  if (!isAuthenticated.value) {
    alert('Please log in to make a booking');
    router.push('/login');
    return;
  }

  isSubmitting.value = true;

  try {
    const bookingData = {
      provider: providerId.value,
      service: bookingForm.value.service,
      requested_date: bookingForm.value.date,
      time_slot: bookingForm.value.timeSlot,
      notes: bookingForm.value.note
    };

    console.log('Sending booking data:', bookingData);

    const response = await bookingsAPI.createBooking(bookingData);
    console.log('Booking response:', response);

    // Show success message
    showSuccessMessage.value = true;

    // Reset form
    bookingForm.value = {
      service: '',
      date: '',
      timeSlot: '',
      note: ''
    };

  } catch (err) {
    console.error('Full error:', err);
    console.error('Error response:', err.response?.data);

    // Handle specific error cases
    if (err.response?.status === 401) {
      alert('Your session has expired. Please log in again.');
      router.push('/login');
      return;
    }

    // Show error message
    let errorMessage = 'Failed to send booking request. ';
    if (err.response?.data) {
      if (typeof err.response.data === 'string') {
        errorMessage += err.response.data;
      } else if (err.response.data.detail) {
        errorMessage += err.response.data.detail;
      } else if (err.response.data.error) {
        errorMessage += err.response.data.error;
      } else {
        errorMessage += 'Please try again.';
      }
    } else {
      errorMessage += err.message;
    }

    alert(errorMessage);
  } finally {
    isSubmitting.value = false;
  }
};

const closeSuccessMessage = () => {
  showSuccessMessage.value = false;
  router.push('/');
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700&display=swap');

* {
  font-family: 'Rubik', sans-serif;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.detail-page {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #FFFBF5;
}

.main-content {
  flex: 1;
  width: 100%;
}

.loading-container {
  text-align: center;
  padding: 60px 20px;
  font-size: 18px;
  color: #666;
}

.error-message {
  max-width: 600px;
  margin: 60px auto;
  padding: 16px 24px;
  background: #fee;
  color: #c33;
  border-radius: 8px;
  text-align: center;
  font-size: 14px;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 40px;
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 40px;
}

/* Profile Section */
.profile-section {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.profile-header {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.profile-image {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  background: #E5E7EB;
  flex-shrink: 0;
}

.profile-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #f0f0f0 25%, transparent 25%),
              linear-gradient(225deg, #f0f0f0 25%, transparent 25%),
              linear-gradient(45deg, #f0f0f0 25%, transparent 25%),
              linear-gradient(315deg, #f0f0f0 25%, #e0e0e0 25%);
  background-size: 20px 20px;
  background-position: 0 0, 10px 0, 10px -10px, 0px 10px;
}

.profile-info {
  flex: 1;
}

.profile-name {
  font-size: 28px;
  font-weight: 600;
  color: #AE664A;
  margin-bottom: 8px;
}

.profile-location {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
}

.profile-address {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.profile-meta {
  display: flex;
  gap: 12px;
  font-size: 13px;
  color: #666;
}

.meta-item {
  display: flex;
  align-items: center;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #AE664A;
  margin-bottom: 16px;
}

.about-text {
  font-size: 15px;
  color: #444;
  line-height: 1.7;
}

.service-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.service-tag {
  display: inline-block;
  background: #AE664A;
  color: white;
  padding: 8px 18px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
}

/* Booking Section */
.booking-section {
  position: sticky;
  top: 20px;
  height: fit-content;
}

.booking-card {
  background: white;
  border: 1px solid #E5D5C3;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.booking-title {
  font-size: 20px;
  font-weight: 600;
  color: #000;
  margin-bottom: 8px;
}

.booking-price {
  font-size: 15px;
  color: #666;
  margin-bottom: 24px;
}

.auth-warning {
  background: #FEF3C7;
  border: 1px solid #F59E0B;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 20px;
  font-size: 14px;
  color: #92400E;
}

.login-link {
  color: #AE664A;
  font-weight: 600;
  text-decoration: underline;
}

.booking-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.form-select,
.form-textarea {
  padding: 12px 16px;
  border: 1px solid #E5D5C3;
  border-radius: 8px;
  font-size: 14px;
  font-family: 'Rubik', sans-serif;
  outline: none;
  transition: border-color 0.2s ease;
}

.form-select:focus,
.form-textarea:focus {
  border-color: #AE664A;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

/* Calendar Styles */
.calendar-container {
  border: 1px solid #E5D5C3;
  border-radius: 8px;
  padding: 16px;
  background: white;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.calendar-month {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.calendar-nav {
  background: none;
  border: none;
  font-size: 20px;
  color: #AE664A;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background 0.2s ease;
}

.calendar-nav:hover {
  background: #f5e6d3;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}

.calendar-day-label {
  text-align: center;
  font-size: 12px;
  font-weight: 600;
  color: #666;
  padding: 8px 0;
}

.calendar-date {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #333;
}

.calendar-date:hover:not(.disabled):not(.other-month) {
  background: #f5e6d3;
}

.calendar-date.other-month {
  color: #ccc;
  cursor: default;
}

.calendar-date.selected {
  background: #AE664A;
  color: white;
  font-weight: 600;
}

.calendar-date.disabled {
  color: #ddd;
  cursor: not-allowed;
}

/* Time Slots */
.slots-loading {
  padding: 20px;
  text-align: center;
  color: #666;
  font-size: 14px;
  background: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #E5D5C3;
}

.no-slots-message {
  padding: 16px;
  background: #FEF3C7;
  border: 1px solid #F59E0B;
  border-radius: 8px;
  color: #92400E;
  font-size: 14px;
}

.no-slots-message p {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.time-slots {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.time-slot {
  padding: 12px 16px;
  border: 1px solid #E5D5C3;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
  font-family: 'Rubik', sans-serif;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.time-slot:hover {
  border-color: #AE664A;
  background: #f5e6d3;
}

.time-slot.selected {
  background: #AE664A;
  border-color: #AE664A;
  color: white;
}

.slot-label {
  font-size: 14px;
  font-weight: 500;
}

.slot-time {
  font-size: 12px;
  opacity: 0.8;
}

.submit-button {
  width: 100%;
  padding: 14px;
  background: #AE664A;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  font-size: 15px;
  cursor: pointer;
  transition: background 0.2s ease;
  font-family: 'Rubik', sans-serif;
  margin-top: 8px;
}

.submit-button:hover:not(:disabled) {
  background: #9A5838;
}

.submit-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* Success Modal */
.success-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.success-modal {
  background: white;
  border-radius: 16px;
  padding: 40px;
  max-width: 450px;
  width: 90%;
  text-align: center;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.success-icon {
  width: 80px;
  height: 80px;
  background: #47C920;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  color: white;
  margin: 0 auto 24px;
  animation: scaleIn 0.5s ease;
}

@keyframes scaleIn {
  from {
    transform: scale(0);
  }
  to {
    transform: scale(1);
  }
}

.success-title {
  font-size: 24px;
  font-weight: 600;
  color: #AE664A;
  margin-bottom: 16px;
  font-family: 'Rubik', sans-serif;
}

.success-text {
  font-size: 15px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 32px;
  font-family: 'Rubik', sans-serif;
}

.success-button {
  width: 100%;
  padding: 14px;
  background: #AE664A;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  font-size: 15px;
  cursor: pointer;
  transition: background 0.2s ease;
  font-family: 'Rubik', sans-serif;
}

.success-button:hover {
  background: #9A5838;
}

/* Responsive Design */
@media (max-width: 768px) {
  .content-container {
    grid-template-columns: 1fr;
    padding: 40px 20px;
  }

  .booking-section {
    position: static;
  }

  .profile-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
}
</style>
