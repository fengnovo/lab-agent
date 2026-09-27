import request from '@/utils/request'
import { type UserResponse } from '@/utils/user'

export interface LoginRequest {
    username: string
    password: string
}
export interface RegisterRequest {
    username: string
    password: string
    confirmPassword: string
}

export const login = (data: LoginRequest): Promise<UserResponse> => {
    return request.post<UserResponse>('/auth/login', data).then(res => res.data)
}
export const register = (data: RegisterRequest): Promise<{ code: number, msg: string }> => {
    return request.post<{ code: number, msg: string }>('/auth/register', data).then(res => {
        // res 实际上是 { code, msg }，但类型系统不知道，所以需要强制转换
        return res as unknown as { code: number, msg: string }
    })
}