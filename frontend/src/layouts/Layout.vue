<template>
    <div>
        <el-container style="height: 100vh; overflow: hidden;">
            <el-header style="display: flex; align-items: center; border-bottom: 1px solid #e4e7ed; padding: 0;
            justify-content: space-between;">
                <div
                    style="font-size: 20px; width: 100%; height: 100%; font-weight: bold; text-align: center;   
                    line-height: 60px; background-color: #fff; display: flex; align-items: center;  padding-left: 20px;">
                    <img src="@/assets/images/lab-icon.png" alt="logo"
                        style="width: 60px; height: 60px; margin-right: 10px;">
                    <span>实验室智能预约系统</span>
                </div>
                <div
                    style="width: 100%; height: 100%; font-weight: bold; text-align: center;  padding-right: 20px;
                    line-height: 60px; background-color: #fff; display: flex; align-items: center; justify-content: end;">
                    <el-dropdown>
                        <div style="display: flex; align-items: center; cursor: pointer;">
                            <el-avatar :size="30" :src="userInfo.avatar" />
                            <span style="margin-left: 10px;">{{ userInfo.username }}</span>
                        </div>
                        <template #dropdown>
                            <el-dropdown-item @click="handleProfile">个人信息</el-dropdown-item>
                            <el-dropdown-item @click="handlePasswordReset">重置密码</el-dropdown-item>
                            <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
                        </template>
                    </el-dropdown>
                </div>
            </el-header>
            <el-container style="min-height: 0;">
                <el-aside width="220px">
                    <el-menu router :default-active="$route.path" style="height: 100%;">
                        <el-menu-item index="/manager/home">
                            <el-icon>
                                <Menu />
                            </el-icon>
                            <span>系统首页</span>
                        </el-menu-item>

                        <!-- student: 只读列表 -->
                        <el-menu-item index="/manager/lablist" v-if="!isAdmin">
                            <el-icon>
                                <OfficeBuilding />
                            </el-icon>
                            <span>实验室列表</span>
                        </el-menu-item>

                        <!-- admin: 管理页面 -->
                        <el-menu-item index="/manager/lab" v-if="isAdmin">
                            <el-icon>
                                <OfficeBuilding />
                            </el-icon>
                            <span>实验室管理</span>
                        </el-menu-item>
                        <el-menu-item index="/manager/equipment" v-if="isAdmin">
                            <el-icon>
                                <Setting />
                            </el-icon>
                            <span>实验室设备管理</span>
                        </el-menu-item>
                        <el-menu-item index="/manager/user" v-if="isAdmin">
                            <el-icon>
                                <User />
                            </el-icon>
                            <span>用户管理</span>
                        </el-menu-item>
                    </el-menu>
                </el-aside>
                <el-main style="padding: 0;">
                    <router-view></router-view>
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>
<script setup lang="ts">
import router from '@/router'
import { computed } from 'vue'
import { removeUserInfo, removeToken } from '@/utils/auth'
import { useUser } from '@/utils/user'

const { userInfo, reloadUserInfo } = useUser()

const isAdmin = computed(() => userInfo.value?.role === 'admin')

console.log(userInfo.value)

const handleLogout = () => {
    removeToken()
    removeUserInfo()
    reloadUserInfo()
    router.push('/login')
}

const handleProfile = () => {
    router.push('/manager/profile')
}

const handlePasswordReset = () => {
    router.push('/manager/password-reset')
}
</script>
<style scoped>
:deep(.el-tooltip__trigger) {
    outline: none;
}
</style>
