import axios from 'axios'

// Create axios instance
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api', // Added /api to base URL
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests if it exists
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for handling token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // If 401 and we haven't tried refreshing yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      const refreshToken = localStorage.getItem('refresh')
      if (refreshToken) {
        try {
          const response = await axios.post('http://localhost:8000/api/auth/refresh/', {
            refresh: refreshToken,
          })

          const newToken = response.data.access
          localStorage.setItem('token', newToken)

          // Retry original request with new token
          originalRequest.headers.Authorization = `Bearer ${newToken}`
          return apiClient(originalRequest)
        } catch (refreshError) {
          // Refresh failed, logout user
          clearAuth()
          window.location.href = '/login'
          return Promise.reject(refreshError)
        }
      }
    }

    return Promise.reject(error)
  }
)

// ============================================================================
// AUTHENTICATION API
// ============================================================================
export const authAPI = {
  signup: (data) => apiClient.post('/auth/signup/', data),
  login: (data) => apiClient.post('/auth/login/', data),
  refreshToken: (refresh) => apiClient.post('/auth/refresh/', { refresh }),
  getProfile: () => apiClient.get('/profile/'),
  updateProfile: (data) => {
    // Check if it's FormData (file upload)
    if (data instanceof FormData) {
      return apiClient.patch('/profile/', data, {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
      })
    }
    // Regular JSON data
    return apiClient.put('/profile/', data)
  },
}

// ============================================================================
// PROVIDERS API (Public)
// ============================================================================
export const providersAPI = {
  getProviders: (params = {}) => apiClient.get('/providers/', { params }),
  getProviderById: (id) => apiClient.get(`/providers/${id}/`),
  getProviderAvailability: (id, date) => {
    console.log('🔍 Calling availability API for provider:', id, 'date:', date);
    return apiClient.get(`/providers/${id}/availability/`, {
      params: { date }
    });
  },
  getProviderReviews: (id) => apiClient.get(`/providers/${id}/reviews/`),
}

// ============================================================================
// PROVIDER DASHBOARD API (Provider role only)
// ============================================================================
export const providerDashboardAPI = {
  getDashboard: () => apiClient.get('/provider/dashboard/'),
  getMyBookings: (params = {}) => apiClient.get('/provider/bookings/', { params }),
  getMyProfile: () => apiClient.get('/provider/profile/'),
  updateMyProfile: (data) => apiClient.put('/provider/profile/', data),
  getMyAvailability: (params = {}) => apiClient.get('/provider/availability/', { params }),
  createAvailability: (data) => apiClient.post('/provider/availability/', data),
  updateAvailability: (slotId, data) => apiClient.put(`/provider/availability/${slotId}/`, data),
  deleteAvailability: (slotId) => apiClient.delete(`/provider/availability/${slotId}/`),
}

// ============================================================================
// BOOKINGS API
// ============================================================================
export const bookingsAPI = {
  createBooking: (data) => apiClient.post('/bookings/', data),
  getBookings: (params = {}) => apiClient.get('/bookings/', { params }),
  getBookingById: (id) => apiClient.get(`/bookings/${id}/`),
  getBookingHistory: () => apiClient.get('/history/'),
  confirmBooking: (id) => apiClient.post(`/bookings/${id}/confirm/`),
  rejectBooking: (id, data) => apiClient.post(`/bookings/${id}/reject/`, data),
  cancelBooking: (id, data) => apiClient.post(`/bookings/${id}/cancel/`, data),
  completeBooking: (id) => apiClient.post(`/bookings/${id}/complete/`),
}

// ============================================================================
// SERVICES API
// ============================================================================
export const servicesAPI = {
  getServices: () => apiClient.get('/services/'),
}

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================
export const setAuthToken = (token) => {
  localStorage.setItem('token', token)
}

export const setUserData = (user) => {
  localStorage.setItem('user', JSON.stringify(user))
}

export const getAuthToken = () => {
  return localStorage.getItem('token')
}

export const getUserData = () => {
  const user = localStorage.getItem('user')
  return user ? JSON.parse(user) : null
}

export const isAuthenticated = () => {
  return !!getAuthToken()
}

export const isProvider = () => {
  const user = getUserData()
  return user?.role === 'provider'
}

export const isRegularUser = () => {
  const user = getUserData()
  return user?.role === 'user'
}

export const clearAuth = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('refresh')
  localStorage.removeItem('user')
}

export const logout = () => {
  clearAuth()
  window.location.href = '/'
}

export default apiClient
