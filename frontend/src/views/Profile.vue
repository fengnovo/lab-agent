<template>
    <div class="common-layout">
        <el-card style="width: 100%; margin: 0 auto;">
            <template #header>
                <span>用户信息</span>
            </template>
            <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
                <el-form-item prop="username" label="用户名">
                    <el-input size="large" v-model="form.username" placeholder="请输入用户名"></el-input>
                </el-form-item>
                <el-form-item prop="role" label="角色" :disabled="true">
                    <el-input size="large" v-model="form.role" placeholder="请输入角色" disabled></el-input>
                </el-form-item>
                <el-form-item prop="name" label="名称">
                    <el-input size="large" v-model="form.name" placeholder="请输入名称"></el-input>
                </el-form-item>
                <el-form-item prop="phone" label="手机号">
                    <el-input size="large" v-model="form.phone" maxlength="11" placeholder="请输入手机号"></el-input>
                </el-form-item>
                <el-form-item prop="email" label="邮箱">
                    <el-input size="large" v-model="form.email" placeholder="请输入邮箱"></el-input>
                </el-form-item>
                <el-form-item prop="avatar" label="头像">
                    <el-upload class="avatar-uploader" :view-file-list="true" :accept="'image/*'"
                        :action="uploadAvatarUrl" :show-file-list="true" :auto-upload="true"
                        :on-success="handleAvatarSuccess">
                        <el-avatar :size="100" v-if="form.avatar" :src="form.avatar" class="avatar" />
                        <el-icon v-else class="avatar-uploader-icon">
                            <Plus />
                        </el-icon>
                    </el-upload>
                </el-form-item>
            </el-form>
            <el-button class="profile-form-button" type="primary" size="large" :loading="loading"
                @click="submitForm">提交</el-button>
        </el-card>
    </div>
</template>
<script setup lang="ts">
import { ElMessage, ElForm } from 'element-plus'
import { reactive, ref, onMounted } from 'vue'
import { type UserResponse } from '@/utils/user'
import { type UserInfo, setUserInfo } from '@/utils/auth'
import { useUser } from '@/utils/user'
import { getUserInfo, updateUserUserInfo } from '@/api/user'

const loading = ref(false)
const { reloadUserInfo, updateUserInfo } = useUser()
const form = reactive({
    username: '',
    role: '',
    name: '',
    phone: '',
    email: '',
    avatar: '',
})

const rules = reactive({
    username: [{ required: false, message: '请输入用户名', trigger: 'blur' }],
    name: [{ required: false, message: '请输入名字', trigger: 'blur' }],
    phone: [{ required: false, pattern: /^1[3456789]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }],
    email: [{ required: false, pattern: /^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*$/, message: '请输入正确的邮箱', trigger: 'blur' }],
})

const formRef = ref<InstanceType<typeof ElForm>>()

const submitForm = async () => {
    if (!formRef.value) return

    const valid = await (formRef.value as unknown as {
        validate: () => Promise<boolean>
    })!.validate().catch(() => false)
    console.log('提交表单验证结果:', valid, form)
    if (!valid) return

    try {
        loading.value = true
        const res = await updateUserUserInfo(form as unknown as UserResponse)
        console.log('更新用户信息结果:', res)
        if (res.code === 200) {
            ElMessage.success('更新用户信息成功')
            if (res.data) {
                setUserInfo(res.data)
                updateUserInfo(res.data)
                reloadUserInfo()
            }
        }
    } catch (error) {
        console.log('更新用户信息失败', error)
    } finally {
        loading.value = false
    }
}

const uploadAvatarUrl = '/api/files/upload'

const handleAvatarSuccess = (res: { code: number, msg: string, data: { url: string } }, file: any) => {
    console.log('上传头像成功:', res, file)
    if (res.code !== 200 || !res.data?.url) {
        ElMessage.error(res.msg)
        return
    }
    form.avatar = res.data.url
}

onMounted(async () => {
    formRef.value?.resetFields()
    const res: UserInfo = await getUserInfo() as UserInfo
    form.username = res.username
    form.role = res.role
    form.name = res.name
    form.phone = res.phone
    form.email = res.email
    form.avatar = res.avatar
})

</script>
<style scoped>
.profile-form-button {
    width: 100%;
}
</style>
