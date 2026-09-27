import request from '@/utils/request'
import { type User } from '@/utils/user'

export interface LoginRequest {
    username: string
    password: string
}

export const login = (data: LoginRequest): Promise<User> => {
    return request.post<User>('/auth/login', data).then(res => res.data)
}