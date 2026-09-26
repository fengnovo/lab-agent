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

const form = ref({
    username: '',
    password: '',
    confirmPassword: ''
})

const loading = ref(false)
const formRef = ref(null)

const rules = ref({
    username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
    ],
    password: [
        { required: true, message: '请输入密码', trigger: 'blur' }
    ],
    confirmPassword: [
        { required: true, message: '请确认密码', trigger: 'blur' }
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
            console.log('注册成功')
            loading.value = false
            router.push('/')
        }
    } catch (error) {
        console.log('注册失败', error)
        ElMessage.error('注册失败')
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
