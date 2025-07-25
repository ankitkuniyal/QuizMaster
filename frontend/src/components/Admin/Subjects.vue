<template>
  <section class="dashboard-section">
    <div class="container-fluid">
      <!-- Toast Notification -->
      <transition name="fade">
        <div v-if="toast.show" class="custom-toast">
          <i class="fas fa-check-circle me-2"></i>
          {{ toast.message }}
        </div>
      </transition>
      <!-- Header Section -->
      <div class="dashboard-header ">
        <div class="row align-items-center">
          <!-- Welcome Section -->
          <div class="col-12 col-lg-7">
            <div class="welcome-content">
              <h1 class="welcome-title">Subject Management 👨‍🏫</h1>
              <p class="welcome-subtitle">
                Organize your learning materials and quizzes
              </p>
            </div>
          </div>
          <div class="col-12 col-lg-5 d-flex justify-content-lg-end align-items-center mt-3 mt-lg-0">
            <a href="/dashboard/admin" class="btn btn-accent mt-2">
              <i class="fas fa-tachometer-alt"></i>
              Dashboard
            </a>
            
              
  
          </div>
        </div>

      

      <!-- Filter Bar -->
      <div class="stats-section mb-5">
        <div class="row g-4">
          <div class="col-12">
            <div class="stat-card stat-primary">
              <div class="stat-icon">
                <i class="fas fa-filter"></i>
              </div>
              <div class="stat-content">
                <div class="d-flex flex-wrap align-items-center gap-4 justify-content-between">
                  <div class="d-flex align-items-center gap-2">
                    <i class="fas fa-book-open text-white"></i>
                    <span class="stat-label">Subject:</span>
                    <select class="form-select ms-2"
                      style="min-width: 180px;"
                      v-model="selectedSubject"
                      @change="selectedSubject ? selectSubject(selectedSubject) : resetAll()"
                    >
                      <option :value="null">Select Subject</option>
                      <option v-for="s in subjects" :key="s.id" :value="s">{{ s.name }}</option>
                    </select>
                  </div>
                  <div class="d-flex align-items-center gap-2">
                    <i class="fas fa-layer-group text-white"></i>
                    <span class="stat-label">Chapter:</span>
                    <select class="form-select ms-2"
                      style="min-width: 180px;"
                      v-model="selectedChapter"
                      :disabled="!selectedSubject"
                      @change="selectedChapter ? selectChapter(selectedChapter) : (sidebarMode = 'chapter', selectedQuiz = null)"
                    >
                      <option :value="null">Select Chapter</option>
                      <option v-for="c in chapters" :key="c.id" :value="c">{{ c.name }}</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
      <!-- Main Content Grid -->
      <div class="content-section mb-5">
        <div class="row g-4">
          <!-- Sidebar -->
          <div class="col-12 col-lg-4">
            <div class="section-card">
              <div class="section-header d-flex align-items-center gap-2">
                <!-- Back Button -->
                <button
                  v-if="sidebarMode !== 'subject'"
                  class="btn btn-link p-0 me-2"
                  style="font-size: 1.2rem; color: #3b82f6;"
                  @click="handleSidebarBack"
                  title="Back"
                >
                  <i class="fas fa-arrow-left"></i>
                </button>
                <div>
                  <h5 class="mb-0 d-inline">
                    <i class="fas" :class="{
                      'fa-book': sidebarMode === 'subject',
                      'fa-layer-group': sidebarMode === 'chapter',
                      'fa-book': sidebarMode === 'quiz'
                    }" me-2></i>
                    {{ sidebarMode === 'subject' ? 'Subjects' : 
                       sidebarMode === 'chapter' ? 'Chapters' : 'Quizzes' }}
                  </h5>
                  <p v-if="sidebarMode === 'subject'">All available subjects</p>
                  <p v-else-if="sidebarMode === 'chapter'">Chapters in {{ selectedSubject?.name }}</p>
                  <p v-else>Quizzes in {{ selectedChapter?.name }}</p>
                </div>
              </div>
              
              <!-- Subjects List -->
              <template v-if="sidebarMode === 'subject'">
                <div class="progress-list">
                  <div
                    v-for="subject in subjects"
                    :key="subject.id"
                    class="progress-item"
                    :class="{ active: selectedSubject && selectedSubject.id === subject.id }"
                    @click="selectSubject(subject)"
                  >
                    <div class="progress-info">
                      <div class="progress-title">{{ subject.name }}</div>
                      <div class="progress-subtitle">{{ subject.description }}</div>
                    </div>
                    <div class="d-flex align-items-center gap-1">
                      <button class="btn-edit" @click.stop="startSubjectEditForm(subject)" title="Edit">
                        <i class="fas fa-edit"></i>
                      </button>
                      <button class="btn-logout" @click.stop="deleteItem('subject', subject.id)" title="Delete">
                        <i class="fas fa-trash"></i>
                      </button>
                    </div>
                  </div>
                </div>
                <div class="alert alert-info text-center mt-3" v-if="!subjects.length && !loading.subjects">
                  No subjects found.
                </div>
              </template>

              <!-- Chapters List -->
              <template v-if="sidebarMode === 'chapter' && selectedSubject">
                <div class="progress-list">
                  <div
                    v-for="chapter in chapters"
                    :key="chapter.id"
                    class="progress-item"
                    :class="{ active: selectedChapter && selectedChapter.id === chapter.id }"
                    @click="selectChapter(chapter)"
                  >
                    <div class="progress-info">
                      <div class="progress-title">{{ chapter.name }}</div>
                    </div>
                    <div class="d-flex align-items-center gap-1">
                      <button class="btn-edit" @click.stop="startChapterEditForm(chapter)" title="Edit">
                        <i class="fas fa-edit"></i>
                      </button>
                      <button class="btn-logout" @click.stop="deleteItem('chapter', chapter.id)" title="Delete">
                        <i class="fas fa-trash"></i>
                      </button>
                    </div>
                  </div>
                </div>
                <div class="alert alert-info text-center mt-3" v-if="!chapters.length && !loading.chapters">
                  No chapters found.
                </div>
              </template>

              <!-- Quizzes List -->
              <template v-if="sidebarMode === 'quiz' && selectedChapter">
                <div class="progress-list">
                  <div
                    v-for="quiz in quizzes"
                    :key="quiz.id"
                    class="progress-item"
                    :class="{ active: selectedQuiz && selectedQuiz.id === quiz.id }"
                    @click="goToQuestionBank(quiz.id)"
                  >
                    <div class="progress-info">
                      <div class="progress-title">{{ quiz.title }}</div>
                      <div class="progress-subtitle">{{ Math.floor(quiz.duration) }} minutes</div>
                    </div>
                    <div class="d-flex align-items-center gap-1">
                      <button class="btn-edit" @click.stop="startQuizEditForm(quiz)" title="Edit">
                        <i class="fas fa-edit"></i>
                      </button>
                      <button class="btn-logout" @click.stop="deleteItem('quiz', quiz.id)" title="Delete">
                        <i class="fas fa-trash"></i>
                      </button>
                    </div>
                  </div>
                </div>
                <div class="alert alert-info text-center mt-3" v-if="!quizzes.length && !loading.quizzes">
                  No quizzes found.
                </div>
              </template>
            </div>
          </div>

          <!-- Main Form Content -->
          <div class="col-12 col-lg-8">
            <div class="section-card">
              <!-- Add/Edit Subject (No subject selected) -->
              <div v-if="sidebarMode === 'subject'" class="mb-4 text-center">
                <h2 class="fw-bold mb-2 text-dark">
                  <template v-if="subjectEditForm.active">
                    Edit {{ subjectEditForm.originalName }}
                  </template>
                  <template v-else>
                    Add Subject
                  </template>
                </h2>
                <p class="text-muted mb-0">
                  <template v-if="subjectEditForm.active">
                    Update details for <b>{{ subjectEditForm.originalName }}</b>.
                  </template>
                  <template v-else>
                    Create a new subject below.
                  </template>
                </p>
                <form class="mb-4 text-start" @submit.prevent="subjectEditForm.active ? updateSubject() : addSubject()">
                  <div class="mb-3">
                    <label class="form-label fw-semibold">Subject Name</label>
                    <input
                      type="text"
                      class="form-control"
                      :value="subjectEditForm.active ? subjectEditForm.name : newSubject.name"
                      @input="subjectEditForm.active ? subjectEditForm.name = $event.target.value : newSubject.name = $event.target.value"
                      :placeholder="subjectEditForm.active ? subjectEditForm.originalName : 'Enter subject name'"
                      required
                    />
                  </div>
                  <div class="mb-3">
                    <label class="form-label fw-semibold">Description</label>
                    <textarea
                      class="form-control"
                      rows="2"
                      :value="subjectEditForm.active ? subjectEditForm.description : newSubject.description"
                      @input="subjectEditForm.active ? subjectEditForm.description = $event.target.value : newSubject.description = $event.target.value"
                      :placeholder="subjectEditForm.active ? subjectEditForm.originalDescription : 'Enter subject description'"
                      required
                    ></textarea>
                  </div>
                  <button type="submit" class="btn btn-accent mt-2">
                    <i class="fas" :class="subjectEditForm.active ? 'fa-save' : 'fa-plus'" me-1></i>
                    {{ subjectEditForm.active ? 'Update Subject' : 'Add Subject' }}
                  </button>
                  <button
                    v-if="subjectEditForm.active"
                    type="button"
                    class="btn btn-secondary mt-2 ms-2"
                    @click="cancelSubjectEditForm"
                  >
                    Cancel
                  </button>
                  <div class="alert alert-danger mt-3" v-if="error.addSubject">
                    {{ error.addSubject }}
                  </div>
                </form>
              </div>

              <!-- Add/Edit Chapter Form -->
              <div v-if="sidebarMode === 'chapter' && selectedSubject" class="mb-4 text-center">
                <h2 class="fw-bold mb-2 text-dark">
                  <template v-if="chapterEditForm.active">
                    Edit {{ chapterEditForm.originalName }}
                  </template>
                  <template v-else>
                    Add Chapter
                  </template>
                </h2>
                <p class="text-muted mb-0">
                  <template v-if="chapterEditForm.active">
                    Update details for <b>{{ chapterEditForm.originalName }}</b>.
                  </template>
                  <template v-else>
                    Create a new chapter for <b>{{ selectedSubject.name }}</b>.
                  </template>
                </p>
                <form class="mb-4 mt-3 text-start" @submit.prevent="chapterEditForm.active ? updateChapter() : addChapter()">
                  <div class="mb-3">
                    <label class="form-label fw-semibold">Chapter Name</label>
                    <input
                      type="text"
                      class="form-control"
                      :value="chapterEditForm.active ? chapterEditForm.name : newChapter.name"
                      @input="chapterEditForm.active ? chapterEditForm.name = $event.target.value : newChapter.name = $event.target.value"
                      :placeholder="chapterEditForm.active ? chapterEditForm.originalName : 'Enter chapter name'"
                      required
                    />
                  </div>
                  <button type="submit" class="btn btn-accent mt-2">
                    <i class="fas" :class="chapterEditForm.active ? 'fa-save' : 'fa-plus'" me-1></i>
                    {{ chapterEditForm.active ? 'Update Chapter Details' : 'Add Chapter' }}
                  </button>
                  <button
                    v-if="chapterEditForm.active"
                    type="button"
                    class="btn btn-secondary mt-2 ms-2"
                    @click="cancelChapterEditForm"
                  >
                    Cancel
                  </button>
                  <div class="alert alert-danger mt-3" v-if="error.addChapter">
                    {{ error.addChapter }}
                  </div>
                </form>
              </div>

              <!-- Add/Edit Quiz Form -->
              <div v-if="sidebarMode === 'quiz' && selectedChapter" class="mb-4 text-center">
                <h2 class="fw-bold mb-2 text-dark">
                  <template v-if="quizEditForm.active">
                    Edit {{ quizEditForm.originalTitle }}
                  </template>
                  <template v-else>
                    Add Quiz
                  </template>
                </h2>
                <p class="text-muted mb-0">
                  <template v-if="quizEditForm.active">
                    Update details for <b>{{ quizEditForm.originalTitle }}</b>.
                  </template>
                  <template v-else>
                    Create a new quiz for <b>{{ selectedChapter.name }}</b>.
                  </template>
                </p>
                <form class="mb-4 mt-3 text-start" @submit.prevent="quizEditForm.active ? updateQuiz() : addQuiz()">
                  <div class="mb-3">
                    <label class="form-label fw-semibold">Quiz Title</label>
                    <input
                      type="text"
                      class="form-control"
                      :value="quizEditForm.active ? quizEditForm.title : newQuiz.title"
                      @input="quizEditForm.active ? quizEditForm.title = $event.target.value : newQuiz.title = $event.target.value"
                      :placeholder="quizEditForm.active ? quizEditForm.originalTitle : 'Enter quiz title'"
                      required
                    />
                  </div>
                  <div class="mb-3">
                    <label class="form-label fw-semibold">Duration (minutes)</label>
                    <input
                      type="number"
                      class="form-control"
                      :value="quizEditForm.active ? quizEditForm.duration : newQuiz.duration"
                      @input="quizEditForm.active ? quizEditForm.duration = Number($event.target.value) : newQuiz.duration = Number($event.target.value)"
                      :placeholder="quizEditForm.active ? quizEditForm.originalDuration || 'Enter duration in minutes' : 'Enter duration in minutes'"
                      min="1"
                      required
                    />
                  </div>
                  <button type="submit" class="btn btn-accent mt-2">
                    <i class="fas" :class="quizEditForm.active ? 'fa-save' : 'fa-plus'" me-1></i>
                    {{ quizEditForm.active ? 'Update Quiz' : 'Add Quiz' }}
                  </button>
                  <button
                    v-if="quizEditForm.active"
                    type="button"
                    class="btn btn-secondary mt-2 ms-2"
                    @click="cancelQuizEditForm"
                  >
                    Cancel
                  </button>
                  <div class="alert alert-danger mt-3" v-if="error.addQuiz">
                    {{ error.addQuiz }}
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import api from '../../api'
import { useRouter } from 'vue-router'
const router = useRouter()

// Toast state
const toast = reactive({
  show: false,
  message: ''
})
let toastTimeout = null
function showToast(msg) {
  toast.message = msg
  toast.show = true
  if (toastTimeout) clearTimeout(toastTimeout)
  toastTimeout = setTimeout(() => {
    toast.show = false
  }, 2500)
}

// State
const subjects = ref([])
const chapters = ref([])
const quizzes = ref([])
const selectedSubject = ref(null)
const selectedChapter = ref(null)
const selectedQuiz = ref(null)
const sidebarMode = ref('subject') // 'subject' | 'chapter' | 'quiz'
const loading = reactive({
  subjects: false,
  chapters: false,
  quizzes: false,
})
const error = reactive({
  subjects: '',
  chapters: '',
  quizzes: '',
  addSubject: '',
  addChapter: '',
  addQuiz: '',
})

// Stats for the profile card
const stats = reactive({
  totalSubjects: 0,
  totalChapters: 0,
  totalQuizzes: 0,
})

// Add/Edit Subject form state
const subjectEditForm = reactive({
  active: false,
  id: null,
  name: '',
  description: '',
  originalName: '',
  originalDescription: ''
})

// Add/Edit Chapter form state
const chapterEditForm = reactive({
  active: false,
  id: null,
  name: '',
  originalName: ''
})

// Add/Edit Quiz form state
const quizEditForm = reactive({
  active: false,
  id: null,
  title: '',
  duration: 1,
  originalTitle: '',
  originalDuration: 1
})

// Add forms
const newSubject = reactive({ name: '', description: '' })
const newChapter = reactive({ name: '' })
const newQuiz = reactive({ title: '', duration: 1 })

// Current date for header
const currentDate = ref(new Date().toLocaleDateString(undefined, {
  weekday: "long",
  year: "numeric",
  month: "long",
  day: "numeric",
}))

// Fetchers
async function fetchSubjects() {
  loading.subjects = true
  error.subjects = ''
  try {
    const res = await api.get('/subjects/with-details')
    subjects.value = res.data
    stats.totalSubjects = res.data.length
    // Calculate total chapters and quizzes
    stats.totalChapters = res.data.reduce((sum, subject) => sum + (subject.chapters?.length || 0), 0)
    stats.totalQuizzes = res.data.reduce((sum, subject) => {
      return sum + (subject.chapters?.reduce((chapSum, chapter) => {
        return chapSum + (chapter.quizzes?.length || 0)
      }, 0) || 0)
    }, 0)
  } catch (e) {
    error.subjects = 'Failed to load subjects'
  } finally {
    loading.subjects = false
  }
}

async function fetchChapters(subjectId) {
  loading.chapters = true
  error.chapters = ''
  try {
    const res = await api.get(`chapters/subject/${subjectId}`)
    chapters.value = res.data
  } catch (e) {
    error.chapters = 'Failed to load chapters'
  } finally {
    loading.chapters = false
  }
}

async function fetchQuizzes(chapterId) {
  loading.quizzes = true
  error.quizzes = ''
  try {
    const res = await api.get(`quizzes/chapter/${chapterId}`)
    quizzes.value = res.data
    console.log(quizzes.value)
  } catch (e) {
    error.quizzes = 'Failed to load quizzes'
  } finally {
    loading.quizzes = false
  }
}

// Selection logic
function resetAll() {
  selectedSubject.value = null
  selectedChapter.value = null
  selectedQuiz.value = null
  sidebarMode.value = 'subject'
  chapters.value = []
  quizzes.value = []
  cancelSubjectEditForm()
  cancelChapterEditForm()
  cancelQuizEditForm()
}

function selectSubject(subject) {
  selectedSubject.value = subject
  selectedChapter.value = null
  selectedQuiz.value = null
  sidebarMode.value = 'chapter'
  fetchChapters(subject.id)
  quizzes.value = []
  cancelSubjectEditForm()
  cancelChapterEditForm()
  cancelQuizEditForm()
}

function selectChapter(chapter) {
  selectedChapter.value = chapter
  selectedQuiz.value = null
  sidebarMode.value = 'quiz'
  fetchQuizzes(chapter.id)
  cancelChapterEditForm()
  cancelQuizEditForm()
}

function goToQuestionBank(quizId) {
  router.push({ name: 'QuestionManagement', params: { quizid: quizId } })
}

// Sidebar back button logic
function handleSidebarBack() {
  if (sidebarMode.value === 'quiz') {
    // Go back to chapter list
    sidebarMode.value = 'chapter'
    selectedQuiz.value = null
    cancelQuizEditForm()
  } else if (sidebarMode.value === 'chapter') {
    // Go back to subject list
    sidebarMode.value = 'subject'
    selectedChapter.value = null
    quizzes.value = []
    cancelChapterEditForm()
    cancelQuizEditForm()
  }
}

// Subject edit form logic
function startSubjectEditForm(subject) {
  subjectEditForm.active = true
  subjectEditForm.id = subject.id
  subjectEditForm.name = subject.name
  subjectEditForm.description = subject.description
  subjectEditForm.originalName = subject.name
  subjectEditForm.originalDescription = subject.description
}

function cancelSubjectEditForm() {
  subjectEditForm.active = false
  subjectEditForm.id = null
  subjectEditForm.name = ''
  subjectEditForm.description = ''
  subjectEditForm.originalName = ''
  subjectEditForm.originalDescription = ''
}

async function updateSubject() {
  error.addSubject = ''
  if (!subjectEditForm.name.trim() || !subjectEditForm.description.trim()) return
  try {
    await api.put(`/subjects/${subjectEditForm.id}`, {
      name: subjectEditForm.name,
      description: subjectEditForm.description
    })
    await fetchSubjects()
    cancelSubjectEditForm()
    showToast('Subject updated successfully!')
  } catch (e) {
    error.addSubject = 'Error updating subject.'
  }
}

// Chapter edit form logic
function startChapterEditForm(chapter) {
  chapterEditForm.active = true
  chapterEditForm.id = chapter.id
  chapterEditForm.name = chapter.name
  chapterEditForm.originalName = chapter.name
}

function cancelChapterEditForm() {
  chapterEditForm.active = false
  chapterEditForm.id = null
  chapterEditForm.name = ''
  chapterEditForm.originalName = ''
}

async function updateChapter() {
  error.addChapter = ''
  if (!chapterEditForm.name.trim() || !chapterEditForm.id) return
  try {
    await api.put(`/chapters/${chapterEditForm.id}`, { name: chapterEditForm.name })
    await fetchChapters(selectedSubject.value.id)
    cancelChapterEditForm()
    showToast('Chapter updated successfully!')
  } catch (e) {
    error.addChapter = 'Error updating chapter.'
  }
}

// Quiz edit form logic
function startQuizEditForm(quiz) {
  quizEditForm.active = true
  quizEditForm.id = quiz.id
  quizEditForm.title = quiz.title
  quizEditForm.duration = quiz.duration
  quizEditForm.originalTitle = quiz.title
  quizEditForm.originalDuration = quiz.duration
}

function cancelQuizEditForm() {
  quizEditForm.active = false
  quizEditForm.id = null
  quizEditForm.title = ''
  quizEditForm.duration = 1
  quizEditForm.originalTitle = ''
  quizEditForm.originalDuration = 1
}

async function updateQuiz() {
  error.addQuiz = ''
  if (!quizEditForm.title.trim() || !quizEditForm.id || !quizEditForm.duration) return
  try {
    await api.put(`/quizzes/${quizEditForm.id}`, { title: quizEditForm.title, duration: quizEditForm.duration })
    await fetchQuizzes(selectedChapter.value.id)
    cancelQuizEditForm()
    showToast('Quiz updated successfully!')
  } catch (e) {
    error.addQuiz = 'Error updating quiz.'
  }
}

async function deleteItem(type, id) {
  if (!confirm('Are you sure?')) return
  try {
    if (type === 'subject') {
      await api.delete(`/subjects/${id}`)
      await fetchSubjects()
      resetAll()
      showToast('Subject deleted!')
    } else if (type === 'chapter') {
      await api.delete(`/chapters/${id}`)
      await fetchChapters(selectedSubject.value.id)
      selectedChapter.value = null
      sidebarMode.value = 'chapter'
      showToast('Chapter deleted!')
    } else if (type === 'quiz') {
      await api.delete(`/quizzes/${id}`)
      await fetchQuizzes(selectedChapter.value.id)
      selectedQuiz.value = null
      sidebarMode.value = 'quiz'
      cancelQuizEditForm()
      showToast('Quiz deleted!')
    }
  } catch (e) {
    // Optionally show error
  }
}

// Add forms logic
async function addSubject() {
  error.addSubject = ''
  if (!newSubject.name.trim() || !newSubject.description.trim()) return
  try {
    await api.post('subjects/addsubject', { name: newSubject.name, description: newSubject.description })
    newSubject.name = ''
    newSubject.description = ''
    await fetchSubjects()
    showToast('Subject added!')
  } catch (e) {
    error.addSubject = 'Error adding subject.'
  }
}

async function addChapter() {
  error.addChapter = ''
  if (!newChapter.name.trim() || !selectedSubject.value) return
  try {
    await api.post('chapters/addchapter', { name: newChapter.name, subject_id: selectedSubject.value.id })
    newChapter.name = ''
    await fetchChapters(selectedSubject.value.id)
    showToast('Chapter added!')
  } catch (e) {
    error.addChapter = 'Error adding chapter.'
  }
}

async function addQuiz() {
  error.addQuiz = ''
  if (!newQuiz.title.trim() || !selectedChapter.value || !newQuiz.duration) return
  try {
    await api.post('quizzes/addquiz', { 
      title: newQuiz.title, 
      chapter_id: selectedChapter.value.id,
      duration: newQuiz.duration
    })
    newQuiz.title = ''
    newQuiz.duration = 1
    await fetchQuizzes(selectedChapter.value.id)
    showToast('Quiz added!')
  } catch (e) {
    error.addQuiz = 'Error adding quiz.'
  }
}

// Logout function
function logout() {
  localStorage.removeItem('token')
  router.push("/login")
}

// Watchers
watch(selectedSubject, (val) => {
  if (!val) {
    chapters.value = []
    selectedChapter.value = null
    sidebarMode.value = 'subject'
    cancelSubjectEditForm()
    cancelChapterEditForm()
    cancelQuizEditForm()
  }
})

watch(selectedChapter, (val) => {
  if (!val) {
    quizzes.value = []
    selectedQuiz.value = null
    sidebarMode.value = selectedSubject.value ? 'chapter' : 'subject'
    cancelChapterEditForm()
    cancelQuizEditForm()
  }
})

watch(selectedQuiz, (val) => {
  if (!val) {
    sidebarMode.value = selectedChapter.value ? 'quiz' : (selectedSubject.value ? 'chapter' : 'subject')
  }
})

// On mount
onMounted(() => {
  fetchSubjects()
})
</script>

<style scoped>
/* Toast styles */
.custom-toast {
  position: fixed;
  top: 30px;
  right: 30px;
  z-index: 9999;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: #fff;
  padding: 1rem 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 4px 16px rgba(34,197,94,0.15);
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  min-width: 200px;
  max-width: 350px;
  animation: fadeInOut 2.5s;
}
@keyframes fadeInOut {
  0% { opacity: 0; transform: translateY(-20px);}
  10% { opacity: 1; transform: translateY(0);}
  90% { opacity: 1; }
  100% { opacity: 0; transform: translateY(-20px);}
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* Reuse all the dashboard styles */
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

.stat-content {
  flex-grow: 0.8;
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
  cursor: pointer;
}

.progress-item:hover {
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
}

.progress-item.active {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
}

.progress-item.active .progress-title,
.progress-item.active .progress-subtitle {
  color: white;
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

.btn-accent {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  border: none;
  color: #fff;
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-accent:hover {
  background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%);
  color: #fff;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.btn-secondary {
  background: #f3f4f6;
  color: #6b7280;
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  font-weight: 500;
  transition: all 0.3s ease;
  border: none;
}

.btn-secondary:hover {
  background: #e5e7eb;
  color: #6b7280;
}

.alert {
  padding: 1rem;
  border-radius: 0.5rem;
  margin-top: 1rem;
}

.alert-danger {
  background-color: #fee2e2;
  color: #991b1b;
  border-left: 4px solid #ef4444;
}

.alert-info {
  background-color: #e0f2fe;
  color: #0369a1;
  border-left: 4px solid #0ea5e9;
}

/* Responsive Design */
@media (max-width: 1200px) {
  .welcome-title {
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

  .profile-card {
    max-width: 100%;
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
}
</style>