<template>
  <div class="detail-page">
    <Navbar :is-authenticated="true"/>

    <main class="main-content">
      <div class="content-container">
        <!-- Left Section: Profile Info -->
        <section class="profile-section">
          <div class="profile-header">
            <div class="profile-image">
              <div class="image-placeholder"></div>
            </div>
            <div class="profile-info">
              <h1 class="profile-name">Pandit John Doe</h1>
              <p class="profile-location">Lorem ipsum dolor sit amet consectetur</p>
              <p class="profile-address">Kathmandu, Nepal</p>
            </div>
          </div>

          <div class="about-section">
            <h2 class="section-title">About Pandit John Doe</h2>
            <p class="about-text">
              Lorem ipsum dolor sit amet consectetur adipiscing elit. Dui eveinet esse enim
              libero accusamus quia laudantium reiciendis fuga tempora repellendus adipisci
              iste, labore seperuntur ut, cupiditate mollitia commodi elenus.
            </p>
          </div>

          <div class="services-section">
            <h2 class="section-title">Services Offered</h2>
            <div class="service-tags">
              <span class="service-tag">Puja</span>
              <span class="service-tag">Wedding Ceremony</span>
              <span class="service-tag">Griha Pravesh</span>
            </div>
          </div>
        </section>

        <!-- Right Section: Booking Form -->
        <section class="booking-section">
          <div class="booking-card">
            <h2 class="booking-title">Book This Service</h2>
            <p class="booking-price">Starts at NPR 5,100</p>

            <form @submit.prevent="submitBooking" class="booking-form">
              <div class="form-group">
                <label class="form-label">Select Service</label>
                <select v-model="bookingForm.service" class="form-select" required>
                  <option value="">Select a service</option>
                  <option value="puja">Puja</option>
                  <option value="wedding">Wedding Ceremony</option>
                  <option value="griha-pravesh">Griha Pravesh</option>
                </select>
              </div>

              <div class="form-group">
                <label class="form-label">Preferred Date</label>
                <input
                  type="date"
                  v-model="bookingForm.date"
                  class="form-input"
                  required
                />
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

              <button type="submit" class="submit-button">
                Send Booking Request
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
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Navbar from '../../../components/NavbarComponent.vue';
import Footer from '../../../components/FooterComponent.vue';

const route = useRoute();
const router = useRouter();

const panditId = ref(route.params.id);

const bookingForm = ref({
  service: '',
  date: '',
  note: ''
});

const submitBooking = () => {
  console.log('Booking submitted:', {
    panditId: panditId.value,
    ...bookingForm.value
  });
  alert('Booking request sent successfully!');
  router.push({ name: 'home' });
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
.form-input,
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
.form-input:focus,
.form-textarea:focus {
  border-color: #AE664A;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
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

.submit-button:hover {
  background: #9A5838;
}

/* Footer */
.footer {
  background: white;
  border-top: 1px solid #E5E7EB;
  padding: 40px;
  margin-top: 60px;
  width: 100%;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  gap: 60px;
}

.footer-section {
  flex: 1;
}

.footer-title {
  font-size: 16px;
  font-weight: 600;
  color: #000;
  margin-bottom: 16px;
}

.footer-text {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
  line-height: 1.6;
}

.contact-support-link {
  display: inline-block;
  margin-top: 8px;
  color: #AE664A;
  text-decoration: none;
  font-weight: 500;
  font-size: 14px;
}

.contact-support-link:hover {
  text-decoration: underline;
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

  .footer-content {
    flex-direction: column;
    gap: 30px;
  }
}
</style>
