const TOKEN_KEY = 'token'
const USER_INFO_KEY = 'userInfo'

export interface UserInfo {
  id: number
  username: string
  email: string
  avatar: string
  created_at: string
  name: string
  phone: string
  role: string
  status: number
  updated_at: string
}

export const getToken = () => localStorage.getItem(TOKEN_KEY)
export const setToken = (token: string) => localStorage.setItem(TOKEN_KEY, token)
export const removeToken = () => localStorage.removeItem(TOKEN_KEY)
export const getUserInfo = () => JSON.parse(localStorage.getItem(USER_INFO_KEY) || '{}')
export const setUserInfo = (userInfo: UserInfo) => localStorage.setItem(USER_INFO_KEY, JSON.stringify(userInfo))
export const removeUserInfo = () => localStorage.removeItem(USER_INFO_KEY)
