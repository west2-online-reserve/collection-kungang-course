import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
    const avatarUrl = ref<string>('')
    const userName = ref<string>('')
    const studentId = ref<string>('')

    const setUserInfo = (info: { avatarUrl?: string; name?: string; studentId?: string }) => {
        if (info.avatarUrl !== undefined) avatarUrl.value = info.avatarUrl
        if (info.name !== undefined) userName.value = info.name
        if (info.studentId !== undefined) studentId.value = info.studentId
    }

    const updateAvatar = (newAvatarUrl: string) => {
        avatarUrl.value = newAvatarUrl
    }

    const updateName = (newName: string) => {
        userName.value = newName
    }

    const clearUserInfo = () => {
        avatarUrl.value = ''
        userName.value = ''
        studentId.value = ''
    }

    return {
        avatarUrl,
        userName,
        studentId,
        setUserInfo,
        updateAvatar,
        updateName,
        clearUserInfo
    }
})
