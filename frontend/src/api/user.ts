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


// ==================== 用户管理(管理员) ====================

export interface UserPageQuery {
    page: number
    page_size: number
    keyword?: string
}

export interface UserCreateRequest {
    username: string
    password: string
    name: string
    role: string
    phone?: string
    email?: string
}

export interface UserAdminUpdateRequest {
    name?: string
    role?: string
    phone?: string
    email?: string
    status?: number
    password?: string
}

export interface UserPageResult {
    list: UserInfo[]
    total: number
    page: number
    page_size: number
}

// 分页查询用户列表
export const pageUsers = (params: UserPageQuery): Promise<UserPageResult> => {
    return request.get<UserPageResult>('/user/page', { params }).then(res => {
        // res 是 { code, msg, data } 响应体, 列表数据在 data 里
        return (res as unknown as { data: UserPageResult }).data
    })
}

// 新增用户
export const addUser = (data: UserCreateRequest): Promise<{ code: number, msg: string }> => {
    return request.post('/user/add', data).then(res => {
        return res as unknown as { code: number, msg: string }
    })
}

// 管理员更新用户(角色/状态/重置密码等)
export const adminUpdateUser = (id: number, data: UserAdminUpdateRequest): Promise<{ code: number, msg: string }> => {
    return request.put(`/user/${id}`, data).then(res => {
        return res as unknown as { code: number, msg: string }
    })
}

// 删除用户
export const deleteUser = (id: number): Promise<{ code: number, msg: string }> => {
    return request.delete(`/user/${id}`).then(res => {
        return res as unknown as { code: number, msg: string }
    })
}