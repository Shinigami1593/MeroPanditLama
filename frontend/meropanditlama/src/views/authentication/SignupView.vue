<template>
  <div class="auth-container">
    <div class="auth-card">
      <!-- Tab Navigation -->
      <div class="tab-container">
        <div class="tab-slider slide-right"></div>
        <button class="tab-button" @click="goToLogin">LOGIN</button>
        <button class="tab-button active">SIGNUP</button>
      </div>

      <!-- Signup Form -->
      <form class="auth-form" @submit.prevent="handleSignup">
        <div class="form-group">
          <label>Username</label>
          <input
            type="text"
            v-model="signupForm.username"
            placeholder="Enter Username"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input
            type="password"
            v-model="signupForm.password"
            placeholder="********"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label>Confirm Password</label>
          <input
            type="password"
            v-model="signupForm.confirmPassword"
            placeholder="********"
            class="form-input"
          />
        </div>

        <button type="submit" class="submit-button">SIGNUP</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const signupForm = ref({
  username: '',
  password: '',
  confirmPassword: '',
})

const handleSignup = () => {
  console.log('Signup:', signupForm.value)
  // Add your signup logic here
  // router.push('/login');
}

const goToLogin = () => {
  router.push('/login')
}
</script>

<style>
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

.submit-button:hover {
  background: #a45c40;
}

.submit-button:active {
  transform: scale(0.98);
}
</style>
