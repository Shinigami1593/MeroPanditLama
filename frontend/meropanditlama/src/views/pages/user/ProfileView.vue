<template>
  <div class="app-wrapper">
    <Navbar />

    <div class="profile-container">
      <h1 class="profile-title">My Profile</h1>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <p>Loading profile...</p>
      </div>

      <!-- Error State -->
      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <!-- Success Message -->
      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>

      <!-- Profile Card -->
      <div v-if="!loading && userData" class="profile-card">
        <div class="profile-left">
          <div class="profile-image">
            <img
              :src="userData.profile_photo || '/images/dummy.png'"
              alt="Profile Picture"
              @error="handleImageError"
            >
          </div>
          <p class="profile-name">{{ userData.first_name }} {{ userData.last_name }}</p>
          <p class="profile-email">{{ userData.email }}</p>

          <!-- Photo Upload -->
          <input
            type="file"
            ref="fileInput"
            @change="handlePhotoChange"
            accept="image/*"
            style="display: none"
          >
          <button class="change-photo-btn" @click="triggerFileInput">
            Change Photo
          </button>
        </div>

        <div class="profile-right">
          <h2>Account Information</h2>

          <!-- Form -->
          <form @submit.prevent="saveChanges">
            <!-- Full Name and Email Row -->
            <div class="form-row">
              <div class="form-group">
                <label>First Name</label>
                <input
                  v-model="formData.first_name"
                  type="text"
                  placeholder="First Name"
                  required
                >
              </div>
              <div class="form-group">
                <label>Last Name</label>
                <input
                  v-model="formData.last_name"
                  type="text"
                  placeholder="Last Name"
                  required
                >
              </div>
            </div>

            <!-- Email (Read-only) -->
            <div class="form-group">
              <label>Email Address</label>
              <input
                v-model="formData.email"
                type="email"
                placeholder="Email Address"
                disabled
                class="disabled-input"
              >
              <small class="form-hint">Email cannot be changed</small>
            </div>

            <!-- Phone Number -->
            <div class="form-group">
              <label>Phone Number (Optional)</label>
              <input
                v-model="formData.phone"
                type="tel"
                placeholder="9841234567"
                pattern="9[0-9]{9}"
                title="Phone must start with 9 and be 10 digits"
              >
              <small class="form-hint">Format: 9841234567</small>
            </div>

            <!-- Save Button -->
            <div class="btn-save">
              <button type="submit" class="save-btn" :disabled="saving">
                {{ saving ? 'Saving...' : 'Save Changes' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '@/components/NavbarComponent.vue'
import Footer from '@/components/FooterComponent.vue'
import { authAPI, isAuthenticated } from '@/axios'

const router = useRouter()

// State
const loading = ref(true)
const saving = ref(false)
const error = ref('')
const successMessage = ref('')

const userData = ref(null)
const formData = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
})

const fileInput = ref(null)
const selectedPhoto = ref(null)

// Check authentication and load profile
onMounted(async () => {
  if (!isAuthenticated()) {
    router.push('/login')
    return
  }

  await loadProfile()
})

// Load user profile from backend
const loadProfile = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await authAPI.getProfile()
    userData.value = response.data

    // Initialize form with current data
    formData.value = {
      first_name: response.data.first_name || '',
      last_name: response.data.last_name || '',
      email: response.data.email || '',
      phone: response.data.phone || '',
    }
  } catch (err) {
    console.error('Error loading profile:', err)
    error.value = 'Failed to load profile. Please try again.'

    // If unauthorized, redirect to login
    if (err.response?.status === 401) {
      router.push('/login')
    }
  } finally {
    loading.value = false
  }
}

// Handle photo selection
const triggerFileInput = () => {
  fileInput.value.click()
}

const handlePhotoChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    // Validate file size (5MB max)
    if (file.size > 10 * 1024 * 1024) {
      error.value = 'Image size must be less than 5MB'
      return
    }

    // Validate file type
    if (!file.type.startsWith('image/')) {
      error.value = 'Please select an image file'
      return
    }

    selectedPhoto.value = file
    uploadPhoto()
  }
}

// Upload photo to backend
const uploadPhoto = async () => {
  if (!selectedPhoto.value) return

  saving.value = true
  error.value = ''
  successMessage.value = ''

  try {
    const formData = new FormData()
    formData.append('profile_photo', selectedPhoto.value)

    // Use PATCH instead of PUT for file uploads
    const response = await authAPI.updateProfile(formData)

    // Update local data
    userData.value = response.data.user || response.data
    successMessage.value = 'Photo updated successfully!'

    // Update localStorage
    const storedUser = JSON.parse(localStorage.getItem('user') || '{}')
    storedUser.profile_photo = userData.value.profile_photo
    localStorage.setItem('user', JSON.stringify(storedUser))

    // Reload profile to get full URL
    await loadProfile()

    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  } catch (err) {
    console.error('Error uploading photo:', err)
    if (err.response?.data?.profile_photo) {
      error.value = err.response.data.profile_photo[0]
    } else if (err.response?.data?.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = 'Failed to upload photo'
    }
  } finally {
    saving.value = false
    selectedPhoto.value = null
    // Clear file input
    if (fileInput.value) {
      fileInput.value.value = ''
    }
  }
}

// Save profile changes
const saveChanges = async () => {
  saving.value = true
  error.value = ''
  successMessage.value = ''

  try {
    const response = await authAPI.updateProfile({
      first_name: formData.value.first_name,
      last_name: formData.value.last_name,
      phone: formData.value.phone,
    })

    // Update local data
    userData.value = response.data.user || response.data
    successMessage.value = 'Profile updated successfully!'

    // Update localStorage
    const storedUser = JSON.parse(localStorage.getItem('user') || '{}')
    storedUser.first_name = userData.value.first_name
    storedUser.last_name = userData.value.last_name
    storedUser.phone = userData.value.phone
    localStorage.setItem('user', JSON.stringify(storedUser))

    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  } catch (err) {
    console.error('Error updating profile:', err)

    if (err.response?.data) {
      const errors = err.response.data
      if (errors.first_name) {
        error.value = `First Name: ${errors.first_name[0]}`
      } else if (errors.last_name) {
        error.value = `Last Name: ${errors.last_name[0]}`
      } else if (errors.phone) {
        error.value = `Phone: ${errors.phone[0]}`
      } else {
        error.value = 'Failed to update profile'
      }
    } else {
      error.value = 'Cannot connect to server. Please try again.'
    }
  } finally {
    saving.value = false
  }
}

// Handle image load error
const handleImageError = (event) => {
  event.target.src = '/images/dummy.png'
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

.profile-title {
  color: #A0673D;
  font-size: 32px;
  margin-bottom: 30px;
  font-weight: 600;
  padding: 10px 15px;
  display: inline-block;
}

.loading-state {
  background: white;
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  font-size: 16px;
  color: #666;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 12px 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  border-left: 4px solid #c33;
}

.success-message {
  background: #efe;
  color: #3a3;
  padding: 12px 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  border-left: 4px solid #3a3;
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
  background: #f5f5f5;
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

.form-group input.disabled-input {
  background-color: #f5f5f5;
  color: #999;
  cursor: not-allowed;
}

.form-hint {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
}

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
  margin-top: 20px;
}

.save-btn:hover:not(:disabled) {
  background-color: #8B5630;
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-save {
  display: flex;
  justify-content: flex-end;
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

  .profile-left {
    min-width: auto;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
