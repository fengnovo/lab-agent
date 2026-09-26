import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/manager/home',
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue'),
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/Register.vue'),
    },
    {
      path: '/manager',
      name: 'Layout',
      component: () => import('@/layouts/Layout.vue'),
      children: [
        {
          path: '/manager/home',
          name: 'Home',
          component: () => import('@/views/Home.vue'),
        },
        {
          path: '/manager/lab',
          name: 'Lab',
          component: () => import('@/views/Lab.vue'),
        },
        {
          path: '/manager/equipment',
          name: 'Equipment',
          component: () => import('@/views/Equipment.vue'),
        },
        {
          path: '/manager/user',
          name: 'User',
          component: () => import('@/views/User.vue'),
        },
      ],
    },
  ],
})

export default router
