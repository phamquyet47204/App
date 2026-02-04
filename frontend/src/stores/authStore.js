import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/utils/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(null)
  const isLoading = ref(false)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.is_admin || false)

  const initFromStorage = () => {
    const storedToken = localStorage.getItem('token')
    const storedUser = localStorage.getItem('user')
    if (storedToken && storedUser) {
      token.value = storedToken
      user.value = JSON.parse(storedUser)
    }
  }

  const login = async (mssv, password) => {
    isLoading.value = true
    try {
      const response = await api.post('/login/student_login/', { mssv, password })
      token.value = response.data.token
      user.value = response.data.student
      localStorage.setItem('token', token.value)
      localStorage.setItem('user', JSON.stringify(user.value))
      return response.data
    } catch (error) {
      throw error.response?.data || error
    } finally {
      isLoading.value = false
    }
  }

  const adminLogin = async (mssv, password) => {
    isLoading.value = true
    try {
      const response = await api.post('/login/admin_login/', { mssv, password })
      token.value = response.data.token
      user.value = response.data.student
      localStorage.setItem('token', token.value)
      localStorage.setItem('user', JSON.stringify(user.value))
      return response.data
    } catch (error) {
      throw error.response?.data || error
    } finally {
      isLoading.value = false
    }
  }

  const logout = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  const changePassword = async (oldPassword, newPassword) => {
    try {
      const response = await api.post('/students/change_password/', {
        old_password: oldPassword,
        new_password: newPassword
      })
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  }

  return {
    user,
    token,
    isLoading,
    isAuthenticated,
    isAdmin,
    initFromStorage,
    login,
    adminLogin,
    logout,
    changePassword
  }
})
