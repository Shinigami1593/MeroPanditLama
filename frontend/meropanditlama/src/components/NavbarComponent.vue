<!-- eslint-disable no-unused-vars -->
<template>
  <nav class="navbar">
    <div class="nav-container">
      <!-- Logo -->
      <router-link to="/" class="logo">MeroPanditLama</router-link>

      <!-- Navigation Links -->
      <div class="nav-links">
        <router-link
          v-if="isAuthenticated"
          to="/"
          class="nav-link"
          :class="{ active: currentRoute === 'home' }"
        >
          Home
        </router-link>
        <router-link to="/browse" class="nav-link" :class="{ active: currentRoute === 'browse' }">
          Browse
        </router-link>
        <router-link
          v-if="isAuthenticated"
          to="/my-bookings"
          class="nav-link"
          :class="{ active: currentRoute === 'my-bookings' }"
        >
          MyBookings
        </router-link>
        <router-link
          v-if="isAuthenticated"
          to="/profile"
          class="nav-link"
          :class="{ active: currentRoute === 'profile' }"
        >
          Profile
        </router-link>
      </div>

      <!-- Right Side Actions -->
      <div class="nav-actions">
        <!-- Login Button (when not authenticated) -->
        <router-link v-if="!isAuthenticated" to="/login" class="login-button"> Login </router-link>

        <!-- Logout Icon (when authenticated) -->
        <button v-if="isAuthenticated" @click="handleLogout" class="logout-button" title="Logout">
          <i class="bi bi-box-arrow-right"></i>
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
// eslint-disable-next-line no-unused-vars
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

// eslint-disable-next-line no-unused-vars
const router = useRouter()
const route = useRoute()

// eslint-disable-next-line no-unused-vars
const props = defineProps({
  isAuthenticated: {
    type: Boolean,
    default: false,
  },
})

const currentRoute = computed(() => route.name)

const handleLogout = () => {
  console.log('Logging out...')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700&display=swap');
@import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css');

* {
  font-family: 'Rubik', sans-serif;
  box-sizing: border-box;
}

.navbar {
  background-color: white;
  border-bottom: 2px solid #f0f0f0;
  padding: 16px 40px;
  position: sticky;
  top: 0;
  width: 100%;
  margin: 0;
}

.nav-container {
  width: 100%;
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.logo {
  font-size: 24px;
  font-weight: 600;
  color: #ae664a;
  text-decoration: none;
  margin-right: 60px;
  padding-left: 321px;
}

.nav-links {
  display: flex;
  gap: 40px;
  flex: 1;
  justify-content: end;
}

.nav-link {
  font-size: 16px;
  font-weight: 500;
  color: #000;
  text-decoration: none;
  position: relative;
  padding-bottom: 4px;
  transition: color 0.2s ease;
}

.nav-link:hover {
  color: #ae664a;
}

.nav-link.active {
  color: #ae664a;
}

.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #ae664a;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 16px;
  padding-left: 20px;
  margin-right: 321px;
}

.login-button {
  padding: 10px 32px;
  background-color: #ae664a;
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 16px;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.login-button:hover {
  background-color: #a45c40;
}

.logout-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 24px;
  color: #ae664a;
  transition: color 0.2s ease;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logout-button:hover {
  color: #a45c40;
}

@media (max-width: 768px) {
  .navbar {
    padding: 16px 20px;
  }

  .nav-links {
    gap: 20px;
    font-size: 14px;
  }

  .logo {
    font-size: 20px;
    margin-right: 20px;
  }
}
</style>
