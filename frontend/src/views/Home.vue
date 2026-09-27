<template>
    <div class="common-layout">
        <el-container style="min-height: 100vh;">
            {{ userInfo?.username }}
        </el-container>
    </div>
</template>
<script setup lang="ts">
import { useUser } from '@/utils/user'
const { userInfo } = useUser()
</script>
<style scoped></style>
