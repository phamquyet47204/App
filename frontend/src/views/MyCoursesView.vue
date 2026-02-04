<template>
  <div class="my-courses-page">
    <h1>Môn học của tôi</h1>

    <div v-if="courseStore.isLoading" class="loading">
      Đang tải dữ liệu...
    </div>

    <div v-else-if="courseStore.myRegistrations.length === 0" class="no-courses">
      <p>Bạn chưa đăng ký môn học nào</p>
      <router-link to="/courses" class="btn btn-primary">
        Đi đến danh sách môn học
      </router-link>
    </div>

    <div v-else class="registrations-grid">
      <div
        v-for="registration in courseStore.myRegistrations"
        :key="registration.id"
        class="registration-card"
      >
        <div class="card-header">
          <h3>{{ registration.course_info.code }}</h3>
          <span class="status-badge">Đã đăng ký</span>
        </div>

        <h2>{{ registration.course_info.name }}</h2>

        <div class="course-details">
          <div class="detail-item">
            <span class="label">Giáo viên:</span>
            <span class="value">{{ registration.course_info.lecturer }}</span>
          </div>
          <div class="detail-item">
            <span class="label">Số tín chỉ:</span>
            <span class="value">{{ registration.course_info.credits }}</span>
          </div>
          <div class="detail-item">
            <span class="label">Lịch học:</span>
            <span class="value">{{ registration.course_info.schedule }}</span>
          </div>
          <div class="detail-item">
            <span class="label">Ngày đăng ký:</span>
            <span class="value">{{ formatDate(registration.registered_at) }}</span>
          </div>
        </div>

        <button
          @click="cancelRegistration(registration.course_info.id)"
          class="btn btn-cancel"
        >
          Huỷ đăng ký
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useCourseStore } from '@/stores/courseStore'

const courseStore = useCourseStore()

onMounted(async () => {
  await courseStore.fetchMyRegistrations()
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('vi-VN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const cancelRegistration = async (courseId) => {
  if (confirm('Bạn chắc chắn muốn huỷ đăng ký môn này?')) {
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
.my-courses-page {
  padding: 2rem 0;
}

.my-courses-page h1 {
  margin-bottom: 2rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.no-courses {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.no-courses p {
  margin-bottom: 1.5rem;
  color: #666;
}

.registrations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
}

.registration-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  padding: 1.5rem;
  transition: transform 0.3s, box-shadow 0.3s;
}

.registration-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 0.5rem;
}

.card-header h3 {
  margin: 0;
  color: #667eea;
  font-size: 1.1rem;
}

.status-badge {
  background-color: #51cf66;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

.registration-card h2 {
  margin: 0.5rem 0 1rem 0;
  font-size: 1.3rem;
  color: #333;
}

.course-details {
  margin-bottom: 1.5rem;
  background-color: #f9f9f9;
  padding: 1rem;
  border-radius: 4px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  margin: 0.5rem 0;
  font-size: 0.9rem;
}

.detail-item .label {
  color: #666;
  font-weight: 500;
}

.detail-item .value {
  color: #333;
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

.btn-cancel {
  background-color: #ff6b6b;
  color: white;
}

.btn-cancel:hover {
  background-color: #ff5252;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(255, 107, 107, 0.3);
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  display: inline-block;
  padding: 0.75rem 1.5rem;
}
</style>
