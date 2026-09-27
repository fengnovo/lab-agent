<template>
    <div class="common-layout">
        <el-card style="width: 100%; margin: 0 auto;">
            <!-- 搜索栏 -->
            <div class="toolbar">
                <el-input v-model="query.keyword" placeholder="搜索名称/型号规格/说明" clearable style="width: 240px"
                    @keyup.enter="handleSearch" @clear="handleSearch">
                    <template #prefix>
                        <el-icon>
                            <Search />
                        </el-icon>
                    </template>
                </el-input>
                <el-select v-model="query.lab_id" placeholder="所属实验室" clearable style="width: 180px"
                    @change="handleSearch">
                    <el-option v-for="lab in labOptions" :key="lab.id" :label="lab.name" :value="lab.id" />
                </el-select>
                <el-button type="primary" @click="handleSearch">查询</el-button>
                <el-button type="success" @click="openAddDialog">新增设备</el-button>
            </div>

            <!-- 设备表格 -->
            <el-table :data="equipmentList" v-loading="loading" stripe border style="width: 100%">
                <el-table-column prop="id" label="ID" width="70" align="center" />
                <el-table-column label="图片" width="100" align="center">
                    <template #default="{ row }">
                        <el-image v-if="row.img" :src="row.img" fit="cover"
                            style="width: 60px; height: 40px; border-radius: 4px;" :preview-src-list="[row.img]"
                            preview-teleported />
                        <span v-else>-</span>
                    </template>
                </el-table-column>
                <el-table-column prop="name" label="设备名称" min-width="140" />
                <el-table-column prop="spec" label="型号规格" min-width="130">
                    <template #default="{ row }">{{ row.spec || '-' }}</template>
                </el-table-column>
                <el-table-column prop="lab_name" label="所属实验室" min-width="130">
                    <template #default="{ row }">{{ row.lab_name || '-' }}</template>
                </el-table-column>
                <el-table-column prop="quantity" label="数量" width="80" align="center" />
                <el-table-column label="状态" width="90" align="center">
                    <template #default="{ row }">
                        <el-switch :model-value="row.status" :active-value="1" :inactive-value="0" active-text=""
                            @change="(val: number) => handleStatusChange(row, val)" />
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="150" align="center" fixed="right">
                    <template #default="{ row }">
                        <el-button type="primary" link @click="openEditDialog(row)">编辑</el-button>
                        <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>

            <!-- 分页 -->
            <el-pagination class="pagination" :current-page="query.page" :page-size="query.page_size" :total="total"
                :page-sizes="[10, 20, 50]" layout="total, sizes, prev, pager, next, jumper"
                @current-change="handlePageChange" @size-change="handleSizeChange" />
        </el-card>

        <!-- 新增/编辑设备弹窗 -->
        <el-dialog v-model="dialogVisible" :title="dialogMode === 'add' ? '新增设备' : '编辑设备'" width="600px"
            @closed="resetForm">
            <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px">
                <el-form-item prop="name" label="设备名称">
                    <el-input v-model="form.name" placeholder="请输入设备名称" />
                </el-form-item>
                <el-form-item prop="lab_id" label="所属实验室">
                    <el-select v-model="form.lab_id" placeholder="请选择所属实验室" style="width: 100%;">
                        <el-option v-for="lab in labOptions" :key="lab.id" :label="lab.name" :value="lab.id" />
                    </el-select>
                </el-form-item>
                <el-form-item prop="spec" label="型号规格">
                    <el-input v-model="form.spec" placeholder="请输入型号规格" />
                </el-form-item>
                <el-form-item prop="quantity" label="数量">
                    <el-input-number v-model="form.quantity" :min="1" style="width: 100%;" />
                </el-form-item>
                <el-form-item prop="status" label="状态">
                    <el-radio-group v-model="form.status">
                        <el-radio :value="1">正常</el-radio>
                        <el-radio :value="0">维修</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item prop="img" label="图片">
                    <el-upload class="img-uploader" :action="uploadUrl" :show-file-list="false"
                        :on-success="handleUploadSuccess" accept="image/*">
                        <el-image v-if="form.img" :src="form.img" fit="cover"
                            style="width: 120px; height: 80px; border-radius: 4px;" />
                        <el-icon v-else class="img-uploader-icon">
                            <Plus />
                        </el-icon>
                    </el-upload>
                </el-form-item>
                <el-form-item prop="description" label="说明">
                    <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入说明" />
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
import { reactive, ref, onMounted } from 'vue'
import {
    pageEquipments,
    addEquipment,
    updateEquipment,
    deleteEquipment,
    type EquipmentPageQuery,
    type EquipmentCreateRequest,
} from '@/api/equipment'
import { type EquipmentInfo } from '@/api/equipment'
import { pageLabs, type LabInfo } from '@/api/lab'

const uploadUrl = '/api/files/upload'
const loading = ref(false)
const submitting = ref(false)
const equipmentList = ref<EquipmentInfo[]>([])
const total = ref(0)
const labOptions = ref<LabInfo[]>([])

const query = reactive<EquipmentPageQuery>({
    page: 1,
    page_size: 10,
    keyword: '',
    lab_id: undefined,
})

// ==================== 列表加载 ====================
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

const loadLabOptions = async () => {
    try {
        // 拉取全量实验室作为下拉选项
        const res = await pageLabs({ page: 1, page_size: 100 })
        labOptions.value = res.list
    } catch (error) {
        console.log('查询实验室选项失败', error)
    }
}

const handleSearch = () => {
    query.page = 1
    loadEquipments()
}

const handleSizeChange = (size: number) => {
    // 防止 el-pagination 挂载/更新时误触发重复请求
    if (size === query.page_size) return
    query.page_size = size
    query.page = 1
    loadEquipments()
}

const handlePageChange = (page: number) => {
    // 防止 el-pagination 挂载/更新时误触发重复请求
    if (page === query.page) return
    query.page = page
    loadEquipments()
}

// ==================== 状态切换 ====================
const handleStatusChange = async (row: EquipmentInfo, val: number) => {
    try {
        await updateEquipment(row.id, { status: val })
        row.status = val
        ElMessage.success(val === 1 ? '已标记为正常' : '已标记为维修')
    } catch (error) {
        console.log('更新设备状态失败', error)
    }
}

// ==================== 新增/编辑弹窗 ====================
const dialogVisible = ref(false)
const dialogMode = ref<'add' | 'edit'>('add')
const editingId = ref<number>(0)

const formRef = ref<InstanceType<typeof ElForm>>()
const form = reactive<EquipmentCreateRequest>({
    lab_id: undefined as unknown as number,
    name: '',
    description: '',
    img: '',
    spec: '',
    quantity: 1,
    status: 1,
})

const formRules = reactive({
    name: [{ required: true, message: '请输入设备名称', trigger: 'blur' }],
    lab_id: [{ required: true, message: '请选择所属实验室', trigger: 'change' }],
    quantity: [{ required: true, message: '请输入数量', trigger: 'blur' }],
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

const openEditDialog = (row: EquipmentInfo) => {
    dialogMode.value = 'edit'
    editingId.value = row.id
    form.name = row.name
    form.lab_id = row.lab_id
    form.description = row.description || ''
    form.img = row.img || ''
    form.spec = row.spec || ''
    form.quantity = row.quantity
    form.status = row.status
    dialogVisible.value = true
}

const resetForm = () => {
    form.name = ''
    form.lab_id = undefined as unknown as number
    form.description = ''
    form.img = ''
    form.spec = ''
    form.quantity = 1
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
            await addEquipment(form)
            ElMessage.success('新增设备成功')
        } else {
            await updateEquipment(editingId.value, form)
            ElMessage.success('更新设备成功')
        }
        dialogVisible.value = false
        loadEquipments()
    } catch (error) {
        console.log('提交设备表单失败', error)
    } finally {
        submitting.value = false
    }
}

// ==================== 删除 ====================
const handleDelete = (row: EquipmentInfo) => {
    ElMessageBox.confirm(`确定删除设备「${row.name}」吗？删除后不可恢复。`, '删除确认', {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning',
    }).then(async () => {
        try {
            await deleteEquipment(row.id)
            ElMessage.success('删除成功')
            loadEquipments()
        } catch (error) {
            console.log('删除设备失败', error)
        }
    }).catch(() => { })
}

onMounted(() => {
    loadLabOptions()
    loadEquipments()
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
