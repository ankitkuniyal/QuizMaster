<template>
  <section class="dashboard-section">
    <!-- Toast Notification -->
    <transition name="fade">
      <div v-if="toast.show" class="custom-toast">
        <i class="fas fa-check-circle me-2"></i>
        {{ toast.message }}
      </div>
    </transition>

    <div class="container-fluid">
      <!-- Header Section -->
      <div class="dashboard-header">
        <div class="row align-items-center">
          <div class="col-12 col-lg-7">
            <div class="welcome-content">
              <h1 class="welcome-title">Quiz Management 👨‍🏫</h1>
              <p class="welcome-subtitle">
                Organize your learning materials and quizzes
              </p>
            </div>
          </div>
          <div class="col-12 col-lg-5 d-flex justify-content-lg-end align-items-center mt-3 mt-lg-0">
            <router-link to="/dashboard/admin" class="btn btn-accent">
              <i class="fas fa-tachometer-alt me-1"></i>
              Dashboard
            </router-link>
          </div>
        </div>
      </div>

      <!-- Info Bar -->
      <div class="row mb-4">
        <div class="col-lg-10">
          <div class="d-flex align-items-stretch gap-3 flex-wrap flex-md-nowrap">
            <!-- Info Bar: 30% width -->
            <div class="stat-card stat-primary d-flex align-items-center justify-content-center mb-0" style="flex: 0 0 30%; max-width: 30%; min-width: 220px; height: 110px;">
              <div>
                <div class="d-flex align-items-center gap-2 mb-2">
                  <i class="fas fa-book-open text-white"></i>
                  <span class="stat-label">Subject:</span>
                  <span v-if="subjectName" class="ms-1 text-white">{{ subjectName }}</span>
                  <span v-else class="ms-1 text-white"><i class="fas fa-spinner fa-spin"></i> Loading...</span>
                </div>
                <div class="d-flex align-items-center gap-2 mb-2">
                  <i class="fas fa-layer-group text-white"></i>
                  <span class="stat-label">Chapter:</span>
                  <span v-if="chapterName" class="ms-1 text-white">{{ chapterName }}</span>
                  <span v-else class="ms-1 text-white"><i class="fas fa-spinner fa-spin"></i> Loading...</span>
                </div>
                <div class="d-flex align-items-center gap-2">
                  <i class="fas fa-clipboard-list text-white"></i>
                  <span class="stat-label">Quiz:</span>
                  <span v-if="quizName" class="ms-1 text-white">{{ quizName }}</span>
                  <span v-else class="ms-1 text-white"><i class="fas fa-spinner fa-spin"></i> Loading...</span>
                </div>
              </div>
            </div>
            <!-- Search Bar: 70% width -->
            <div class="info-bar bg-white rounded-4 shadow-sm px-3 d-flex align-items-center gap-3 flex-grow-1" style="flex: 0 0 70%;  min-width: 89%; height: 110px; ">
              <input
                v-model="searchQuery"
                type="text"
                class="form-control"
                placeholder="Search questions..."
                style="width: 70%; min-width: 0; border: none; outline: none; box-shadow: none; font-size: large;"
                @focus="event => event.target.style.boxShadow = 'none'"
                @blur="event => event.target.style.boxShadow = 'none'"
              />
              <select v-model="searchDifficulty" class="form-select" style="width: 30%; min-width: 120px;">
                <option value="">All Difficulties</option>
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="content-section mb-5">
        <div class="row g-4">
          <!-- Questions Sidebar -->
          <div class="col-lg-3">
            <div class="section-card h-100" style="overflow-y: auto; max-height: 600px;">
              <div class="section-header">
                <h5><i class="fas fa-list-ol me-2"></i>Questions</h5>
                <p>{{ filteredQuestions.length }} question(s) found</p>
              </div>
              <div class="progress-list hide-scrollbar" style="overflow-y: auto; max-height: 450px;">
                <div
                  v-for="(question, idx) in filteredQuestions"
                  :key="question.id"
                  class="progress-item"
                  :class="{ active: idx === currentQuestionIndex }"
                  @click="handleSidebarSelect(idx)"
                  style="word-break: break-word;"
                >
                  <div class="progress-info">
                    <div class="progress-title" style="white-space: normal; overflow: hidden; text-overflow: ellipsis;">
                      Q{{ idx + 1 }}: {{ question.text.length > 30 ? question.text.slice(0, 30) + '...' : question.text }}
                    </div>
                    <div class="progress-subtitle">
                      <span class="badge me-2" :class="{
                        'bg-success': question.difficulty === 'easy',
                        'bg-warning text-dark': question.difficulty === 'medium',
                        'bg-danger': question.difficulty === 'hard'
                      }">
                        {{ question.difficulty ? question.difficulty.charAt(0).toUpperCase() + question.difficulty.slice(1) : '' }}
                      </span>
                    </div>
                  </div>
                  <i class="fas fa-chevron-right"></i>
                </div>
                <div v-if="filteredQuestions.length === 0" class="alert alert-info text-center mt-3">
                  No questions found
                </div>
              </div>
            </div>
          </div>

          <!-- Question Editor -->
          <div class="col-lg-9">
            <div class="section-card">
              <div v-if="currentQuestionIndex === -1">
                <div class="section-header">
                  <h5><i class="fas fa-plus-circle me-2"></i>Add New Question</h5>
                  <p>Create a new question for this quiz</p>
                </div>
                <form @submit.prevent="addQuestion" class="mb-4">
                  <div class="mb-3">
                    <label class="form-label fw-semibold">Question Text</label>
                    <input v-model="newQuestion.text" type="text" class="form-control" placeholder="Enter question" required />
                  </div>
                  <div class="mb-3">
                    <label class="form-label fw-semibold">Options</label>
                    <div v-for="(option, idx) in newQuestion.options" :key="idx" class="input-group mb-2">
                      <input
                        v-model="newQuestion.options[idx].text"
                        type="text"
                        class="form-control"
                        :placeholder="`Option ${idx + 1}`"
                        required
                      />
                      <div class="input-group-text">
                        <input
                          type="radio"
                          :name="'correctOption'"
                          :checked="newQuestion.correctIndex === idx"
                          @change="newQuestion.correctIndex = idx"
                          aria-label="Select as correct answer"
                        />
                      </div>
                    </div>
                  </div>
                  <div class="mb-3">
                    <label class="form-label fw-semibold">Difficulty</label>
                    <select v-model="newQuestion.difficulty" class="form-select" required>
                      <option disabled value="">Select difficulty</option>
                      <option value="easy">Easy</option>
                      <option value="medium">Medium</option>
                      <option value="hard">Hard</option>
                    </select>
                  </div>
                  <button type="submit" class="btn btn-accent" :disabled="addingQuestion">
                    <i class="fas fa-plus me-1"></i>
                    <span v-if="addingQuestion">Adding...</span>
                    <span v-else>Add Question</span>
                  </button>
                </form>
              </div>

              <div v-else>
                <div class="section-header d-flex justify-content-between align-items-center">
                  <div>
                    <h5>
                      <i
                        class="fas me-2"
                        :class="isEditMode ? 'fa-edit' : 'fa-eye'"
                      ></i>
                      {{ isEditMode ? 'Edit Question' : 'View Question' }}
                    </h5>
                    <p>Question {{ currentQuestionIndex + 1 }} of {{ filteredQuestions.length }}</p>
                  </div>
                  <div>
                    <button @click="clearSelection" class="btn btn-sm btn-secondary">
                      <i class="fas fa-times me-1"></i> Close
                    </button>
                  </div>
                </div>

                <form v-if="isEditMode" @submit.prevent="updateQuestion" class="mb-4">
                  <div class="mb-3">
                    <label class="form-label fw-semibold">Question Text</label>
                    <input v-model="editQuestion.text" type="text" class="form-control" required />
                  </div>
                  <div class="mb-3">
                    <label class="form-label fw-semibold">Options</label>
                    <div v-for="(option, idx) in editQuestion.options" :key="idx" class="input-group mb-2">
                      <input
                        v-model="editQuestion.options[idx].text"
                        type="text"
                        class="form-control"
                        :placeholder="`Option ${idx + 1}`"
                        required
                      />
                      <div class="input-group-text">
                        <input
                          type="radio"
                          :name="'editCorrectOption'"
                          :checked="editQuestion.correctIndex === idx"
                          @change="editQuestion.correctIndex = idx"
                          aria-label="Select as correct answer"
                        />
                      </div>
                    </div>
                  </div>
                  <div class="mb-3">
                    <label class="form-label fw-semibold">Difficulty</label>
                    <select v-model="editQuestion.difficulty" class="form-select" required>
                      <option value="easy">Easy</option>
                      <option value="medium">Medium</option>
                      <option value="hard">Hard</option>
                    </select>
                  </div>
                  <div class="d-flex flex-wrap gap-2">
                    <button type="submit" class="btn btn-accent" :disabled="updatingQuestion">
                      <i class="fas fa-save me-1"></i>
                      <span v-if="updatingQuestion">Saving...</span>
                      <span v-else>Save Changes</span>
                    </button>
                    <button type="button" class="btn btn-outline-danger" @click="deleteQuestion(editIndex)">
                      <i class="fas fa-trash me-1"></i> Delete
                    </button>
                    <button type="button" class="btn btn-secondary" @click="isEditMode = false">
                      <i class="fas fa-eye me-1"></i> View Mode
                    </button>
                  </div>
                  <div v-if="updateError" class="alert alert-danger mt-3">
                    {{ updateError }}
                  </div>
                </form>

                <div v-else>
                  <div class="mb-3">
                    <label class="form-label fw-semibold">Question Text</label>
                    <div class="form-control bg-light">{{ editQuestion.text }}</div>
                  </div>
                  <div class="mb-3">
                    <label class="form-label fw-semibold">Options</label>
                    <div class="list-group">
                      <div
                        v-for="(option, idx) in editQuestion.options"
                        :key="idx"
                        class="list-group-item d-flex align-items-center"
                        :class="{ 'bg-success text-white': editQuestion.correctIndex === idx }"
                      >
                        <span class="me-2">{{ String.fromCharCode(65 + idx) }}.</span>
                        <span>{{ option.text }}</span>
                        <span v-if="editQuestion.correctIndex === idx" class="badge bg-light text-success ms-auto">
                          <i class="fas fa-check"></i> Correct
                        </span>
                      </div>
                    </div>
                  </div>
                  <div class="mb-3">
                    <label class="form-label fw-semibold">Difficulty</label>
                    <div>
                      <span class="badge" :class="{
                        'bg-success': editQuestion.difficulty === 'easy',
                        'bg-warning text-dark': editQuestion.difficulty === 'medium',
                        'bg-danger': editQuestion.difficulty === 'hard'
                      }">
                        {{ editQuestion.difficulty ? editQuestion.difficulty.charAt(0).toUpperCase() + editQuestion.difficulty.slice(1) : '' }}
                      </span>
                    </div>
                  </div>
                  <div class="d-flex flex-wrap gap-2">
                    <button @click="isEditMode = true" class="btn btn-accent">
                      <i class="fas fa-edit me-1"></i> Edit
                    </button>
                    <button @click="deleteQuestion(editIndex)" class="btn btn-outline-danger">
                      <i class="fas fa-trash me-1"></i> Delete
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import api from '../../api'
import { useRoute } from 'vue-router'
const route = useRoute()

// Toast notification
const toast = reactive({
  show: false,
  message: ''
})

function showToast(message) {
  toast.message = message
  toast.show = true
  setTimeout(() => { toast.show = false }, 3000)
}

// Quiz info
const subjectName = ref('')
const chapterName = ref('')
const quizName = ref('')
const quizId = ref(null)

// Questions data
const questions = ref([])
const loadingQuestions = ref(false)
const currentQuestionIndex = ref(-1)
const searchQuery = ref('')
const searchDifficulty = ref('')

// Question forms
const newQuestion = reactive({
  text: '',
  options: Array(4).fill().map(() => ({ text: '' })),
  correctIndex: 0,
  difficulty: ''
})

const editQuestion = reactive({
  text: '',
  options: [],
  correctIndex: 0,
  difficulty: ''
})

const editIndex = ref(-1)
const isEditMode = ref(false)
const addingQuestion = ref(false)
const updatingQuestion = ref(false)
const updateError = ref('')

// Fetch quiz info and questions
onMounted(async () => {
  try {
    quizId.value = route.params.quizid
    const quizRes = await api.get(`/quizzes/${quizId.value}`)
    quizName.value = quizRes.data.title
    
    if (quizRes.data.chapter_id) {
      const chapterRes = await api.get(`/chapters/${quizRes.data.chapter_id}`)
      chapterName.value = chapterRes.data.name
      
      if (chapterRes.data.subject_id) {
        const subjectRes = await api.get(`/subjects/${chapterRes.data.subject_id}`)
        subjectName.value = subjectRes.data.name
      }
    }
    
    await fetchQuestions()
  } catch (error) {
    showToast('Failed to load quiz data')
  }
})

async function fetchQuestions() {
  loadingQuestions.value = true
  try {
    const res = await api.get(`/questions/quiz/${quizId.value}`)
    questions.value = res.data.map(q => ({
      ...q,
      options: q.options && q.options.length === 4 ? q.options : Array(4).fill().map((_, i) => q.options[i] || { text: '' })
    }))
  } catch (error) {
    showToast('Failed to load questions')
  }
  loadingQuestions.value = false
}

const filteredQuestions = computed(() => {
  let filtered = questions.value
  if (searchQuery.value.trim()) {
    filtered = filtered.filter(q =>
      q.text.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }
  if (searchDifficulty.value) {
    filtered = filtered.filter(q => q.difficulty === searchDifficulty.value)
  }
  return filtered
})

function getOriginalIndex(filteredIdx) {
  const question = filteredQuestions.value[filteredIdx]
  return questions.value.findIndex(q => q.id === question.id)
}

function handleSidebarSelect(idx) {
  currentQuestionIndex.value = idx
  const originalIdx = getOriginalIndex(idx)
  editIndex.value = originalIdx
  loadEditQuestion(originalIdx)
  isEditMode.value = false
  updateError.value = ''
}

function loadEditQuestion(idx) {
  const q = questions.value[idx]
  editQuestion.text = q.text
  editQuestion.options = q.options.map(opt => ({ ...opt }))
  editQuestion.correctIndex = q.correctIndex
  editQuestion.difficulty = q.difficulty
}

function clearSelection() {
  currentQuestionIndex.value = -1
  editIndex.value = -1
  isEditMode.value = false
  updateError.value = ''
}

async function addQuestion() {
  if (!validateQuestion(newQuestion)) return
  
  addingQuestion.value = true
  try {
    const payload = {
      text: newQuestion.text.trim(),
      options: newQuestion.options.map(opt => ({ text: opt.text.trim() })),
      correctIndex: newQuestion.correctIndex,
      difficulty: newQuestion.difficulty
    }
    await api.post(`/questions/${quizId.value}`, payload)
    showToast('Question added successfully')
    resetNewQuestionForm()
    await fetchQuestions()
  } catch (error) {
    showToast('Failed to add question')
  }
  addingQuestion.value = false
}

async function updateQuestion() {
  if (editIndex.value < 0 || !validateQuestion(editQuestion)) return
  
  updatingQuestion.value = true
  updateError.value = ''
  try {
    const q = questions.value[editIndex.value]
    const payload = {
      text: editQuestion.text.trim(),
      options: editQuestion.options.map(opt => ({ text: opt.text.trim() })),
      correctIndex: editQuestion.correctIndex,
      difficulty: editQuestion.difficulty
    }
    await api.put(`/questions/${q.id}`, payload)
    showToast('Question updated successfully')
    await fetchQuestions()
    isEditMode.value = false
  } catch (error) {
    updateError.value = 'Failed to update question'
  }
  updatingQuestion.value = false
}

async function deleteQuestion(idx) {
  if (!confirm('Are you sure you want to delete this question?')) return
  
  const q = questions.value[idx]
  if (!q) return
  
  try {
    await api.delete(`/questions/${q.id}`)
    showToast('Question deleted successfully')
    await fetchQuestions()
    clearSelection()
  } catch (error) {
    showToast('Failed to delete question')
  }
}

function validateQuestion(question) {
  return question.text.trim() && 
         question.options.length === 4 &&
         question.options.every(opt => opt.text.trim()) &&
         question.difficulty
}

function resetNewQuestionForm() {
  newQuestion.text = ''
  newQuestion.options = Array(4).fill().map(() => ({ text: '' }))
  newQuestion.correctIndex = 0
  newQuestion.difficulty = ''
}

watch(filteredQuestions, (newList) => {
  if (currentQuestionIndex.value >= newList.length) {
    currentQuestionIndex.value = newList.length > 0 ? 0 : -1
  }
})
</script>

<style scoped>
/* Dashboard Base Styles */
.dashboard-section {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  min-height: 100vh;
  padding: 1rem 0;
  width: 100vw;
}

.container-fluid {
  max-width: 100%;
  padding: 0 1rem;
}

/* Header Styles */
.dashboard-header {
  margin-bottom: 1rem;
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

/* Stats Section */
.stats-section {
  margin-bottom: 1.5rem;
}

.stat-card {
  background: white;
  border-radius: 1.25rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.stat-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
}

.stat-label {
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

/* Progress List (Questions Sidebar) */
.progress-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Hide scrollbar utility */
.hide-scrollbar {
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE 10+ */
}
.hide-scrollbar::-webkit-scrollbar {
  display: none; /* Chrome/Safari/Webkit */
}

.progress-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 0.75rem;
  transition: all 0.3s ease;
  cursor: pointer;
}

.progress-item:hover {
  background: #f1f5f9;
  transform: translateX(3px);
}

.progress-item.active {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
}

.progress-item.active .progress-title,
.progress-item.active .progress-subtitle {
  color: white;
}

.progress-info {
  flex-grow: 1;
}

.progress-title {
  font-weight: 500;
  color: #1f2937;
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.progress-subtitle {
  font-size: 0.85rem;
  color: #6b7280;
}

/* Form Styles */
.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.form-control:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-select {
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
}

/* Button Styles */
.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-accent {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  border: none;
}

.btn-accent:hover {
  background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn-secondary {
  background: #f3f4f6;
  color: #6b7280;
  border: none;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

.btn-outline-danger {
  border-color: #ef4444;
  color: #ef4444;
}

.btn-outline-danger:hover {
  background: #ef4444;
  color: white;
}

/* Alert Styles */
.alert {
  padding: 1rem;
  border-radius: 0.5rem;
  margin-top: 1rem;
}

.alert-info {
  background: #e0f2fe;
  color: #0369a1;
  border-left: 4px solid #0ea5e9;
}

.alert-danger {
  background: #fee2e2;
  color: #991b1b;
  border-left: 4px solid #ef4444;
}

/* Badge Styles */
.badge {
  padding: 0.35em 0.65em;
  font-size: 0.75em;
  font-weight: 600;
  border-radius: 0.5rem;
}

.bg-success {
  background-color: #10b981 !important;
}

.bg-warning {
  background-color: #f59e0b !important;
}

.bg-danger {
  background-color: #ef4444 !important;
}

/* Toast Styles */
.custom-toast {
  position: fixed;
  top: 30px;
  right: 30px;
  z-index: 9999;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  padding: 1rem 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
  display: flex;
  align-items: center;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* List Group Styles */
.list-group-item {
  padding: 1rem;
  border: 1px solid #e5e7eb;
}

.list-group-item:first-child {
  border-top-left-radius: 0.5rem;
  border-top-right-radius: 0.5rem;
}

.list-group-item:last-child {
  border-bottom-left-radius: 0.5rem;
  border-bottom-right-radius: 0.5rem;
}

/* Responsive Adjustments */
@media (max-width: 992px) {
  .welcome-title {
    font-size: 2rem;
  }
  
  .section-card {
    padding: 1rem;
  }
}

@media (max-width: 768px) {
  .container-fluid {
    padding: 0 1rem;
  }
  
  .welcome-title {
    font-size: 1.75rem;
  }
  
  .progress-title {
    font-size: 0.9rem;
  }
}

@media (max-width: 576px) {
  .welcome-title {
    font-size: 1.5rem;
  }
  
  .btn {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }
}
</style>