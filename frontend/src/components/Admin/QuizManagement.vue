<template>
  <section class="quiz-management-section d-flex flex-column min-vh-100">
    <nav class="navbar navbar-expand-lg navbar-dark shadow-sm rounded-4 mt-4 mx-auto"
         style="max-width: 900px; background: linear-gradient(90deg, #6366f1 0%, #06b6d4 100%);">
      <div class="container-fluid">
        <router-link class="navbar-brand fw-bold text-white">
          <i class="fas fa-cogs me-2"></i>Quiz Master
        </router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#quizNavbar" aria-controls="quizNavbar" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="quizNavbar">
          <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link :to="{ path: '/dashboard/admin' }" class="nav-link text-white">Dashboard</router-link>
            </li>
            <li class="nav-item">
              <router-link :to="{ path: '/dashboard/admin/subjects' }" class="nav-link text-white">Subjects</router-link>
            </li>
            <li class="nav-item">
              <router-link
                :to="{ path: `/dashboard/admin/chapters/${chapterInfo?.subject_id ?? ''}` }"
                class="nav-link text-white"
              >Chapters</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container my-5">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="card border-0 shadow-lg rounded-4 p-4 bg-white">
            <div class="mb-4 text-center">
              <div class="d-flex flex-column flex-md-row justify-content-center align-items-center gap-3 mb-3">
                <span
                  class="px-4 py-2 fs-6 shadow rounded-pill d-flex align-items-center"
                  style="background: #6366f1; color: #fff; border: none;"
                >
                  <i class="fas fa-book-open me-2" style="color: #fff;"></i>
                  <span class="fw-semibold" style="color: #fff;">Subject:</span>
                  <span class="ms-1" style="color: #fff;">{{ chapterInfo?.subject_name ?? '—' }}</span>
                </span>
                <span
                  class="px-4 py-2 fs-6 shadow rounded-pill d-flex align-items-center"
                  style="background: #06b6d4; color: #fff; border: none;"
                >
                  <i class="fas fa-layer-group me-2" style="color: #fff;"></i>
                  <span class="fw-semibold" style="color: #fff;">Chapter:</span>
                  <span class="ms-1" style="color: #fff;">{{ chapterInfo?.name ?? '—' }}</span>
                </span>
              </div>
           
            <div class="mb-4">
              <div class="d-flex flex-column flex-md-row align-items-stretch align-items-md-center justify-content-between gap-2">
                <div class="flex-grow-1">
                  <input
                    v-model="search"
                    type="text"
                    class="form-control shadow-sm"
                    style="max-width: 500px;"
                    placeholder="Search quizzes by title..."
                    aria-label="Search quizzes"
                  />
                </div>
                <div>
                  <button class="btn btn-accent btn-sm d-flex align-items-center shadow-sm" @click="openAddQuizPopup">
                    <i class="fas fa-plus me-1"></i>
                    <span>Add Quiz</span>
                  </button>
                </div>
              </div>
            </div>
            <div v-if="loading" class="text-center my-4">
              <div class="spinner-border text-accent" role="status"></div>
            </div>
            <div v-else>
              <div v-if="filteredQuizzes.length === 0" class="alert alert-info text-center">
                No quizzes found for this chapter.
              </div>
              <ul class="list-group">
                <li
                  v-for="quiz in filteredQuizzes"
                  :key="quiz.id"
                  class="list-group-item d-flex flex-column flex-md-row justify-content-between align-items-start align-items-md-center mb-2 shadow-sm"
                  style="border-radius: 0.5rem;"
                >
                  <div class="mb-2 mb-md-0">
                    <span class="fw-semibold fs-5">{{ quiz.title }}</span>
                    <div class="text-muted small">Created: {{ quiz.created_at ? new Date(quiz.created_at).toLocaleString() : '' }}</div>
                  </div>
                  <div class="d-flex gap-2">
                    <button class="btn btn-sm btn-outline-info" @click="goToQuestionBank(quiz.id)" title="Manage Question Bank">
                      <i class="fas fa-database"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-primary" @click="openEditQuizPopup(quiz)" title="Edit Quiz">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" @click="deleteQuiz(quiz.id)" title="Delete Quiz">
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </li>
              </ul>
            </div>
            </div>
            </div>
            </div>
            </div>
            </div>

    <!-- Add Quiz Popup -->
    <div v-if="showAddQuizPopup" class="popup-overlay">
      <div class="popup-card bg-white p-4 rounded-4 shadow-lg">
        <h5 class="fw-bold mb-3">Add Quiz</h5>
        <form @submit.prevent="handleAddQuiz">
          <div class="mb-3">
            <label class="form-label">Quiz Title</label>
            <input v-model="addQuizForm.title" type="text" class="form-control" required />
          </div>
          <div class="d-flex justify-content-end gap-2">
            <button type="button" class="btn btn-secondary btn-sm" @click="closeAddQuizPopup">Cancel</button>
            <button type="submit" class="btn btn-accent btn-sm">Add</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Edit Quiz Popup -->
    <div v-if="showEditQuizPopup" class="popup-overlay">
      <div class="popup-card bg-white p-4 rounded-4 shadow-lg">
        <h5 class="fw-bold mb-3">Edit Quiz</h5>
        <form @submit.prevent="handleEditQuiz">
          <div class="mb-3">
            <label class="form-label">Quiz Title</label>
            <input v-model="editQuizForm.title" type="text" class="form-control" required />
          </div>
          <div class="d-flex justify-content-end gap-2">
            <button type="button" class="btn btn-secondary btn-sm" @click="closeEditQuizPopup">Cancel</button>
            <button type="submit" class="btn btn-accent btn-sm">Save</button>
          </div>
        </form>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../../api.js'

const route = useRoute()
const router = useRouter()

const quizzes = ref([])
const loading = ref(false)
const chapterInfo = ref(null)

const search = ref('')

const showAddQuizPopup = ref(false)
const addQuizForm = ref({
  title: '',
  chapter_id: route.params.chapterid ? Number(route.params.chapterid) : ''
})

const showEditQuizPopup = ref(false)
const editQuizForm = ref({
  id: null,
  title: ''
})

const filteredQuizzes = computed(() => {
  if (!search.value.trim()) return quizzes.value
  return quizzes.value.filter(q =>
    q.title && q.title.toLowerCase().includes(search.value.trim().toLowerCase())
  )
})

async function fetchChapterInfo() {
  try {
    const chapterId = route.params.chapterid ? Number(route.params.chapterid) : null
    if (chapterId) {
      const res = await api.get(`/chapters/${chapterId}`)
      chapterInfo.value = res.data
    }
  } catch (err) {
    console.error('Error fetching chapter info:', err)
    chapterInfo.value = null
  }
}

async function fetchQuizzes() {
  loading.value = true
  try {
    const chapterId = route.params.chapterid ? Number(route.params.chapterid) : null
    if (chapterId) {
      const res = await api.get(`/quizzes/chapter/${chapterId}`)
      quizzes.value = res.data || []
    } else {
      quizzes.value = []
    }
  } catch (err) {
    quizzes.value = []
  }
  loading.value = false
}

onMounted(() => {
  fetchChapterInfo()
  fetchQuizzes()
})

// Watch for route changes to refetch chapter info
watch(() => route.params.chapterid, () => {
  fetchChapterInfo()
  fetchQuizzes()
})

function openAddQuizPopup() {
  showAddQuizPopup.value = true
  addQuizForm.value = {
    title: '',
    chapter_id: route.params.chapterid ? Number(route.params.chapterid) : ''
  }
}
function closeAddQuizPopup() {
  showAddQuizPopup.value = false
  addQuizForm.value = { title: '', chapter_id: route.params.chapterid ? Number(route.params.chapterid) : '' }
}
async function handleAddQuiz() {
  const { title } = addQuizForm.value
  const chapter_id = route.params.chapterid ? Number(route.params.chapterid) : ''
  if (!title.trim() || !chapter_id) return
  try {
    await api.post('/quizzes/addquiz', {
      title: title.trim(),
      chapter_id
    })
    await fetchQuizzes()
    await fetchChapterInfo() // Refresh chapter info
    closeAddQuizPopup()
  } catch (err) {
    // Optionally handle error
  }
}

function openEditQuizPopup(quiz) {
  editQuizForm.value = {
    id: quiz.id,
    title: quiz.title
  }
  showEditQuizPopup.value = true
}
function closeEditQuizPopup() {
  showEditQuizPopup.value = false
  editQuizForm.value = { id: null, title: '' }
}
async function handleEditQuiz() {
  const { id, title } = editQuizForm.value
  if (!id || !title.trim()) return
  try {
    const res = await api.put(`/quizzes/${id}`, {
      title: title.trim()
    })
    const idx = quizzes.value.findIndex(q => q.id === id)
    if (idx !== -1) {
      quizzes.value[idx] = res.data
    }
    await fetchChapterInfo() // Refresh chapter info
    closeEditQuizPopup()
  } catch (err) {
    // Optionally handle error
  }
}

async function deleteQuiz(quizId) {
  if (!confirm('Are you sure you want to delete this quiz?')) return
  try {
    await api.delete(`/quizzes/${quizId}`)
    quizzes.value = quizzes.value.filter(q => q.id !== quizId)
    await fetchChapterInfo() // Refresh chapter info
  } catch (err) {
    // Optionally handle error
  }
}

// Dummy goToQuestionBank for completeness (if not already present)
function goToQuestionBank(quizId) {
  router.push({ name: 'QuestionManagement', params: { quizid: quizId } })
}

</script>

<style scoped>
.quiz-management-section {
  min-height: 100vh;
  background: linear-gradient(90deg, #6366f1 0%, #06b6d4 100%);
}
.popup-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.25);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}
.popup-card {
  min-width: 320px;
  max-width: 500px;
  width: 100%;
}
.btn-accent {
  background: #6366f1;
  color: #fff;
  border: none;
}
.btn-accent:hover, .btn-accent:focus {
  background: #06b6d4;
  color: #fff;
}
</style>
