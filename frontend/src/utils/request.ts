import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'
import { getToken, removeToken, removeUserInfo, getUserInfo } from './auth'

const service = axios.create({
  baseURL: '/api',
  timeout: 5000,
})


service.interceptors.request.use(
  (config) => {
    const token = getToken()
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

service.interceptors.response.use(
  (response) => {
    const { data } = response
    if (data.code === 401) {
      ElMessage.error(data.msg || '登录过期，请重新登录')
      removeToken()
      removeUserInfo()
      router.push({ name: 'Login' })
      return Promise.reject(data)
    } else if (data.code !== 200) {
      ElMessage.error(data.msg || '请求失败')
      return Promise.reject(data)
    }
    return data
  },
  (error) => {
    const { response } = error
    if (response) {
      const { status } = response
      if (status === 401) {
        ElMessage.error('登录过期，请重新登录')
        removeToken()
        removeUserInfo()
        router.push({ name: 'Login' })
        return Promise.reject(error)
      } else {
        ElMessage.error(response.data?.msg || response.data?.message || '请求失败')
      }
    } else {
      ElMessage.error(error.message || '服务器异常，请稍后重试')
    }
    return Promise.reject(error)
  },
)

export default service
