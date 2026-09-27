import { createRouter, createWebHistory } from 'vue-router'
import { getToken, getUserInfo } from '@/utils/auth'

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
          meta: { requiresAdmin: true },
        },
        {
          path: '/manager/lablist',
          name: 'LabList',
          component: () => import('@/views/LabList.vue'),
        },
        {
          path: '/manager/lablist/:id',
          name: 'LabDetail',
          component: () => import('@/views/LabDetail.vue'),
        },
        {
          path: '/manager/my-reservations',
          name: 'MyReservations',
          component: () => import('@/views/MyReservations.vue'),
        },
        {
          path: '/manager/reservation',
          name: 'ReservationManage',
          component: () => import('@/views/ReservationManage.vue'),
          meta: { requiresAdmin: true },
        },
        {
          path: '/manager/equipment',
          name: 'Equipment',
          component: () => import('@/views/Equipment.vue'),
          meta: { requiresAdmin: true },
        },
        {
          path: '/manager/user',
          name: 'User',
          component: () => import('@/views/User.vue'),
          meta: { requiresAdmin: true },
        },
        {
          path: '/manager/profile',
          name: 'Profile',
          component: () => import('@/views/Profile.vue'),
        },
        {
          path: '/manager/password-reset',
          name: 'PasswordReset',
          component: () => import('@/views/PasswordReset.vue'),
        },
      ],
    },
  ],
})

// 路由守卫, 检查是否有token
router.beforeEach((to) => {
  // 登录页和注册页不需要token
  if (to.name === 'Login' || to.name === 'Register') {
    return true
  }
  const token = getToken()
  if (!token) {
    return { name: 'Login' }
  }
  // 管理页面仅 admin 可访问, 其他角色重定向到实验室列表
  if (to.meta.requiresAdmin) {
    const userInfo = getUserInfo()
    if (userInfo?.role !== 'admin') {
      return { path: '/manager/lablist' }
    }
  }
  return true
})

export default router
