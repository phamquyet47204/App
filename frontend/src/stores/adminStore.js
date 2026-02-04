import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/utils/api'

export const useAdminStore = defineStore('admin', () => {
  const periods = ref([])
  const isLoading = ref(false)

  const fetchPeriods = async () => {
    isLoading.value = true
    try {
      const response = await api.get('/periods/list_periods/')
      periods.value = response.data.results || response.data
      return periods.value
    } catch (error) {
      throw error.response?.data || error
    } finally {
      isLoading.value = false
    }
  }

  const createPeriod = async (periodData) => {
    try {
      const response = await api.post('/periods/create_period/', periodData)
      await fetchPeriods()
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  }

  const updatePeriod = async (periodData) => {
    try {
      const response = await api.put('/periods/update_period/', periodData)
      await fetchPeriods()
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  }

  return {
    periods,
    isLoading,
    fetchPeriods,
    createPeriod,
    updatePeriod
  }
})
