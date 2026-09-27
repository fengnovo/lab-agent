<template>
    <div class="login-container">
        <div class="login-form">
            <h1 class="login-form-title">实验室智能预约系统</h1>
            <el-form :model="form" :rules="rules" ref="formRef">
                <el-form-item prop="username">
                    <el-input size="large" v-model="form.username" placeholder="请输入用户名" prefix-icon="User"></el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input size="large" v-model="form.password" type="password" placeholder="请输入密码" show-password
                        prefix-icon="Lock"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button class="login-form-button" type="primary" size="large" :loading="loading"
                        @click="submitForm">登录</el-button>
                    <div class="login-form-register">
                        还没有账号？请<router-link to="/register" style="color: #409eff;">请注册账号</router-link>
                    </div>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import router from '@/router'
import { login } from '@/api/auth'
import { useUser } from '@/utils/user'

const { saveUserInfo } = useUser()

const form = ref({
    username: '',
    password: ''
})

const loading = ref(false)
const formRef = ref(null)

const rules = ref({
    username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
    ],
    password: [
        { required: true, message: '请输入密码', trigger: 'blur' }
    ]
})

const submitForm = async () => {
    if (!formRef.value) return

    const valid = await (formRef.value as unknown as {
        validate: () => Promise<boolean>
    })!.validate().catch(() => false)
    console.log('登录表单验证结果:', valid, form.value)
    if (!valid) return

    try {
        loading.value = true
        const response = await login(form.value)
        if (response) {
            saveUserInfo(response)
            ElMessage.success('登录成功')
            router.push('/manager/home')
        }
    } finally {
        loading.value = false
    }
}
</script>
<style scoped>
.login-form-title {
    text-align: center;
    margin-bottom: 20px;
}

.login-container {
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.login-form {
    width: 400px;
    height: 340px;
    background-color: #fff;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.login-form h1 {
    text-align: center;
    margin-bottom: 30px;
}

.login-form-button {
    width: 100%;
}

.login-form-register {
    float: right;
}
</style>
