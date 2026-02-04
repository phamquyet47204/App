<template>
  <div class="dashboard">
    <div class="welcome-section">
      <h1>Chào mừng, {{ authStore.user?.full_name }}!</h1>
      <p class="mssv">MSSV: {{ authStore.user?.mssv }}</p>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <h3>Môn học đã đăng ký</h3>
        <p class="stat-number">{{ courseStore.myRegistrations.length }}</p>
      </div>

      <div class="stat-card">
        <h3>Tổng môn học</h3>
        <p class="stat-number">{{ courseStore.courses.length }}</p>
      </div>

      <div class="stat-card">
        <h3>Khoảng đăng ký</h3>
        <p class="stat-status" :class="{ active: isRegistrationOpen }">
          {{ isRegistrationOpen ? 'Đang mở' : 'Đóng' }}
        </p>
      </div>
    </div>

    <div class="action-section">
      <h2>Trang chủ</h2>
      <div class="action-buttons">
        <router-link to="/courses" class="btn btn-primary">
          Xem tất cả môn học
        </router-link>
        <router-link to="/my-courses" class="btn btn-secondary">
          Xem môn của tôi
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useCourseStore } from '@/stores/courseStore'

const authStore = useAuthStore()
const courseStore = useCourseStore()

const isRegistrationOpen = computed(() => {
  return courseStore.activePeriod?.is_open === true
})

onMounted(async () => {
  await courseStore.fetchCourses()
  await courseStore.fetchMyRegistrations()
  await courseStore.fetchActivePeriod()
})
</script>

<style scoped>
.dashboard {
  padding: 2rem 0;
}

.welcome-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.welcome-section h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
}

.mssv {
  margin: 0;
  opacity: 0.9;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  text-align: center;
}

.stat-card h3 {
  color: #666;
  margin: 0 0 1rem 0;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-number {
  margin: 0;
  font-size: 2.5rem;
  color: #667eea;
  font-weight: bold;
}

.stat-status {
  margin: 0;
  font-size: 1.5rem;
  color: #ff6b6b;
  font-weight: bold;
}

.stat-status.active {
  color: #51cf66;
}

.action-section h2 {
  margin-bottom: 1.5rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  display: inline-block;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-secondary {
  background-color: #f0f0f0;
  color: #333;
}

.btn-secondary:hover {
  background-color: #e0e0e0;
}
</style>
