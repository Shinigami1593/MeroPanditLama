<template>
  <div class="provider-layout">
    <ProviderNavbar />
    <div class="provider-main">
      <h2 class="page-title">Edit Your Profile</h2>

      <div class="profile-card">
        <!-- Left Section: Profile Photo -->
        <div class="profile-left">
          <div class="profile-image-container">
            <img src="/images/dummy.png" alt="Profile" class="profile-image">
          </div>
          <button class="change-photo-btn">Change Photo</button>
        </div>

        <!-- Right Section: Form -->
        <div class="profile-right">
          <div class="form-row">
            <div class="form-group">
              <label>Full Name</label>
              <input v-model="profile.fullName" type="text" placeholder="Enter your full name" class="form-input">
            </div>
            <div class="form-group">
              <label>Title / Specialization</label>
              <input v-model="profile.title" type="text" placeholder="e.g., Pandit, Lama" class="form-input">
            </div>
          </div>
        </div>
      </div>

      <!-- About Me Section -->
      <div class="form-section">
        <div class="form-group full-width">
          <label>About Me</label>
          <textarea v-model="profile.aboutMe" placeholder="Tell us about yourself..." class="form-textarea"></textarea>
        </div>
      </div>

      <!-- Rituals Section -->
      <div class="form-section">
        <div class="form-group full-width">
          <label>Rituals Offered (comma separated)</label>
          <input v-model="profile.rituals" type="text" placeholder="e.g., Puja, Wedding Ceremony, Griha Pravesh" class="form-input">
        </div>
      </div>

      <!-- Contact Section -->
      <div class="form-section">
        <div class="form-row">
          <div class="form-group">
            <label>Phone Number</label>
            <input v-model="profile.phone" type="tel" placeholder="Enter phone number" class="form-input">
          </div>
          <div class="form-group">
            <label>Location</label>
            <input v-model="profile.location" type="text" placeholder="Enter your location" class="form-input">
          </div>
        </div>
      </div>

      <!-- Save Button -->
      <div class="button-container">
        <button class="save-btn">Save Changes</button>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ProviderNavbar from '../../../components/ProviderNavbar.vue'
import Footer from '../../../components/FooterComponent.vue'

const profile = ref({
  fullName: 'Pandit Ram Prasad',
  title: 'Pandit',
  aboutMe: 'Experienced spiritual guide with over 10 years of experience in conducting rituals and ceremonies.',
  rituals: 'Puja, Wedding Ceremony, Griha Pravesh',
  phone: '+977 9800000000',
  location: 'Kathmandu, Nepal'
})

// const saveProfile = () => {
//   console.log('Profile saved:', profile.value)
//   localStorage.setItem('providerProfile', JSON.stringify(profile.value))
// }
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
  color: #000;
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 32px 0;
}

/* Profile Card */
.profile-card {
  background: white;
  border-radius: 12px;
  padding: 40px;
  display: flex;
  gap: 40px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.profile-left {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 200px;
}

.profile-image-container {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid #A0673D;
  margin-bottom: 16px;
}

.profile-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.change-photo-btn {
  background: #E8C9B8;
  color: #A0673D;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.2s;
}

.change-photo-btn:hover {
  background: #D9B5A0;
}

.profile-right {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* Form Sections */
.form-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  color: #333;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
}

.form-input,
.form-textarea {
  background: #F9F5F0;
  border: 1px solid #E8D4C4;
  border-radius: 6px;
  padding: 12px 14px;
  font-family: 'Rubik', sans-serif;
  font-size: 14px;
  color: #333;
  transition: border-color 0.2s, background 0.2s;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #A0673D;
  background: #fff;
}

.form-textarea {
  min-height: 100px;
  resize: vertical;
}

.button-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 32px;
}

.save-btn {
  background: #A0673D;
  color: white;
  border: none;
  padding: 12px 32px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s;
}

.save-btn:hover {
  background: #8B5630;
}
</style>
