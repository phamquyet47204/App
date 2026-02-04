<template>
  <div class="courses-page">
    <h1>Danh sách môn học</h1>

    <div v-if="!isRegistrationOpen" class="alert-warning">
      <div class="alert-icon">🔒</div>
      <div class="alert-content">
        <strong>Kỳ đăng ký chưa mở</strong>
        <p>Hệ thống không cho phép đăng ký lúc này. Bạn vẫn có thể xem danh sách môn học.</p>
      </div>
    </div>

    <div v-else-if="courseStore.activePeriod?.period" class="alert-success">
      <div class="alert-icon">✅</div>
      <div class="alert-content">
        <strong>Đang trong kỳ đăng ký: {{ courseStore.activePeriod.period.name }}</strong>
        <p>Kết thúc: {{ formatDate(courseStore.activePeriod.period.end_date) }}</p>
      </div>
    </div>

    <div v-if="courseStore.isLoading" class="loading">
      Đang tải dữ liệu...
    </div>

    <div v-else class="courses-grid">
      <div
        v-for="course in courseStore.courses"
        :key="course.id"
        class="course-card"
      >
        <div class="course-header">
          <h3>{{ course.code }}</h3>
          <span class="semester">Kỳ {{ course.semester }}</span>
        </div>

        <h2>{{ course.name }}</h2>

        <div class="course-info">
          <p><strong>Giáo viên:</strong> {{ course.lecturer }}</p>
          <p><strong>Số tín chỉ:</strong> {{ course.credits }}</p>
          <p><strong>Lịch học:</strong> {{ course.schedule }}</p>
          <p v-if="course.description">{{ course.description }}</p>
        </div>

        <div class="capacity-info">
          <div class="capacity-bar">
            <div
              class="capacity-fill"
              :style="{ width: capacityPercent(course) + '%' }"
            ></div>
          </div>
          <p class="capacity-text">
            {{ course.enrolled_count }} / {{ course.capacity }}
          </p>
        </div>

        <button
          v-if="!course.is_registered && isRegistrationOpen"
          @click="register(course.id)"
          class="btn btn-register"
          :disabled="course.available_spots <= 0"
        >
          {{ course.available_spots <= 0 ? 'Hết chỗ' : 'Đăng ký' }}
        </button>

        <button
          v-else-if="course.is_registered && isRegistrationOpen"
          @click="cancel(course.id)"
          class="btn btn-cancel"
        >
          Huỷ đăng ký
        </button>

        <button v-else class="btn btn-disabled" disabled>
          {{ course.is_registered ? 'Đã đăng ký' : 'Chưa mở đăng ký' }}
        </button>
      </div>
    </div>

    <div v-if="!courseStore.isLoading && courseStore.courses.length === 0" class="no-courses">
      Không có môn học nào
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, computed } from 'vue'
import { useCourseStore } from '@/stores/courseStore'

const courseStore = useCourseStore()

const isRegistrationOpen = computed(() => {
  return courseStore.activePeriod?.is_open === true
})

let refreshTimer = null

const refreshStatus = async () => {
  await courseStore.fetchActivePeriod()
}

onMounted(async () => {
  await refreshStatus()
  await courseStore.fetchCourses()
  refreshTimer = setInterval(refreshStatus, 30000)
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('vi-VN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const capacityPercent = (course) => {
  return (course.enrolled_count / course.capacity) * 100
}

const register = async (courseId) => {
  try {
    await courseStore.registerCourse(courseId)
    alert('Đăng ký thành công')
  } catch (error) {
    alert(error.error || 'Lỗi đăng ký')
  }
}

const cancel = async (courseId) => {
  if (confirm('Bạn chắc chắn muốn huỷ đăng ký?')) {
    try {
      await courseStore.cancelCourse(courseId)
      alert('Huỷ đăng ký thành công')
    } catch (error) {
      alert(error.error || 'Lỗi huỷ đăng ký')
    }
  }
}
</script>

<style scoped>
.courses-page {
  padding: 2rem 0;
}

.courses-page h1 {
  margin-bottom: 2rem;
}

.alert-warning {
  display: flex;
  align-items: center;
  gap: 1rem;
  background-color: #fff3cd;
  border: 2px solid #ffeaa7;
  color: #856404;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.alert-success {
  display: flex;
  align-items: center;
  gap: 1rem;
  background-color: #d4edda;
  border: 2px solid #c3e6cb;
  color: #155724;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.alert-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.alert-content {
  flex: 1;
}

.alert-content strong {
  display: block;
  font-size: 1.1rem;
  margin-bottom: 0.25rem;
}

.alert-content p {
  margin: 0;
  font-size: 0.95rem;
  opacity: 0.9;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.course-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  padding: 1.5rem;
  transition: transform 0.3s, box-shadow 0.3s;
}

.course-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}

.course-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 0.5rem;
}

.course-header h3 {
  margin: 0;
  color: #667eea;
  font-size: 1.1rem;
}

.semester {
  background-color: #f0f0f0;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  color: #666;
}

.course-card h2 {
  margin: 0.5rem 0 1rem 0;
  font-size: 1.3rem;
  color: #333;
}

.course-info {
  margin-bottom: 1rem;
}

.course-info p {
  margin: 0.5rem 0;
  font-size: 0.9rem;
  color: #666;
}

.capacity-info {
  margin: 1rem 0;
}

.capacity-bar {
  width: 100%;
  height: 8px;
  background-color: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.capacity-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transition: width 0.3s;
}

.capacity-text {
  font-size: 0.85rem;
  color: #666;
  margin: 0;
}

.btn {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
}

.btn-register {
  background: linear-gradient(135deg, #51cf66, #37b24d);
  color: white;
}

.btn-register:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(81, 207, 102, 0.3);
}

.btn-register:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-cancel {
  background-color: #ff6b6b;
  color: white;
}

.btn-cancel:hover {
  background-color: #ff5252;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(255, 107, 107, 0.3);
}

.btn-disabled {
  background-color: #e0e0e0;
  color: #999;
  cursor: not-allowed;
}

.no-courses {
  text-align: center;
  padding: 2rem;
  color: #999;
}
</style>
