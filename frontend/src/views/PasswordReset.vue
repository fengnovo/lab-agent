<template>
    <div class="common-layout">
        <el-card style="width: 100%; margin: 0 auto;">
            <template #header>
                <span>用户信息</span>
            </template>
            <el-form :model="form" :rules="rules" ref="formRef" label-width="140px">
                <el-form-item prop="old_password" label="旧密码">
                    <el-input size="large" v-model="form.old_password" type="password" placeholder="请输入旧密码"></el-input>
                </el-form-item>
                <el-form-item prop="new_password" label="新密码">
                    <el-input size="large" v-model="form.new_password" type="password" placeholder="请输入新密码"></el-input>
                </el-form-item>
                <el-form-item prop="confirm_password" label="确认新密码">
                    <el-input size="large" v-model="form.confirm_password" type="password"
                        placeholder="请输入确认新密码"></el-input>
                </el-form-item>
            </el-form>
            <el-button class="password-reset-form-button" type="primary" size="large" :loading="loading"
                @click="submitForm">重置密码</el-button>
        </el-card>
    </div>
</template>
<script setup lang="ts">
import { ElMessage, ElForm } from 'element-plus'
import { reactive, ref } from 'vue'
import { resetPasswordUserInfo } from '@/api/user'

const loading = ref(false)

const form = reactive({
    old_password: '',
    new_password: '',
    confirm_password: '',
})

const rules = reactive({
    old_password: [{ required: true, message: '请输入旧密码', trigger: 'blur' }],
    new_password: [{ required: true, message: '请输入新密码', trigger: 'blur' }],
    confirm_password: [{
        required: true,
        validator: (rule: any, value: string, callback: any) => {
            if (!value) {
                callback(new Error('请输入确认新密码'))
                return
            }
            if (value !== form.new_password) {
                callback(new Error('确认新密码与新密码不一致'))
            } else {
                callback()
            }
        }, trigger: 'blur'
    }],
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
        const res = await resetPasswordUserInfo(form)
        console.log('重置密码结果:', res)
        if (res.code === 200) {
            ElMessage.success('重置密码成功')
        }
    } catch (error) {
        console.log('重置密码失败', error)
    } finally {
        loading.value = false
    }
}
</script>
<style scoped>
.password-reset-form-button {
    width: 100%;
}
</style>
