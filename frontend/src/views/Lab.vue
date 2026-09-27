<template>
    <div class="common-layout">
        <el-card style="width: 100%; margin: 0 auto;">
            <!-- 搜索栏 -->
            <div class="toolbar">
                <el-input v-model="query.keyword" placeholder="搜索名称/位置/简介" clearable style="width: 260px"
                    @keyup.enter="handleSearch" @clear="handleSearch">
                    <template #prefix>
                        <el-icon>
                            <Search />
                        </el-icon>
                    </template>
                </el-input>
                <el-button type="primary" @click="handleSearch">查询</el-button>
                <el-button v-if="isAdmin" type="success" @click="openAddDialog">新增实验室</el-button>
            </div>

            <!-- 实验室表格 -->
            <el-table :data="labList" v-loading="loading" stripe border style="width: 100%">
                <el-table-column prop="id" label="ID" width="70" align="center" />
                <el-table-column label="封面" width="100" align="center">
                    <template #default="{ row }">
                        <el-image v-if="row.img" :src="row.img" fit="cover"
                            style="width: 60px; height: 40px; border-radius: 4px;" :preview-src-list="[row.img]"
                            preview-teleported />
                        <span v-else>-</span>
                    </template>
                </el-table-column>
                <el-table-column prop="name" label="名称" min-width="140" />
                <el-table-column prop="description" label="简介" min-width="180" show-overflow-tooltip>
                    <template #default="{ row }">{{ row.description || '-' }}</template>
                </el-table-column>
                <el-table-column prop="location" label="位置" min-width="130">
                    <template #default="{ row }">{{ row.location || '-' }}</template>
                </el-table-column>
                <el-table-column prop="capacity" label="容量" width="80" align="center" />
                <el-table-column label="开放时间" min-width="140" align="center">
                    <template #default="{ row }">
                        {{ row.open_time || '--' }} ~ {{ row.close_time || '--' }}
                    </template>
                </el-table-column>
                <el-table-column label="状态" width="90" align="center">
                    <template #default="{ row }">
                        <el-switch v-if="isAdmin" :model-value="row.status" :active-value="1" :inactive-value="0"
                            @change="(val: number) => handleStatusChange(row, val)" />
                        <el-tag v-else :type="row.status === 1 ? 'success' : 'info'">
                            {{ row.status === 1 ? '开放' : '关闭' }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column v-if="isAdmin" label="操作" width="150" align="center" fixed="right">
                    <template #default="{ row }">
                        <el-button type="primary" link @click="openEditDialog(row)">编辑</el-button>
                        <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>

            <!-- 分页 -->
            <el-pagination class="pagination" :current-page="query.page" :page-size="query.page_size" :total="total"
                :page-sizes="[5, 10, 20, 50]" layout="total, sizes, prev, pager, next, jumper"
                @current-change="handlePageChange" @size-change="handleSizeChange" />
        </el-card>

        <!-- 新增/编辑实验室弹窗 -->
        <el-dialog v-model="dialogVisible" :title="dialogMode === 'add' ? '新增实验室' : '编辑实验室'" width="560px"
            @closed="resetForm">
            <el-form ref="formRef" :model="form" :rules="formRules" label-width="90px">
                <el-form-item prop="name" label="名称">
                    <el-input v-model="form.name" placeholder="请输入实验室名称" />
                </el-form-item>
                <el-form-item prop="location" label="位置">
                    <el-input v-model="form.location" placeholder="请输入位置" />
                </el-form-item>
                <el-form-item prop="capacity" label="容量">
                    <el-input-number v-model="form.capacity" :min="0" style="width: 100%;" />
                </el-form-item>
                <el-form-item prop="open_time" label="开放时间">
                    <div class="time-range">
                        <el-time-select v-model="form.open_time" start="00:00" step="00:30" end="23:30"
                            placeholder="开始时间" style="width: 50%;" />
                        <el-time-select v-model="form.close_time" :start="form.open_time || '00:00'" step="00:30"
                            end="23:59" placeholder="结束时间" style="width: 50%;" />
                    </div>
                </el-form-item>
                <el-form-item prop="description" label="简介">
                    <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入简介" />
                </el-form-item>
                <el-form-item prop="img" label="封面">
                    <el-upload class="img-uploader" :action="uploadUrl" :show-file-list="false"
                        :on-success="handleUploadSuccess" accept="image/*">
                        <el-image v-if="form.img" :src="form.img" fit="cover"
                            style="width: 120px; height: 80px; border-radius: 4px;" />
                        <el-icon v-else class="img-uploader-icon">
                            <Plus />
                        </el-icon>
                    </el-upload>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="dialogVisible = false">取消</el-button>
                <el-button type="primary" :loading="submitting" @click="submitForm">确定</el-button>
            </template>
        </el-dialog>
    </div>
</template>
<script setup lang="ts">
import { ElMessage, ElMessageBox, ElForm } from 'element-plus'
import { reactive, ref, computed, onMounted } from 'vue'
import {
    pageLabs,
    addLab,
    updateLab,
    deleteLab,
    type LabPageQuery,
    type LabCreateRequest,
} from '@/api/lab'
import { type LabInfo } from '@/api/lab'
import { useUser } from '@/utils/user'

const { userInfo } = useUser()
const isAdmin = computed(() => userInfo.value?.role === 'admin')

const uploadUrl = '/api/files/upload'
const loading = ref(false)
const submitting = ref(false)
const labList = ref<LabInfo[]>([])
const total = ref(0)

const query = reactive<LabPageQuery>({
    page: 1,
    page_size: 10,
    keyword: '',
})

// ==================== 列表加载 ====================
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
    // 防止 el-pagination 挂载/更新时误触发重复请求
    if (size === query.page_size) return
    query.page_size = size
    query.page = 1
    loadLabs()
}

const handlePageChange = (page: number) => {
    // 防止 el-pagination 挂载/更新时误触发重复请求
    if (page === query.page) return
    query.page = page
    loadLabs()
}

// ==================== 状态切换 ====================
const handleStatusChange = async (row: LabInfo, val: number) => {
    try {
        await updateLab(row.id, { status: val })
        row.status = val
        ElMessage.success(val === 1 ? '已开放' : '已关闭')
    } catch (error) {
        console.log('更新实验室状态失败', error)
    }
}

// ==================== 新增/编辑弹窗 ====================
const dialogVisible = ref(false)
const dialogMode = ref<'add' | 'edit'>('add')
const editingId = ref<number>(0)

const formRef = ref<InstanceType<typeof ElForm>>()
const form = reactive<LabCreateRequest>({
    name: '',
    description: '',
    img: '',
    location: '',
    capacity: 0,
    open_time: '',
    close_time: '',
    status: 1,
})

const formRules = reactive({
    name: [{ required: true, message: '请输入实验室名称', trigger: 'blur' }],
    capacity: [{ required: true, message: '请输入容量', trigger: 'blur' }],
})

const handleUploadSuccess = (res: { code: number, msg: string, data: { url: string } }) => {
    if (res.code !== 200 || !res.data?.url) {
        ElMessage.error(res.msg)
        return
    }
    form.img = res.data.url
}

const openAddDialog = () => {
    dialogMode.value = 'add'
    dialogVisible.value = true
}

const openEditDialog = (row: LabInfo) => {
    dialogMode.value = 'edit'
    editingId.value = row.id
    form.name = row.name
    form.description = row.description || ''
    form.img = row.img || ''
    form.location = row.location || ''
    form.capacity = row.capacity
    form.open_time = row.open_time || ''
    form.close_time = row.close_time || ''
    form.status = row.status
    dialogVisible.value = true
}

const resetForm = () => {
    form.name = ''
    form.description = ''
    form.img = ''
    form.location = ''
    form.capacity = 0
    form.open_time = ''
    form.close_time = ''
    form.status = 1
    formRef.value?.clearValidate()
}

const submitForm = async () => {
    if (!formRef.value) return
    const valid = await (formRef.value as unknown as {
        validate: () => Promise<boolean>
    })!.validate().catch(() => false)
    if (!valid) return

    try {
        submitting.value = true
        if (dialogMode.value === 'add') {
            await addLab(form)
            ElMessage.success('新增实验室成功')
        } else {
            await updateLab(editingId.value, form)
            ElMessage.success('更新实验室成功')
        }
        dialogVisible.value = false
        loadLabs()
    } catch (error) {
        console.log('提交实验室表单失败', error)
    } finally {
        submitting.value = false
    }
}

// ==================== 删除 ====================
const handleDelete = (row: LabInfo) => {
    ElMessageBox.confirm(`确定删除实验室「${row.name}」吗？删除后不可恢复。`, '删除确认', {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning',
    }).then(async () => {
        try {
            await deleteLab(row.id)
            ElMessage.success('删除成功')
            loadLabs()
        } catch (error) {
            console.log('删除实验室失败', error)
        }
    }).catch(() => { })
}

onMounted(() => {
    loadLabs()
})
</script>
<style scoped>
.toolbar {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
}

.pagination {
    margin-top: 16px;
    justify-content: flex-end;
}

.time-range {
    display: flex;
    gap: 8px;
    width: 100%;
}

.img-uploader :deep(.el-upload) {
    border: 1px dashed var(--el-border-color);
    border-radius: 6px;
    cursor: pointer;
    overflow: hidden;
    width: 120px;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.img-uploader :deep(.el-upload:hover) {
    border-color: var(--el-color-primary);
}

.img-uploader-icon {
    font-size: 24px;
    color: #8c939d;
}
</style>
