<template>
    <el-dialog v-model="visible" :title="equipment ? `预约设备: ${equipment.name}` : `预约实验室: ${lab?.name}`"
        width="480px" @closed="resetForm">
        <el-form ref="formRef" :model="form" :rules="formRules" label-width="80px">
            <el-form-item label="实验室">
                <el-input :model-value="lab?.name" disabled />
            </el-form-item>
            <el-form-item v-if="equipment" label="设备">
                <el-input :model-value="equipment.name" disabled />
            </el-form-item>
            <el-form-item prop="date" label="日期">
                <el-date-picker v-model="form.date" type="date" placeholder="选择预约日期"
                    :disabled-date="disabledPastDate" value-format="YYYY-MM-DD" style="width: 100%;" />
            </el-form-item>
            <el-form-item prop="start_time" label="开始时间">
                <el-time-select v-model="form.start_time" :max-time="form.end_time || lab?.close_time"
                    :start="lab?.open_time || '08:00'" :end="lab?.close_time || '20:00'" step="00:30"
                    placeholder="开始时间" style="width: 100%;" />
            </el-form-item>
            <el-form-item prop="end_time" label="结束时间">
                <el-time-select v-model="form.end_time" :min-time="form.start_time"
                    :start="lab?.open_time || '08:00'" :end="lab?.close_time || '20:00'" step="00:30"
                    placeholder="结束时间" style="width: 100%;" />
            </el-form-item>
            <el-form-item label="开放时间">
                <span style="color: var(--el-text-color-secondary); font-size: 13px;">
                    实验室开放: {{ lab?.open_time }} - {{ lab?.close_time }}
                </span>
            </el-form-item>
            <el-form-item prop="remark" label="备注">
                <el-input v-model="form.remark" type="textarea" :rows="3" placeholder="备注(选填)" />
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="visible = false">取消</el-button>
            <el-button type="primary" :loading="submitting" @click="submitForm">提交预约</el-button>
        </template>
    </el-dialog>
</template>
<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElForm, ElMessage } from 'element-plus'
import { addReservation } from '@/api/reservation'
import type { LabInfo } from '@/api/lab'
import type { EquipmentInfo } from '@/api/equipment'

const props = defineProps<{
    lab: LabInfo | null
    equipment?: EquipmentInfo | null
}>()
const emit = defineEmits<{
    (e: 'success'): void
}>()

const visible = ref(false)
const submitting = ref(false)
const formRef = ref<InstanceType<typeof ElForm>>()

const form = reactive({
    date: '',
    start_time: '',
    end_time: '',
    remark: '',
})

const formRules = reactive({
    date: [{ required: true, message: '请选择预约日期', trigger: 'change' }],
    start_time: [{ required: true, message: '请选择开始时间', trigger: 'change' }],
    end_time: [{ required: true, message: '请选择结束时间', trigger: 'change' }],
})

// 禁止选择今天之前的日期
const disabledPastDate = (d: Date) => {
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    return d.getTime() < today.getTime()
}

const open = () => {
    visible.value = true
}

const resetForm = () => {
    form.date = ''
    form.start_time = ''
    form.end_time = ''
    form.remark = ''
    formRef.value?.clearValidate()
}

const submitForm = async () => {
    if (!formRef.value || !props.lab) return
    const valid = await (formRef.value as unknown as {
        validate: () => Promise<boolean>
    })!.validate().catch(() => false)
    if (!valid) return

    try {
        submitting.value = true
        await addReservation({
            lab_id: props.lab.id,
            equipment_id: props.equipment?.id ?? null,
            date: form.date,
            start_time: form.start_time,
            end_time: form.end_time,
            remark: form.remark || undefined,
        })
        ElMessage.success('预约提交成功, 请等待审核')
        visible.value = false
        emit('success')
    } catch (error) {
        console.log('提交预约失败', error)
    } finally {
        submitting.value = false
    }
}

defineExpose({ open })
</script>
