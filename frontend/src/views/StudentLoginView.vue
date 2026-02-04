<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <div class="icon">👨‍🎓</div>
        <h2>Đăng nhập Sinh viên</h2>
        <p class="subtitle">Đăng ký và quản lý môn học</p>
      </div>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="mssv">Mã số sinh viên (MSSV)</label>
          <input
            v-model="form.mssv"
            type="text"
            id="mssv"
            placeholder="Nhập MSSV"
            required
            autocomplete="username"
          />
        </div>

        <div class="form-group">
          <label for="password">Mật khẩu</label>
          <input
            v-model="form.password"
            type="password"
            id="password"
            placeholder="Nhập mật khẩu"
            required
            autocomplete="current-password"
          />
        </div>

        <div v-if="error" class="error-message">{{ error }}</div>

        <button type="submit" class="btn-submit" :disabled="authStore.isLoading">
          {{ authStore.isLoading ? 'Đang đăng nhập...' : 'Đăng nhập' }}
        </button>
      </form>

      <div class="login-footer">
        <p>Bạn là quản trị viên? <router-link to="/admin-login" class="link">Đăng nhập Admin</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()
const router = useRouter()
const error = ref('')

const form = ref({
  mssv: '',
  password: ''
})

const handleLogin = async () => {
  error.value = ''
  try {
    await authStore.login(form.value.mssv, form.value.password)
    router.push('/courses')
  } catch (err) {
    error.value = err.detail || err.error || 'Đăng nhập thất bại. Vui lòng kiểm tra lại MSSV và mật khẩu.'
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px);
  padding: 2rem 1rem;
}

.login-box {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 420px;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.icon {
  font-size: 3.5rem;
  margin-bottom: 1rem;
}

.login-box h2 {
  margin: 0 0 0.5rem 0;
  color: #333;
  font-size: 1.75rem;
}

.subtitle {
  margin: 0;
  color: #666;
  font-size: 0.95rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.85rem;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.error-message {
  background-color: #fee;
  color: #c33;
  padding: 0.85rem;
  border-radius: 6px;
  margin-bottom: 1.25rem;
  border: 1px solid #fcc;
  font-size: 0.9rem;
}

.btn-submit {
  width: 100%;
  padding: 0.85rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1.05rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.login-footer {
  text-align: center;
  margin-top: 1.75rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e0e0e0;
}

.login-footer p {
  margin: 0;
  color: #666;
  font-size: 0.95rem;
}

.link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s;
}

.link:hover {
  color: #764ba2;
  text-decoration: underline;
}
</style>
