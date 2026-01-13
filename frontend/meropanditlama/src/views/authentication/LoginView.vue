<template>
  <div class="auth-container">
    <div class="auth-card">
      <!-- Tab Navigation -->
      <div class="tab-container">
        <div class="tab-slider"></div>
        <button class="tab-button active">LOGIN</button>
        <button class="tab-button" @click="goToSignup">SIGNUP</button>
      </div>

      <!-- Error Message -->
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <!-- Success Message -->
      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>

      <!-- Login Form -->
      <form class="auth-form" @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Email</label>
          <input
            type="email"
            v-model="loginForm.email"
            placeholder="Enter your email"
            class="form-input"
            required
          />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input
            type="password"
            v-model="loginForm.password"
            placeholder="********"
            class="form-input"
            required
          />
        </div>

        <a href="#" class="forgot-password">Forgot Password?</a>

        <button type="submit" class="submit-button" :disabled="loading">
          {{ loading ? 'LOGGING IN...' : 'LOGIN' }}
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

const loginForm = ref({
  email: '',
  password: '',
})

const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const handleLogin = async () => {
  // Reset messages
  errorMessage.value = ''
  successMessage.value = ''
  loading.value = true

  try {
    // Call backend API
    const response = await authAPI.login({
      email: loginForm.value.email,
      password: loginForm.value.password,
    })

    // Store token and user data
    setAuthToken(response.data.token)
    setUserData(response.data.user)

    // Store refresh token if provided
    if (response.data.refresh) {
      localStorage.setItem('refresh', response.data.refresh)
    }

    successMessage.value = 'Login successful! Redirecting...'

    // Redirect based on user role
    setTimeout(() => {
      if (response.data.user.role === 'provider') {
        router.push('/provider/dashboard')
      } else {
        router.push('/') // or '/home' for regular users
      }
    }, 1000)
  } catch (error) {
    console.error('Login error:', error)

    if (error.response) {
      // Backend returned an error
      if (error.response.data.email) {
        errorMessage.value = error.response.data.email[0]
      } else if (error.response.data.password) {
        errorMessage.value = error.response.data.password[0]
      } else if (error.response.data.non_field_errors) {
        errorMessage.value = error.response.data.non_field_errors[0]
      } else {
        errorMessage.value = 'Invalid email or password'
      }
    } else if (error.request) {
      // Network error
      errorMessage.value = 'Cannot connect to server. Please try again.'
    } else {
      errorMessage.value = 'An error occurred. Please try again.'
    }
  } finally {
    loading.value = false
  }
}

const goToSignup = () => {
  router.push('/signup')
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

.forgot-password {
  text-align: right;
  color: #ae664a;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  margin-top: -12px;
}

.forgot-password:hover {
  text-decoration: underline;
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
