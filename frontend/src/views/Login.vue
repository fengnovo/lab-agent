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
                        还没有账号？请<a href="/register" style="color: #409eff;">请注册账号</a>
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
    loading.value = true
    if (!formRef.value) {
        return
    }
    try {
        const success = await formRef.value.validate()
        console.log(form.value)

        if (success) {
            ElMessage.success('登录成功')
            loading.value = false
            router.push('/')
        }
    } catch (error) {
        ElMessage.error('登录失败，请检查用户名和密码')
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
