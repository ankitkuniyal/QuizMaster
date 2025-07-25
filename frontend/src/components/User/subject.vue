<template>
  <section class="dashboard-section">
    <div class="container-fluid">
      <!-- Header Section -->
      <div class="dashboard-header">
        <div class="row align-items-center">
          <div class="col-12 d-flex justify-content-between align-items-center">
            <div class="welcome-content">
              <h1 class="welcome-title">Explore Subjects</h1>
              <p class="welcome-subtitle">
                Browse all available subjects, chapters, and quizzes.
              </p>
            </div>
            <nav class="ms-3">
              <a
                :href="`/dashboard/user/${userID}`"
                class="btn-dashboard"
                title="Go to Dashboard"
              >
                <i class="fas fa-tachometer-alt me-2"></i>
                Dashboard
              </a>
            </nav>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="content-section ">
        <div class="row g-4">
          <div class="col-12">
            <div class="section-card">
              <div class="section-header">
                <h5><i class="fas fa-layer-group me-2"></i>All Subjects</h5>
                <p>Explore all learning materials organized by subjects</p>
              </div>
              
              <!-- Search and Filter -->
              <div class="search-section mb-4">
                <div class="row g-3">
                  <div class="col-md-8">
                    <div class="search-input-wrapper">
                      <i class="fas fa-search search-icon"></i>
                      <input 
                        type="text" 
                        class="form-input search-input" 
                        placeholder="Search subjects, chapters, or quizzes..."
                        v-model="searchQuery"
                      >
                    </div>
                  </div>
                  <div class="col-md-4">
                    <select class="form-input" v-model="sortBy">
                      <option value="name">Sort by Name</option>
                      <option value="chapters">Sort by Chapters</option>
                      <option value="quizzes">Sort by Quizzes</option>
                    </select>
                  </div>
                </div>
              </div>

              <div class="subjects-grid">
                <div
                  v-for="subject in filteredSubjects"
                  :key="subject.id"
                  class="subject-card"
                  @click="handleSubjectClick(subject)"
                  style="cursor: pointer;"
                >
                  <div class="subject-header">
                    <div class="subject-icon" :style="{ color: getColor(subject.id) }">
                      <i :class="getIcon(subject.id)"></i>
                    </div>
                  </div>
                  
                  <div class="subject-info">
                    <h6>{{ subject.name }}</h6>
                    <p class="subject-description">{{ subject.description }}</p>
                    
                    <div class="subject-stats">
                      <span><i class="fas fa-book me-1"></i>{{ subject.chapters.length }} chapters</span>
                      <span><i class="fas fa-question-circle me-1"></i>{{ totalQuizzes(subject) }} quizzes</span>
                    </div>
                  </div>
                  
                  <div class="subject-footer">
                    <div class="subject-btn">
                      <i class="fas fa-play me-2"></i>
                      Start Learning
                    </div>
                    <span class="expand-arrow">
                      <i class="fas fa-chevron-right"></i>
                    </span>
                  </div>
                </div>
                
                <!-- Empty State -->
                <div v-if="filteredSubjects.length === 0" class="empty-state">
                  <i class="fas fa-search"></i>
                  <div>No subjects found</div>
                  <small>Try adjusting your search criteria</small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div> 

    <!-- Subject Details Modal -->
    <div v-if="showModal" class="modal-backdrop" @click.self="closeModal">
      <div class="modal-content-custom">
        <div class="modal-header-custom">
          <div class="modal-title">
            <div class="modal-icon" :style="{ color: getColor(selectedSubject.id) }">
              <i :class="getIcon(selectedSubject.id)"></i>
            </div>
            <div class="modal-title-text">
              <h4>{{ selectedSubject.name }}</h4>
              <p>{{ getSubjectDescription(selectedSubject.name) }}</p>
            </div>
          </div>
          <button class="close-btn" @click="closeModal">
            <i class="fas fa-times"></i>
          </button>
        </div>
        
        <div class="modal-body-custom">
          <div class="modal-left">
            <div class="modal-section">
              <h6><i class="fas fa-list me-2"></i>Chapters & Quizzes</h6>
              <div v-if="selectedSubject.chapters && selectedSubject.chapters.length" class="chapters-list">
                <div
                  v-for="(chapter, idx) in selectedSubject.chapters"
                  :key="chapter.id"
                  class="chapter-item"
                  @click="toggleChapter(idx)"
                >
                  <div class="chapter-header"  style="cursor:pointer;">
                    <RoundProgressBar
                      :progress="getChapterProgress(chapter)"
                      :size="36"
                      :stroke="5"
                      :color="getColor(selectedSubject.id)"
                      :bgColor="'#dbeafe'"
                      :label="''"
                      style="margin-right: 10px;"
                    />
                    <strong>{{ chapter.name }}</strong>
                    <span class="chapter-badge">{{ chapter.quizzes ? chapter.quizzes.length : 0 }} quizzes</span>
                    <span style="margin-left:auto;">
                      <i :class="openedChapters[idx] ? 'fas fa-chevron-down' : 'fas fa-chevron-right'"></i>
                    </span>
                  </div>
                  
                  <transition name="fade">
                    <div v-show="openedChapters[idx]" style="margin-top: 0.5rem;">
                      <div v-if="chapter.quizzes && chapter.quizzes.length" class="quizzes-list">
                        <div
                          v-for="quiz in chapter.quizzes"
                          :key="quiz.id"
                          class="quiz-item"
                        >
                          <router-link
                            :to="`/user/quizzes/${quiz.id}`"
                            class="quiz-link"
                            @click.stop
                            @mouseenter="showQuizScore(quiz.id)"
                            @mouseleave="hideQuizScore"
                          >
                            <div style="display:flex;align-items:center;gap:0.5rem;">
                              <i class="fas fa-play-circle me-2"></i>
                              {{ quiz.title }}
                            </div>
                            <span class="quiz-duration">
                              <i class="fas fa-clock me-1"></i>
                              {{Math.floor(quiz.duration/60)}} min
                            </span>
                            <!-- Show score always if available, and completed tag if submitted -->
                            <span
                              v-if="quizResults[quiz.id]"
                              class="quiz-score-tooltip"
                              style="margin-left:1rem; color:#10b981; font-weight:600;"
                            >
                              Score: {{ quizResults[quiz.id].score !== undefined ? quizResults[quiz.id].score + '%' : 'N/A' }}
                            </span>
                          </router-link>
                        </div>
                      </div>
                      <div v-else class="no-quizzes">
                        <i class="fas fa-info-circle me-2"></i>
                        No quizzes available in this chapter
                      </div>
                    </div>
                  </transition>
                </div>
              </div>
              <div v-else class="no-chapters">
                <i class="fas fa-folder me-2"></i>
                No chapters available for this subject
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, watch, defineComponent, h, watchEffect } from "vue";
import api from "../../api.js";
import { useRoute } from "vue-router";

// RoundProgressBar as a SFC-compatible component (no template string)
const RoundProgressBar = defineComponent({
  name: "RoundProgressBar",
  props: {
    progress: { type: Number, required: true },
    size: { type: Number, default: 60 },
    stroke: { type: Number, default: 8 },
    color: { type: String, default: "#3b82f6" },
    bgColor: { type: String, default: "#e5e7eb" },
    label: { type: String, default: "" }
  },
  setup(props) {
    const radius = computed(() => (props.size - props.stroke) / 2);
    const circumference = computed(() => 2 * Math.PI * radius.value);
    const dash = computed(() => (props.progress / 100) * circumference.value);

    return () =>
      h(
        "svg",
        {
          width: props.size,
          height: props.size,
          viewBox: `0 0 ${props.size} ${props.size}`
        },
        [
          h("circle", {
            cx: props.size / 2,
            cy: props.size / 2,
            r: radius.value,
            stroke: props.bgColor,
            "stroke-width": props.stroke,
            fill: "none"
          }),
          h("circle", {
            cx: props.size / 2,
            cy: props.size / 2,
            r: radius.value,
            stroke: props.color,
            "stroke-width": props.stroke,
            fill: "none",
            "stroke-linecap": "round",
            "stroke-dasharray": circumference.value,
            "stroke-dashoffset": circumference.value - dash.value,
            style: "transition: stroke-dashoffset 0.5s;"
          }),
          props.label
            ? h(
                "text",
                {
                  x: props.size / 2,
                  y: props.size / 2 + 5,
                  "text-anchor": "middle",
                  "font-size": 14,
                  fill: "#1f2937",
                  "font-weight": "bold"
                },
                props.label
              )
            : null
        ]
      );
  }
});

const route = useRoute();
const userID = route.params.userid;

const subjects = ref([]);
const showModal = ref(false);
const selectedSubject = ref({});
const searchQuery = ref('');
const sortBy = ref('name');

const openedChapters = ref([]); // For modal: which chapters are open
const hoveredQuizId = ref(null);

// New: quizResults will store { [quizId]: { score: number, submitted: boolean } }
const quizResults = ref({});

const recommendations = ref([
  {
    id: 1,
    title: "Complete Mathematics Basics",
    description: "Master fundamental mathematical concepts with interactive quizzes and step-by-step explanations."
  },
  {
    id: 2,
    title: "Science Lab Experiments",
    description: "Hands-on virtual experiments to understand scientific principles and methodology."
  },
  {
    id: 3,
    title: "Advanced Programming",
    description: "Take your coding skills to the next level with advanced algorithms and data structures."
  }
]);

// Computed properties
const totalChapters = computed(() => {
  return subjects.value.reduce((sum, subject) => sum + (subject.chapters ? subject.chapters.length : 0), 0);
});

const totalQuizzesCount = computed(() => {
  return subjects.value.reduce((sum, subject) => sum + totalQuizzes(subject), 0);
});

const filteredSubjects = computed(() => {
  let filtered = subjects.value.filter(subject =>
    subject.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );

  // Sort subjects
  filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'chapters':
        return (b.chapters?.length || 0) - (a.chapters?.length || 0);
      case 'quizzes':
        return totalQuizzes(b) - totalQuizzes(a);
      default:
        return a.name.localeCompare(b.name);
    }
  });

  return filtered;
});

// Methods
function handleSubjectClick(subject) {
  // Only one subject modal open at a time
  if (showModal.value && selectedSubject.value.id === subject.id) {
    closeModal();
  } else {
    openSubject(subject);
  }
}

function openSubject(subject) {
  selectedSubject.value = subject;
  showModal.value = true;
  // All chapters closed by default
  openedChapters.value = subject.chapters ? subject.chapters.map(() => false) : [];
  // No need to fetch quiz scores here, as all quiz results are loaded on mount
}

function closeModal() {
  showModal.value = false;
  hoveredQuizId.value = null;
}

function openSuggestion(suggestion) {
  // Handle suggestion click
  console.log('Opening suggestion:', suggestion.title);
}

const colorPalette = [
  "#3b82f6", "#10b981", "#06b6d4", "#f59e0b", "#ef4444", "#8b5cf6", "#f472b6", "#14b8a6"
];

const iconPalette = [
  "fas fa-flask", "fas fa-calculator", "fas fa-globe", "fas fa-book", 
  "fas fa-brain", "fas fa-laptop-code", "fas fa-atom", "fas fa-microscope"
];

function getColor(id) {
  return colorPalette[id % colorPalette.length];
}

function getIcon(id) {
  return iconPalette[id % iconPalette.length];
}

function totalQuizzes(subject) {
  return subject.chapters ? subject.chapters.reduce((sum, ch) => sum + (ch.quizzes ? ch.quizzes.length : 0), 0) : 0;
}

// --- Progress Calculation ---
function getChapterProgress(chapter) {
  // Calculate chapter progress as average of quiz scores (or 0 if none)
  if (!chapter.quizzes || !chapter.quizzes.length) return 0;
  let total = 0;
  let count = 0;
  for (const quiz of chapter.quizzes) {
    const result = quizResults.value[quiz.id];
    total += (result && typeof result.score === "number") ? result.score : 0;
    count++;
  }
  return count ? Math.round(total / count) : 0;
}

// --- Chapter Dropdown ---
function toggleChapter(idx) {
  openedChapters.value = openedChapters.value.map((open, i) => i === idx ? !open : false);
}

// --- Quiz Score Tooltip ---
function showQuizScore(quizId) {
  hoveredQuizId.value = quizId;
}
function hideQuizScore() {
  hoveredQuizId.value = null;
}

function getSubjectDescription(name) {
  const descriptions = {
    'Mathematics': 'Master numbers, equations, and mathematical reasoning',
    'Science': 'Explore the natural world through scientific inquiry',
    'History': 'Journey through time and understand human civilization',
    'Literature': 'Discover the beauty and power of written expression',
    'Physics': 'Understand the fundamental laws governing our universe',
    'Chemistry': 'Explore matter, energy, and chemical reactions',
    'Biology': 'Study living organisms and life processes',
    'Computer Science': 'Learn programming, algorithms, and digital systems'
  };
  return descriptions[name] || 'Expand your knowledge in this subject area';
}

// --- Freeze background when modal is open ---
watch(showModal, (val) => {
  if (val) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
});

// --- Fetch all quiz results for the user on mount ---
onMounted(async () => {
  try {
    // Get all subjects with chapters and quizzes
    const res = await api.get("/subjects/with-details");
    subjects.value = res.data;
    // Fetch all quiz results for this user
    const resultRes = await api.get(`/result/${userID}`);
    // resultRes.data is expected to be an array of objects like:
    // { quiz_id: number, score: number, submitted: boolean }
    // We'll map this to { [quizId]: { score, submitted } }
    const resultMap = {};
    if (Array.isArray(resultRes.data)) {
      for (const r of resultRes.data) {
        if (r.quiz_id !== undefined) {
          resultMap[r.quiz_id] = {
            score: r.score,
            submitted: !!r.submitted
          };
        }
      }
    }
    quizResults.value = resultMap;
  } catch (err) {
    console.error('Error loading subjects or results:', err);
    subjects.value = [];
    quizResults.value = {};
  }
});
</script>

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

.btn-dashboard {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
}

.btn-dashboard:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
  color: white;
  text-decoration: none;
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

.section-header h5 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.section-header p {
  font-size: 0.9rem;
  color: #6b7280;
  margin-bottom: 0;
}

/* Search Section */
.search-section {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 1rem;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.search-input-wrapper {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #6b7280;
}

.search-input {
  padding-left: 2.5rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  background: white;
  padding-left: 40px;
}

.form-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Subjects Grid */
.subjects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
}

.subject-card {
  background: white;
  border-radius: 1.25rem;
  padding: 1.5rem;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.subject-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
  border-color: #e5e7eb;
}

.subject-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.subject-icon {
  font-size: 2.5rem;
  margin-bottom: 0;
}

.subject-badge {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.subject-info {
  margin-bottom: 1.5rem;
}

.subject-info h6 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.subject-description {
  font-size: 0.9rem;
  color: #6b7280;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.subject-stats {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.subject-stats span {
  font-size: 0.85rem;
  color: #6b7280;
  background: #f8fafc;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
}

.subject-progress {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.progress-bar-container {
  flex: 1;
  height: 6px;
  background: #e5e7eb;
  border-radius: 3px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.8rem;
  color: #6b7280;
  font-weight: 500;
}

.subject-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.subject-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  padding: 0.75rem 1.25rem;
  border-radius: 0.75rem;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
}

.expand-arrow {
  color: #6b7280;
  font-size: 1.25rem;
  transition: all 0.3s ease;
}

.subject-card:hover .expand-arrow {
  transform: translateX(4px);
  color: #3b82f6;
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
  background: white;
  border-radius: 1.25rem;
  padding: 1.5rem;
  position: relative;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.suggestion-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
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
  text-align: center;
}

.suggestion-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.suggestion-content h6 {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.75rem;
}

.suggestion-content p {
  font-size: 0.9rem;
  color: #6b7280;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}
/* Continuing from suggestion-btn */
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

/* Empty State */
.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #6b7280;
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #d1d5db;
}

.empty-state div {
  font-size: 1.1rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.empty-state small {
  font-size: 0.9rem;
  color: #9ca3af;
}

/* Modal Styles */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content-custom {
  background: white;
  border-radius: 1.5rem;
  width: 100%;
  max-width: 900px;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header-custom {
  padding: 2rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

.modal-title {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.modal-icon {
  font-size: 2.5rem;
}

.modal-title-text h4 {
  font-weight: 600;
  color: #1f2937;
  margin: 0;
  margin-bottom: 0.25rem;
}

.modal-title-text p {
  color: #6b7280;
  margin: 0;
  font-size: 0.95rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6b7280;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.5rem;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: #f3f4f6;
  color: #1f2937;
}

.modal-body-custom {
  display: flex;
  height: 500px;
  overflow: hidden;
}

.modal-left {
  flex: 2;
  padding: 2rem;
  overflow-y: auto;
  border-right: 1px solid #e5e7eb;
}

.modal-right {
  flex: 1;
  padding: 2rem;
  background: #f8fafc;
  overflow-y: auto;
}

.modal-section {
  margin-bottom: 2rem;
}

.modal-section:last-child {
  margin-bottom: 0;
}

.modal-section h6 {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
  font-size: 1rem;
}

/* Chapters and Quizzes */


.chapter-item {
  background: #f8fafc;
  border-radius: 1rem;
  padding: 1.5rem;
  margin-bottom: 1rem;
  border: 1px solid #e5e7eb;
}

.chapter-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.chapter-header strong {
  color: #1f2937;
  font-weight: 600;
  flex: 1;
  min-width: 0;
}

.chapter-badge {
  background: #dbeafe;
  color: #1d4ed8;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  font-weight: 500;
}

.quizzes-list {
  padding-left: 1rem;
  border-left: 3px solid #e5e7eb;
  margin-left: 1rem;
}

.quiz-item {
  margin-bottom: 0.75rem;
}

.quiz-link {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: white;
  border-radius: 0.75rem;
  text-decoration: none;
  color: #374151;
  transition: all 0.3s ease;
  border: 1px solid #e5e7eb;
}

.quiz-link:hover {
  background: #3b82f6;
  color: white;
  text-decoration: none;
  transform: translateX(4px);
}

.quiz-duration {
  font-size: 0.8rem;
  color: inherit;
  opacity: 0.7;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.no-quizzes,
.no-chapters {
  text-align: center;
  padding: 2rem 1rem;
  color: #6b7280;
  background: #f9fafb;
  border-radius: 0.75rem;
  border: 2px dashed #d1d5db;
}

/* Modal Actions */
.modal-actions {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.explore-btn {
  display: inline-flex;
  align-items: center;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  padding: 1rem 2rem;
  border-radius: 0.75rem;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  width: 100%;
  justify-content: center;
}

.explore-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
  color: white;
  text-decoration: none;
}

/* Progress Overview */
.progress-overview {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 1rem;
  border: 1px solid #e5e7eb;
}

.progress-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: conic-gradient(#3b82f6 0deg, #3b82f6 180deg, #e5e7eb 180deg, #e5e7eb 360deg);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  flex-shrink: 0;
}

.progress-circle::before {
  content: '';
  position: absolute;
  width: 60px;
  height: 60px;
  background: white;
  border-radius: 50%;
}

.progress-value {
  position: relative;
  z-index: 1;
  font-weight: 700;
  color: #1f2937;
  font-size: 1rem;
}

.progress-stats {
  display: flex;
  gap: 1.5rem;
  flex: 1;
}

.progress-stat {
  text-align: center;
  flex: 1;
}

.stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.9rem;
  color: #6b7280;
  font-weight: 500;
}

/* Recent Activity */
.recent-activity {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  border: 1px solid #e5e7eb;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f3f4f6;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-item span {
  flex: 1;
  font-size: 0.9rem;
  color: #374151;
}

.activity-item small {
  font-size: 0.8rem;
  color: #9ca3af;
}

/* Responsive Design */
@media (max-width: 768px) {
  .container-fluid {
    padding: 0 1rem;
  }

  .welcome-title {
    font-size: 2rem;
  }

  .welcome-subtitle {
    font-size: 1rem;
  }

  .subjects-grid {
    grid-template-columns: 1fr;
  }

  .suggestions-grid {
    grid-template-columns: 1fr;
  }

  .stat-card {
    padding: 1.5rem;
  }

  .stat-number {
    font-size: 2rem;
  }

  .modal-content-custom {
    max-width: 95vw;
    margin: 1rem;
  }

  .modal-body-custom {
    flex-direction: column;
    height: auto;
    max-height: 60vh;
  }

  .modal-left,
  .modal-right {
    flex: none;
  }

  .modal-right {
    border-right: none;
    border-top: 1px solid #e5e7eb;
  }

  .progress-overview {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .progress-stats {
    justify-content: center;
  }

  .search-section .row {
    flex-direction: column;
  }

  .search-section .col-md-8,
  .search-section .col-md-4 {
    width: 100%;
    margin-bottom: 1rem;
  }

  .search-section .col-md-4 {
    margin-bottom: 0;
  }
}

@media (max-width: 480px) {
  .dashboard-section {
    padding: 1rem 0;
  }

  .welcome-title {
    font-size: 1.75rem;
  }

  .stat-card {
    padding: 1rem;
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .stat-icon {
    width: 50px;
    height: 50px;
  }

  .stat-number {
    font-size: 1.75rem;
  }

  .subject-card {
    padding: 1rem;
  }

  .subject-footer {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .subject-btn {
    justify-content: center;
  }

  .modal-header-custom {
    padding: 1.5rem;
  }

  .modal-left,
  .modal-right {
    padding: 1.5rem;
  }

  .tip-card {
    padding: 0.75rem;
  }

  .tip-icon {
    width: 35px;
    height: 35px;
  }
}

/* Custom Scrollbar */
.modal-left::-webkit-scrollbar,
.modal-right::-webkit-scrollbar {
  width: 6px;
}

.modal-left::-webkit-scrollbar-track,
.modal-right::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.modal-left::-webkit-scrollbar-thumb,
.modal-right::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.modal-left::-webkit-scrollbar-thumb:hover,
.modal-right::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Utility Classes */
.text-success {
  color: #10b981;
}

.text-primary {
  color: #3b82f6;
}

/* Animation for loading states */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in-up {
  animation: fadeInUp 0.6s ease-out;
}

/* Loading spinner */
.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e5e7eb;
  border-left: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 2rem auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>