<template>
  <div class="profile-page">
    <h1>Thông tin tài khoản</h1>

    <div class="profile-container">
      <div class="profile-card">
        <h2>Thông tin sinh viên</h2>
        <div class="profile-info">
          <div class="info-group">
            <label>Mã số sinh viên</label>
            <p>{{ authStore.user?.mssv }}</p>
          </div>
          <div class="info-group">
            <label>Họ và tên</label>
            <p>{{ authStore.user?.full_name }}</p>
          </div>
          <div class="info-group">
            <label>Email</label>
            <p>{{ authStore.user?.email }}</p>
          </div>
          <div class="info-group">
            <label>Số điện thoại</label>
            <p>{{ authStore.user?.phone || 'Chưa cập nhật' }}</p>
          </div>
          <div class="info-group">
            <label>Khoa</label>
            <p>{{ authStore.user?.department }}</p>
          </div>
        </div>
      </div>

      <div class="password-card">
        <h2>Thay đổi mật khẩu</h2>
        <form @submit.prevent="handleChangePassword">
          <div class="form-group">
            <label for="old_password">Mật khẩu cũ</label>
            <input
              v-model="passwordForm.old_password"
              type="password"
              id="old_password"
              placeholder="Nhập mật khẩu cũ"
              required
            />
          </div>

          <div class="form-group">
            <label for="new_password">Mật khẩu mới</label>
            <input
              v-model="passwordForm.new_password"
              type="password"
              id="new_password"
              placeholder="Nhập mật khẩu mới"
              required
            />
          </div>

          <div class="form-group">
            <label for="confirm_password">Xác nhận mật khẩu mới</label>
            <input
              v-model="passwordForm.confirm_password"
              type="password"
              id="confirm_password"
              placeholder="Xác nhận mật khẩu mới"
              required
            />
          </div>

          <div v-if="error" class="error-message">{{ error }}</div>
          <div v-if="success" class="success-message">{{ success }}</div>

          <button type="submit" class="btn btn-submit" :disabled="isLoading">
            {{ isLoading ? 'Đang cập nhật...' : 'Cập nhật mật khẩu' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()
const isLoading = ref(false)
const error = ref('')
const success = ref('')

const passwordForm = ref({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

const handleChangePassword = async () => {
  error.value = ''
  success.value = ''

  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    error.value = 'Mật khẩu mới không khớp'
    return
  }

  if (passwordForm.value.new_password.length < 6) {
    error.value = 'Mật khẩu mới phải có ít nhất 6 ký tự'
    return
  }

  isLoading.value = true
  try {
    await authStore.changePassword(
      passwordForm.value.old_password,
      passwordForm.value.new_password
    )
    success.value = 'Thay đổi mật khẩu thành công'
    passwordForm.value = {
      old_password: '',
      new_password: '',
      confirm_password: ''
    }
  } catch (err) {
    error.value = err.error || 'Lỗi thay đổi mật khẩu'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.profile-page {
  padding: 2rem 0;
}

.profile-page h1 {
  margin-bottom: 2rem;
}

.profile-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

@media (max-width: 768px) {
  .profile-container {
    grid-template-columns: 1fr;
  }
}

.profile-card,
.password-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #333;
}

.profile-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-group {
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 1rem;
}

.info-group label {
  display: block;
  color: #666;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.25rem;
}

.info-group p {
  margin: 0;
  font-size: 1rem;
  color: #333;
  font-weight: 500;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
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

.btn-submit {
  width: 100%;
  padding: 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
