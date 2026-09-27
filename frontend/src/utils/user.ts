import { ref } from 'vue'
import { type UserInfo, getUserInfo, setToken, setUserInfo } from '@/utils/auth'

const userInfo = ref<UserInfo>(getUserInfo())

export interface UserResponse {
    user: UserInfo
    token: string
}

export const useUser = () => {
    const saveUserInfo = (data: UserResponse) => {
        setToken(data.token)
        setUserInfo(data.user)
        userInfo.value = data.user
    }
    const updateUserInfo = (user: UserInfo) => {
        userInfo.value = user
    }
    const reloadUserInfo = () => {
        userInfo.value = getUserInfo()
    }
    return {
        userInfo,
        saveUserInfo,
        updateUserInfo,
        reloadUserInfo,
    }
}
