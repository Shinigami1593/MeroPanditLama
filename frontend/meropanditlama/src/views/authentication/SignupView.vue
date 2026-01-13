<template>
  <div class="auth-container">
    <div class="auth-card">
      <!-- Tab Navigation -->
      <div class="tab-container">
        <div class="tab-slider slide-right"></div>
        <button class="tab-button" @click="goToLogin">LOGIN</button>
        <button class="tab-button active">SIGNUP</button>
      </div>

      <!-- Error Message -->
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <!-- Success Message -->
      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>

      <!-- Signup Form -->
      <form class="auth-form" @submit.prevent="handleSignup">
        <div class="form-group">
          <label>Full Name</label>
          <input
            type="text"
            v-model="signupForm.fullName"
            placeholder="Enter your full name"
            class="form-input"
            required
          />
        </div>

        <div class="form-group">
          <label>Email</label>
          <input
            type="email"
            v-model="signupForm.email"
            placeholder="Enter your email"
            class="form-input"
            required
          />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input
            type="password"
            v-model="signupForm.password"
            placeholder="********"
            class="form-input"
            required
            minlength="8"
          />
        </div>

        <div class="form-group">
          <label>Confirm Password</label>
          <input
            type="password"
            v-model="signupForm.password2"
            placeholder="********"
            class="form-input"
            required
          />
        </div>

        <button type="submit" class="submit-button" :disabled="loading">
          {{ loading ? 'SIGNING UP...' : 'SIGNUP' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI, setAuthToken, setUserData } from '../../axios'

const router = useRouter()

const signupForm = ref({
  fullName: '',
  email: '',
  password: '',
  password2: '',
})

const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const handleSignup = async () => {
  // Reset messages
  errorMessage.value = ''
  successMessage.value = ''

  // Validate passwords match
  if (signupForm.value.password !== signupForm.value.password2) {
    errorMessage.value = 'Passwords do not match'
    return
  }

  // Validate password length
  if (signupForm.value.password.length < 8) {
    errorMessage.value = 'Password must be at least 8 characters'
    return
  }

  // Split full name into first and last name
  const nameParts = signupForm.value.fullName.trim().split(' ')
  const firstName = nameParts[0] || ''
  const lastName = nameParts.slice(1).join(' ') || nameParts[0] || 'User'

  loading.value = true

  try {
    // Call backend API with split names
    const response = await authAPI.signup({
      email: signupForm.value.email,
      first_name: firstName,
      last_name: lastName,
      password: signupForm.value.password,
      password2: signupForm.value.password2,
      role:'user',
    })

    // Store token and user data
    setAuthToken(response.data.token)
    setUserData(response.data.user)

    // Store refresh token if provided
    if (response.data.refresh) {
      localStorage.setItem('refresh', response.data.refresh)
    }

    successMessage.value = 'Account created successfully! Redirecting...'

    // Redirect to dashboard after 1 second
    setTimeout(() => {
      router.push('/login') // or '/home'
    }, 1000)
  } catch (error) {
    console.error('Signup error:', error)

    if (error.response && error.response.data) {
      // Handle field-specific errors
      const errors = error.response.data
      if (errors.email) {
        errorMessage.value = `Email: ${errors.email[0]}`
      } else if (errors.password) {
        errorMessage.value = `Password: ${errors.password[0]}`
      } else if (errors.password2) {
        errorMessage.value = errors.password2[0]
      } else if (errors.first_name) {
        errorMessage.value = `Name: ${errors.first_name[0]}`
      } else if (errors.last_name) {
        errorMessage.value = `Name: ${errors.last_name[0]}`
      } else {
        errorMessage.value = 'Registration failed. Please check your information.'
      }
    } else if (error.request) {
      errorMessage.value = 'Cannot connect to server. Please try again.'
    } else {
      errorMessage.value = 'An error occurred. Please try again.'
    }
  } finally {
    loading.value = false
  }
}

const goToLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Rubik', sans-serif;
}

.auth-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #e8d5c4;
  padding: 20px;
  overflow-y: auto;
}

.auth-card {
  background: #f9fafb;
  border-radius: 32px;
  padding: 40px;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.tab-container {
  position: relative;
  display: flex;
  gap: 8px;
  margin-bottom: 40px;
  background: #e5e7eb;
  border-radius: 50px;
  padding: 4px;
}

.tab-slider {
  position: absolute;
  top: 4px;
  left: 4px;
  height: calc(100% - 8px);
  width: calc(50% - 8px);
  background: #ae664a;
  border-radius: 50px;
  transition: transform 0.3s ease;
  z-index: 1;
}

.tab-slider.slide-right {
  transform: translateX(calc(100% + 8px));
}

.tab-button {
  flex: 1;
  padding: 12px 24px;
  background: transparent;
  border: none;
  border-radius: 50px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: color 0.3s ease;
  position: relative;
  z-index: 2;
  color: #ae664a;
}

.tab-button.active {
  color: white;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 12px 16px;
  border-radius: 12px;
  margin-bottom: 20px;
  font-size: 14px;
  border-left: 4px solid #c33;
}

.success-message {
  background: #efe;
  color: #3a3;
  padding: 12px 16px;
  border-radius: 12px;
  margin-bottom: 20px;
  font-size: 14px;
  border-left: 4px solid #3a3;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 16px;
  font-weight: 500;
  color: #000;
}

.form-input {
  padding: 14px 20px;
  border: 2px solid #e5e7eb;
  border-radius: 50px;
  font-size: 15px;
  background: white;
  transition: border-color 0.2s ease;
  font-family: 'Rubik', sans-serif;
}

.form-input::placeholder {
  color: #939393;
}

.form-input:focus {
  outline: none;
  border-color: #ae664a;
}

.submit-button {
  padding: 16px;
  background: #ae664a;
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s ease;
  margin-top: 8px;
  letter-spacing: 0.5px;
}

.submit-button:hover:not(:disabled) {
  background: #a45c40;
}

.submit-button:active:not(:disabled) {
  transform: scale(0.98);
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
