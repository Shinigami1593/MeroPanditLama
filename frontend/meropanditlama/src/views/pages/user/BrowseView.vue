<template>
  <div class="browse-page">
    <Navbar :isAuthenticated="true" />

    <main class="main-content">
      <!-- Hero Section with Search -->
      <section class="hero-section">
        <h1 class="page-title">Find a Pandit or Lama</h1>
        <p class="page-subtitle">Explore our list of experienced spiritual guides.</p>

        <!-- Search Bar with Filter -->
        <div class="search-container">
          <div class="search-box">
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Search by name or ritual..."
              class="search-input"
            />
            <button class="search-button">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <circle cx="9" cy="9" r="7" stroke="#AE664A" stroke-width="2" />
                <line x1="14" y1="14" x2="18" y2="18" stroke="#AE664A" stroke-width="2" />
              </svg>
            </button>
          </div>

          <select v-model="selectedService" class="service-dropdown">
            <option value="all">All</option>
            <option value="hindu">Pandit</option>
            <option value="buddhist">Lama</option>
          </select>
        </div>
      </section>

      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <p>Loading providers...</p>
      </div>

      <!-- Error State -->
      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <!-- Pandit Cards Grid -->
      <section class="cards-section" v-if="!loading">
        <div class="cards-grid">
          <div v-for="provider in filteredProviders" :key="provider.id" class="pandit-card">
            <div class="card-image">
              <img
                v-if="provider.profilePhoto"
                :src="getImageUrl(provider.profilePhoto)"
                :alt="provider.name"
                class="profile-photo"
              />
              <div v-else class="image-placeholder"></div>
            </div>
            <div class="card-content">
              <span class="card-tag">{{ provider.type }}</span>
              <h3 class="card-name">{{ provider.name }}</h3>
              <p class="card-price">{{ provider.price }}</p>
              <button class="details-button" @click="viewDetails(provider.id)">View Details</button>
            </div>
          </div>
        </div>
      </section>

      <!-- Footer -->
      <Footer/>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '../../../components/NavbarComponent.vue'
import Footer from '../../../components/FooterComponent.vue'
import { providersAPI } from '@/axios'

const router = useRouter()

// Search and filter state
const searchQuery = ref('')
const selectedService = ref('all')
const loading = ref(true)
const error = ref('')
const providers = ref([])

// Load providers on mount
onMounted(async () => {
  await loadProviders()
})

// Load providers from backend
const loadProviders = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await providersAPI.getProviders({
      verified: true
    })

    const apiProviders = response.data.results || response.data

    // Map API data to component format
    providers.value = apiProviders.map(p => ({
      id: p.id,
      religionType: p.religion_type,
      type: p.religion_type === 'hindu' ? 'Pandit' : 'Lama',
      name: `${p.religion_type === 'hindu' ? 'Pandit' : 'Lama'} ${p.user.first_name} ${p.user.last_name}`,
      price: `Starts at NPR ${parseFloat(p.price_per_service).toLocaleString('en-NP')}`,
      profilePhoto: p.user.profile_photo
    }))

  } catch (err) {
    console.error('Error loading providers:', err)
    error.value = 'Failed to load providers. Please try again.'
  } finally {
    loading.value = false
  }
}

// Filter providers based on search and service type
const filteredProviders = computed(() => {
  let filtered = providers.value

  // Filter by service type
  if (selectedService.value !== 'all') {
    filtered = filtered.filter(p => p.religionType === selectedService.value)
  }

  // Filter by search query
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(p =>
      p.name.toLowerCase().includes(query)
    )
  }

  return filtered
})

// Helper function to get full image URL
const getImageUrl = (photoPath) => {
  if (!photoPath) return null
  // If it's already a full URL, return it
  if (photoPath.startsWith('http')) return photoPath
  // Otherwise, prepend your backend URL
  return `http://localhost:8000${photoPath}`
}

const viewDetails = (id) => {
  router.push(`/browse/${id}`)
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700&display=swap');

* {
  font-family: 'Rubik', sans-serif;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.browse-page {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #fffbf5;
}

.main-content {
  flex: 1;
  width: 100%;
}

/* Hero Section */
.hero-section {
  padding: 60px 40px 40px;
  text-align: center;
  background-color: #FFF5E1;
  width: 100%;
}

.page-title {
  font-size: 36px;
  font-weight: 600;
  color: #ae664a;
  margin-bottom: 12px;
}

.page-subtitle {
  font-size: 16px;
  color: #666;
  margin-bottom: 40px;
}

/* Search Container */
.search-container {
  max-width: 700px;
  margin: 0 auto;
  display: flex;
  gap: 16px;
  align-items: center;
}

.search-box {
  flex: 1;
  display: flex;
  background: white;
  border: 1px solid #e5d5c3;
  border-radius: 8px;
  overflow: hidden;
}

.search-input {
  flex: 1;
  padding: 14px 20px;
  border: none;
  font-size: 15px;
  outline: none;
  font-family: 'Rubik', sans-serif;
}

.search-input::placeholder {
  color: #999;
}

.search-button {
  background: white;
  border: none;
  padding: 0 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-button:hover {
  background: #f9f9f9;
}

.service-dropdown {
  padding: 14px 20px;
  background: white;
  border: 1px solid #ae664a;
  border-radius: 8px;
  color: #ae664a;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  outline: none;
  font-family: 'Rubik', sans-serif;
  min-width: 150px;
}

/* Loading & Error States */
.loading-container {
  text-align: center;
  padding: 60px 20px;
  font-size: 18px;
  color: #666;
}

.error-message {
  max-width: 600px;
  margin: 20px auto;
  padding: 16px 24px;
  background: #fee;
  color: #c33;
  border-radius: 8px;
  text-align: center;
  font-size: 14px;
}

/* Cards Section */
.cards-section {
  padding: 60px 40px;
  background-color: #FFF5E1;
  width: 100%;
}

.cards-grid {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.pandit-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.pandit-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.card-image {
  width: 100%;
  height: 180px;
  background: #e5e7eb;
}

.profile-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  background:
    linear-gradient(135deg, #f0f0f0 25%, transparent 25%),
    linear-gradient(225deg, #f0f0f0 25%, transparent 25%),
    linear-gradient(45deg, #f0f0f0 25%, transparent 25%),
    linear-gradient(315deg, #f0f0f0 25%, #e0e0e0 25%);
  background-size: 20px 20px;
  background-position:
    0 0,
    10px 0,
    10px -10px,
    0px 10px;
}

.card-content {
  padding: 20px;
}

.card-tag {
  display: inline-block;
  background: #f5e6d3;
  color: #ae664a;
  padding: 5px 14px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 10px;
}

.card-name {
  font-size: 16px;
  font-weight: 600;
  color: #000;
  margin: 10px 0 8px;
}

.card-price {
  font-size: 13px;
  color: #666;
  margin-bottom: 16px;
}

.details-button {
  width: 100%;
  padding: 11px;
  background: #ae664a;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s ease;
  font-family: 'Rubik', sans-serif;
}

.details-button:hover {
  background: #9a5838;
}

/* Footer */
.footer {
  background: white;
  border-top: 1px solid #e5e7eb;
  padding: 40px;
  margin-top: auto;
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
  color: #ae664a;
  text-decoration: none;
  font-weight: 500;
  font-size: 14px;
}

.contact-support-link:hover {
  text-decoration: underline;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .cards-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 40px 20px 30px;
  }

  .page-title {
    font-size: 28px;
  }

  .search-container {
    flex-direction: column;
    gap: 12px;
  }

  .service-dropdown {
    width: 100%;
  }

  .cards-section {
    padding: 40px 20px;
  }

  .cards-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }

  .footer-content {
    flex-direction: column;
    gap: 30px;
  }
}

@media (max-width: 480px) {
  .cards-grid {
    grid-template-columns: 1fr;
  }
}
</style>
