<template>
  <nav class="provider-navbar">
    <div class="navbar-content">
      <div class="navbar-brand">
        <h1>MeroPanditLama</h1>
      </div>
      <ul class="navbar-menu">
        <li><router-link to="/provider/home" class="nav-link">Home</router-link></li>
        <li><router-link to="/provider/availability" class="nav-link">Availability</router-link></li>
        <li><router-link to="/provider/requests" class="nav-link">Requests</router-link></li>
        <li><router-link to="/provider/history" class="nav-link">History</router-link></li>
        <li><router-link to="/provider/profile" class="nav-link">Profile</router-link></li>
        <li><button class="logout-btn" @click="logout">Logout</button></li>
      </ul>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const logout = () => {
  localStorage.removeItem('isAuthenticated')
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.provider-navbar {
  background: white;
  border-bottom: 1px solid #E5E7EB;
  padding: 0 40px;
  width: 100%;
  box-sizing: border-box;
  font-family: 'Rubik', sans-serif;
}

.navbar-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px;
}

.navbar-brand h1 {
  color: #A0673D;
  font-size: 24px;
  font-weight: 700;
  margin: 0;
}

.navbar-menu {
  display: flex;
  gap: 30px;
  list-style: none;
  margin: 0;
  padding: 0;
  align-items: center;
}

.nav-link {
  color: #333;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.2s;
}

.nav-link:hover {
  color: #A0673D;
}

.nav-link.router-link-active {
  color: #A0673D;
  border-bottom: 2px solid #A0673D;
  padding-bottom: 22px;
}

.logout-btn {
  background: none;
  border: none;
  color: #333;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  font-family: 'Rubik', sans-serif;
  transition: color 0.2s;
}

.logout-btn:hover {
  color: #A0673D;
}

@media (max-width: 768px) {
  .navbar-content {
    flex-direction: column;
    height: auto;
    padding: 15px 0;
  }

  .navbar-menu {
    flex-direction: column;
    gap: 15px;
    margin-top: 15px;
  }
}
</style>
