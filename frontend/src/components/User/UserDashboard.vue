<template>
  <section class="dashboard-section">
    <div class="container-fluid">
      <!-- Header Section -->
      <div class="dashboard-header mb-5">
        <div class="row align-items-center">
          <!-- Welcome Section -->
          <div class="col-12 col-lg-7">
            <div class="welcome-content">
              <h1 class="welcome-title">Welcome back, {{ user.name }}! 👋</h1>
              <p class="welcome-subtitle">
                {{ greeting }} Ready to continue learning?
              </p>

              <!-- Tip of the Day -->
              <div class="tip-card">
                <div class="d-flex align-items-center">
                  <div class="tip-icon">
                    <i class="fas fa-lightbulb"></i>
                  </div>
                  <div class="tip-content">
                    <span class="tip-label">Tip of the Day:</span>
                    <span class="tip-text">{{ tipOfTheDay }}</span>
                  </div>
                </div>
              </div>

              <div class="date-info">
                <i class="fas fa-calendar-alt me-2"></i>
                {{ currentDate }}
              </div>
            </div>
          </div>

          <!-- Profile Card (Always Expanded) -->
          <div class="col-12 col-lg-5">
            <div class="profile-wrapper">
              <div class="profile-card expanded">
                <div class="profile-expanded">
                  <!-- View Mode -->
                  <div v-if="!profileEdit" class="profile-view">
                    <div class="profile-header">
                      <div class="profile-avatar-small">
                        <i class="fas fa-user-circle"></i>
                      </div>
                      <div class="profile-info">
                        <h6 class="profile-name-expanded">{{ user.name }}</h6>
                        <p class="profile-email">{{ user.email }}</p>
                        <span class="profile-badge">{{
                          user.qualification
                        }}</span>
                      </div>
                      <div class="profile-actions">
                        <button class="btn-edit" @click="startProfileEdit">
                          <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn-logout" @click="logout" title="Logout" style="margin-left: 0.5rem;">
                          <i class="fas fa-sign-out-alt"></i>
                        </button>
                      </div>
                    </div>
                  </div>

                  <!-- Edit Mode -->
                  <div v-else class="profile-edit">
                    <form @submit.prevent="saveProfile">
                      <div class="form-group">
                        <label>Name</label>
                        <input
                          v-model="editUser.name"
                          type="text"
                          class="form-input"
                          required
                        />
                      </div>
                      <div class="form-group">
                        <label>Qualification</label>
                        <input
                          v-model="editUser.qualification"
                          type="text"
                          class="form-input"
                        />
                      </div>
                      <div class="form-actions">
                        <button
                          type="button"
                          class="btn-cancel"
                          @click="cancelProfileEdit"
                        >
                          Cancel
                        </button>
                        <button type="submit" class="btn-save">
                          Save Changes
                        </button>
                      </div>
                    </form>
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
                <i class="fas fa-clipboard-check"></i>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ stats.totalQuizzes }}</div>
                <div class="stat-label">Quizzes Submitted</div>
              </div>
            </div>
          </div>
          <div class="col-6 col-lg-3">
            <div class="stat-card stat-info">
              <div class="stat-icon">
                <i class="fas fa-book"></i>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ stats.subjectsAttempted }}</div>
                <div class="stat-label">Subjects Attempted</div>
              </div>
            </div>
          </div>
          <div class="col-6 col-lg-3">
            <div class="stat-card stat-success">
              <div class="stat-icon">
                <i class="fas fa-bullseye"></i>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ stats.avgScore }}%</div>
                <div class="stat-label">Average Score</div>
              </div>
            </div>
          </div>
          <div class="col-6 col-lg-3">
            <div class="stat-card stat-warning">
              <div class="stat-icon">
                <i class="fas fa-fire"></i>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ stats.streak }}</div>
                <div class="stat-label">Day Streak</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="charts-section mb-5">
        <div class="row g-4">
          <div class="col-12 col-lg-8">
            <div class="chart-card">
              <div class="chart-header">
                <h5><i class="fas fa-chart-line me-2"></i>Progress Trend</h5>
                <p>Your performance over all quizzes submitted</p>
              </div>
              <div class="chart-body">
                <canvas ref="progressChart" height="300"></canvas>
              </div>
            </div>
          </div>
          <div class="col-12 col-lg-4">
            <div class="target-card">
              <div class="target-header">
                <h5><i class="fas fa-target me-2"></i>Weekly Target</h5>
              </div>
              <div class="target-body">
                <div class="target-visual">
                  <div class="target-circle">
                    <div class="target-progress" :style="{ '--progress': (stats.totalQuizzes / stats.weeklyTarget) * 100 + '%' }">
                      <span class="target-percentage">{{ Math.round((stats.totalQuizzes / stats.weeklyTarget) * 100) }}%</span>
                    </div>
                  </div>
                </div>
                <div class="target-info">
                  <div class="target-stat">
                    <span class="target-current">{{ stats.totalQuizzes }}</span>
                    <span class="target-total">/ {{ stats.weeklyTarget }}</span>
                  </div>
                  <div class="target-label">Quizzes this week</div>
                </div>
                <div class="streak-info">
                  <i class="fas fa-fire"></i>
                  <span>{{ stats.streak }} day streak!</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="content-section mb-5">
        <div class="row g-4"> 
          <!---
          Subject
          <div class="col-12 col-xl-8">
            <div class="section-card">
              <div class="section-header">
                <h5><i class="fas fa-layer-group me-2"></i>Your Subjects</h5>
                <p>Explore your learning materials</p>
              </div>
              <div class="subjects-grid">
                <div
                  v-for="subject in subjects"
                  :key="subject.id"
                  class="subject-card"
                >
                  <div class="subject-icon" :style="{ color: subject.color }">
                    <i :class="subject.icon"></i>
                  </div>
                  <div class="subject-info">
                    <h6>{{ subject.name }}</h6>
                    <div class="subject-stats">
                      <span>{{ subject.chapters }} chapters</span>
                      <span>{{ subject.quizzes }} quizzes</span>
                    </div>
                  </div>
                  <router-link
                    :to="`/subjects/${subject.id}/chapters`"
                    class="subject-btn"
                  >
                    Explore <i class="fas fa-arrow-right ms-1"></i>
                  </router-link>
                </div>
              </div>
            </div>
          </div> -->

          <!-- Recommendations Section (now main content, not sidebar) -->
          <div class="suggestions-section mb-5" v-if="suggested.length">
            <div class="section-card">
              <div class="section-header" style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                  <h5><i class="fas fa-star me-2"></i>Recommended for You</h5>
                  <p>Based on your learning progress</p>
                </div>
                <router-link
                  :to="`/user/subjects/${userId}`"
                  class="suggestion-btn"
                  style="margin-left: 1rem; white-space: nowrap;"
                >
                  Explore All <i class="fas fa-arrow-right ms-1"></i>
                </router-link>
              </div>
              <div class="suggestions-grid">
                <div
                  v-for="quiz in suggested"
                  :key="quiz.id"
                  class="suggestion-card"
                >
                  <div class="suggestion-badge">
                    <i class="fas fa-star"></i>
                    Recommended
                  </div>
                  <div class="suggestion-content">
                    <h6>{{ quiz.title }}</h6>
                    <p>{{ quiz.chapterName }}</p>
                    <router-link
                      :to="`/quizzes/${quiz.id}/start`"
                      class="suggestion-btn"
                    >
                      Start Quiz <i class="fas fa-arrow-right ms-1"></i>
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Sidebar (now after recommendations) -->
          <div class="col-12 col-xl-4">
            <!-- In Progress -->
            <div class="section-card mb-4" v-if="inProgress.length">
              <div class="section-header">
                <h6>
                  <i class="fas fa-play-circle me-2"></i>Continue Learning
                </h6>
              </div>
              <div class="progress-list">
                <div
                  v-for="item in inProgress"
                  :key="item.quizId"
                  class="progress-item"
                >
                  <div class="progress-info">
                    <div class="progress-title">{{ item.chapterName }}</div>
                    <div class="progress-subtitle">{{ item.quizTitle }}</div>
                  </div>
                  <router-link
                    :to="`/quizzes/${item.quizId}/resume`"
                    class="progress-btn"
                  >
                    <i class="fas fa-play"></i>
                  </router-link>
                </div>
              </div>
            </div>

            <!-- Announcements -->
            <div class="section-card" v-if="announcements.length">
              <div class="section-header">
                <h6><i class="fas fa-bullhorn me-2"></i>Latest Updates</h6>
              </div>
              <div class="announcements-list">
                <div
                  v-for="announcement in announcements"
                  :key="announcement.id"
                  class="announcement-item"
                >
                  <div class="announcement-icon">
                    <i class="fas fa-info-circle"></i>
                  </div>
                  <div class="announcement-content">
                    <h6>{{ announcement.title }}</h6>
                    <p>{{ announcement.message }}</p>
                    <span class="announcement-date">{{
                      announcement.date
                    }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- Activity Table -->
          <div class="col-12 mt-4">
            <div class="section-card">
              <div class="section-header">
                <h5><i class="fas fa-history me-2"></i>Recent Activity</h5>
                <p>Your latest quiz results</p>
              </div>
              <div class="activity-table-wrapper">
                <table class="activity-table">
                  <thead>
                    <tr>
                      <th>Score</th>
                      <th>Date</th>
                      <th>Quiz</th>
                      <th>View</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="activity in recentActivity" :key="activity.id">
                      <td>
                        <span
                          class="score-badge"
                          :class="getScoreClass(activity.score)"
                        >
                          {{ activity.score }}%
                        </span>
                      </td>
                      <td>
                        <span class="activity-date">{{ activity.date }}</span>
                      </td>
                      <td>
                        <span class="activity-quiz">{{ activity.quizTitle }}</span>
                      </td>
                      <td>
                        <router-link
                          :to="`/quizzes/${activity.quizId}/results`"
                          class="activity-btn"
                        >
                          <i class="fas fa-eye"></i>
                        </router-link>
                      </td>
                    </tr>
                    <tr v-if="recentActivity.length === 0">
                      <td colspan="4" class="empty-state">
                        <i class="fas fa-inbox"></i>
                        <div>No activity yet</div>
                        <small>Start taking quizzes to see your progress</small>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
          <!-- End Activity Table -->
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue";
import Chart from "chart.js/auto";

import { useRoute, useRouter } from "vue-router";
const route = useRoute();
const router = useRouter();
const userId = route.params.userid;

import api from "../../api"; // adjust path as needed

const user = ref({});

const editUser = ref({ ...user.value });
const profileEdit = ref(false);
const isLoading = ref(false);
const error = ref(null);

async function fetchUserProfile() {
  try {
    isLoading.value = true;
    error.value = null;
    const res = await api.get(`auth/profile/${userId}`);
    user.value = { ...res.data };
  } catch (e) {
    error.value = "Failed to load user profile";
    console.error("Error fetching user profile:", e);
  } finally {
    isLoading.value = false;
  }
}

onMounted(fetchUserProfile);

function startProfileEdit() {
  editUser.value = { ...user.value };
  profileEdit.value = true;
}

async function saveProfile() {
  try {
    isLoading.value = true;
    error.value = null;
    await api.put(`/auth/profile/${userId}`, {
      name: editUser.value.name,
      qualification: editUser.value.qualification,
    });
    await fetchUserProfile();
    profileEdit.value = false;
  } catch (e) {
    error.value = "Failed to update profile";
    console.error("Error updating profile:", e);
  } finally {
    isLoading.value = false;
  }
}

function cancelProfileEdit() {
  profileEdit.value = false;
  error.value = null;
}

// Logout function
function logout() {
 localStorage.removeItem('token');
  router.push("/login");
}

function getScoreClass(score) {
  if (score >= 90) return "score-excellent";
  if (score >= 80) return "score-good";
  if (score >= 70) return "score-average";
  return "score-poor";
}

const greeting = ref("");
const currentDate = ref("");

// Tip of the Day logic
const tips = [
  "Consistency beats intensity.",
  "Every day is a new opportunity to learn.",
  "Small steps every day lead to big results.",
  "Mistakes are proof that you are trying.",
  "Stay curious and keep exploring.",
  "Believe in yourself and all that you are.",
  "Success is the sum of small efforts repeated.",
  "Learning never exhausts the mind.",
  "Progress, not perfection.",
  "Your only limit is your mind.",
  "Dream big, work hard, stay focused.",
  "The expert in anything was once a beginner.",
  "Push yourself, because no one else is going to do it for you.",
  "Don’t watch the clock; do what it does. Keep going.",
  "You don’t have to be perfect to be amazing."
];

function getTipOfTheDay() {
  // Use the current date as a seed to pick a tip for the day
  const today = new Date();
  // Format: YYYYMMDD
  const dateSeed = today.getFullYear() * 10000 + (today.getMonth() + 1) * 100 + today.getDate();
  // Simple deterministic "random" index based on date
  const index = dateSeed % tips.length;
  return tips[index];
}

const tipOfTheDay = ref("");

// --- REWRITE: Fetch stats from backend using @models.py and @authRoute.py ---
const stats = ref({
  totalQuizzes: 0,
  avgScore: 0,
  subjectsAttempted: 0,
  streak: 0,
  weeklyTarget: 7,
});

// --- Progress Chart Data for ALL quizzes submitted ---
const progressData = ref([]);
const progressLabels = ref([]);

// Helper to get weekday name from date (0=Sun, 1=Mon, ..., 6=Sat)
function getWeekdayName(date) {
  return ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][date.getDay()];
}

async function fetchUserStats() {
  try {
    // Fetch all quizzes, subjects, and results from backend
    const [quizzesRes, subjectsRes, resultsRes] = await Promise.all([
      api.get('/auth/quizzes'),
      api.get('/auth/subjects'),
      api.get('/auth/results'),
    ]);

    // Filter results for this user
    // Ensure both r.user_id and userId are the same type (number)
    const userResults = resultsRes.data.results
      .filter(r => Number(r.user_id) === Number(userId))
      .sort((a, b) => new Date(a.created_at) - new Date(b.created_at)); // sort by date ascending

    // Total quizzes submitted by user
    const totalQuizzes = userResults.length;

    // Average score (rounded to nearest integer)
    const avgScore = totalQuizzes
      ? Math.round(userResults.reduce((sum, r) => sum + (r.score || 0), 0) / totalQuizzes)
      : 0;

    // Subjects attempted (unique subject_ids in user's results)
    const subjectIds = new Set(userResults.map(r => r.subject_id));
    const subjectsAttempted = subjectIds.size;

    // Day streak: count consecutive days with at least one quiz result
    const dates = userResults
      .map(r => r.created_at ? new Date(r.created_at).toDateString() : null)
      .filter(Boolean);
    const uniqueDates = Array.from(new Set(dates)).sort((a, b) => new Date(b) - new Date(a));
    let streak = 0;
    let current = new Date();
    for (let i = 0; i < uniqueDates.length; i++) {
      if (new Date(uniqueDates[i]).toDateString() === current.toDateString()) {
        streak++;
        current.setDate(current.getDate() - 1);
      } else {
        break;
      }
    }

    stats.value = {
      totalQuizzes,
      avgScore,
      subjectsAttempted,
      streak,
      weeklyTarget: 7,
    };

    // --- Progress graph: show all user quiz scores from the beginning ---
    // Each point: label = date (YYYY-MM-DD), value = score
    progressData.value = userResults.map(r => r.score || 0);
    progressLabels.value = userResults.map(r => {
      if (r.created_at) {
        // Format as "YYYY-MM-DD"
        return r.created_at.slice(0, 10);
      }
      return "";
    });
    // If you need to use created_at instead of date_submitted, this is already correct.

    // If you want to update recentActivity to use created_at instead of date_submitted:
    // (Assuming you want to show the 5 most recent activities)
    recentActivity.value = userResults
      .slice(-5)
      .reverse()
      .map((r, idx) => ({
        id: r.id || idx,
        quizId: r.quiz_id,
        quizTitle: r.quiz_title || "Quiz",
        score: r.score,
        date: r.created_at ? r.created_at.slice(0, 10) : "",
      }));

    // If you want to update inProgress as well, you can do so here if needed.

    // console.log(userResults)
  } catch (e) {
    // fallback: keep stats as 0
    console.error("Failed to fetch user stats", e);
  }
}

onMounted(() => {
  greeting.value = getGreeting();
  currentDate.value = new Date().toLocaleDateString(undefined, {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  tipOfTheDay.value = getTipOfTheDay();

  fetchUserStats().then(() => {
    // Render progress chart after data is ready
    nextTick(() => {
      const ctx = document.querySelector("canvas");
      if (ctx) {
        new Chart(ctx, {
          type: "line",
          data: {
            labels: progressLabels.value,
            datasets: [
              {
                label: "Score (%)",
                data: progressData.value,
                borderColor: "#3b82f6",
                backgroundColor: "rgba(59,130,246,0.1)",
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointBackgroundColor: "#3b82f6",
                pointBorderColor: "#fff",
                pointBorderWidth: 3,
                pointRadius: 6,
                pointHoverRadius: 8,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { display: false },
              tooltip: {
                callbacks: {
                  title: function(context) {
                    // Show date in tooltip
                    return "Date: " + context[0].label;
                  },
                  label: function(context) {
                    return "Score: " + context.parsed.y + "%";
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
                  text: "Quiz Submission Date",
                  color: "#6b7280",
                  font: { weight: "bold" }
                }
              },
              y: {
                beginAtZero: true,
                max: 100,
                grid: {
                  color: "#f3f4f6",
                  drawBorder: false,
                },
                border: { display: false },
                ticks: {
                  color: "#6b7280",
                  callback: function (value) {
                    return value + "%";
                  },
                },
                title: {
                  display: true,
                  text: "Score (%)",
                  color: "#6b7280",
                  font: { weight: "bold" }
                }
              },
            },
          },
        });
      }
    });
  });
});

const subjects = ref([
  {
    id: 1,
    name: "Mathematics",
    chapters: 8,
    quizzes: 12,
    icon: "fas fa-calculator",
    color: "#3b82f6",
  },
  {
    id: 2,
    name: "Science",
    chapters: 7,
    quizzes: 10,
    icon: "fas fa-flask",
    color: "#10b981",
  },
]);

const inProgress = ref([
  { quizId: 101, quizTitle: "Algebra Basics", chapterName: "Algebra" },
  { quizId: 102, quizTitle: "Photosynthesis", chapterName: "Biology" },
]);

const recentActivity = ref([
  // This will be overwritten by fetchUserStats to use created_at
]);

const announcements = ref([
  {
    id: 1,
    title: "New Quizzes Added!",
    message: "Check out the latest quizzes in Science.",
    date: "2024-06-10",
  },
  {
    id: 2,
    title: "Maintenance Notice",
    message: "Platform will be down for maintenance on June 12.",
    date: "2024-06-09",
  },
]);

const suggested = ref([
  { id: 301, title: "Trigonometry", chapterName: "Mathematics" },
  { id: 302, title: "Chemical Reactions", chapterName: "Science" },
]);

function getGreeting() {
  const hour = new Date().getHours();
  if (hour < 12) return "Good morning";
  if (hour < 18) return "Good afternoon";
  return "Good evening";
}
</script>

<style scoped>
.progress-dates-list {
  font-size: 0.95rem;
  color: #374151;
}
.progress-dates-label {
  margin-bottom: 0.25rem;
}
.progress-dates-ul {
  list-style: none;
  padding-left: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem 1.5rem;
}
.progress-date-label {
  font-family: monospace;
  color: #2563eb;
  margin-right: 0.25em;
}
.progress-date-score {
  color: #6b7280;
}
</style>

<style scoped>
.dashboard-section {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  min-height: 100vh;
  padding: 2rem 0;
}

.container-fluid {
  max-width: 1400px;
  padding: 0 1.5rem;
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

.btn-edit {
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
  color: #6b7280;
}

.btn-edit:hover {
  background: #3b82f6;
  color: white;
}

/* Logout Button */
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

.profile-edit {
  animation: slideIn 0.3s ease;
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

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  font-size: 0.9rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.btn-cancel,
.btn-save {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-cancel {
  background: #f3f4f6;
  color: #6b7280;
}

.btn-cancel:hover {
  background: #e5e7eb;
}

.btn-save {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
}

.btn-save:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
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

/* Charts Section */
.charts-section {
  margin-bottom: 3rem;
}

.chart-card,
.target-card {
  background: white;
  border-radius: 1.25rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  height: 100%;
}

.chart-header,
.target-header {
  padding: 1.5rem 1.5rem 0 1.5rem;
}

.chart-header h5,
.target-header h5 {
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

.chart-body {
  padding: 1rem 1.5rem 1.5rem 1.5rem;
  height: 300px;
}

.target-body {
  padding: 1rem 1.5rem 1.5rem 1.5rem;
  text-align: center;
}

.target-visual {
  margin-bottom: 2rem;
}

.target-circle {
  width: 120px;
  height: 120px;
  margin: 0 auto;
  position: relative;
  background: conic-gradient(
    from 0deg,
    #3b82f6 0deg,
    #3b82f6 var(--progress, 0deg),
    #e5e7eb var(--progress, 0deg),
    #e5e7eb 360deg
  );
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.target-circle::before {
  content: "";
  position: absolute;
  width: 80px;
  height: 80px;
  background: white;
  border-radius: 50%;
}

.target-progress {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.target-percentage {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
}

.target-info {
  margin-bottom: 1.5rem;
}

.target-stat {
  margin-bottom: 0.5rem;
}

.target-current {
  font-size: 2rem;
  font-weight: 700;
  color: #3b82f6;
}

.target-total {
  font-size: 1.2rem;
  color: #6b7280;
}

.target-label {
  font-size: 0.9rem;
  color: #6b7280;
}

.streak-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
  padding: 0.75rem;
  border-radius: 0.75rem;
  font-weight: 600;
}

/* Content Section */
.content-section {
  margin-bottom: 3rem;
  height: auto;
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

/* Subjects Grid */
.subjects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.subject-card {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 1rem;
  padding: 1.5rem;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.subject-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  border-color: #e5e7eb;
}

.subject-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.subject-info h6 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.subject-stats {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.subject-stats span {
  font-size: 0.85rem;
  color: #6b7280;
  background: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.5rem;
}

.subject-btn {
  display: inline-flex;
  align-items: center;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  padding: 0.75rem 1.25rem;
  border-radius: 0.75rem;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.subject-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
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

.progress-btn {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  transition: all 0.3s ease;
}

.progress-btn:hover {
  transform: scale(1.1);
  color: white;
  text-decoration: none;
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

/* Suggestions Section */
.suggestions-section {
  margin-bottom: 3rem;
}

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

/* Activity Section */
.activity-table-wrapper {
  overflow-x: auto;
}

.activity-table {
  width: 100%;
  border-collapse: collapse;
}

.activity-table th {
  background: #f8fafc;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
  border-bottom: 2px solid #e5e7eb;
}

.activity-table td {
  padding: 1rem;
  border-bottom: 1px solid #f3f4f6;
  vertical-align: middle;
}

.activity-quiz {
  font-weight: 500;
  color: #1f2937;
}

.score-badge {
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.85rem;
  font-weight: 600;
}

.score-excellent {
  background: #d1fae5;
  color: #065f46;
}

.score-good {
  background: #dbeafe;
  color: #1e40af;
}

.score-average {
  background: #fef3c7;
  color: #92400e;
}

.score-poor {
  background: #fee2e2;
  color: #991b1b;
}

.activity-date {
  font-size: 0.9rem;
  color: #6b7280;
}

.activity-btn {
  width: 35px;
  height: 35px;
  background: #f3f4f6;
  color: #6b7280;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  transition: all 0.3s ease;
}

.activity-btn:hover {
  background: #3b82f6;
  color: white;
  text-decoration: none;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #9ca3af;
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
}

.empty-state div {
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.empty-state small {
  font-size: 0.85rem;
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
  .container-fluid {
    padding: 0 1rem;
  }

  .dashboard-section {
    padding: 1rem 0;
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

  .subjects-grid {
    grid-template-columns: 1fr;
  }

  .suggestions-grid {
    grid-template-columns: 1fr;
  }

  .profile-card {
    max-width: 100%;
  }

  .target-circle {
    width: 100px;
    height: 100px;
  }

  .target-circle::before {
    width: 70px;
    height: 70px;
  }

  .target-percentage {
    font-size: 1.25rem;
  }
}

@media (max-width: 576px) {
  .profile-avatar {
    font-size: 3rem;
  }

  .stat-icon {
    width: 50px;
    height: 50px;
    font-size: 1.25rem;
  }

  .chart-body {
    height: 250px;
  }

  .activity-table th,
  .activity-table td {
    padding: 0.75rem 0.5rem;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>
