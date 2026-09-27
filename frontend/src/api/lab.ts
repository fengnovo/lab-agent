import request from '@/utils/request'

export interface LabInfo {
    id: number
    name: string
    description: string
    img: string
    location: string
    capacity: number
    open_time: string
    close_time: string
    status: number
    created_at: string
    updated_at: string
}

export interface LabPageQuery {
    page: number
    page_size: number
    keyword?: string
}

export interface LabPageResult {
    list: LabInfo[]
    total: number
    page: number
    page_size: number
}

export interface LabCreateRequest {
    name: string
    description?: string
    img?: string
    location?: string
    capacity?: number
    open_time?: string
    close_time?: string
    status?: number
}

export interface LabUpdateRequest {
    name?: string
    description?: string
    img?: string
    location?: string
    capacity?: number
    open_time?: string
    close_time?: string
    status?: number
}

// 分页查询实验室列表
export const pageLabs = (params: LabPageQuery): Promise<LabPageResult> => {
    return request.get<LabPageResult>('/lab/page', { params }).then(res => {
        return (res as unknown as { data: LabPageResult }).data
    })
}

// 新增实验室
export const addLab = (data: LabCreateRequest): Promise<{ code: number, msg: string }> => {
    return request.post('/lab/add', data).then(res => {
        return res as unknown as { code: number, msg: string }
    })
}

// 更新实验室
export const updateLab = (id: number, data: LabUpdateRequest): Promise<{ code: number, msg: string }> => {
    return request.put(`/lab/${id}`, data).then(res => {
        return res as unknown as { code: number, msg: string }
    })
}

// 删除实验室
export const deleteLab = (id: number): Promise<{ code: number, msg: string }> => {
    return request.delete(`/lab/${id}`).then(res => {
        return res as unknown as { code: number, msg: string }
    })
}
