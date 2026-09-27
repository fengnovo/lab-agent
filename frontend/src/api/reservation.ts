import request from '@/utils/request'

export interface ReservationInfo {
    id: number
    user_id: number
    username: string
    lab_id: number
    lab_name: string
    equipment_id: number | null
    equipment_name: string | null
    date: string
    start_time: string
    end_time: string
    remark: string | null
    status: number
    created_at: string
}

export interface ReservationPageQuery {
    page: number
    page_size: number
    status?: number
    keyword?: string
    date?: string
}

export interface ReservationPageResult {
    list: ReservationInfo[]
    total: number
    page: number
    page_size: number
}

export interface ReservationCreateRequest {
    lab_id: number
    equipment_id?: number | null
    date: string
    start_time: string
    end_time: string
    remark?: string
}

// 提交预约
export const addReservation = (data: ReservationCreateRequest): Promise<ReservationInfo> => {
    return request.post('/reservation/add', data).then(res => {
        return (res as unknown as { data: ReservationInfo }).data
    })
}

// 我的预约列表
export const pageMyReservations = (params: ReservationPageQuery): Promise<ReservationPageResult> => {
    return request.get('/reservation/my', { params }).then(res => {
        return (res as unknown as { data: ReservationPageResult }).data
    })
}

// 取消预约
export const cancelReservation = (id: number): Promise<{ code: number, msg: string }> => {
    return request.put(`/reservation/${id}/cancel`).then(res => {
        return res as unknown as { code: number, msg: string }
    })
}

// 管理员: 全部预约列表
export const pageReservations = (params: ReservationPageQuery): Promise<ReservationPageResult> => {
    return request.get('/reservation/page', { params }).then(res => {
        return (res as unknown as { data: ReservationPageResult }).data
    })
}

// 管理员: 审核 (1 通过 / 2 拒绝)
export const auditReservation = (
    id: number,
    data: { status: number, remark?: string }
): Promise<{ code: number, msg: string }> => {
    return request.put(`/reservation/${id}/audit`, data).then(res => {
        return res as unknown as { code: number, msg: string }
    })
}
