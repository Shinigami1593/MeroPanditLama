<template>
  <div class="auth-container">
    <div class="auth-card">
      <!-- Tab Navigation -->
      <div class="tab-container">
        <div class="tab-slider"></div>
        <button class="tab-button active">
          LOGIN
        </button>
        <button class="tab-button" @click="goToSignup">
          SIGNUP
        </button>
      </div>

      <!-- Login Form -->
      <form class="auth-form" @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Username</label>
          <input 
            type="text" 
            v-model="loginForm.username"
            placeholder="Enter Username"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input 
            type="password" 
            v-model="loginForm.password"
            placeholder="********"
            class="form-input"
          />
        </div>

        <a href="#" class="forgot-password">Forgot Password?</a>

        <button type="submit" class="submit-button">LOGIN</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const loginForm = ref({
  username: '',
  password: ''
});

const handleLogin = () => {
  console.log('Login:', loginForm.value);
  // Add your login logic here
  // router.push('/home');
};

const goToSignup = () => {
  router.push('/signup');
};
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
  background-color: #E8D5C4;
  padding: 20px;
  overflow-y: auto;
}

.auth-card {
  background: #F9FAFB;
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
  background: #E5E7EB;
  border-radius: 50px;
  padding: 4px;
}

.tab-slider {
  position: absolute;
  top: 4px;
  left: 4px;
  height: calc(100% - 8px);
  width: calc(50% - 8px);
  background: #AE664A;
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
  color: #AE664A;
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
  border: 2px solid #E5E7EB;
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
  border-color: #AE664A;
}

.forgot-password {
  text-align: right;
  color: #AE664A;
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
  background: #AE664A;
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
  background: #A45C40;
}

.submit-button:active {
  transform: scale(0.98);
}
</style>