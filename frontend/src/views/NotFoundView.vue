<template>
  <div class="not-found">
    <div class="not-found-content">
      <h1>404</h1>
      <h2>Trang không tìm thấy</h2>
      <p>Xin lỗi, trang bạn tìm kiếm không tồn tại.</p>
      <router-link to="/" class="btn btn-home">
        Quay về trang chủ
      </router-link>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.not-found {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 300px);
}

.not-found-content {
  text-align: center;
}

.not-found-content h1 {
  font-size: 5rem;
  margin: 0;
  color: #667eea;
}

.not-found-content h2 {
  font-size: 1.5rem;
  margin: 1rem 0;
  color: #333;
}

.not-found-content p {
  color: #666;
  margin-bottom: 2rem;
}

.btn-home {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: all 0.3s;
}

.btn-home:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
}
</style>
