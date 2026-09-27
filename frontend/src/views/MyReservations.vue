<template>
    <div class="common-layout">
        <el-card style="width: 100%;">
            <!-- 筛选栏 -->
            <div class="toolbar">
                <el-select v-model="query.status" placeholder="预约状态" clearable style="width: 140px"
                    @change="handleSearch">
                    <el-option label="待审核" :value="0" />
                    <el-option label="已通过" :value="1" />
                    <el-option label="已拒绝" :value="2" />
                    <el-option label="已取消" :value="3" />
                </el-select>
                <el-date-picker v-model="query.date" type="date" placeholder="预约日期" value-format="YYYY-MM-DD"
                    style="width: 180px" @change="handleSearch" />
                <el-button type="primary" @click="handleSearch">查询</el-button>
            </div>

            <!-- 预约表格 -->
            <el-table :data="list" v-loading="loading" stripe border style="width: 100%">
                <el-table-column prop="id" label="ID" width="70" align="center" />
                <el-table-column prop="lab_name" label="实验室" min-width="130" />
                <el-table-column label="预约对象" min-width="120">
                    <template #default="{ row }">
                        {{ row.equipment_name ? '设备: ' + row.equipment_name : '整间实验室' }}
                    </template>
                </el-table-column>
                <el-table-column label="预约时间" min-width="180">
                    <template #default="{ row }">
                        {{ row.date }} {{ row.start_time }} - {{ row.end_time }}
                    </template>
                </el-table-column>
                <el-table-column prop="remark" label="备注" min-width="140" show-overflow-tooltip>
                    <template #default="{ row }">{{ row.remark || '-' }}</template>
                </el-table-column>
                <el-table-column label="状态" width="100" align="center">
                    <template #default="{ row }">
                        <el-tag :type="statusType[row.status]">{{ statusText[row.status] }}</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="100" align="center">
                    <template #default="{ row }">
                        <el-button type="danger" link
                            :disabled="row.status === 2 || row.status === 3"
                            @click="handleCancel(row)">取消</el-button>
                    </template>
                </el-table-column>
            </el-table>

            <el-pagination class="pagination" :current-page="query.page" :page-size="query.page_size" :total="total"
                :page-sizes="[10, 20, 50]" layout="total, sizes, prev, pager, next, jumper"
                @current-change="handlePageChange" @size-change="handleSizeChange" />
        </el-card>
    </div>
</template>
<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
    pageMyReservations,
    cancelReservation,
    type ReservationInfo,
    type ReservationPageQuery,
} from '@/api/reservation'

const loading = ref(false)
const list = ref<ReservationInfo[]>([])
const total = ref(0)

const statusText = ['待审核', '已通过', '已拒绝', '已取消']
const statusType = ['warning', 'success', 'danger', 'info'] as const

const query = reactive<ReservationPageQuery>({
    page: 1,
    page_size: 10,
    status: undefined,
    date: '',
})

const loadList = async () => {
    loading.value = true
    try {
        const res = await pageMyReservations(query)
        list.value = res.list
        total.value = res.total
    } catch (error) {
        console.log('查询我的预约失败', error)
    } finally {
        loading.value = false
    }
}

const handleSearch = () => {
    query.page = 1
    loadList()
}

const handleSizeChange = (size: number) => {
    if (size === query.page_size) return
    query.page_size = size
    query.page = 1
    loadList()
}

const handlePageChange = (page: number) => {
    if (page === query.page) return
    query.page = page
    loadList()
}

const handleCancel = (row: ReservationInfo) => {
    ElMessageBox.confirm(`确定取消 ${row.date} ${row.start_time} 的预约吗？`, '取消确认', {
        confirmButtonText: '取消预约',
        cancelButtonText: '再想想',
        type: 'warning',
    }).then(async () => {
        try {
            await cancelReservation(row.id)
            ElMessage.success('预约已取消')
            loadList()
        } catch (error) {
            console.log('取消预约失败', error)
        }
    }).catch(() => { })
}

onMounted(() => {
    loadList()
})
</script>
<style scoped>
.toolbar {
    display: flex;
    gap: 12px;
    margin-bottom: 16px;
}

.pagination {
    margin-top: 16px;
    justify-content: flex-end;
}
</style>
