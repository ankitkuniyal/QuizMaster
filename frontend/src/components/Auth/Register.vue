<template>
  <section class="register-section">
    <div class="container">
      <div class="row justify-content-center align-items-center min-vh-100">
        <div class="col-lg-7 col-xl-6">
          <div class="card register-card border-0 shadow-lg">
            <div class="p-5">
              <div class="mb-4 text-center">
                <span class="badge bg-accent px-3 py-2 mb-2 fs-6 shadow-sm">Welcome</span>
                <h2 class="fw-bold mb-2 text-dark">Create your account</h2>
                <p class="text-muted mb-0">Join Quiz Master and start your journey!</p>
              </div>
              <form @submit.prevent="handleRegister">
                <!-- Full Name -->
                <div class="mb-3">
                  <label for="name" class="form-label">Full Name</label>
                  <div class="input-group">
                    <span class="input-group-text bg-light"><i class="fas fa-user"></i></span>
                    <input type="text" id="name" class="form-control" placeholder="Full Name" v-model="form.name" required />
                  </div>
                </div>
                <!-- Email -->
                <div class="mb-3">
                  <label for="email" class="form-label">Email</label>
                  <div class="input-group">
                    <span class="input-group-text bg-light"><i class="fas fa-envelope"></i></span>
                    <input type="email" id="email" class="form-control" placeholder="you@example.com" v-model="form.email" required />
                  </div>
                </div>
                <!-- Password -->
                <div class="mb-3">
                  <label for="password" class="form-label">Password</label>
                  <div class="input-group">
                    <span class="input-group-text bg-light"><i class="fas fa-lock"></i></span>
                    <input type="password" id="password" class="form-control" placeholder="Enter password" v-model="form.password" required />
                  </div>
                </div>
                <!-- Confirm Password -->
                <div class="mb-3">
                  <label for="confirmPassword" class="form-label">Confirm Password</label>
                  <div class="input-group">
                    <span class="input-group-text bg-light"><i class="fas fa-key"></i></span>
                    <input type="password" id="confirmPassword" class="form-control" placeholder="Confirm password" v-model="form.confirmPassword" required />
                  </div>
                </div>
                <!-- Qualification -->
                <div class="mb-3">
                  <label for="qualification" class="form-label">Qualification</label>
                  <label for="password" class="form-label">Password</label>
                  <div class="input-group">
                    <span class="input-group-text bg-light"><i class="fas fa-graduation-cap"></i></span>
                    <input
                    type="text"
                    id="qualification"
                    class="form-control"
                    placeholder="Enter your qualification"
                    v-model="form.qualification"
                    required
                  />
                  </div>
                  
                  
                </div>
                <!-- Terms -->
                <div class="form-check mb-4">
                  <input class="form-check-input" type="checkbox" id="terms" v-model="form.terms" required />
                  <label class="form-check-label" for="terms">
                    I agree to the <a href="#" class="text-accent text-decoration-underline">Terms & Conditions</a>
                  </label>
                </div>
                <!-- Submit Button -->
                <div class="d-grid mb-3">
                  <button type="submit" class="btn btn-accent btn-lg shadow-sm" :disabled="loading">
                    <i class="fas fa-user-plus me-2"></i> 
                    <span v-if="loading">Creating...</span>
                    <span v-else>Create Account</span>
                  </button>
                </div>
                <div v-if="error" class="alert alert-danger py-2 mb-3">{{ error }}</div>
                <div class="text-center">
                  <span class="text-muted">Already have an account?</span>
                  <router-link to="/login" class="text-accent fw-semibold text-decoration-none ms-1">Sign In</router-link>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../api'

const router = useRouter()
const loading = ref(false)
const error = ref('')

const form = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
  qualification: '',
  terms: false
})

async function handleRegister() {
  error.value = ''
  if (form.password !== form.confirmPassword) {
    error.value = "Passwords do not match."
    return
  }
  loading.value = true
  try {
    await api.post('/auth/register', {
      name: form.name,
      email: form.email,
      password: form.password,
      qualification: form.qualification,
      terms: form.terms
    })
    router.push('/login')
  } catch (err) {
    error.value = err.response?.data?.message || 'Registration failed.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-section {
  background: linear-gradient(120deg, #f8fafc 0%, #e0e7ff 100%);
  min-height: 100vh;
  padding: 0;
  /* Subtle animated gradient */
  animation: gradientBG 10s ease-in-out infinite alternate;
}
@keyframes gradientBG {
  0% { background: linear-gradient(120deg, #f8fafc 0%, #e0e7ff 100%);}
  100% { background: linear-gradient(120deg, #e0e7ff 0%, #f8fafc 100%);}
}
.register-card {
  border-radius: 1.5rem;
  overflow: hidden;
  background: #fff;
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.10);
  border: 1px solid #e0e7ff;
}
.bg-accent {
  background: linear-gradient(90deg, #6366f1 0%, #06b6d4 100%) !important;
  color: #fff !important;
}
.text-accent {
  color: #06b6d4 !important;
}
.btn-accent {
  background: linear-gradient(90deg, #6366f1 0%, #06b6d4 100%);
  border: none;
  color: #fff;
  transition: background 0.2s;
}
.btn-accent:hover, .btn-accent:focus {
  background: linear-gradient(90deg, #06b6d4 0%, #6366f1 100%);
  color: #fff;
}
@media (max-width: 767px) {
  .register-card {
    border-radius: 1rem;
    padding: 1.5rem 0.5rem;
  }
  .p-5 {
    padding: 2rem !important;
  }
}
</style>