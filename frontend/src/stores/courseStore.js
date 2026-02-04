import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/utils/api'

export const useCourseStore = defineStore('course', () => {
  const courses = ref([])
  const myRegistrations = ref([])
  const isLoading = ref(false)
  const activePeriod = ref(null)

  const fetchCourses = async () => {
    isLoading.value = true
    try {
      const response = await api.get('/courses/')
      courses.value = response.data.results || response.data
      return courses.value
    } catch (error) {
      throw error.response?.data || error
    } finally {
      isLoading.value = false
    }
  }

  const fetchMyRegistrations = async () => {
    isLoading.value = true
    try {
      const response = await api.get('/registrations/my_courses/')
      myRegistrations.value = response.data.results || response.data
      return myRegistrations.value
    } catch (error) {
      throw error.response?.data || error
    } finally {
      isLoading.value = false
    }
  }

  const registerCourse = async (courseId) => {
    try {
      const response = await api.post('/registrations/register/', { course_id: courseId })
      await fetchCourses()
      await fetchMyRegistrations()
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  }

  const cancelCourse = async (courseId) => {
    try {
      const response = await api.post('/registrations/cancel/', { course_id: courseId })
      await fetchCourses()
      await fetchMyRegistrations()
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  }

  const fetchActivePeriod = async () => {
    try {
      const response = await api.get('/periods/active_period/')
      activePeriod.value = response.data
      return activePeriod.value
    } catch (error) {
      activePeriod.value = null
      return null
    }
  }

  return {
    courses,
    myRegistrations,
    isLoading,
    activePeriod,
    fetchCourses,
    fetchMyRegistrations,
    registerCourse,
    cancelCourse,
    fetchActivePeriod
  }
})
