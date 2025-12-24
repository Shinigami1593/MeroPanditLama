import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/LandingView.vue'),
  },
  {
    path: '/browse',
    name: 'browse',
    component: () => import('../views/pages/user/BrowseView.vue'),
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/authentication/LoginView.vue'),
  },
  {
    path: '/signup',
    name: 'signup',
    component: () => import('../views/authentication/SignupView.vue'),
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('../views/pages/user/ProfileView.vue'),
  },
  {
    path: '/my-bookings',
    name: 'my-bookings',
    component: () => import('../views/pages/user/MyBookingsView.vue'),
  },
  {
    path: '/browse/:id',
    name: 'pandit-detail',
    component: () => import('../views/pages/user/DetailsView.vue'),
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return { top: 0, behavior: 'smooth' } // Scroll to top with smooth effect
  },
})

router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresConsultation)) {
    const consultationForm = JSON.parse(localStorage.getItem('consultation_form'))

    if (!consultationForm) {
      return next({ name: 'consultation' })
    }

    // Check for additional condition if `requiresConsultation2` is present
    if (
      to.matched.some((record) => record.meta.requiresConsultation2) &&
      !consultationForm.symptoms
    ) {
      return next({ name: 'consultation2' })
    }
  }

  next() // Ensure to call next() once at the end if all checks pass
})

export default router
