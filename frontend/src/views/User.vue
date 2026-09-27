<template>
    <div class="common-layout">
        <el-card style="width: 100%; margin: 0 auto;">
            <!-- 搜索栏 -->
            <div class="toolbar">
                <el-input v-model="query.keyword" placeholder="搜索用户名/姓名/手机号/邮箱" clearable style="width: 260px"
                    @keyup.enter="handleSearch" @clear="handleSearch">
                    <template #prefix>
                        <el-icon>
                            <Search />
                        </el-icon>
                    </template>
                </el-input>
                <el-button type="primary" @click="handleSearch">查询</el-button>
                <el-button type="success" @click="openAddDialog">新增用户</el-button>
            </div>

            <!-- 用户表格 -->
            <el-table :data="userList" v-loading="loading" stripe border style="width: 100%">
                <el-table-column prop="id" label="ID" width="70" align="center" />
                <el-table-column label="头像" width="80" align="center">
                    <template #default="{ row }">
                        <el-avatar :size="40" :src="row.avatar">
                            <el-icon>
                                <User />
                            </el-icon>
                        </el-avatar>
                    </template>
                </el-table-column>
                <el-table-column prop="username" label="用户名" min-width="120" />
                <el-table-column prop="name" label="姓名" min-width="100" />
                <el-table-column label="角色" width="100" align="center">
                    <template #default="{ row }">
                        <el-tag :type="row.role === 'admin' ? 'warning' : 'primary'">
                            {{ row.role === 'admin' ? '管理员' : '学生' }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="phone" label="手机号" min-width="130">
                    <template #default="{ row }">{{ row.phone || '-' }}</template>
                </el-table-column>
                <el-table-column prop="email" label="邮箱" min-width="180">
                    <template #default="{ row }">{{ row.email || '-' }}</template>
                </el-table-column>
                <el-table-column label="状态" width="90" align="center">
                    <template #default="{ row }">
                        <el-switch :model-value="row.status" :active-value="1" :inactive-value="0"
                            :disabled="row.id === currentUserId"
                            @change="(val: number) => handleStatusChange(row, val)" />
                    </template>
                </el-table-column>
                <el-table-column label="创建时间" width="120" align="center">
                    <template #default="{ row }">{{ row.created_at?.slice(0, 10) }}</template>
                </el-table-column>
                <el-table-column label="操作" width="150" align="center" fixed="right">
                    <template #default="{ row }">
                        <el-button type="primary" link @click="openEditDialog(row)">编辑</el-button>
                        <el-button type="danger" link :disabled="row.id === currentUserId"
                            @click="handleDelete(row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>

            <!-- 分页 -->
            <el-pagination class="pagination" :current-page="query.page" :page-size="query.page_size" :total="total"
                :page-sizes="[5, 10, 20, 50]" layout="total, sizes, prev, pager, next, jumper"
                @current-change="handlePageChange" @size-change="handleSizeChange" />
        </el-card>

        <!-- 新增/编辑用户弹窗 -->
        <el-dialog v-model="dialogVisible" :title="dialogMode === 'add' ? '新增用户' : '编辑用户'" width="500px"
            @closed="resetForm">
            <el-form ref="formRef" :model="form" :rules="formRules" label-width="80px">
                <el-form-item prop="username" label="用户名">
                    <el-input v-model="form.username" placeholder="请输入用户名" :disabled="dialogMode === 'edit'" />
                </el-form-item>
                <el-form-item prop="password" label="密码">
                    <el-input v-model="form.password" type="password" show-password
                        :placeholder="dialogMode === 'add' ? '请输入密码' : '不修改请留空'" />
                </el-form-item>
                <el-form-item prop="name" label="姓名">
                    <el-input v-model="form.name" placeholder="请输入姓名" />
                </el-form-item>
                <el-form-item prop="role" label="角色">
                    <el-select v-model="form.role" placeholder="请选择角色" style="width: 100%;">
                        <el-option label="学生" value="student" />
                        <el-option label="管理员" value="admin" />
                    </el-select>
                </el-form-item>
                <el-form-item prop="phone" label="手机号">
                    <el-input v-model="form.phone" placeholder="请输入手机号" />
                </el-form-item>
                <el-form-item prop="email" label="邮箱">
                    <el-input v-model="form.email" placeholder="请输入邮箱" />
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
    pageUsers,
    addUser,
    adminUpdateUser,
    deleteUser,
    getUserInfo,
    type UserPageQuery,
    type UserCreateRequest,
} from '@/api/user'
import { type UserInfo } from '@/utils/auth'

const loading = ref(false)
const submitting = ref(false)
const userList = ref<UserInfo[]>([])
const total = ref(0)
const currentUserId = ref<number>(0)

const query = reactive<UserPageQuery>({
    page: 1,
    page_size: 10,
    keyword: '',
})

// ==================== 列表加载 ====================
const loadUsers = async () => {
    loading.value = true
    try {
        const res = await pageUsers(query)
        userList.value = res.list
        total.value = res.total
    } catch (error) {
        console.log('查询用户列表失败', error)
    } finally {
        loading.value = false
    }
}

const handleSearch = () => {
    query.page = 1
    loadUsers()
}

const handleSizeChange = (size: number) => {
    // 防止 el-pagination 挂载/更新时误触发重复请求
    if (size === query.page_size) return
    query.page_size = size
    query.page = 1
    loadUsers()
}

const handlePageChange = (page: number) => {
    // 防止 el-pagination 挂载/更新时误触发重复请求
    if (page === query.page) return
    query.page = page
    loadUsers()
}

// ==================== 新增/编辑弹窗 ====================
const dialogVisible = ref(false)
const dialogMode = ref<'add' | 'edit'>('add')
const editingId = ref<number>(0)

const formRef = ref<InstanceType<typeof ElForm>>()
const form = reactive<UserCreateRequest>({
    username: '',
    password: '',
    name: '',
    role: 'student',
    phone: '',
    email: '',
})

const formRules = reactive({
    username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
    password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
    name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
    role: [{ required: true, message: '请选择角色', trigger: 'change' }],
})

const openAddDialog = () => {
    dialogMode.value = 'add'
    dialogVisible.value = true
}

const openEditDialog = (row: UserInfo) => {
    dialogMode.value = 'edit'
    editingId.value = row.id
    form.username = row.username
    form.password = ''
    form.name = row.name
    form.role = row.role
    form.phone = row.phone || ''
    form.email = row.email || ''
    dialogVisible.value = true
}

const resetForm = () => {
    form.username = ''
    form.password = ''
    form.name = ''
    form.role = 'student'
    form.phone = ''
    form.email = ''
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
            await addUser(form)
            ElMessage.success('新增用户成功')
        } else {
            // 编辑时密码留空则不修改
            await adminUpdateUser(editingId.value, {
                name: form.name,
                role: form.role,
                phone: form.phone || undefined,
                email: form.email || undefined,
                password: form.password || undefined,
            })
            ElMessage.success('更新用户成功')
        }
        dialogVisible.value = false
        loadUsers()
    } catch (error) {
        console.log('提交用户表单失败', error)
    } finally {
        submitting.value = false
    }
}

// ==================== 状态切换/删除 ====================
const handleStatusChange = async (row: UserInfo, val: number) => {
    try {
        await adminUpdateUser(row.id, { status: val })
        row.status = val
        ElMessage.success(val === 1 ? '已启用' : '已禁用')
    } catch (error) {
        console.log('更新用户状态失败', error)
    }
}

const handleDelete = (row: UserInfo) => {
    ElMessageBox.confirm(`确定删除用户「${row.username}」吗？删除后不可恢复。`, '删除确认', {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning',
    }).then(async () => {
        try {
            await deleteUser(row.id)
            ElMessage.success('删除成功')
            loadUsers()
        } catch (error) {
            console.log('删除用户失败', error)
        }
    }).catch(() => { })
}

onMounted(async () => {
    // 获取当前登录用户信息, 用于禁止操作自己的账号
    try {
        const me = await getUserInfo()
        currentUserId.value = me.id
    } catch (error) {
        console.log('获取当前用户信息失败', error)
    }
    loadUsers()
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
</style>
