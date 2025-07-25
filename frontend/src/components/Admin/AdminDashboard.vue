<template>
  <section class="dashboard-section">
    <div class="container-fluid">
      <!-- Sidebar Navigation -->
      <aside
        class="sidebar"
        :class="{ collapsed: isSidebarCollapsed }"
        @mouseenter="expandSidebar"
        @mouseleave="collapseSidebar"
      >
        <div class="sidebar-brand">
          <i class="fas fa-graduation-cap gradient-text"></i>
          <h2 class="sidebar-title" v-if="!isSidebarCollapsed">QuizMaster</h2>
        </div>
        <nav class="sidebar-nav">
          <router-link
            to="/dashboard/admin"
            class="nav-item"
            :class="{ active: $route.path === '/dashboard/admin' }"
          >
            <i class="fas fa-tachometer-alt"></i>
            <span v-if="!isSidebarCollapsed">Dashboard</span>
          </router-link>
          <router-link
            to="/dashboard/admin/subjects"
            class="nav-item"
            :class="{ active: $route.path === '/dashboard/admin/subjects' }"
          >
            <i class="fas fa-layer-group"></i>
            <span v-if="!isSidebarCollapsed">Subjects</span>
          </router-link>
          <router-link
            to="/dashboard/admin/db"
            class="nav-item"
            :class="{ active: $route.path === '/dashboard/admin/db' }"
          >
            <i class="fas fa-users"></i>
            <span v-if="!isSidebarCollapsed">Database</span>
          </router-link>
          <div class="nav-item logout" @click="logout">
            <i class="fas fa-sign-out-alt"></i>
            <span v-if="!isSidebarCollapsed">Logout</span>
          </div>
        </nav>
      </aside>

      <!-- Main Content -->
      <main class="main-content" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
        <!-- Header Section -->
        <div class="dashboard-header mb-5">
          <div class="row align-items-center">
            <!-- Welcome Section -->
            <div class="col-12 col-lg-8">
              <div class="welcome-content">
                <h1 class="welcome-title">Admin Dashboard 🚀</h1>
                <p class="welcome-subtitle">
                  Welcome back, Admin! Monitor your platform's performance.
                </p>

                <!-- Tip of the Day -->
                <!-- <div class="tip-card">
                  <div class="d-flex align-items-center">
                    <div class="tip-icon">
                      <i class="fas fa-lightbulb"></i>
                    </div>
                    <div class="tip-content">
                      <span class="tip-label">Admin Tip:</span>
                      <span class="tip-text">Monitor user engagement and quiz completion rates regularly</span>
                    </div>
                  </div>
                </div> -->

                <div class="date-info">
                  <i class="fas fa-calendar-alt me-2"></i>
                  {{ currentDate }}
                </div>
              </div>
            </div>

            <!-- Quick Actions Card -->
            <div class="col-12 col-lg-4">
              <div class="profile-wrapper">
                <div class="profile-card expanded">
                  <div class="profile-expanded">
                    <div class="profile-view">
                      <div class="profile-header">
                        <div class="profile-avatar-small">
                          <i class="fas fa-user-shield"></i>
                        </div>
                        <div class="profile-info">
                          <h6 class="profile-name-expanded">Administrator</h6>
                          <p class="profile-email">System Manager</p>
                          <span class="profile-badge">Admin Panel</span>
                        </div>
                        <div class="profile-actions">
                          <button class="btn-logout" @click="logout" title="Logout">
                            <i class="fas fa-sign-out-alt"></i>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Stats Grid -->
        <div class="stats-section mb-5">
          <div class="row g-4">
            <div class="col-6 col-lg-3">
              <div class="stat-card stat-primary">
                <div class="stat-icon">
                  <i class="fas fa-users"></i>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ analytics.totalUsers }}</div>
                  <div class="stat-label">Total Users</div>
                </div>
              </div>
            </div>
            <div class="col-6 col-lg-3">
              <div class="stat-card stat-warning">
                <div class="stat-icon">
                  <i class="fas fa-layer-group"></i>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ analytics.totalSubjects }}</div>
                  <div class="stat-label">Total Subjects</div>
                </div>
              </div>
            </div>
            <div class="col-6 col-lg-3">
              <div class="stat-card stat-info">
                <div class="stat-icon">
                  <i class="fas fa-book"></i>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ analytics.totalChapters }}</div>
                  <div class="stat-label">Total Chapters</div>
                </div>
              </div>
            </div>
            <div class="col-6 col-lg-3">
              <div class="stat-card stat-success">
                <div class="stat-icon">
                  <i class="fas fa-question-circle"></i>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ analytics.totalQuizzes }}</div>
                  <div class="stat-label">Total Quizzes</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Additional Stats Row -->
        <div class="stats-section mb-5">
          <div class="row g-4">
            <div class="col-12 col-lg-9">
              <!-- Chart Section -->
              <div class="chart-card">
                <div class="chart-header">
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <h5><i class="fas fa-chart-line me-2"></i>Quiz Submissions Over Time</h5>
                      <p>Monitor platform activity and user engagement</p>
                    </div>
                    <select v-model="analytics.selectedRange" @change="updateChart" class="chart-select">
                      <option value="7d">Last 7 Days</option>
                      <option value="24h">Last 24 Hours</option>
                      <option value="30d">Last 30 Days</option>
                    </select>
                  </div>
                </div>
                <div class="chart-body">
                  <canvas ref="quizAttemptsChart" height="300"></canvas>
                </div>
              </div>
            </div>
            <div class="col-12 col-lg-3">
              <!-- System Status -->
              <div class="section-card mb-4">
                <div class="section-header">
                  <h6><i class="fas fa-server me-2"></i>System Status</h6>
                </div>
                <div class="progress-list">
                  <div class="progress-item">
                    <div class="progress-info">
                      <div class="progress-title">Server Status</div>
                      <div class="progress-subtitle">All systems operational</div>
                    </div>
                    <div class="status-indicator online"></div>
                  </div>
                  <div class="progress-item">
                    <div class="progress-info">
                      <div class="progress-title">Database</div>
                      <div class="progress-subtitle">Connected and healthy</div>
                    </div>
                    <div class="status-indicator online"></div>
                  </div>
                  <div class="progress-item">
                    <div class="progress-info">
                      <div class="progress-title">API Services</div>
                      <div class="progress-subtitle">Running smoothly</div>
                    </div>
                    <div class="status-indicator online"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions Section -->
        <div class="content-section">
          <div class="row g-4">
            <!-- Quick Actions -->
            <div class="col-12 col-lg-8">
              <div class="section-card">
                <div class="section-header">
                  <h5><i class="fas fa-bolt me-2"></i>Quick Actions</h5>
                  <p>Manage your platform efficiently</p>
                </div>
                <div class="suggestions-grid">
                  <div class="suggestion-card">
                    <div class="suggestion-badge">
                      <i class="fas fa-plus"></i>
                      Action
                    </div>
                    <div class="suggestion-content">
                      <h6>Add New Subject</h6>
                      <p>Create a new subject category</p>
                      <router-link to="/dashboard/admin/subjects" class="suggestion-btn">
                        Create <i class="fas fa-arrow-right ms-1"></i>
                      </router-link>
                    </div>
                  </div>
                  <div class="suggestion-card">
                    <div class="suggestion-badge">
                      <i class="fas fa-users"></i>
                      Manage
                    </div>
                    <div class="suggestion-content">
                      <h6>User Management</h6>
                      <p>View and manage user accounts</p>
                      <router-link to="/dashboard/admin/db" class="suggestion-btn">
                        Manage <i class="fas fa-arrow-right ms-1"></i>
                      </router-link>
                    </div>
                  </div>
                  <div class="suggestion-card">
                    <div class="suggestion-badge">
                      <i class="fas fa-chart-bar"></i>
                      Analytics
                    </div>
                    <div class="suggestion-content">
                      <h6>View Analytics</h6>
                      <p>Detailed platform statistics</p>
                      <a href="#" class="suggestion-btn">
                        View <i class="fas fa-arrow-right ms-1"></i>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Recent Activity -->
            <div class="col-12 col-lg-4">
              <div class="section-card">
                <div class="section-header">
                  <h6><i class="fas fa-bell me-2"></i>Recent Activity</h6>
                </div>
                <div class="announcements-list">
                  <div class="announcement-item">
                    <div class="announcement-icon">
                      <i class="fas fa-user-plus"></i>
                    </div>
                    <div class="announcement-content">
                      <h6>New User Registration</h6>
                      <p>5 new users joined today</p>
                      <span class="announcement-date">Today</span>
                    </div>
                  </div>
                  <div class="announcement-item">
                    <div class="announcement-icon">
                      <i class="fas fa-chart-line"></i>
                    </div>
                    <div class="announcement-content">
                      <h6>Quiz Activity</h6>
                      <p>High engagement this week</p>
                      <span class="announcement-date">This week</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Chart from 'chart.js/auto'
import api from '../../api'

const router = useRouter()
const $route = useRoute()

const analytics = ref({
  totalUsers: 0,
  totalChapters: 0,
  totalQuizzes: 0,
  totalSubjects: 0,
  totalResults: 0,
  usersGrowthPercent: 0,
  chaptersGrowthPercent: 0,
  quizzesGrowthPercent: 0,
  // Chart-related analytics
  selectedRange: '7d',
  allResults: [],
})

const isSidebarCollapsed = ref(true)
const currentDate = ref('')

function expandSidebar() {
  isSidebarCollapsed.value = false
}
function collapseSidebar() {
  isSidebarCollapsed.value = true
}

if (typeof window !== 'undefined') {
  window.addEventListener('mousemove', (e) => {
    if (e.clientX <= 8) {
      expandSidebar()
    }
  })
}

const quizAttemptsChart = ref(null)
let chartInstance = null

function logout() {
  router.push('/login')
}

// Fetch all analytics and results in one function
async function fetchAllAnalytics() {
  // Users
  const usersData = await api.get("/auth/users")
  analytics.value.totalUsers = usersData.data.users ? usersData.data.users.length : 0

  // Chapters
  const chaptersData = await api.get("/auth/chapters")
  analytics.value.totalChapters = chaptersData.data.chapters ? chaptersData.data.chapters.length : 0

  // Quizzes
  const quizzesData = await api.get("/auth/quizzes")
  analytics.value.totalQuizzes = quizzesData.data.quizzes ? quizzesData.data.quizzes.length : 0

  // Subjects
  const subjectsData = await api.get("/auth/subjects")
  analytics.value.totalSubjects = subjectsData.data.subjects ? subjectsData.data.subjects.length : 0

  // Growth percents (dummy, set to 0)
  analytics.value.usersGrowthPercent = 0
  analytics.value.chaptersGrowthPercent = 0
  analytics.value.quizzesGrowthPercent = 0

  // Results for chart
  const resultsData = await api.get("/auth/results")
  analytics.value.allResults = resultsData.data.results || []
  analytics.value.totalResults = analytics.value.allResults.length
}

// Prepare chart data based on selected range
function getChartData() {
  const now = new Date()
  let start, labels = [], counts = []

  if (analytics.value.selectedRange === '24h') {
    // Last 24 hours, group by hour
    start = new Date(now.getTime() - 24 * 60 * 60 * 1000)
    for (let i = 0; i < 24; i++) {
      const hour = new Date(start.getTime() + i * 60 * 60 * 1000)
      labels.push(hour.getHours().toString().padStart(2, '0') + ':00')
    }
    counts = Array(24).fill(0)
    analytics.value.allResults.forEach(r => {
      const created = new Date(r.created_at)
      if (created >= start && created <= now) {
        const diffH = Math.floor((created - start) / (60 * 60 * 1000))
        if (diffH >= 0 && diffH < 24) counts[diffH]++
      }
    })
  } else if (analytics.value.selectedRange === '7d') {
    // Last 7 days, group by day
    start = new Date(now.getTime() - 6 * 24 * 60 * 60 * 1000)
    for (let i = 0; i < 7; i++) {
      const day = new Date(start.getTime() + i * 24 * 60 * 60 * 1000)
      labels.push(day.toISOString().slice(0, 10))
    }
    counts = Array(7).fill(0)
    analytics.value.allResults.forEach(r => {
      const created = new Date(r.created_at)
      if (created >= start && created <= now) {
        const diffD = Math.floor((created - start) / (24 * 60 * 60 * 1000))
        if (diffD >= 0 && diffD < 7) counts[diffD]++
      }
    })
  } else if (analytics.value.selectedRange === '30d') {
    // Last 30 days, group by day
    start = new Date(now.getTime() - 29 * 24 * 60 * 60 * 1000)
    for (let i = 0; i < 30; i++) {
      const day = new Date(start.getTime() + i * 24 * 60 * 60 * 1000)
      labels.push(day.toISOString().slice(0, 10))
    }
    counts = Array(30).fill(0)
    analytics.value.allResults.forEach(r => {
      const created = new Date(r.created_at)
      if (created >= start && created <= now) {
        const diffD = Math.floor((created - start) / (24 * 60 * 60 * 1000))
        if (diffD >= 0 && diffD < 30) counts[diffD]++
      }
    })
  }
  // Ensure counts are rounded whole numbers (though they are already integers, for generality)
  counts = counts.map(c => Math.round(c))
  return { labels, counts }
}

// Draw or update the chart
function updateChart() {
  if (!quizAttemptsChart.value) return
  const { labels, counts } = getChartData()
  if (chartInstance) {
    chartInstance.data.labels = labels
    chartInstance.data.datasets[0].data = counts
    chartInstance.options.scales.x.title.text = analytics.value.selectedRange === '24h' ? 'Hour' : 'Date'
    chartInstance.update()
  } else {
    chartInstance = new Chart(quizAttemptsChart.value, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: 'Quiz Submissions',
          data: counts,
          fill: true,
          borderColor: '#3b82f6',
          backgroundColor: 'rgba(59,130,246,0.1)',
          tension: 0.4,
          pointRadius: 6,
          pointBackgroundColor: '#3b82f6',
          pointBorderColor: '#fff',
          pointBorderWidth: 3,
          pointHoverRadius: 8,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              // Show only rounded whole numbers in tooltip
              label: function(context) {
                let value = context.parsed.y
                return `Quiz Submissions: ${Math.round(value)}`
              }
            }
          }
        },
        scales: {
          x: { 
            grid: { display: false },
            border: { display: false },
            ticks: { color: "#6b7280" },
            title: { 
              display: true, 
              text: analytics.value.selectedRange === '24h' ? 'Hour' : 'Date',
              color: "#6b7280",
              font: { weight: "bold" }
            } 
          },
          y: { 
            beginAtZero: true, 
            grid: {
              color: "#f3f4f6",
              drawBorder: false,
            },
            border: { display: false },
            ticks: {
              color: "#6b7280",
              // Show only whole numbers on y-axis
              callback: function(value) {
                return Number.isInteger(value) ? value : ''
              },
              stepSize: 1
            },
            title: { 
              display: true, 
              text: 'Submissions',
              color: "#6b7280",
              font: { weight: "bold" }
            }
          }
        }
      }
    })
  }
}

onMounted(async () => {
  currentDate.value = new Date().toLocaleDateString(undefined, {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });
  
  await fetchAllAnalytics()
  await nextTick()
  updateChart()
})

watch(() => analytics.value.selectedRange, () => {
  updateChart()
})
</script>

<style scoped>
.dashboard-section {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  min-height: 100vh;
  padding: 0;
  position: relative;
}

.container-fluid {
  max-width: 100%;
  padding: 0;
  display: flex;
  min-height: 100vh;
}

/* Sidebar Styles */
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  width: 250px;
  background: white;
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  transition: all 0.3s ease;
  overflow: hidden;
}

.sidebar.collapsed {
  width: 70px;
}

.sidebar-brand {
  padding: 2rem 1rem;
  text-align: center;
  border-bottom: 1px solid #f3f4f6;
}

.sidebar-brand i {
  font-size: 2rem;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: block;
  margin-bottom: 0.5rem;
}

.sidebar-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.sidebar-nav {
  padding: 1rem 0;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 1rem 1.5rem;
  color: #6b7280;
  text-decoration: none;
  transition: all 0.3s ease;
  border-radius: 0;
  margin: 0.25rem 0;
}

.nav-item:hover {
  background: linear-gradient(135deg, #f0f7ff 0%, #e0f2fe 100%);
  color: #3b82f6;
  text-decoration: none;
}

.nav-item.active {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.nav-item i {
  font-size: 1.25rem;
  margin-right: 1rem;
  min-width: 20px;
  text-align: center;
}

.nav-item.logout {
  cursor: pointer;
  margin-top: 2rem;
  border-top: 1px solid #f3f4f6;
  padding-top: 1.5rem;
  color: #ef4444;
}

.nav-item.logout:hover {
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  color: #dc2626;
}

.sidebar.collapsed .nav-item span {
  display: none;
}

.sidebar.collapsed .nav-item {
  padding: 1rem 1.25rem;
  justify-content: center;
}

.sidebar.collapsed .nav-item i {
  margin-right: 0;
}

/* Main Content */
.main-content {
  flex: 1;
  margin-left: 250px;
  padding: 2rem;
  transition: all 0.3s ease;
  min-height: 100vh;
}

.main-content.sidebar-collapsed {
  margin-left: 70px;
}

/* Header Section */
.dashboard-header {
  margin-bottom: 3rem;
}

.welcome-content {
  padding: 1rem 0;
}

.welcome-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.welcome-subtitle {
  font-size: 1.2rem;
  color: #6b7280;
  margin-bottom: 1.5rem;
}

.tip-card {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-radius: 1rem;
  padding: 1rem;
  margin-bottom: 1rem;
  border-left: 4px solid #f59e0b;
}

.tip-icon {
  width: 40px;
  height: 40px;
  background: #f59e0b;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-right: 1rem;
  flex-shrink: 0;
}

.tip-content {
  display: flex;
  flex-direction: column;
}

.tip-label {
  font-weight: 600;
  color: #92400e;
  font-size: 0.9rem;
}

.tip-text {
  color: #78350f;
  font-size: 0.95rem;
}

.date-info {
  color: #6b7280;
  font-size: 1rem;
}

/* Profile Card */
.profile-wrapper {
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.profile-card {
  background: white;
  border-radius: 1.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  width: 100%;
  max-width: 400px;
}

.profile-expanded {
  padding: 1.5rem;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.profile-avatar-small {
  font-size: 2.5rem;
  color: #3b82f6;
}

.profile-info {
  flex-grow: 1;
}

.profile-name-expanded {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.profile-email {
  font-size: 0.9rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.profile-badge {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  font-weight: 500;
}

.profile-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-logout {
  width: 35px;
  height: 35px;
  border: none;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #f3f4f6;
  color: #ef4444;
}

.btn-logout:hover {
  background: #ef4444;
  color: white;
}

/* Stats Section */
.stats-section {
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  border-radius: 1.25rem;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  height: 100%;
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
  flex-shrink: 0;
}

.stat-primary .stat-icon {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
}
.stat-success .stat-icon {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}
.stat-info .stat-icon {
  background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
}
.stat-warning .stat-icon {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}
.stat-danger .stat-icon {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.stat-content {
  flex-grow: 1;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.95rem;
  color: #6b7280;
  font-weight: 500;
}

/* Chart Section */
.chart-card {
  background: white;
  border-radius: 1.25rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  height: 100%;
}

.chart-header {
  padding: 1.5rem 1.5rem 0 1.5rem;
}

.chart-header h5 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.chart-header p {
  font-size: 0.9rem;
  color: #6b7280;
  margin-bottom: 0;
}

.chart-select {
  padding: 0.5rem 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  background: white;
  color: #374151;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.chart-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.chart-body {
  padding: 1rem 1.5rem 1.5rem 1.5rem;
  height: 300px;
}

/* Content Section */
.content-section {
  margin-bottom: 3rem;
}

.section-card {
  background: white;
  border-radius: 1.25rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  height: 100%;
}

.section-header {
  margin-bottom: 1.5rem;
}

.section-header h5,
.section-header h6 {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.section-header h5 {
  font-size: 1.2rem;
}

.section-header h6 {
  font-size: 1.1rem;
}

.section-header p {
  font-size: 0.9rem;
  color: #6b7280;
  margin-bottom: 0;
}

/* Suggestions Grid */
.suggestions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.suggestion-card {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 1rem;
  padding: 1.5rem;
  position: relative;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.suggestion-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  border-color: #fbbf24;
}

.suggestion-badge {
  position: absolute;
  top: -0.5rem;
  right: 1rem;
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.suggestion-content {
  margin-top: 1rem;
}

.suggestion-content h6 {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.suggestion-content p {
  font-size: 0.9rem;
  color: #6b7280;
  margin-bottom: 1rem;
}

.suggestion-btn {
  display: inline-flex;
  align-items: center;
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  color: white;
  padding: 0.75rem 1.25rem;
  border-radius: 0.75rem;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.suggestion-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(251, 191, 36, 0.4);
  color: white;
  text-decoration: none;
}

/* Progress List */
.progress-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.progress-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 0.75rem;
  transition: all 0.3s ease;
}

.progress-item:hover {
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
}

.progress-info {
  flex-grow: 1;
}

.progress-title {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.progress-subtitle {
  font-size: 0.85rem;
  color: #6b7280;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
}

.status-indicator.online {
  background: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
}

.status-indicator.offline {
  background: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.2);
}

/* Announcements */
.announcements-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.announcement-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border-radius: 0.75rem;
  border-left: 4px solid #0ea5e9;
}

.announcement-icon {
  width: 40px;
  height: 40px;
  background: #0ea5e9;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.announcement-content h6 {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.announcement-content p {
  font-size: 0.9rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.announcement-date {
  font-size: 0.8rem;
  color: #9ca3af;
}

/* Responsive Design */
@media (max-width: 1200px) {
  .welcome-title {
    font-size: 2rem;
  }

  .stat-number {
    font-size: 2rem;
  }
}

@media (max-width: 768px) {
  .sidebar {
    width: 70px;
  }
  
  .sidebar.collapsed {
    width: 70px;
  }
  
  .main-content {
    margin-left: 70px;
  }
  
  .main-content.sidebar-collapsed {
    margin-left: 70px;
  }

  .welcome-title {
    font-size: 1.75rem;
  }

  .welcome-subtitle {
    font-size: 1rem;
  }

  .stat-card {
    padding: 1.5rem;
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .stat-number {
    font-size: 1.75rem;
  }

  .suggestions-grid {
    grid-template-columns: 1fr;
  }

  .profile-card {
    max-width: 100%;
  }
}

@media (max-width: 576px) {
  .main-content {
    padding: 1rem;
    margin-left: 0;
  }
  
  .sidebar {
    transform: translateX(-100%);
  }
  
  .sidebar:hover {
    transform: translateX(0);
  }

  .stat-icon {
    width: 50px;
    height: 50px;
    font-size: 1.25rem;
  }

  .chart-body {
    height: 250px;
  }
}

/* Loading Animation */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.loading {
  animation: pulse 2s infinite;
}

/* Smooth Scrollbar */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #6366f1 0%, #3b82f6 100%);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #4f46e5 0%, #2563eb 100%);
}
</style>