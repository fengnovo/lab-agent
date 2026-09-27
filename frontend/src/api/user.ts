import request from '@/utils/request'
import { type UserResponse } from '@/utils/user'
import { type UserInfo } from '@/utils/auth'


// 获取用户信息
export const getUserInfo = (): Promise<UserInfo> => {
    return request.get<UserInfo>('/user/info').then(res => res.data)
}

// 上传文件
export const uploadFile = (data: FormData): Promise<{ code: number, msg: string, data: string }> => {
    return request.post<{ code: number, msg: string, data: string }>('/files/upload', data).then(res => {
        // res 实际上是 { code, msg, data }，但类型系统不知道，所以需要强制转换
        return res as unknown as { code: number, msg: string, data: string }
    })
}

// 更新用户信息
export const updateUserUserInfo = (data: UserResponse): Promise<{ code: number, data: UserInfo, msg: string }> => {
    return request.put<{ code: number, data: UserInfo, msg: string }>('/user/update', data).then(res => {
        // res 实际上是 { code, data: UserInfo, msg: msg }，但类型系统不知道，所以需要强制转换
        return res as unknown as { code: number, data: UserInfo, msg: string }
    })
}


// 重置密码
export const resetPasswordUserInfo = (data: { new_password: string, old_password: string }): Promise<{ code: number, msg: string }> => {
    return request.post<{ code: number, msg: string }>('/user/reset-password', data).then(res => {
        // res 实际上是 { code, msg: msg }，但类型系统不知道，所以需要强制转换
        return res as unknown as { code: number, msg: string }
    })
}