<template>
  <div id="app">
    <div v-if="isAdminArea" class="admin-layout">
      <header class="admin-navbar">
        <div class="container">
          <div class="navbar-brand">
            <h1>Admin Portal</h1>
          </div>
          <nav class="navbar-menu" v-if="authStore.isAuthenticated">
            <ul>
              <li><router-link to="/admin">Dashboard</router-link></li>
              <li><button @click="logoutAdmin" class="btn-logout">Đăng xuất</button></li>
            </ul>
          </nav>
        </div>
      </header>

      <main class="container">
        <router-view />
      </main>

      <footer class="footer admin-footer">
        <p>&copy; 2026 Admin Portal. All rights reserved.</p>
      </footer>
    </div>

    <div v-else class="student-layout">
      <header class="navbar">
        <div class="container">
          <div class="navbar-brand">
            <h1>Hệ thống đăng ký môn học</h1>
          </div>
          <nav class="navbar-menu" v-if="authStore.isAuthenticated">
            <ul>
              <li><router-link to="/dashboard">Trang chủ</router-link></li>
              <li><router-link to="/courses">Danh sách môn học</router-link></li>
              <li><router-link to="/my-courses">Môn của tôi</router-link></li>
              <li><router-link to="/profile">Tài khoản</router-link></li>
              <li v-if="authStore.isAdmin"><router-link to="/admin">Admin</router-link></li>
              <li><button @click="logout" class="btn-logout">Đăng xuất</button></li>
            </ul>
          </nav>
        </div>
      </header>

      <main class="container">
        <router-view />
      </main>

      <footer class="footer">
        <p>&copy; 2024 Hệ thống đăng ký môn học. Bảo lưu mọi quyền.</p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

const isAdminArea = computed(() => route.meta?.adminArea === true)

onMounted(() => {
  authStore.initFromStorage()
})

const logout = () => {
  authStore.logout()
  router.push('/login')
}

const logoutAdmin = () => {
  authStore.logout()
  router.push('/admin-login')
}
</script>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
}

.navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.admin-navbar {
  background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.navbar .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand h1 {
  font-size: 1.5rem;
  margin: 0;
}

.navbar-menu ul {
  list-style: none;
  display: flex;
  gap: 2rem;
  align-items: center;
}

.navbar-menu a {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background 0.3s;
}

.navbar-menu a:hover {
  background-color: rgba(255,255,255,0.2);
}

.btn-logout {
  background-color: #ff6b6b;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-logout:hover {
  background-color: #ff5252;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
  flex: 1;
}

.footer {
  background-color: #333;
  color: white;
  text-align: center;
  padding: 2rem;
  margin-top: auto;
}

.admin-footer {
  background-color: #111827;
}
</style>
