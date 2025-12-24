<template>
  <div class="app-wrapper">
    <Navbar :isAuthenticated="true" />

    <div class="profile-container">
      <h1 class="profile-title">My Profile</h1>

      <div class="profile-card">
        <div class="profile-left">
          <div class="profile-image">
            <img :src="userData.profileImage || '/images/dummy.png'" alt="Profile Picture">
          </div>
          <p class="profile-name">{{ userData.fullName || 'John Doe' }}</p>
          <p class="profile-email">{{ userData.email || 'john@example.com' }}</p>
          <button class="change-photo-btn">Change Photo</button>
        </div>

        <div class="profile-right">
          <h2>Account Information</h2>

          <!-- Updated form layout: Full Name on left, Email on right -->
          <div class="form-row">
            <div class="form-group">
              <label>Full Name</label>
              <input
                v-model="formData.fullName"
                type="text"
                placeholder="Full Name"
              >
            </div>
            <div class="form-group">
              <label>Email Address</label>
              <input
                v-model="formData.email"
                type="email"
                placeholder="Email Address"
              >
            </div>
          </div>

          <div class="form-group">
            <label>Phone Number</label>
            <input
              v-model="formData.phoneNumber"
              type="tel"
              placeholder="Phone Number"
            >
          </div>
          <div class="btn-save">
            <button class="save-btn" @click="saveChanges">Save Changes</button>
          </div>
        </div>
      </div>
    </div>

    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Navbar from '@/components/NavbarComponent.vue'
import Footer from '@/components/FooterComponent.vue'

const isAuthenticated = ref(false)
const userData = ref({
  fullName: 'John Doe',
  email: 'john@example.com',
  phoneNumber: '+977 9800000806'
})

const formData = ref({
  fullName: '',
  email: '',
  phoneNumber: '',
  profileImage: ''
})

onMounted(() => {
  isAuthenticated.value = localStorage.getItem('isAuthenticated') === 'true'

  // Load user data from localStorage or use defaults
  const savedUser = localStorage.getItem('userData')
  if (savedUser) {
    userData.value = JSON.parse(savedUser)
  }

  // Initialize form with current data
  formData.value = { ...userData.value }
})

const saveChanges = () => {
  // Save changes to localStorage
  userData.value = { ...formData.value }
  localStorage.setItem('userData', JSON.stringify(userData.value))
  alert('Changes saved successfully!')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;600&display=swap');

.app-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100vw;
  font-family: 'Rubik', sans-serif;
}

.profile-container {
  width: 100%;
  flex: 1;
  background-color: #F5E6D3;
  padding: 40px 360px;
  box-sizing: border-box;
}

/* Added dotted border around the title */
.profile-title {
  color: #A0673D;
  font-size: 32px;
  margin-bottom: 30px;
  font-weight: 600;
  /* border: 2px dotted #A0673D; */
  padding: 10px 15px;
  display: inline-block;
}

.profile-card {
  background: white;
  border-radius: 12px;
  padding: 40px;
  display: flex;
  gap: 60px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.profile-left {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  min-width: 320px;
}

.profile-image {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 3px solid #D4A574;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.profile-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-name {
  font-size: 18px;
  color: #333;
  font-weight: 600;
  margin: 0;
}

.profile-email {
  font-size: 13px;
  color: #999;
  margin: 0;
}

.change-photo-btn {
  background-color: #e4a58c6c;
  color: #A45C40;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  font-family: 'Rubik', sans-serif;
  transition: background-color 0.3s;
}

.change-photo-btn:hover {
  background-color: #C29560;
}

.profile-right {
  flex: 1;
}

.profile-right h2 {
  color: #333;
  font-size: 18px;
  margin: 0 0 25px 0;
  font-weight: 600;
}

.form-group {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-size: 13px;
  color: #333;
  margin-bottom: 8px;
  font-weight: 500;
}

.form-group input {
  padding: 10px 12px;
  border: none;
  background-color: #E8E8E8;
  border-radius: 4px;
  font-family: 'Rubik', sans-serif;
  font-size: 14px;
  color: #333;
}

.form-group input::placeholder {
  color: #999;
}

/* Full Name and Email Address are now side by side */
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.form-row .form-group {
  margin-bottom: 0;
}

.save-btn {
  background-color: #A0673D;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  font-family: 'Rubik', sans-serif;
  transition: background-color 0.3s;
  align-self: flex-end;
  margin-top: 20px;
}

.btn-save{
  display: flex;
  justify-content: flex-end;
}

.save-btn:hover {
  background-color: #8B5630;
}

@media (max-width: 768px) {
  .profile-container {
    padding: 20px;
  }

  .profile-title {
    font-size: 24px;
  }

  .profile-card {
    flex-direction: column;
    gap: 30px;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
