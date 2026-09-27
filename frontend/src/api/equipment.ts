import request from '@/utils/request'

export interface EquipmentInfo {
    id: number
    lab_id: number
    lab_name: string
    name: string
    description: string
    img: string
    spec: string
    quantity: number
    status: number
    created_at: string
    updated_at: string
}

export interface EquipmentPageQuery {
    page: number
    page_size: number
    keyword?: string
    lab_id?: number
}

export interface EquipmentPageResult {
    list: EquipmentInfo[]
    total: number
    page: number
    page_size: number
}

export interface EquipmentCreateRequest {
    lab_id: number
    name: string
    description?: string
    img?: string
    spec?: string
    quantity?: number
    status?: number
}

export interface EquipmentUpdateRequest {
    lab_id?: number
    name?: string
    description?: string
    img?: string
    spec?: string
    quantity?: number
    status?: number
}

// 分页查询设备列表
export const pageEquipments = (params: EquipmentPageQuery): Promise<EquipmentPageResult> => {
    return request.get<EquipmentPageResult>('/equipment/page', { params }).then(res => {
        return (res as unknown as { data: EquipmentPageResult }).data
    })
}

// 新增设备
export const addEquipment = (data: EquipmentCreateRequest): Promise<{ code: number, msg: string }> => {
    return request.post('/equipment/add', data).then(res => {
        return res as unknown as { code: number, msg: string }
    })
}

// 更新设备
export const updateEquipment = (id: number, data: EquipmentUpdateRequest): Promise<{ code: number, msg: string }> => {
    return request.put(`/equipment/${id}`, data).then(res => {
        return res as unknown as { code: number, msg: string }
    })
}

// 删除设备
export const deleteEquipment = (id: number): Promise<{ code: number, msg: string }> => {
    return request.delete(`/equipment/${id}`).then(res => {
        return res as unknown as { code: number, msg: string }
    })
}
