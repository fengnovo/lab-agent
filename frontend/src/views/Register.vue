<template>
    <div class="register-container">
        <div class="register-form">
            <h1 class="register-form-title">实验室智能预约系统注册</h1>
            <el-form :model="form" :rules="rules" ref="formRef">
                <el-form-item prop="username">
                    <el-input size="large" v-model="form.username" placeholder="请输入用户名" prefix-icon="User"></el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input size="large" v-model="form.password" type="password" placeholder="请输入密码" show-password
                        prefix-icon="Lock"></el-input>
                </el-form-item>
                <el-form-item prop="confirmPassword">
                    <el-input size="large" v-model="form.confirmPassword" type="password" placeholder="请确认密码"
                        show-password prefix-icon="Lock"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button class="register-form-button" type="primary" size="large" :loading="loading"
                        @click="submitForm">注册</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import router from '@/router'
import { register } from '@/api/auth'

const form = ref({
    username: '',
    password: '',
    confirmPassword: ''
})

const loading = ref(false)
const formRef = ref(null)

const validateConfirmPassword = (rule: any, value: string, callback: any) => {
    if (!value) {
        callback(new Error('请输入确认密码'))
    } else {
        if (value !== form.value.password) {
            callback(new Error('两次输入密码不一致'))
        }
        callback()
    }
}

const rules = ref({
    username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
    ],
    password: [
        { required: true, message: '请输入密码', trigger: 'blur' }
    ],
    confirmPassword: [
        { validator: validateConfirmPassword, trigger: 'blur' }
    ]
})

const submitForm = async () => {
    if (!formRef.value) return

    const valid = await (formRef.value as unknown as {
        validate: () => Promise<boolean>
    })!.validate().catch(() => false)
    console.log('注册表单验证结果:', valid, form.value)
    if (!valid) return

    try {
        loading.value = true
        const res = await register(form.value)
        console.log('注册结果:', res)
        if (res.code === 200) {
            ElMessage.success('注册成功')
            router.push('/login')
        }
    } catch (error) {
        console.log('注册失败', error)
        loading.value = false
    }
}
</script>
<style scoped>
.register-form-title {
    text-align: center;
    margin-bottom: 20px;
}

.register-container {
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.register-form {
    width: 400px;
    height: 340px;
    background-color: #fff;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.register-form h1 {
    text-align: center;
    margin-bottom: 30px;
}

.register-form-button {
    width: 100%;
}

.register-form-register {
    float: right;
}
</style>
