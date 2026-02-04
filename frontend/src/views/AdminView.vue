<template>
  <div class="admin-page">
    <h1>Quản lý kỳ đăng ký</h1>

    <div class="section">
      <h2>Thiết lập khoảng đăng ký</h2>
      <form @submit.prevent="handleCreatePeriod" class="form-section">
        <div class="form-group">
          <label for="period_name">Tên kỳ đăng ký</label>
          <input
            v-model="newPeriod.name"
            type="text"
            id="period_name"
            placeholder="VD: Kỳ đăng ký hôm nay"
            required
          />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="start_date">Bắt đầu</label>
            <input
              v-model="newPeriod.start_date"
              type="datetime-local"
              id="start_date"
              required
            />
          </div>
          <div class="form-group">
            <label for="end_date">Kết thúc</label>
            <input
              v-model="newPeriod.end_date"
              type="datetime-local"
              id="end_date"
              required
            />
          </div>
        </div>

        <div class="form-group checkbox">
          <input
            v-model="newPeriod.is_active"
            type="checkbox"
            id="is_active"
          />
          <label for="is_active">Mở đăng ký ngay</label>
        </div>

        <div v-if="periodError" class="error-message">{{ periodError }}</div>
        <div v-if="periodSuccess" class="success-message">{{ periodSuccess }}</div>

        <button type="submit" class="btn btn-primary" :disabled="adminStore.isLoading">
          {{ adminStore.isLoading ? 'Đang lưu...' : 'Lưu và áp dụng' }}
        </button>
      </form>
    </div>

    <div class="section">
      <h2>Trạng thái hiện tại</h2>
      <div v-if="adminStore.isLoading" class="loading">
        Đang tải...
      </div>
      <div v-else-if="adminStore.periods.length === 0" class="no-data">
        Chưa có kỳ đăng ký nào
      </div>
      <div v-else class="periods-list">
        <div
          v-for="period in adminStore.periods"
          :key="period.id"
          class="period-item"
        >
          <div class="period-info">
            <h3>{{ period.name }}</h3>
            <p>{{ formatDate(period.start_date) }} - {{ formatDate(period.end_date) }}</p>
          </div>
          <div class="period-actions">
            <button
              @click="togglePeriod(period)"
              :class="{ active: period.is_active }"
              class="btn btn-toggle"
            >
              {{ period.is_active ? 'Đang mở' : 'Đang đóng' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAdminStore } from '@/stores/adminStore'

const adminStore = useAdminStore()
const periodError = ref('')
const periodSuccess = ref('')

const getDefaultPeriod = () => {
  const now = new Date()
  const start = new Date(now)
  start.setHours(7, 0, 0, 0)
  const end = new Date(now)
  end.setHours(17, 0, 0, 0)

  const toLocalInput = (date) => {
    const offset = date.getTimezoneOffset() * 60000
    return new Date(date.getTime() - offset).toISOString().slice(0, 16)
  }

  return {
    name: `Đăng ký hôm nay (${start.toLocaleDateString('vi-VN')})`,
    start_date: toLocalInput(start),
    end_date: toLocalInput(end),
    is_active: true
  }
}

const newPeriod = ref(getDefaultPeriod())

onMounted(async () => {
  await adminStore.fetchPeriods()
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

const handleCreatePeriod = async () => {
  periodError.value = ''
  periodSuccess.value = ''

  try {
    await adminStore.createPeriod(newPeriod.value)
    periodSuccess.value = 'Tạo kỳ đăng ký thành công'
    newPeriod.value = getDefaultPeriod()
  } catch (error) {
    periodError.value = error.error || 'Lỗi tạo kỳ đăng ký'
  }
}

const togglePeriod = async (period) => {
  try {
    await adminStore.updatePeriod({
      id: period.id,
      is_active: !period.is_active
    })
    periodSuccess.value = 'Cập nhật thành công'
  } catch (error) {
    periodError.value = error.error || 'Lỗi cập nhật'
  }
}
</script>

<style scoped>
.admin-page {
  padding: 2rem 0;
}

.admin-page h1 {
  margin-bottom: 2rem;
}

.admin-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: 2px solid #e0e0e0;
}

.tab-button {
  padding: 1rem 1.5rem;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  font-size: 1rem;
  color: #666;
  transition: all 0.3s;
}

.tab-button.active {
  color: #667eea;
  border-bottom-color: #667eea;
}

.tab-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 2rem;
}

@media (max-width: 768px) {
  .tab-content {
    grid-template-columns: 1fr;
  }
}

.section {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.section h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
}

.form-section {
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 500;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group.checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.form-group.checkbox input {
  width: auto;
  margin: 0;
}

.form-group.checkbox label {
  margin: 0;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  border: 1px solid #f5c6cb;
}

.success-message {
  background-color: #d4edda;
  color: #155724;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  border: 1px solid #c3e6cb;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  width: 100%;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.no-data {
  text-align: center;
  padding: 2rem;
  color: #999;
}

.periods-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.period-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background-color: #f9f9f9;
  border-radius: 4px;
  border-left: 4px solid #667eea;
}

.period-info h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.period-info p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.period-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-toggle {
  padding: 0.5rem 1rem;
  background-color: #e0e0e0;
  color: #666;
  border: 1px solid #d0d0d0;
}

.btn-toggle.active {
  background-color: #51cf66;
  color: white;
  border-color: #51cf66;
}

/* Quick Toggle Section Styles */
.quick-toggle-section {
  grid-column: 1 / -1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.quick-toggle-section h2 {
  color: white;
  font-size: 1.5rem;
}

.quick-toggle-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.status-info {
  padding: 1rem;
  background-color: rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  backdrop-filter: blur(10px);
}

.status-active {
  color: #d4edda;
  font-size: 1.1rem;
  margin: 0;
}

.status-inactive {
  color: #f8d7da;
  font-size: 1.1rem;
  margin: 0;
}

.time-info {
  font-size: 0.9rem;
  opacity: 0.9;
}

.quick-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.quick-actions .btn {
  flex: 1;
  min-width: 150px;
  font-size: 1rem;
  padding: 1rem 1.5rem;
  font-weight: 600;
}

.btn-success {
  background-color: #51cf66;
  color: white;
}

.btn-success:hover:not(:disabled) {
  background-color: #40b050;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(81, 207, 102, 0.4);
}

.btn-info {
  background-color: #339af0;
  color: white;
}

.btn-info:hover:not(:disabled) {
  background-color: #228be6;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(51, 154, 240, 0.4);
}

.btn-danger {
  background-color: #ff6b6b;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background-color: #fa5252;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 107, 107, 0.4);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.quick-message {
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
  font-weight: 600;
  animation: slideIn 0.3s ease;
}

.quick-message.success {
  background-color: rgba(81, 207, 102, 0.2);
  border: 2px solid rgba(81, 207, 102, 0.5);
}

.quick-message.error {
  background-color: rgba(255, 107, 107, 0.2);
  border: 2px solid rgba(255, 107, 107, 0.5);
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .quick-actions {
    flex-direction: column;
  }
  
  .quick-actions .btn {
    width: 100%;
  }
}
</style>
