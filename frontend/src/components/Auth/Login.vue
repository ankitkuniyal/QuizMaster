<template>
  <section class="login-section">
    <div class="container">
      <div class="row justify-content-center align-items-center min-vh-100">
        <div class="col-lg-7 col-xl-6 d-none d-lg-block">
          <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/draw2.svg"
            class="img-fluid rounded-4" alt="Login illustration">
        </div>
        <div class="col-lg-5 col-xl-4">
          <div class="card login-card border-0 shadow-lg">
            <div class="p-5">
              <div class="mb-4 text-center">
                <span class="badge bg-accent px-3 py-2 mb-2 fs-6 shadow-sm">Welcome Back</span>
                <h2 class="fw-bold mb-2 text-dark">Sign In</h2>
                <p class="text-muted mb-0">Login to your Quiz Master account</p>
              </div>
              <form @submit.prevent="handleLogin">
                <!-- Email -->
                <div class="mb-3">
                  <label for="email" class="form-label">Email</label>
                  <div class="input-group">
                    <span class="input-group-text bg-light"><i class="fas fa-envelope"></i></span>
                    <input
                      type="email"
                      id="email"
                      class="form-control"
                      placeholder="you@example.com"
                      v-model="email"
                      required
                    />
                  </div>
                </div>
                <!-- Password -->
                <div class="mb-3">
                  <label for="password" class="form-label">Password</label>
                  <div class="input-group">
                    <span class="input-group-text bg-light"><i class="fas fa-lock"></i></span>
                    <input
                      type="password"
                      id="password"
                      class="form-control"
                      placeholder="Enter password"
                      v-model="password"
                      required
                    />
                  </div>
                </div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                  <a href="#" class="text-accent text-decoration-underline">Forgot password?</a>
                </div>
                <!-- Error Message -->
                <div v-if="error" class="alert alert-danger py-2 mb-3 text-center">
                  {{ error }}
                </div>
                <!-- Submit Button -->
                <div class="d-grid mb-3">
                  <button type="submit" class="btn btn-accent btn-lg shadow-sm" :disabled="loading">
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                    <i class="fas fa-sign-in-alt me-2"></i> Sign In
                  </button>
                </div>
                <div class="text-center">
                  <span class="text-muted">Don't have an account?</span>
                  <router-link to="/register" class="text-accent fw-semibold text-decoration-none ms-1">Register</router-link>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../api'

export default {
  name: 'Login',
  setup() {
    const email = ref('');
    const password = ref('');
    const error = ref('');
    const loading = ref(false);
    const router = useRouter();

    const handleLogin = async () => {
      error.value = '';
      loading.value = true;
      try {
        const response = await api.post('/auth/login', {
          email: email.value,
          password: password.value
        });

        // Save token to localStorage
        

        // Decode JWT token and verify email and role before storing
        const token = response.data.access_token;
        let isValid = false;
        if (token) {
          const parts = token.split('.');
          if (parts.length === 3) {
            try {
              const payload = JSON.parse(atob(parts[1]));
              // Check for email and role in payload (commonly in 'sub' or directly in payload)
              let email, role;
              if (payload && payload.sub && typeof payload.sub === 'object') {
                email = payload.sub.email;
                role = payload.sub.role;
              } else {
                email = payload.email;
                role = payload.role;
              }
              if (email && role) {
                localStorage.setItem('token', token);
                isValid = true;
              }
            } catch (e) {
              isValid = false;
            }
          }
        }
        if (!isValid) {
          error.value = 'Unauthorized Acces. Please try again.';
          loading.value = false;
          return;
        }

        // Redirect based on role
        // Get role by decoding JWT token
        let userRole = null;
        if (token) {
          const parts = token.split('.');
          if (parts.length === 3) {
            try {
              const payload = JSON.parse(atob(parts[1]));
              if (payload && payload.sub && typeof payload.sub === 'object') {
                userRole = payload.sub.role;
              } else {
                userRole = payload.role;
              }
            } catch (e) {
              userRole = null;
            }
          }
        }
        if (userRole === 'admin') {
          router.push('/dashboard/admin');
        } else {
          router.push(`/dashboard/user/${response.data.user.id}`);
        }
      } catch (err) {
        if (err.response && err.response.data && err.response.data.message) {
          error.value = err.response.data.message;
        } else {
          error.value = 'An error occurred. Please try again.';
        }
      } finally {
        loading.value = false;
      }
    };

    return {
      email,
      password,
      error,
      loading,
      handleLogin
    };
  }
}
</script>

<style scoped>
.login-section {
  background: linear-gradient(120deg, #f8fafc 0%, #e0e7ff 100%);
  min-height: 100vh;
  padding: 0;
  animation: gradientBG 10s ease-in-out infinite alternate;
}
@keyframes gradientBG {
  0% { background: linear-gradient(120deg, #f8fafc 0%, #e0e7ff 100%);}
  100% { background: linear-gradient(120deg, #e0e7ff 0%, #f8fafc 100%);}
}
.login-card {
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
  .login-card {
    border-radius: 1rem;
    padding: 1.5rem 0.5rem;
  }
  .p-5 {
    padding: 2rem !important;
  }
}
</style>