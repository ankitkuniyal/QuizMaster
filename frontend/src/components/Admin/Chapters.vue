<template>
  <section class="quiz-section d-flex flex-column min-vh-100" style="background: linear-gradient(90deg, #6366f1 0%, #06b6d4 100%);">
    <!-- Quiz NavBar -->
    <nav class="navbar navbar-expand-lg navbar-dark shadow-sm rounded-4 mt-4 mx-auto"
         style="max-width: 900px; background: linear-gradient(90deg, #6366f1 0%, #06b6d4 100%);">
      <div class="container-fluid">
        <a class="navbar-brand fw-bold text-white" href="#">
          <i class="fas fa-graduation-cap me-2"></i>Quiz Master
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#quizNavbar" aria-controls="quizNavbar" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="quizNavbar">
          <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a href="/dashboard/admin" class="nav-link text-white">Dashboard</a>
            </li>
            <li class="nav-item">
              <a href="/dashboard/admin/subjects" class="nav-link text-white">Subjects</a>
            </li>
            <li class="nav-item">
              <a href="/dashboard/admin/chapters/1" class="nav-link text-white">Chapters</a>
            </li>
            <li class="nav-item">
              <a href="/dashboard/admin/quizzes/1" class="nav-link text-white">Quizzes</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <!-- End Quiz NavBar -->

    <!-- Filter Bar -->
    <div class="container mt-4" style="max-width: 100vw;">
      <div class="row justify-content-center">
        <div class="col-lg-9">
          <div class="info-bar bg-white rounded-4 shadow-sm p-4 mb-4 d-flex flex-wrap align-items-center gap-4 justify-content-between">
            <div class="d-flex align-items-center gap-2">
              <i class="fas fa-book-open text-accent"></i>
              <span class="fw-semibold">Subject:</span>
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
              <i class="fas fa-layer-group text-info"></i>
              <span class="fw-semibold">Chapter:</span>
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
    <!-- End Filter Bar -->

    <div class="container my-5">
      <div class="row justify-content-center">
        <!-- Sidebar -->
        <div class="col-lg-3 mb-4 mb-lg-0">
          <div class="sidebar-card shadow-sm rounded-4 p-3 bg-white h-100">
            <!-- Subjects List -->
            <template v-if="sidebarMode === 'subject'">
              <h5 class="fw-bold mb-3 text-accent">Subjects</h5>
              <div class="sidebar-questions-list mb-4">
                <div
                  v-for="subject in subjects"
                  :key="subject.id"
                  class="sidebar-question-item d-flex justify-content-between align-items-center"
                  :class="{ active: selectedSubject && selectedSubject.id === subject.id }"
                  style="cursor: pointer;"
                  @click="selectSubject(subject)"
                >
                  <template v-if="editingItem.type === 'subject' && editingItem.id === subject.id">
                    <input
                      v-model="editingItem.name"
                      class="form-control form-control-sm me-2"
                      style="max-width: 120px;"
                      @keyup.enter="saveEdit"
                      @blur="saveEdit"
                      autofocus
                    />
                    <div class="d-flex align-items-center ms-2">
                      <button class="btn btn-sm btn-success" @click.stop="saveEdit" title="Save"><i class="fas fa-check"></i></button>
                      <button class="btn btn-sm btn-secondary ms-1" @click.stop="cancelEdit" title="Cancel"><i class="fas fa-times"></i></button>
                    </div>
                  </template>
                  <template v-else>
                    <span class="fw-semibold flex-grow-1 text-start">{{ subject.name }}</span>
                    <div class="d-flex align-items-center ms-2">
                      <button class="btn btn-sm btn-outline-secondary" title="Rename" @click.stop="startSubjectEditForm(subject)">
                        <i class="fas fa-edit"></i>
                      </button>
                      <button class="btn btn-sm btn-outline-danger ms-1" title="Delete" @click.stop="deleteItem('subject', subject.id)">
                        <i class="fas fa-trash"></i>
                      </button>
                    </div>
                  </template>
                </div>
              </div>
              <div class="alert alert-info text-center mt-3" v-if="!subjects.length && !loading.subjects">
                No subjects found.
              </div>
            </template>

            <!-- Chapters List -->
            <template v-if="sidebarMode === 'chapter' && selectedSubject">
              <h5 class="fw-bold mb-3 text-accent">Chapters</h5>
              <div class="sidebar-questions-list mb-4">
                <div
                  v-for="chapter in chapters"
                  :key="chapter.id"
                  class="sidebar-question-item d-flex justify-content-between align-items-center"
                  :class="{ active: selectedChapter && selectedChapter.id === chapter.id }"
                  style="cursor: pointer;"
                  @click="selectChapter(chapter)"
                >
                  <template v-if="editingItem.type === 'chapter' && editingItem.id === chapter.id">
                    <input
                      v-model="editingItem.name"
                      class="form-control form-control-sm me-2"
                      style="max-width: 120px;"
                      @keyup.enter="saveEdit"
                      @blur="saveEdit"
                      autofocus
                    />
                    <div class="d-flex align-items-center ms-2">
                      <button class="btn btn-sm btn-success" @click.stop="saveEdit" title="Save"><i class="fas fa-check"></i></button>
                      <button class="btn btn-sm btn-secondary ms-1" @click.stop="cancelEdit" title="Cancel"><i class="fas fa-times"></i></button>
                    </div>
                  </template>
                  <template v-else>
                    <span class="fw-semibold flex-grow-1 text-start">{{ chapter.name }}</span>
                    <div class="d-flex align-items-center ms-2">
                      <button class="btn btn-sm btn-outline-secondary" title="Rename" @click.stop="startChapterEditForm(chapter)">
                        <i class="fas fa-edit"></i>
                      </button>
                      <button class="btn btn-sm btn-outline-danger ms-1" title="Delete" @click.stop="deleteItem('chapter', chapter.id)">
                        <i class="fas fa-trash"></i>
                      </button>
                    </div>
                  </template>
                </div>
              </div>
              <div class="alert alert-info text-center mt-3" v-if="!chapters.length && !loading.chapters">
                No chapters found.
              </div>
            </template>

            <!-- Quizzes List -->
            <template v-if="sidebarMode === 'quiz' && selectedChapter">
              <h5 class="fw-bold mb-3 text-accent">Quizzes</h5>
              <div class="sidebar-questions-list mb-4">
                <div
                  v-for="quiz in quizzes"
                  :key="quiz.id"
                  class="sidebar-question-item d-flex justify-content-between align-items-center"
                  :class="{ active: selectedQuiz && selectedQuiz.id === quiz.id }"
                  style="cursor: pointer;"
                  @click="goToQuestionBank(quiz.id)"
                >
                  <template v-if="quizEditForm.active && quizEditForm.id === quiz.id">
                    <span class="fw-semibold flex-grow-1 text-start">{{ quiz.title }}</span>
                    <div class="d-flex align-items-center ms-2">
                      <span class="badge bg-info text-white">Editing...</span>
                    </div>
                  </template>
                  <template v-else>
                    <span class="fw-semibold flex-grow-1 text-start">{{ quiz.title }}</span>
                    <div class="d-flex align-items-center ms-2">
                      <button class="btn btn-sm btn-outline-secondary" title="Rename" @click.stop="startQuizEditForm(quiz)">
                        <i class="fas fa-edit"></i>
                      </button>
                      <button class="btn btn-sm btn-outline-danger ms-1" title="Delete" @click.stop="deleteItem('quiz', quiz.id)">
                        <i class="fas fa-trash"></i>
                      </button>
                    </div>
                  </template>
                </div>
              </div>
              <div class="alert alert-info text-center mt-3" v-if="!quizzes.length && !loading.quizzes">
                No quizzes found.
              </div>
            </template>
          </div>
        </div>
        <!-- Main content -->
        <div class="col-lg-9">
          <div class="card border-0 shadow-lg rounded-4 p-4 bg-white position-relative">
            <!-- Add/Edit Subject (No subject selected) -->
            <div v-if="sidebarMode === 'subject'" class="mb-4 text-center">
              <span class="badge bg-accent px-3 py-2 mb-2 fs-6 shadow-sm">
                {{ subjectEditForm.active ? 'Edit Subject' : 'Add New Subject' }}
              </span>
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
              <span class="badge bg-accent px-3 py-2 mb-2 fs-6 shadow-sm">
                {{ chapterEditForm.active ? 'Edit Chapter' : 'Add New Chapter' }}
              </span>
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
              <span class="badge bg-accent px-3 py-2 mb-2 fs-6 shadow-sm">
                {{ quizEditForm.active ? 'Edit Quiz' : 'Add New Quiz' }}
              </span>
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
        <!-- End Main content -->
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import api from '../../api'
import { useRouter } from 'vue-router'
const router = useRouter()
// State
const subjects = ref([])
const chapters = ref([])
const quizzes = ref([])
const questions = ref([])

const selectedSubject = ref(null)
const selectedChapter = ref(null)
const selectedQuiz = ref(null)
const sidebarMode = ref('subject') // 'subject' | 'chapter' | 'quiz' | 'question'
const loading = reactive({
  subjects: false,
  chapters: false,
  quizzes: false,
  questions: false,
})
const error = reactive({
  subjects: '',
  chapters: '',
  quizzes: '',
  questions: '',
  addSubject: '',
  addChapter: '',
  addQuiz: '',
  addQuestion: '',
  updateQuestion: '',
})

// Inline edit state
const editingItem = reactive({
  type: null, // 'subject' | 'chapter' | 'quiz'
  id: null,
  name: '',
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
const newQuestion = reactive({
  text: '',
  options: ['', '', '', ''],
  correct: 0,
  difficulty: '',
})

// Question editing state
const selectedQuestionIndex = ref(-1)
const isEditMode = ref(false)
const editQuestion = ref({
  text: '',
  options: ['', '', '', ''],
  correct: 0,
  difficulty: ''
})

// Fetchers
async function fetchSubjects() {
  loading.subjects = true
  error.subjects = ''
  try {
    const res = await api.get('/subjects/with-details')
    subjects.value = res.data
  } catch (e) {
    error.subjects = 'Failed to load subjects'
  }
  loading.subjects = false
}
async function fetchChapters(subjectId) {
  loading.chapters = true
  error.chapters = ''
  try {
    const res = await api.get(`chapters/subject/${subjectId}`)
    chapters.value = res.data
  } catch (e) {
    error.chapters = 'Failed to load chapters'
  }
  loading.chapters = false
}
async function fetchQuizzes(chapterId) {
  loading.quizzes = true
  error.quizzes = ''
  try {
    const res = await api.get(`quizzes/chapter/${chapterId}`)
    quizzes.value = res.data
  } catch (e) {
    error.quizzes = 'Failed to load quizzes'
  }
  loading.quizzes = false
}
async function fetchQuestions(quizId) {
  loading.questions = true
  error.questions = ''
  try {
    const res = await api.get(`/questions/quiz/${quizId}`)
    questions.value = res.data
  } catch (e) {
    error.questions = 'Failed to load questions'
  }
  loading.questions = false
  clearSelectedQuestion()
}

// Selection logic
function resetAll() {
  selectedSubject.value = null
  selectedChapter.value = null
  selectedQuiz.value = null
  sidebarMode.value = 'subject'
  chapters.value = []
  quizzes.value = []
  questions.value = []
  clearSelectedQuestion()
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
  questions.value = []
  clearSelectedQuestion()
  cancelSubjectEditForm()
  cancelChapterEditForm()
  cancelQuizEditForm()
}
function selectChapter(chapter) {
  selectedChapter.value = chapter
  selectedQuiz.value = null
  sidebarMode.value = 'quiz'
  fetchQuizzes(chapter.id)
  questions.value = []
  clearSelectedQuestion()
  cancelChapterEditForm()
  cancelQuizEditForm()
}
function selectQuiz(quiz) {
  selectedQuiz.value = quiz
  sidebarMode.value = 'question'
  fetchQuestions(quiz.id)
  clearSelectedQuestion()
}
function selectQuestion(idx) {
  selectedQuestionIndex.value = idx
  isEditMode.value = false
  if (questions.value[idx]) {
    // Deep copy to avoid mutating original
    editQuestion.value = JSON.parse(JSON.stringify(questions.value[idx]))
    // Defensive: ensure editQuestion.value is always a valid object with required fields
    if (
      !editQuestion.value ||
      typeof editQuestion.value !== 'object' ||
      !Array.isArray(editQuestion.value.options) ||
      typeof editQuestion.value.text !== 'string' ||
      typeof editQuestion.value.correct !== 'number' ||
      typeof editQuestion.value.difficulty !== 'string'
    ) {
      editQuestion.value = {
        text: '',
        options: ['', '', '', ''],
        correct: 0,
        difficulty: ''
      }
    }
  } else {
    // Defensive: always set to a valid object
    editQuestion.value = {
      text: '',
      options: ['', '', '', ''],
      correct: 0,
      difficulty: ''
    }
  }
}
function clearSelectedQuestion() {
  selectedQuestionIndex.value = -1
  isEditMode.value = false
  editQuestion.value = {
    text: '',
    options: ['', '', '', ''],
    correct: 0,
    difficulty: ''
  }
}

// Inline edit logic for sidebar quick rename
function startEdit(type, item) {
  // Only allow inline edit for subject/chapter, not quiz
  if (type === 'quiz') return
  editingItem.type = type
  editingItem.id = item.id
  editingItem.name = item.name || item.title
}
function cancelEdit() {
  editingItem.type = null
  editingItem.id = null
  editingItem.name = ''
}
async function saveEdit() {
  if (!editingItem.name.trim()) return
  try {
    if (editingItem.type === 'subject') {
      await api.put(`/subjects/${editingItem.id}`, { name: editingItem.name })
      await fetchSubjects()
    } else if (editingItem.type === 'chapter') {
      await api.put(`/chapters/${editingItem.id}`, { name: editingItem.name })
      await fetchChapters(selectedSubject.value.id)
    }
    cancelEdit()
  } catch (e) {
    // Optionally show error
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
    } else if (type === 'chapter') {
      await api.delete(`/chapters/${id}`)
      await fetchChapters(selectedSubject.value.id)
      selectedChapter.value = null
      sidebarMode.value = 'chapter'
    } else if (type === 'quiz') {
      await api.delete(`/quizzes/${id}`)
      await fetchQuizzes(selectedChapter.value.id)
      selectedQuiz.value = null
      sidebarMode.value = 'quiz'
      cancelQuizEditForm()
    }
  } catch (e) {
    // Optionally show error
  }
}

// Add forms logic
function goToQuestionBank(quizId) {
  router.push({ name: 'QuestionManagement', params: { quizid: quizId } })
}
async function addSubject() {
  error.addSubject = ''
  if (!newSubject.name.trim() || !newSubject.description.trim()) return
  try {
    await api.post('subjects/addsubject', { name: newSubject.name, description: newSubject.description })
    newSubject.name = ''
    newSubject.description = ''
    await fetchSubjects()
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
  } catch (e) {
    error.addQuiz = 'Error adding quiz.'
  }
}
async function addQuestion() {
  error.addQuestion = ''
  // Validate input
  if (
    !newQuestion.text.trim() ||
    newQuestion.options.some(opt => !opt.trim()) ||
    new Set(newQuestion.options).size !== 4 ||
    !newQuestion.difficulty ||
    selectedQuiz.value == null
  ) return

  try {
    const payload = {
      text: newQuestion.text,
      options: newQuestion.options.map(opt => ({ text: opt })),
      correctIndex: Number(newQuestion.correct),
      difficulty: newQuestion.difficulty,
    }
    await api.post(`/questions/${selectedQuiz.value.id}`, payload)
    // Reset form
    Object.assign(newQuestion, {
      text: '',
      options: ['', '', '', ''],
      correct: 0,
      difficulty: ''
    })
    await fetchQuestions(selectedQuiz.value.id)
  } catch (e) {
    error.addQuestion = 'Error adding question.'
  }
}

// Edit Question logic
function editQuestionHandler(idx) {
  selectQuestion(idx)
  isEditMode.value = true
}
async function updateQuestion() {
  error.updateQuestion = ''
  if (
    !editQuestion.value ||
    typeof editQuestion.value !== 'object' ||
    !editQuestion.value.text ||
    !Array.isArray(editQuestion.value.options) ||
    editQuestion.value.options.some(opt => !opt || typeof opt !== 'string' || !opt.trim()) ||
    new Set(editQuestion.value.options).size !== 4 ||
    !editQuestion.value.difficulty ||
    selectedQuiz.value == null ||
    selectedQuestionIndex.value === -1
  ) return

  try {
    const payload = {
      text: editQuestion.value.text,
      options: editQuestion.value.options.map(opt => ({ text: opt })),
      correctIndex: Number(editQuestion.value.correct),
      difficulty: editQuestion.value.difficulty,
    }
    const qid = questions.value[selectedQuestionIndex.value].id
    await api.put(`/questions/${qid}`, payload)
    await fetchQuestions(selectedQuiz.value.id)
    isEditMode.value = false
    // Keep the same question selected after update
    const idx = questions.value.findIndex(q => q.id === qid)
    if (idx !== -1) selectQuestion(idx)
    else clearSelectedQuestion()
  } catch (e) {
    error.updateQuestion = 'Error updating question.'
  }
}
async function deleteQuestion(idx) {
  if (!questions.value[idx]) return
  if (!confirm('Delete this question?')) return
  try {
    const qid = questions.value[idx].id
    await api.delete(`/questions/${qid}`)
    await fetchQuestions(selectedQuiz.value.id)
    clearSelectedQuestion()
  } catch (e) {
    // Optionally show error
  }
}

// Watchers
watch(selectedSubject, (val) => {
  if (!val) {
    chapters.value = []
    selectedChapter.value = null
    sidebarMode.value = 'subject'
    clearSelectedQuestion()
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
    clearSelectedQuestion()
    cancelChapterEditForm()
    cancelQuizEditForm()
  }
})
watch(selectedQuiz, (val) => {
  if (!val) {
    questions.value = []
    sidebarMode.value = selectedChapter.value ? 'quiz' : (selectedSubject.value ? 'chapter' : 'subject')
    clearSelectedQuestion()
  }
})

// On mount
onMounted(() => {
  resetAll()
  fetchSubjects()
})
</script>

<style scoped>
.quiz-section {
  min-height: 100vh;
  background: linear-gradient(90deg, #6366f1 0%, #06b6d4 100%);
}
.bg-accent {
  background: #06b6d4 !important;
  color: #fff !important;
}
.text-accent {
  color: #6366f1 !important;
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
.btn-edit-icon {
  background: #fff;
  border: none;
  box-shadow: 0 2px 8px 0 rgba(31, 38, 135, 0.10);
  border-radius: 50%;
  width: 2.2rem;
  height: 2.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: box-shadow 0.2s;
}
.btn-edit-icon:hover, .btn-edit-icon:focus {
  box-shadow: 0 4px 16px 0 rgba(6,182,212,0.15);
  background: #e0e7ff;
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
  max-width: 900px;
  width: 100%;
}
.popup-card-large {
  min-width: 600px;
  max-width: 900px;
  width: 100%;
}
.question-card {
  border-radius: 1rem;
  background: #f8fafc;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.list-group-item.bg-success {
  background: #06b6d4 !important;
  color: #fff !important;
}

/* Sidebar styles */
.sidebar-card {
  min-height: 400px;
  max-height: 100vh;
  overflow-y: auto;
}
.sidebar-questions-list {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.sidebar-question-item {
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  color: #334155;
}
.sidebar-question-item.active,
.sidebar-question-item:hover {
  background: #6366f1;
  color: #fff;
}
.sidebar-question-text {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.current-question {
  border: 2px solid #06b6d4;
}

/* Info bar styles */
.info-bar {
  font-size: 1.05rem;
  background: #f1f5f9;
  border-left: 5px solid #06b6d4;
}
</style>


