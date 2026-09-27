<template>
    <div class="common-layout">
        <el-card>
            <template #header>
                <span>实验室列表</span>
            </template>

            <!-- 搜索栏 -->
            <div class="toolbar">
                <el-input v-model="query.keyword" placeholder="请输入名称查询" clearable style="width: 280px"
                    @keyup.enter="handleSearch" @clear="handleSearch" />
                <el-button type="primary" @click="handleSearch">查询</el-button>
            </div>

            <!-- 实验室卡片 -->
            <div v-loading="loading" class="lab-grid">
                <el-card v-for="lab in labList" :key="lab.id" class="lab-card" shadow="hover">
                    <el-image :src="lab.img || defaultImg" fit="cover" class="lab-img" />
                    <div class="lab-body">
                        <div class="lab-name">{{ lab.name }}</div>
                        <div class="lab-info">
                            <div>位置: {{ lab.location || '-' }}</div>
                            <div>容量: {{ lab.capacity }} 人</div>
                            <div>开放: {{ lab.open_time }} - {{ lab.close_time }}</div>
                        </div>
                        <div class="lab-actions">
                            <el-button size="small" @click="goDetail(lab.id)">查看设备</el-button>
                            <el-button size="small" type="primary" @click="goDetail(lab.id)">预约</el-button>
                        </div>
                    </div>
                </el-card>
                <el-empty v-if="!loading && labList.length === 0" description="暂无实验室" />
            </div>

            <!-- 分页 -->
            <el-pagination class="pagination" :current-page="query.page" :page-size="query.page_size" :total="total"
                :page-sizes="[8, 12, 24]" layout="total, sizes, prev, pager, next, jumper"
                @current-change="handlePageChange" @size-change="handleSizeChange" />
        </el-card>
    </div>
</template>
<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { pageLabs, type LabInfo, type LabPageQuery } from '@/api/lab'

const router = useRouter()
const loading = ref(false)
const labList = ref<LabInfo[]>([])
const total = ref(0)
const defaultImg = 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=modern%20laboratory%20interior%20with%20computers%20and%20equipment%2C%20bright%20clean%20white%20room%2C%20realistic%20photo&image_size=landscape_16_9'

const query = reactive<LabPageQuery>({
    page: 1,
    page_size: 8,
    keyword: '',
})

const loadLabs = async () => {
    loading.value = true
    try {
        const res = await pageLabs(query)
        labList.value = res.list
        total.value = res.total
    } catch (error) {
        console.log('查询实验室列表失败', error)
    } finally {
        loading.value = false
    }
}

const handleSearch = () => {
    query.page = 1
    loadLabs()
}

const handleSizeChange = (size: number) => {
    if (size === query.page_size) return
    query.page_size = size
    query.page = 1
    loadLabs()
}

const handlePageChange = (page: number) => {
    if (page === query.page) return
    query.page = page
    loadLabs()
}

const goDetail = (id: number) => {
    router.push(`/manager/lablist/${id}`)
}

onMounted(() => {
    loadLabs()
})
</script>
<style scoped>
.toolbar {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
}

.lab-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 20px;
    min-height: 200px;
}

.lab-card :deep(.el-card__body) {
    padding: 0;
}

.lab-img {
    width: 100%;
    height: 160px;
    display: block;
}

.lab-body {
    padding: 12px 16px;
}

.lab-name {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 8px;
}

.lab-info {
    font-size: 13px;
    color: var(--el-text-color-secondary);
    line-height: 1.8;
    margin-bottom: 12px;
}

.lab-actions {
    display: flex;
    justify-content: space-between;
}

.pagination {
    margin-top: 20px;
    justify-content: center;
}
</style>
