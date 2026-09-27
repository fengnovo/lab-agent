<template>
    <div class="common-layout">
        <el-card>
            <template #header>
                <div class="header-bar">
                    <span>{{ lab?.name || '实验室详情' }}</span>
                    <div>
                        <el-button type="primary" @click="ElMessage.info('预约功能开发中')">预约实验室</el-button>
                        <el-button @click="router.back()">返回实验室列表</el-button>
                    </div>
                </div>
            </template>

            <!-- 实验室简介 -->
            <el-alert v-if="lab" type="info" :closable="false" class="lab-desc">
                <p>简介: {{ lab.description || lab.name }}</p>
                <p>
                    位置: {{ lab.location || '-' }} &nbsp;|&nbsp;
                    容纳: {{ lab.capacity }} 人 &nbsp;|&nbsp;
                    开放: {{ lab.open_time }} - {{ lab.close_time }}
                </p>
            </el-alert>

            <!-- 设备表格 -->
            <el-table :data="equipmentList" v-loading="loading" border stripe style="width: 100%">
                <el-table-column label="图片" width="100" align="center">
                    <template #default="{ row }">
                        <el-image v-if="row.img" :src="row.img" fit="cover"
                            style="width: 60px; height: 40px; border-radius: 4px;" :preview-src-list="[row.img]"
                            preview-teleported />
                        <el-image v-else :src="defaultEqImg" fit="cover"
                            style="width: 60px; height: 40px; border-radius: 4px;" />
                    </template>
                </el-table-column>
                <el-table-column prop="name" label="设备名称" min-width="160" />
                <el-table-column prop="spec" label="型号规格" min-width="160">
                    <template #default="{ row }">{{ row.spec || '-' }}</template>
                </el-table-column>
                <el-table-column prop="quantity" label="数量" width="90" align="center" />
                <el-table-column label="状态" width="100" align="center">
                    <template #default="{ row }">
                        <el-tag :type="row.status === 1 ? 'success' : 'warning'">
                            {{ row.status === 1 ? '正常' : '维修中' }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="110" align="center">
                    <template #default>
                        <el-button type="primary" link @click="ElMessage.info('预约功能开发中')">预约</el-button>
                    </template>
                </el-table-column>
            </el-table>

            <!-- 分页 -->
            <el-pagination class="pagination" :current-page="query.page" :page-size="query.page_size" :total="total"
                :page-sizes="[10, 20, 50]" layout="total, sizes, prev, pager, next, jumper"
                @current-change="handlePageChange" @size-change="handleSizeChange" />
        </el-card>
    </div>
</template>
<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getLabDetail, type LabInfo } from '@/api/lab'
import { pageEquipments, type EquipmentInfo, type EquipmentPageQuery } from '@/api/equipment'

const route = useRoute()
const router = useRouter()
const labId = Number(route.params.id)

const lab = ref<LabInfo | null>(null)
const equipmentList = ref<EquipmentInfo[]>([])
const total = ref(0)
const loading = ref(false)
const defaultEqImg = 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=electronic%20test%20equipment%20oscilloscope%20on%20lab%20bench%2C%20realistic%20photo&image_size=landscape_4_3'

const query = reactive<EquipmentPageQuery>({
    page: 1,
    page_size: 10,
    lab_id: labId,
})

const loadLab = async () => {
    try {
        lab.value = await getLabDetail(labId)
    } catch (error) {
        console.log('查询实验室详情失败', error)
    }
}

const loadEquipments = async () => {
    loading.value = true
    try {
        const res = await pageEquipments(query)
        equipmentList.value = res.list
        total.value = res.total
    } catch (error) {
        console.log('查询设备列表失败', error)
    } finally {
        loading.value = false
    }
}

const handleSizeChange = (size: number) => {
    if (size === query.page_size) return
    query.page_size = size
    query.page = 1
    loadEquipments()
}

const handlePageChange = (page: number) => {
    if (page === query.page) return
    query.page = page
    loadEquipments()
}

onMounted(() => {
    loadLab()
    loadEquipments()
})
</script>
<style scoped>
.header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 600;
}

.lab-desc {
    margin-bottom: 16px;
    line-height: 1.8;
}

.pagination {
    margin-top: 16px;
    justify-content: flex-end;
}
</style>
