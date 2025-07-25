<template>
  <section class="dashboard-section">
    <div class="container-fluid">
      <!-- Already Submitted Modal -->
      <div v-if="showAlreadySubmittedModal" class="modal-backdrop">
        <div class="modal-content already-submitted-modal">
          <div class="modal-header already-submitted-header">
            <h2 class="modal-title already-submitted-title">
              <i class="fas fa-exclamation-circle me-2"></i>
              Quiz Already Submitted
            </h2>
          </div>
          <div class="modal-body already-submitted-body">
            <div class="already-submitted-icon">
              <i class="fas fa-exclamation-triangle"></i>
            </div>
            <p class="already-submitted-text">
              <b>You have already submitted this quiz.</b>
              <br>
              If you proceed, you will <span style="color:#ef4444;font-weight:600;">re-attempt</span> the quiz and your new submission will <span style="color:#ef4444;font-weight:600;">overwrite</span> the previous one.
            </p>
          </div>
          <div class="modal-footer already-submitted-footer">
            <button class="btn btn-gradient-primary btn-lg" @click="proceedAfterAlreadySubmitted">
              <i class="fas fa-redo me-2"></i> Re-attempt Quiz
            </button>
            <button class="btn btn-outline-secondary btn-lg me-2" @click="goBackToDashboard">
              <i class="fas fa-times me-2"></i> Cancel
            </button>
          </div>
        </div>
      </div>
      <!-- Quiz Header -->
      <div class="dashboard-header mb-4">
        <div class="row align-items-center">
          <div class="col-12">
            <div class="welcome-content">
              <h1 class="welcome-title">
                {{ quiz.title }}
              </h1>
              <div class="quiz-meta">
                <span class="badge bg-primary me-2" v-if="quiz.subject || quiz.subject_name">
                  <i class="fas fa-book me-1"></i> {{ quiz.subject || quiz.subject_name }}
                </span>
                <span class="badge bg-info me-2" v-if="quiz.chapter || quiz.chapter_name">
                  <i class="fas fa-bookmark me-1"></i> {{ quiz.chapter || quiz.chapter_name }}
                </span>
                <span class="badge bg-secondary me-2" v-if="quiz.difficulty">
                  <i class="fas fa-signal me-1"></i> {{ quiz.difficulty }}
                </span>
                <span class="badge bg-light text-dark me-2" v-if="quiz.timeLimit">
                  <i class="fas fa-clock me-1"></i> {{ Math.round(quiz.timeLimit/60) }} min
                </span>
                <span class="badge bg-light text-dark me-2" v-if="questions.length">
                  <i class="fas fa-question me-1"></i> Question {{ currentQuestionIndex + 1 }} of {{ questions.length }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="!quizLoaded" class="loading-state">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p>Loading quiz...</p>
      </div>

      <!-- Quiz Content -->
      <div v-else class="content-section">
        <div class="row">
          <!-- Main Quiz Area -->
          <div class="col-12 col-lg-8">
            <div class="section-card">
              <!-- Question Card (Normal/Review Mode) -->
              <div v-if="questions.length && (!showReviewMode)" class="question-content">
                <div class="question-header mb-4">
                  <div class="question-number-label">
                    <span class="question-number-badge">
                      <i class="fas fa-q"></i>  {{  currentQuestionIndex + 1 }}
                    </span>
                  </div>
                  <h3 class="question-text">{{ currentQuestion.text }}</h3>
                  <div v-if="currentQuestion.image" class="question-image mt-3">
                    <img :src="currentQuestion.image" alt="Question illustration" class="img-fluid rounded">
                  </div>
                </div>

                <!-- Options List -->
                <div class="options-grid">
                  <div 
                    v-for="(option, index) in currentQuestion.options" 
                    :key="index"
                    class="option-card"
                    :class="{
                      'selected': userAnswers[currentQuestionIndex] === index,
                      'correct': showResults && isCorrectOption(index),
                      'incorrect': showResults && userAnswers[currentQuestionIndex] === index && !isCorrectOption(index)
                    }"
                    @click="selectOption(index)"
                  >
                    <div class="option-letter" :style="{ backgroundColor: getOptionColor(index) }">
                      {{ String.fromCharCode(65 + index) }}
                    </div>
                    <div class="option-content">
                      <div class="option-text">{{ option }}</div>
                      <div v-if="showResults" class="option-feedback">
                        <i v-if="isCorrectOption(index)" class="fas fa-check-circle correct-icon"></i>
                        <i v-else-if="userAnswers[currentQuestionIndex] === index && !isCorrectOption(index)" class="fas fa-times-circle incorrect-icon"></i>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Report Question Button and Message -->
                <div class="d-flex align-items-center mb-3" style="gap: 1rem;">
                  <button
                    class="btn btn-outline-danger"
                    @click="reportCurrentQuestion"
                    :disabled="userAnswers[currentQuestionIndex] === -1"
                  >
                    <i class="fas fa-flag me-2"></i> Report Question
                  </button>
                  <span v-if="showReportMessage" class="text-danger" style="font-weight:600;">
                    Question reported. It will be reviewed shortly. Moving to next question...
                  </span>
                </div>

                <!-- Navigation Buttons -->
                <div class="quiz-navigation mt-4">
                  <button 
                    v-if="currentQuestionIndex !== 0"
                    class="btn btn-outline-secondary" 
                    @click="prevQuestion"
                  >
                    <i class="fas fa-arrow-left me-2"></i> Previous
                  </button>
                  <span v-else></span>
                  <button
                    v-if="currentQuestionIndex < questions.length - 1"
                    class="btn btn-gradient-primary"
                    @click="nextQuestion"
                  >
                    Next Question <i class="fas fa-arrow-right ms-2"></i>
                  </button>
                  <button
                    v-else
                    class="btn btn-gradient-primary"
                    @click="confirmSubmit"
                    :disabled="showQuizResults"
                  >
                    <i class="fas fa-paper-plane me-2"></i> Submit Quiz
                  </button>
                </div>
              </div>

              <!-- Review Mode -->
              <div v-if="showReviewMode && questions.length" class="question-content">
                <div class="question-header mb-4">
                  <div class="question-number-label">
                    <span class="question-number-badge">
                      <i class="fas fa-hashtag"></i> {{ currentQuestionIndex + 1 }}
                    </span>
                    <span class="question-number-total">/ {{ questions.length }}</span>
                  </div>
                  <h3 class="question-text">Review: {{ currentQuestion.text }}</h3>
                  <div v-if="currentQuestion.image" class="question-image mt-3">
                    <img :src="currentQuestion.image" alt="Question illustration" class="img-fluid rounded">
                  </div>
                </div>
                <div class="options-grid">
                  <div
                    v-for="(option, index) in currentQuestion.options"
                    :key="index"
                    class="option-card"
                    :class="{
                      'selected': userAnswers[currentQuestionIndex] === index,
                      'correct': isReviewCorrectOption(index),
                      'incorrect': isReviewIncorrectOption(index)
                    }"
                  >
                    <div class="option-letter" :style="{ backgroundColor: getOptionColor(index) }">
                      {{ String.fromCharCode(65 + index) }}
                    </div>
                    <div class="option-content">
                      <div class="option-text">{{ option }}</div>
                      <div class="option-feedback">
                        <i v-if="isReviewCorrectOption(index)" class="fas fa-check-circle correct-icon"></i>
                        <i v-else-if="isReviewIncorrectOption(index)" class="fas fa-times-circle incorrect-icon"></i>
                      </div>
                    </div>
                  </div>
                </div>
                <!-- Navigation Buttons in Review Mode -->
                <div class="quiz-navigation mt-4">
                  <button 
                    v-if="currentQuestionIndex !== 0"
                    class="btn btn-outline-secondary" 
                    @click="prevQuestion"
                  >
                    <i class="fas fa-arrow-left me-2"></i> Previous
                  </button>
                  <span v-else></span>
                  <button
                    v-if="currentQuestionIndex < questions.length - 1"
                    class="btn btn-gradient-primary"
                    @click="nextQuestion"
                  >
                    Next Question <i class="fas fa-arrow-right ms-2"></i>
                  </button>
                  <button
                    v-else
                    class="btn btn-gradient-primary"
                    @click="exitReviewMode"
                  >
                    Done Reviewing
                  </button>
                </div>
              </div>

              <!-- Empty State -->
              <div v-else-if="!questions.length" class="empty-state">
                <i class="fas fa-exclamation-circle"></i>
                <p>No questions available for this quiz</p>
              </div>
            </div>
          </div>

          <!-- Sidebar -->
          <div class="col-12 col-lg-4">
            <div class="section-card sidebar-card">
              <!-- Timer -->
              <div class="sidebar-timer" :class="{ 'warning': timeLeft < 30 }">
                <i class="fas fa-clock me-2"></i>
                {{ formatTime(timeLeft) }}
                <span class="sidebar-label">Time Remaining</span>
              </div>

              <!-- Question Navigation -->
              <div class="sidebar-section">
                <h6 class="sidebar-title">
                  <i class="fas fa-list-ol me-2"></i> Questions
                </h6>
                <div class="questions-grid">
                  <div
                    v-for="(question, idx) in questions"
                    :key="question.id"
                    class="question-number"
                    :class="{
                      'active': idx === currentQuestionIndex,
                      'answered': userAnswers[idx] !== null && !showReviewMode
                    }"
                    @click="goToQuestion(idx)"
                  >
                    {{ idx + 1 }}
                  </div>
                </div>
              </div>
              <!-- No Submit Quiz button in sidebar -->
            </div>
          </div>
        </div>
      </div>

      <!-- Quiz Results Modal -->
      <div v-if="showQuizResults && !showReviewMode" class="modal-backdrop">
        <div class="modal-content quiz-results">
          <div class="modal-header">
            <h2 class="modal-title">
              <i class="fas fa-trophy me-2"></i>
              Quiz Results
            </h2>
          </div>
          <div class="modal-body">
            <!-- Congrats Banner -->
            <div class="quiz-congrats-banner">
              🎉 Congratulations! You have completed the quiz! 🎉
            </div>
            <div class="result-stats">
              <div class="stat-card stat-primary">
                <div class="stat-icon">
                  <i class="fas fa-check-circle"></i>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ resultData.correct_answers }}</div>
                  <div class="stat-label">Correct Answers</div>
                </div>
              </div>
              
              <div class="stat-card stat-incorrect">
                <div class="stat-icon">
                  <i class="fas fa-times-circle"></i>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ incorrectAnswers }}</div>
                  <div class="stat-label">Incorrect Answers</div>
                </div>
              </div>

              <div class="stat-card stat-success">
                <div class="stat-icon">
                  <i class="fas fa-percentage"></i>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ Math.round(resultData.score) }}%</div>
                  <div class="stat-label">Score</div>
                </div>
              </div>
              
              <div class="stat-card stat-info">
                <div class="stat-icon">
                  <i class="fas fa-clock"></i>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ formatTime(resultData.time_taken) }}</div>
                  <div class="stat-label">Time Taken</div>
                </div>
              </div>
              <div class="stat-card stat-info">
                <div class="stat-icon">
                  <i class="fas fa-list"></i>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ questions.length }}</div>
                  <div class="stat-label">Total Questions</div>
                </div>
              </div>
            </div>
            <!-- Extra Info: Show percentage of correct answers -->
            <div class="text-center mt-3" style="font-size:1.1rem;">
              <span>
                You answered <b>{{ resultData.correct_answers }}</b> out of <b>{{ questions.length }}</b> questions correctly.
                <span v-if="incorrectAnswers > 0"> You got <b>{{ incorrectAnswers }}</b> wrong.</span>
              </span>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-outline-secondary me-2" @click="enterReviewMode">
              <i class="fas fa-eye me-2"></i> Review Answers
            </button>
            <button class="btn btn-gradient-primary" @click="finishQuiz">
              <i class="fas fa-home me-2"></i> Return to Dashboard
            </button>
          </div>
        </div>
      </div>

      <!-- Confirmation Modal -->
      <div v-if="showConfirmModal" class="modal-backdrop">
        <div class="modal-content" style="max-width:500px;">
          <div class="modal-header">
            <h2 class="modal-title">
              <i class="fas fa-question-circle me-2"></i>
              Confirm Submission
            </h2>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to submit your quiz? You won't be able to change your answers after submission.</p>
            <div class="progress-summary mt-3">
              <div class="progress-item">
                <span class="progress-label">Questions Answered:</span>
                <span class="progress-value">{{ answeredCount }} / {{ questions.length }}</span>
              </div>
              <div class="progress-bar mt-2">
                <div class="progress-fill" :style="{ width: (answeredCount / questions.length) * 100 + '%' }"></div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-outline-secondary me-2" @click="showConfirmModal = false">
              Cancel
            </button>
            <button class="btn btn-gradient-primary" @click="submitQuiz">
              Submit Quiz
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../../api'

const router = useRouter()
const route = useRoute()

const quiz = ref({
  
  description: '',
  subject: '',
  subject_name: '',
  chapter: '',
  chapter_name: '',
  difficulty: '',
  author: '',
  author_name: '',
  timeLimit: '',
  created_at: ''
})
const questions = ref([])
const currentQuestionIndex = ref(0)
const userAnswers = ref([])
const showResults = ref(false)
const showQuizResults = ref(false)
const timeLeft = ref(300)
const timer = ref(null)
const resultData = ref({})
const quizLoaded = ref(false)
const quizId = route.params.quizid
const showConfirmModal = ref(false)
const showReviewMode = ref(false)
const showAlreadySubmittedModal = ref(false)
const alreadySubmitted = ref(false)

// For reporting question
const showReportMessage = ref(false)
let reportTimeout = null

function getUserIdFromToken() {
  try {
    const token = localStorage.getItem('token')
    if (!token) return null
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.sub.id
  } catch {
    return null
  }
}

const userId = getUserIdFromToken()

const currentQuestion = computed(() => questions.value[currentQuestionIndex.value] || { options: [] })

const answeredCount = computed(() => {
  return userAnswers.value.filter(answer => answer !== null).length
})

const incorrectAnswers = computed(() => {
  if (typeof resultData.value.correct_answers !== 'number') return 0
  return questions.value.length - resultData.value.correct_answers
})

function getOptionColor(index) {
  const colors = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6']
  return colors[index % colors.length]
}

function selectOption(index) {
  if (!showResults.value && !showQuizResults.value && userAnswers.value[currentQuestionIndex.value] !== -1) {
    userAnswers.value[currentQuestionIndex.value] = index
  }
}

function nextQuestion() {
  if (currentQuestionIndex.value < questions.value.length - 1) {
    currentQuestionIndex.value++
  }
}

function prevQuestion() {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
  }
}

function goToQuestion(idx) {
  currentQuestionIndex.value = idx
}

function formatTime(seconds) {
  if (!seconds && seconds !== 0) return '--:--'
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

function isCorrectOption(index) {
  if (!showQuizResults.value || !resultData.value.answers) return false
  const qid = questions.value[currentQuestionIndex.value].id
  const correctIdx = resultData.value.answers && resultData.value.answers[qid]
  return correctIdx === index && resultData.value.user_correct_answers && resultData.value.user_correct_answers[qid]
}

async function fetchQuizMeta() {
  try {
    const { data } = await api.get(`/quizzes/${quizId}`)
    quiz.value.title = data.title || 'Quiz'
    quiz.value.description = data.description || ''
    quiz.value.subject = data.subject || data.subject_name || ''
    quiz.value.subject_name = data.subject_name || ''
    quiz.value.chapter = data.chapter || data.chapter_name || ''
    quiz.value.chapter_name = data.chapter_name || ''
    quiz.value.difficulty = data.difficulty || ''
    quiz.value.author = data.author_name || data.author || ''
    quiz.value.author_name = data.author_name || ''
    quiz.value.timeLimit = data.duration || data.timeLimit || 300
    quiz.value.created_at = data.created_at || ''
    timeLeft.value = quiz.value.timeLimit
  } catch (e) {
    console.error("Error fetching quiz metadata:", e)
  }
}

async function fetchQuizQuestions() {
  try {
    const { data } = await api.get(`/quizzes/${quizId}/take`)
    questions.value = data.questions || []
    userAnswers.value = Array(questions.value.length).fill(null)
  } catch (e) {
    console.error("Error fetching quiz questions:", e)
    questions.value = []
    userAnswers.value = []
  }
}

// Fetch user's previous results for this quiz
async function checkIfAlreadySubmitted() {
  try {
    // Fetch all results for this user
    const { data } = await api.get(`/result/${userId}`)
    // Check if any result matches this quizId
    if (Array.isArray(data)) {
      alreadySubmitted.value = data.some(r => String(r.quiz_id) === String(quizId))
      if (alreadySubmitted.value) {
        showAlreadySubmittedModal.value = true
      }
    }
  } catch (e) {
    console.error("Error checking previous quiz submission:", e)
  }
}

async function fetchQuiz() {
  quizLoaded.value = false
  await Promise.all([fetchQuizMeta(), fetchQuizQuestions()])
  quizLoaded.value = true
}

function confirmSubmit() {
  showConfirmModal.value = true
}

async function submitQuiz() {
  if (showQuizResults.value) return
  showConfirmModal.value = false
  clearInterval(timer.value)
  
  const answers = {}
  questions.value.forEach((q, idx) => {
    answers[q.id] = userAnswers.value[idx] !== null ? userAnswers.value[idx] : null
  })
  
  const payload = {
    answers,
    user_id: userId,
    time_taken: quiz.value.timeLimit - timeLeft.value
  }
  
  try {
    // Always allow submission (re-attempt overwrites previous)
    const { data } = await api.post(`/quizzes/${quizId}/submit`, payload)
    resultData.value = data
    showResults.value = true
    showQuizResults.value = true
  } catch (e) {
    console.error("Error submitting quiz:", e)
  }
}

function finishQuiz() {
  router.push(`/dashboard/user/${userId}`)
}

// Review mode logic
function enterReviewMode() {
  showReviewMode.value = true
  currentQuestionIndex.value = 0
}
function exitReviewMode() {
  showReviewMode.value = false
}

// Modal actions
function proceedAfterAlreadySubmitted() {
  showAlreadySubmittedModal.value = false
  // Now load the quiz as normal (re-attempt)
  fetchQuiz().then(() => {
    quizLoaded.value = true
    timer.value = setInterval(() => {
      if (timeLeft.value > 0) {
        timeLeft.value--
      } else {
        submitQuiz()
      }
    }, 1000)
  })
}
function goBackToDashboard() {
  router.push(`/dashboard/user/${userId}`)
}

// Report Question Logic
async function reportCurrentQuestion() {
  if (userAnswers.value[currentQuestionIndex.value] === -1) return
  userAnswers.value[currentQuestionIndex.value] = -1
  showReportMessage.value = true

  // Optionally, send report to backend (uncomment if endpoint exists)
  // try {
  //   await api.post(`/questions/${questions.value[currentQuestionIndex.value].id}/report`, {
  //     user_id: userId,
  //     quiz_id: quizId
  //   })
  // } catch (e) {
  //   // Ignore error for now
  // }

  // Move to next question after a short delay
  if (reportTimeout) clearTimeout(reportTimeout)
  reportTimeout = setTimeout(() => {
    showReportMessage.value = false
    if (currentQuestionIndex.value < questions.value.length - 1) {
      currentQuestionIndex.value++
    }
  }, 1800)
}

onMounted(async () => {
  // First, check if already submitted
  await checkIfAlreadySubmitted()
  // If not already submitted, proceed to load quiz
  if (!alreadySubmitted.value) {
    await fetchQuiz()
    timer.value = setInterval(() => {
      if (timeLeft.value > 0) {
        timeLeft.value--
      } else {
        submitQuiz()
      }
    }, 1000)
  }
})

onUnmounted(() => {
  clearInterval(timer.value)
  if (reportTimeout) clearTimeout(reportTimeout)
})
function isReviewCorrectOption(index){
  return resultData.value.correct_answers === index;
}
function isReviewIncorrectOption(index){
  return !(resultData.value.correct_answers === index) && userAnswers.value[currentQuestionIndex.value] === index;
}
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

/* Already Submitted Modal Custom Styles */
.already-submitted-modal {
  max-width: 520px !important;
  min-width: 350px;
  min-height: 340px;
  padding: 2.5rem 2rem 2rem 2rem;
  border: 3px solid #ef4444;
  box-shadow: 0 8px 32px rgba(239,68,68,0.18);
  display: flex;
  flex-direction: column;
  align-items: center;
}
.already-submitted-header {
  border-bottom: none;
  padding-bottom: 0;
  width: 100%;
  justify-content: center;
}
.already-submitted-title {
  color: #ef4444;
  font-size: 2rem;
  font-weight: 800;
  text-align: center;
  width: 100%;
}
.already-submitted-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
}
.already-submitted-icon {
  font-size: 3.5rem;
  color: #ef4444;
  margin-bottom: 1rem;
  animation: shake 0.7s;
}
@keyframes shake {
  10%, 90% { transform: translateX(-2px); }
  20%, 80% { transform: translateX(4px); }
  30%, 50%, 70% { transform: translateX(-8px); }
  40%, 60% { transform: translateX(8px); }
}
.already-submitted-text {
  font-size: 1.15rem;
  color: #1f2937;
  text-align: center;
  margin-bottom: 0;
  line-height: 1.6;
}
.already-submitted-footer {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  width: 100%;
  border-top: none;
  padding-top: 0;
}
.btn-lg {
  font-size: 1.1rem;
  padding: 1rem 2.25rem;
  border-radius: 1rem;
}

/* Question Number Label */
.question-number-label {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
  gap: 0.5rem;
}
.question-number-badge {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: #fff;
  font-weight: 700;
  font-size: 1.1rem;
  border-radius: 0.75rem;
  padding: 0.4rem 1.1rem;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 8px rgba(59,130,246,0.08);
}
.question-number-total {
  color: #6b7280;
  font-size: 1.1rem;
  font-weight: 500;
}

/* Header Section */
.dashboard-header {
  margin-bottom: 2rem;
}

.welcome-content {
  padding: 1rem 0;
}

.welcome-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
}

.quiz-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}

.badge {
  padding: 0.5rem 0.75rem;
  border-radius: 0.75rem;
  font-size: 0.85rem;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  color: #6c757d;
}

.loading-state p {
  margin-top: 1rem;
}

/* Content Section */
.content-section {
  margin-bottom: 3rem;
}

.section-card {
  background: white;
  border-radius: 1.25rem;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  height: 100%;
}

/* Question Content */
.question-content {
  min-height: 400px;
  display: flex;
  flex-direction: column;
}

.question-header {
  margin-bottom: 1.5rem;
}

.question-text {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  line-height: 1.5;
}

.question-image {
  margin-top: 1rem;
  max-width: 100%;
  border-radius: 0.75rem;
  overflow: hidden;
}

.question-image img {
  max-width: 100%;
  height: auto;
  display: block;
}

/* Options Grid */
.options-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  margin-bottom: 2rem;
}

.option-card {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.25rem;
  border-radius: 0.75rem;
  background-color: #f9fafb;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid transparent;
}

.option-card:hover {
  background-color: #f3f4f6;
}

.option-card.selected {
  border-color: #3b82f6;
  background-color: #f0f7ff;
}

.option-card.correct {
  border-color: #10b981;
  background-color: #ecfdf5;
}

.option-card.incorrect {
  border-color: #ef4444;
  background-color: #fef2f2;
}

.option-letter {
  width: 36px;
  height: 36px;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  flex-shrink: 0;
}

.option-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.option-text {
  color: #1f2937;
  font-size: 1rem;
}

.option-feedback {
  margin-left: 1rem;
}

.correct-icon {
  color: #10b981;
  font-size: 1.25rem;
}

.incorrect-icon {
  color: #ef4444;
  font-size: 1.25rem;
}

/* Quiz Navigation */
.quiz-navigation {
  display: flex;
  justify-content: space-between;
  margin-top: auto;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  font-weight: 500;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
}

.btn-outline-secondary {
  border: 2px solid #e5e7eb;
  color: #6b7280;
}

.btn-outline-secondary:hover {
  background-color: #f3f4f6;
}

.btn-outline-secondary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-gradient-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  border: none;
}

.btn-gradient-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn-gradient-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* Report Button */
.btn-outline-danger {
  border: 2px solid #ef4444;
  color: #ef4444;
  background: #fff;
  transition: all 0.2s;
}
.btn-outline-danger:hover {
  background: #fef2f2;
  color: #b91c1c;
  border-color: #b91c1c;
}
.btn-outline-danger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Sidebar */
.sidebar-card {
  position: sticky;
  top: 1rem;
}

.sidebar-timer {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  padding: 1rem;
  border-radius: 0.75rem;
  background-color: #f9fafb;
  text-align: center;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sidebar-timer.warning {
  color: #ef4444;
  background-color: #fef2f2;
}

.sidebar-label {
  font-size: 0.85rem;
  font-weight: 400;
  color: #6b7280;
  margin-left: 0.5rem;
}

.sidebar-section {
  margin-bottom: 1.5rem;
}

.sidebar-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
}

.questions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(40px, 1fr));
  gap: 0.75rem;
}

.question-number {
  width: 40px;
  height: 40px;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f3f4f6;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
}

.question-number:hover {
  background-color: #e5e7eb;
}

.question-number.active {
  background-color: #3b82f6;
  color: white;
}

.question-number.answered {
  background-color: #10b981;
  color: white;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  color: #9ca3af;
  text-align: center;
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.empty-state p {
  font-weight: 500;
}

/* Modal styles */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 1.25rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.quiz-results {
  max-width: 800px;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  display: flex;
  align-items: center;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
}

/* Result Stats */
.result-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  border-radius: 1rem;
}

.stat-primary {
  background-color: #f0f7ff;
}

.stat-success {
  background-color: #ecfdf5;
}

.stat-info {
  background-color: #f0f9ff;
}

/* Incorrect stat card style */
.stat-incorrect {
  background-color: #fef2f2;
  color: #ef4444;
}

.stat-incorrect .stat-icon {
  background-color: #ef4444;
  color: white;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.stat-primary .stat-icon {
  background-color: #3b82f6;
  color: white;
}

.stat-success .stat-icon {
  background-color: #10b981;
  color: white;
}

.stat-info .stat-icon {
  background-color: #06b6d4;
  color: white;
}

.stat-number {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1f2937;
}

.stat-incorrect .stat-number {
  color: #ef4444;
}

.stat-label {
  font-size: 0.95rem;
  color: #6b7280;
}

.stat-incorrect .stat-label {
  color: #ef4444;
}

/* Quiz congrats banner */
.quiz-congrats-banner {
  background: linear-gradient(90deg, #10b981 0%, #3b82f6 100%);
  color: #fff;
  font-size: 1.25rem;
  font-weight: 700;
  text-align: center;
  border-radius: 0.75rem;
  padding: 1rem 0.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(16,185,129,0.08);
}

/* Result Breakdown */
.result-breakdown h4 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.questions-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.75rem;
}

.question-result {
  display: flex;
  align-items: center;
  padding: 1rem;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.question-result:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.question-result.correct {
  background-color: #ecfdf5;
  color: #10b981;
}

.question-result.incorrect {
  background-color: #fef2f2;
  color: #ef4444;
}

.question-number {
  margin-right: 1rem;
  font-weight: 600;
}

.question-status {
  margin-right: 1rem;
  font-size: 1.25rem;
}

.question-text {
  flex: 1;
  font-size: 0.95rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Progress Summary */
.progress-summary {
  background-color: #f9fafb;
  border-radius: 0.75rem;
  padding: 1rem;
}

.progress-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.progress-label {
  font-weight: 500;
  color: #6b7280;
}

.progress-value {
  font-weight: 600;
  color: #1f2937;
}

.progress-bar {
  height: 8px;
  background-color: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  border-radius: 4px;
  transition: width 0.3s ease;
}

/* Responsive Design */
@media (max-width: 992px) {
  .welcome-title {
    font-size: 1.75rem;
  }
  
  .result-stats {
    grid-template-columns: 1fr;
  }
  
  .questions-grid {
    grid-template-columns: repeat(auto-fill, minmax(35px, 1fr));
  }
  
  .question-number {
    width: 35px;
    height: 35px;
    font-size: 0.9rem;
  }
  .already-submitted-modal {
    max-width: 98vw !important;
    min-width: 0;
    padding: 1.5rem 0.5rem 1.5rem 0.5rem;
  }
}

@media (max-width: 768px) {
  .container-fluid {
    padding: 0 1rem;
  }
  
  .dashboard-section {
    padding: 1rem 0;
  }
  
  .section-card {
    padding: 1.5rem;
  }
  
  .quiz-navigation {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }
  
  .modal-content {
    width: 95%;
  }
}

@media (max-width: 576px) {
  .welcome-title {
    font-size: 1.5rem;
  }
  
  .quiz-meta {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .question-text {
    font-size: 1.1rem;
  }
  
  .option-card {
    padding: 1rem;
  }
  
  .option-letter {
    width: 30px;
    height: 30px;
    font-size: 0.9rem;
  }
  
  .option-text {
    font-size: 0.9rem;
  }
  .already-submitted-modal {
    padding: 1rem 0.2rem 1rem 0.2rem;
  }
  .already-submitted-title {
    font-size: 1.2rem;
  }
  .already-submitted-icon {
    font-size: 2.2rem;
  }
}
</style>