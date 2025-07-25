<template>
  <section class="admin-quiz-section">
    <div class="container">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="mb-0">Admin Dashboard</h2>
        <div>
          <router-link to="/dashboard/admin" class="btn btn-outline-primary me-2">
            <i class="fas fa-arrow-left"></i> Back to Dashboard
          </router-link>
          <button class="btn btn-danger" @click="deleteDatabase" :disabled="deletingDb">
            <i class="fas fa-trash-alt"></i>
            <span v-if="!deletingDb"> Delete Database</span>
            <span v-else><i class="fas fa-spinner fa-spin"></i> Deleting...</span>
          </button>
        </div>
      </div>
      <div v-if="loading" class="text-center my-5">
        <i class="fas fa-spinner fa-spin fa-2x"></i>
      </div>
      <div v-else>
        <!-- Table Selector -->
        <div class="mb-4 d-flex align-items-center gap-3">
          <label for="tableSelect" class="form-label mb-0">Show Table:</label>
          <select id="tableSelect" v-model="selectedTable" class="form-select w-auto">
            <option value="all">All</option>
            <option value="users">Users</option>
            <option value="quizzes">Quizzes</option>
            <option value="subjects">Subjects</option>
            <option value="chapters">Chapters</option>
            <option value="questions">Questions</option>
            <option value="results">Results</option>
          </select>
        </div>

        <!-- All Tables -->
        <template v-if="selectedTable === 'all'">
          <!-- Users Table -->
          <div>
            <h4 class="mt-4 mb-2">All Users</h4>
            <div class="mb-2 d-flex gap-2 align-items-center">
              <input v-model="userSearch" class="form-control w-auto" placeholder="Search users..." />
              <select v-model="userSortKey" class="form-select w-auto">
                <option value="name">Sort by Name</option>
                <option value="email">Sort by Email</option>
                <option value="role">Sort by Role</option>
                <option value="id">Sort by ID</option>
              </select>
              <button class="btn btn-outline-secondary btn-sm" @click="userSortAsc = !userSortAsc">
                <i :class="userSortAsc ? 'fas fa-sort-alpha-down' : 'fas fa-sort-alpha-up'"></i>
              </button>
            </div>
            <div class="table-responsive mb-4">
              <table class="table table-striped table-bordered align-middle">
                <thead class="table-light">
                  <tr>
                    <th>User ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Qualification</th>
                    <th>Role</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="user in filteredSortedUsers" :key="user.id">
                    <td>{{ user.id }}</td>
                    <td>{{ user.name }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.qualification }}</td>
                    <td>{{ user.role }}</td>
                  </tr>
                  <tr v-if="filteredSortedUsers.length === 0">
                    <td colspan="6" class="text-center text-muted">No users found.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Quizzes Table -->
          <div>
            <h4 class="mt-4 mb-2">All Quizzes</h4>
            <div class="mb-2 d-flex gap-2 align-items-center">
              <input v-model="quizSearch" class="form-control w-auto" placeholder="Search quizzes..." />
              <select v-model="quizSortKey" class="form-select w-auto">
                <option value="id">Sort by Quiz ID</option>
                <option value="title">Sort by Title</option>
                <option value="chapter_id">Sort by Chapter ID</option>
                <option value="duration">Sort by Duration</option>
                <option value="created_at">Sort by Created At</option>
              </select>
              <button class="btn btn-outline-secondary btn-sm" @click="quizSortAsc = !quizSortAsc">
                <i :class="quizSortAsc ? 'fas fa-sort-alpha-down' : 'fas fa-sort-alpha-up'"></i>
              </button>
            </div>
            <div class="table-responsive mb-4">
              <table class="table table-striped table-bordered align-middle">
                <thead class="table-light">
                  <tr>
                    <th>Quiz ID</th>
                    <th>Title</th>
                    <th>Subject ID</th>
                    <th>Chapter ID</th>
                    <th>Duration</th>
                    <th>Created At</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="quiz in filteredSortedQuizzes" :key="quiz.id">
                    <td>{{ quiz.id }}</td>
                    <td>{{ quiz.title }}</td>
                    <td>{{ getSubjectIdByChapterId(quiz.chapter_id) }}</td>
                    <td>{{ quiz.chapter_id }}</td>
                    <td>{{ quiz.duration }}</td>
                    <td>{{ quiz.created_at }}</td>
                  </tr>
                  <tr v-if="filteredSortedQuizzes.length === 0">
                    <td colspan="7" class="text-center text-muted">No quizzes found.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Subjects Table -->
          <div>
            <h4 class="mt-4 mb-2">All Subjects</h4>
            <div class="mb-2 d-flex gap-2 align-items-center">
              <input v-model="subjectSearch" class="form-control w-auto" placeholder="Search subjects..." />
              <select v-model="subjectSortKey" class="form-select w-auto">
                <option value="id">Sort by Subject ID</option>
                <option value="name">Sort by Name</option>
              </select>
              <button class="btn btn-outline-secondary btn-sm" @click="subjectSortAsc = !subjectSortAsc">
                <i :class="subjectSortAsc ? 'fas fa-sort-alpha-down' : 'fas fa-sort-alpha-up'"></i>
              </button>
            </div>
            <div class="table-responsive mb-4">
              <table class="table table-striped table-bordered align-middle">
                <thead class="table-light">
                  <tr>
                    <th>Subject ID</th>
                    <th>Name</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="subject in filteredSortedSubjects" :key="subject.id">
                    <td>{{ subject.id }}</td>
                    <td>{{ subject.name }}</td>
                    <td>{{ subject.description }}</td>
                  </tr>
                  <tr v-if="filteredSortedSubjects.length === 0">
                    <td colspan="4" class="text-center text-muted">No subjects found.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Chapters Table -->
          <div>
            <h4 class="mt-4 mb-2">All Chapters</h4>
            <div class="mb-2 d-flex gap-2 align-items-center">
              <input v-model="chapterSearch" class="form-control w-auto" placeholder="Search chapters..." />
              <select v-model="chapterSortKey" class="form-select w-auto">
                <option value="id">Sort by Chapter ID</option>
                <option value="name">Sort by Name</option>
                <option value="subject_id">Sort by Subject ID</option>
              </select>
              <button class="btn btn-outline-secondary btn-sm" @click="chapterSortAsc = !chapterSortAsc">
                <i :class="chapterSortAsc ? 'fas fa-sort-alpha-down' : 'fas fa-sort-alpha-up'"></i>
              </button>
            </div>
            <div class="table-responsive mb-4">
              <table class="table table-striped table-bordered align-middle">
                <thead class="table-light">
                  <tr>
                    <th>Chapter ID</th>
                    <th>Name</th>
                    <th>Subject ID</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="chapter in filteredSortedChapters" :key="chapter.id">
                    <td>{{ chapter.id }}</td>
                    <td>{{ chapter.name }}</td>
                    <td>{{ chapter.subject_id }}</td>
                  </tr>
                  <tr v-if="filteredSortedChapters.length === 0">
                    <td colspan="5" class="text-center text-muted">No chapters found.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Questions Table -->
          <div>
            <h4 class="mt-4 mb-2">All Questions</h4>
            <div class="mb-2 d-flex gap-2 align-items-center">
              <input v-model="questionSearch" class="form-control w-auto" placeholder="Search questions..." />
              <select v-model="questionSortKey" class="form-select w-auto">
                <option value="id">Sort by Question ID</option>
                <option value="quiz_id">Sort by Quiz ID</option>
                <option value="text">Sort by Text</option>
              </select>
              <button class="btn btn-outline-secondary btn-sm" @click="questionSortAsc = !questionSortAsc">
                <i :class="questionSortAsc ? 'fas fa-sort-alpha-down' : 'fas fa-sort-alpha-up'"></i>
              </button>
            </div>
            <div class="table-responsive mb-4">
              <table class="table table-striped table-bordered align-middle">
                <thead class="table-light">
                  <tr>
                    <th>Question ID</th>
                    <th>Quiz ID</th>
                    <th>Text</th>
                    <th>Options</th>
                    <th>Answer</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="question in filteredSortedQuestions" :key="question.id">
                    <td>{{ question.id }}</td>
                    <td>{{ question.quiz_id }}</td>
                    <td>{{ question.text }}</td>
                    <td>
                      <div v-if="question.option_a || question.option_b || question.option_c || question.option_d">
                        <ul class="mb-0 ps-3 ">
                          <li v-if="question.option_a">A. {{ question.option_a }}</li>
                          <li v-if="question.option_b">B. {{ question.option_b }}</li>
                          <li v-if="question.option_c">C. {{ question.option_c }}</li>
                          <li v-if="question.option_d">D. {{ question.option_d }}</li>
                        </ul>
                      </div>
                      <div v-else class="text-muted">No options</div>
                    </td>
                    <td>
                      <span v-if="question.correct_option !== undefined && question.correct_option !== null && question.correct_option !== ''">
                        {{ question.correct_option }}
                      </span>
                      <span v-else class="text-muted">No answer</span>
                    </td>
                  </tr>
                  <tr v-if="filteredSortedQuestions.length === 0">
                    <td colspan="6" class="text-center text-muted">No questions found.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Results Table -->
          <div>
            <h4 class="mt-4 mb-2">All Results</h4>
            <div class="mb-2 d-flex gap-2 align-items-center">
              <input v-model="resultSearch" class="form-control w-auto" placeholder="Search results..." />
              <select v-model="resultSortKey" class="form-select w-auto">
                <option value="id">Sort by Result ID</option>
                <option value="user_id">Sort by User ID</option>
                <option value="quiz_id">Sort by Quiz ID</option>
                <option value="score">Sort by Score</option>
                <option value="taken_at">Sort by Taken At</option>
              </select>
              <button class="btn btn-outline-secondary btn-sm" @click="resultSortAsc = !resultSortAsc">
                <i :class="resultSortAsc ? 'fas fa-sort-alpha-down' : 'fas fa-sort-alpha-up'"></i>
              </button>
            </div>
            <div class="table-responsive mb-4">
              <table class="table table-striped table-bordered align-middle">
                <thead class="table-light">
                  <tr>
                    <th>Result ID</th>
                    <th>User ID</th>
                    <th>Quiz ID</th>
                    <th>Score</th>
                    <th>Time Taken</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="result in filteredSortedResults" :key="result.id">
                    <td>{{ result.id }}</td>
                    <td>{{ result.user_id }}</td>
                    <td>{{ result.quiz_id }}</td>
                    <td>{{ result.score }}</td>
                    <td>{{ result.time_taken/60 }} min</td>
                  </tr>
                  <tr v-if="filteredSortedResults.length === 0">
                    <td colspan="6" class="text-center text-muted">No results found.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </template>

        <!-- Users Table -->
        <div v-else-if="selectedTable === 'users'">
          <h4 class="mt-4 mb-2">All Users</h4>
          <div class="mb-2 d-flex gap-2 align-items-center">
            <input v-model="userSearch" class="form-control w-auto" placeholder="Search users..." />
            <select v-model="userSortKey" class="form-select w-auto">
              <option value="name">Sort by Name</option>
              <option value="email">Sort by Email</option>
              <option value="role">Sort by Role</option>
              <option value="id">Sort by ID</option>
            </select>
            <button class="btn btn-outline-secondary btn-sm" @click="userSortAsc = !userSortAsc">
              <i :class="userSortAsc ? 'fas fa-sort-alpha-down' : 'fas fa-sort-alpha-up'"></i>
            </button>
          </div>
          <div class="table-responsive mb-4">
            <table class="table table-striped table-bordered align-middle">
              <thead class="table-light">
                <tr>
                  <th>User ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Qualification</th>
                  <th>Role</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in filteredSortedUsers" :key="user.id">
                  <td>{{ user.id }}</td>
                  <td>{{ user.name }}</td>
                  <td>{{ user.email }}</td>
                  <td>{{ user.qualification }}</td>
                  <td>{{ user.role }}</td>
                </tr>
                <tr v-if="filteredSortedUsers.length === 0">
                  <td colspan="6" class="text-center text-muted">No users found.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Quizzes Table -->
        <div v-else-if="selectedTable === 'quizzes'">
          <h4 class="mt-4 mb-2">All Quizzes</h4>
          <div class="mb-2 d-flex gap-2 align-items-center">
            <input v-model="quizSearch" class="form-control w-auto" placeholder="Search quizzes..." />
            <select v-model="quizSortKey" class="form-select w-auto">
              <option value="id">Sort by Quiz ID</option>
              <option value="title">Sort by Title</option>
              <option value="chapter_id">Sort by Chapter ID</option>
              <option value="duration">Sort by Duration</option>
              <option value="created_at">Sort by Created At</option>
            </select>
            <button class="btn btn-outline-secondary btn-sm" @click="quizSortAsc = !quizSortAsc">
              <i :class="quizSortAsc ? 'fas fa-sort-alpha-down' : 'fas fa-sort-alpha-up'"></i>
            </button>
          </div>
          <div class="table-responsive mb-4">
            <table class="table table-striped table-bordered align-middle">
              <thead class="table-light">
                <tr>
                  <th>Quiz ID</th>
                  <th>Title</th>
                  <th>Subject ID</th>
                  <th>Chapter ID</th>
                  <th>Duration</th>
                  <th>Created At</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="quiz in filteredSortedQuizzes" :key="quiz.id">
                  <td>{{ quiz.id }}</td>
                  <td>{{ quiz.title }}</td>
                  <td>{{ getSubjectIdByChapterId(quiz.chapter_id) }}</td>
                  <td>{{ quiz.chapter_id }}</td>
                  <td>{{ quiz.duration }}</td>
                  <td>{{ quiz.created_at }}</td>
                </tr>
                <tr v-if="filteredSortedQuizzes.length === 0">
                  <td colspan="7" class="text-center text-muted">No quizzes found.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Subjects Table -->
        <div v-else-if="selectedTable === 'subjects'">
          <h4 class="mt-4 mb-2">All Subjects</h4>
          <div class="mb-2 d-flex gap-2 align-items-center">
            <input v-model="subjectSearch" class="form-control w-auto" placeholder="Search subjects..." />
            <select v-model="subjectSortKey" class="form-select w-auto">
              <option value="id">Sort by Subject ID</option>
              <option value="name">Sort by Name</option>
            </select>
            <button class="btn btn-outline-secondary btn-sm" @click="subjectSortAsc = !subjectSortAsc">
              <i :class="subjectSortAsc ? 'fas fa-sort-alpha-down' : 'fas fa-sort-alpha-up'"></i>
            </button>
          </div>
          <div class="table-responsive mb-4">
            <table class="table table-striped table-bordered align-middle">
              <thead class="table-light">
                <tr>
                  <th>Subject ID</th>
                  <th>Name</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="subject in filteredSortedSubjects" :key="subject.id">
                  <td>{{ subject.id }}</td>
                  <td>{{ subject.name }}</td>
                  <td>{{ subject.description }}</td>
                </tr>
                <tr v-if="filteredSortedSubjects.length === 0">
                  <td colspan="4" class="text-center text-muted">No subjects found.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Chapters Table -->
        <div v-else-if="selectedTable === 'chapters'">
          <h4 class="mt-4 mb-2">All Chapters</h4>
          <div class="mb-2 d-flex gap-2 align-items-center">
            <input v-model="chapterSearch" class="form-control w-auto" placeholder="Search chapters..." />
            <select v-model="chapterSortKey" class="form-select w-auto">
              <option value="id">Sort by Chapter ID</option>
              <option value="name">Sort by Name</option>
              <option value="subject_id">Sort by Subject ID</option>
            </select>
            <button class="btn btn-outline-secondary btn-sm" @click="chapterSortAsc = !chapterSortAsc">
              <i :class="chapterSortAsc ? 'fas fa-sort-alpha-down' : 'fas fa-sort-alpha-up'"></i>
            </button>
          </div>
          <div class="table-responsive mb-4">
            <table class="table table-striped table-bordered align-middle">
              <thead class="table-light">
                <tr>
                  <th>Chapter ID</th>
                  <th>Name</th>
                  <th>Subject ID</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="chapter in filteredSortedChapters" :key="chapter.id">
                  <td>{{ chapter.id }}</td>
                  <td>{{ chapter.name }}</td>
                  <td>{{ chapter.subject_id }}</td>
                </tr>
                <tr v-if="filteredSortedChapters.length === 0">
                  <td colspan="5" class="text-center text-muted">No chapters found.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Questions Table -->
        <div v-else-if="selectedTable === 'questions'">
          <h4 class="mt-4 mb-2">All Questions</h4>
          <div class="mb-2 d-flex gap-2 align-items-center">
            <input v-model="questionSearch" class="form-control w-auto" placeholder="Search questions..." />
            <select v-model="questionSortKey" class="form-select w-auto">
              <option value="id">Sort by Question ID</option>
              <option value="quiz_id">Sort by Quiz ID</option>
              <option value="text">Sort by Text</option>
            </select>
            <button class="btn btn-outline-secondary btn-sm" @click="questionSortAsc = !questionSortAsc">
              <i :class="questionSortAsc ? 'fas fa-sort-alpha-down' : 'fas fa-sort-alpha-up'"></i>
            </button>
          </div>
          <div class="table-responsive mb-4">
            <table class="table table-striped table-bordered align-middle">
              <thead class="table-light">
                <tr>
                  <th>Question ID</th>
                  <th>Quiz ID</th>
                  <th>Text</th>
                  <th>Options</th>
                  <th>Answer</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="question in filteredSortedQuestions" :key="question.id">
                  <td>{{ question.id }}</td>
                  <td>{{ question.quiz_id }}</td>
                  <td>{{ question.text }}</td>
                  <td>
                    <div v-if="Array.isArray(question.options) && question.options.length">
                      <ul class="mb-0 ps-3">
                        <li v-for="(opt, oidx) in question.options" :key="oidx">{{ opt }}</li>
                      </ul>
                    </div>
                    <div v-else class="text-muted">No options</div>
                  </td>
                  <td>
                    <span v-if="question.answer !== undefined && question.answer !== null && question.answer !== ''">
                      {{ question.answer }}
                    </span>
                    <span v-else class="text-muted">No answer</span>
                  </td>
                </tr>
                <tr v-if="filteredSortedQuestions.length === 0">
                  <td colspan="6" class="text-center text-muted">No questions found.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Results Table -->
        <div v-else-if="selectedTable === 'results'">
          <h4 class="mt-4 mb-2">All Results</h4>
          <div class="mb-2 d-flex gap-2 align-items-center">
            <input v-model="resultSearch" class="form-control w-auto" placeholder="Search results..." />
            <select v-model="resultSortKey" class="form-select w-auto">
              <option value="id">Sort by Result ID</option>
              <option value="user_id">Sort by User ID</option>
              <option value="quiz_id">Sort by Quiz ID</option>
              <option value="score">Sort by Score</option>
              <option value="taken_at">Sort by Taken At</option>
            </select>
            <button class="btn btn-outline-secondary btn-sm" @click="resultSortAsc = !resultSortAsc">
              <i :class="resultSortAsc ? 'fas fa-sort-alpha-down' : 'fas fa-sort-alpha-up'"></i>
            </button>
          </div>
          <div class="table-responsive mb-4">
            <table class="table table-striped table-bordered align-middle">
              <thead class="table-light">
                <tr>
                  <th>Result ID</th>
                  <th>User ID</th>
                  <th>Quiz ID</th>
                  <th>Score</th>
                  <th>Time Taken</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="result in filteredSortedResults" :key="result.id">
                  <td>{{ result.id }}</td>
                  <td>{{ result.user_id }}</td>
                  <td>{{ result.quiz_id }}</td>
                  <td>{{ result.score }}</td>
                  <td>{{ result.time_taken/60 }} min</td>
                </tr>
                <tr v-if="filteredSortedResults.length === 0">
                  <td colspan="6" class="text-center text-muted">No results found.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../api'

const users = ref([])
const quizzes = ref([])
const subjects = ref([])
const chapters = ref([])
const questions = ref([])
const results = ref([])
const loading = ref(false)
const error = ref('')

const deletingDb = ref(false) // Track delete state

// Table selection
const selectedTable = ref('all')

// Search and sort states for each table
const userSearch = ref('')
const userSortKey = ref('name')
const userSortAsc = ref(true)

const quizSearch = ref('')
const quizSortKey = ref('id')
const quizSortAsc = ref(true)

const subjectSearch = ref('')
const subjectSortKey = ref('id')
const subjectSortAsc = ref(true)

const chapterSearch = ref('')
const chapterSortKey = ref('id')
const chapterSortAsc = ref(true)

const questionSearch = ref('')
const questionSortKey = ref('id')
const questionSortAsc = ref(true)

const resultSearch = ref('')
const resultSortKey = ref('id')
const resultSortAsc = ref(true)

// Helper: Get subject_id by chapter_id
function getSubjectIdByChapterId(chapterId) {
  const chapter = chapters.value.find(c => c.id === chapterId)
  return chapter ? chapter.subject_id : 'N/A'
}

// Filtering and sorting for each table
const filteredSortedUsers = computed(() => {
  let arr = users.value.filter(u =>
    (u.name && u.name.toLowerCase().includes(userSearch.value.toLowerCase())) ||
    (u.email && u.email.toLowerCase().includes(userSearch.value.toLowerCase())) ||
    (u.role && u.role.toLowerCase().includes(userSearch.value.toLowerCase())) ||
    (u.qualification && u.qualification.toLowerCase().includes(userSearch.value.toLowerCase())) ||
    (String(u.id).includes(userSearch.value))
  )
  arr = arr.sort((a, b) => {
    let aVal = a[userSortKey.value]
    let bVal = b[userSortKey.value]
    if (typeof aVal === 'string') aVal = aVal.toLowerCase()
    if (typeof bVal === 'string') bVal = bVal.toLowerCase()
    if (aVal === bVal) return 0
    if (userSortAsc.value) return aVal > bVal ? 1 : -1
    else return aVal < bVal ? 1 : -1
  })
  return arr
})

const filteredSortedQuizzes = computed(() => {
  let arr = quizzes.value.filter(q =>
    (q.title && q.title.toLowerCase().includes(quizSearch.value.toLowerCase())) ||
    (String(q.id).includes(quizSearch.value)) ||
    (String(q.chapter_id).includes(quizSearch.value)) ||
    (String(q.duration).includes(quizSearch.value)) ||
    (q.created_at && q.created_at.toLowerCase().includes(quizSearch.value.toLowerCase()))
  )
  arr = arr.sort((a, b) => {
    let aVal = a[quizSortKey.value]
    let bVal = b[quizSortKey.value]
    if (typeof aVal === 'string') aVal = aVal.toLowerCase()
    if (typeof bVal === 'string') bVal = bVal.toLowerCase()
    if (aVal === bVal) return 0
    if (quizSortAsc.value) return aVal > bVal ? 1 : -1
    else return aVal < bVal ? 1 : -1
  })
  return arr
})

const filteredSortedSubjects = computed(() => {
  let arr = subjects.value.filter(s =>
    (s.name && s.name.toLowerCase().includes(subjectSearch.value.toLowerCase())) ||
    (String(s.id).includes(subjectSearch.value)) ||
    (s.description && s.description.toLowerCase().includes(subjectSearch.value.toLowerCase()))
  )
  arr = arr.sort((a, b) => {
    let aVal = a[subjectSortKey.value]
    let bVal = b[subjectSortKey.value]
    if (typeof aVal === 'string') aVal = aVal.toLowerCase()
    if (typeof bVal === 'string') bVal = bVal.toLowerCase()
    if (aVal === bVal) return 0
    if (subjectSortAsc.value) return aVal > bVal ? 1 : -1
    else return aVal < bVal ? 1 : -1
  })
  return arr
})

const filteredSortedChapters = computed(() => {
  let arr = chapters.value.filter(c =>
    (c.name && c.name.toLowerCase().includes(chapterSearch.value.toLowerCase())) ||
    (String(c.id).includes(chapterSearch.value)) ||
    (String(c.subject_id).includes(chapterSearch.value))
  )
  arr = arr.sort((a, b) => {
    let aVal = a[chapterSortKey.value]
    let bVal = b[chapterSortKey.value]
    if (typeof aVal === 'string') aVal = aVal.toLowerCase()
    if (typeof bVal === 'string') bVal = bVal.toLowerCase()
    if (aVal === bVal) return 0
    if (chapterSortAsc.value) return aVal > bVal ? 1 : -1
    else return aVal < bVal ? 1 : -1
  })
  return arr
})

const filteredSortedQuestions = computed(() => {
  let arr = questions.value.filter(q =>
    (q.text && q.text.toLowerCase().includes(questionSearch.value.toLowerCase())) ||
    (String(q.id).includes(questionSearch.value)) ||
    (String(q.quiz_id).includes(questionSearch.value)) ||
    (q.answer && q.answer.toLowerCase().includes(questionSearch.value.toLowerCase()))
  )
  arr = arr.sort((a, b) => {
    let aVal = a[questionSortKey.value]
    let bVal = b[questionSortKey.value]
    if (typeof aVal === 'string') aVal = aVal.toLowerCase()
    if (typeof bVal === 'string') bVal = bVal.toLowerCase()
    if (aVal === bVal) return 0
    if (questionSortAsc.value) return aVal > bVal ? 1 : -1
    else return aVal < bVal ? 1 : -1
  })
  return arr
})

const filteredSortedResults = computed(() => {
  let arr = results.value.filter(r =>
    (String(r.id).includes(resultSearch.value)) ||
    (String(r.user_id).includes(resultSearch.value)) ||
    (String(r.quiz_id).includes(resultSearch.value)) ||
    (String(r.score).includes(resultSearch.value)) ||
    (r.taken_at && r.taken_at.toLowerCase().includes(resultSearch.value.toLowerCase()))
  )
  arr = arr.sort((a, b) => {
    let aVal = a[resultSortKey.value]
    let bVal = b[resultSortKey.value]
    if (typeof aVal === 'string') aVal = aVal.toLowerCase()
    if (typeof bVal === 'string') bVal = bVal.toLowerCase()
    if (aVal === bVal) return 0
    if (resultSortAsc.value) return aVal > bVal ? 1 : -1
    else return aVal < bVal ? 1 : -1
  })
  return arr
})

// Delete database function with confirmation
async function deleteDatabase() {
  if (deletingDb.value) return
  if (!window.confirm('Are you sure you want to delete the entire database? This action cannot be undone!')) {
    return
  }
  deletingDb.value = true
  error.value = ''
  try {
    await api.delete('/auth/db')
    // Optionally, you can clear the data or reload
    users.value = []
    quizzes.value = []
    subjects.value = []
    chapters.value = []
    questions.value = []
    results.value = []
    alert('Database deleted successfully.')
   window.location.reload()
  } catch (e) {
    error.value = 'Failed to delete database.'
  } finally {
    deletingDb.value = false
  }
}

async function fetchAllData() {
  loading.value = true
  error.value = ''
  try {
    const [
      usersRes,
      quizzesRes,
      subjectsRes,
      chaptersRes,
      questionsRes,
      resultsRes
    ] = await Promise.all([
      api.get('/auth/users'),
      api.get('/auth/quizzes'),
      api.get('/auth/subjects'),
      api.get('/auth/chapters'),
      api.get('/auth/questions'),
      api.get('/auth/results')
    ])
    users.value = usersRes.data.users || []
    quizzes.value = quizzesRes.data.quizzes || []
    subjects.value = subjectsRes.data.subjects || []
    chapters.value = chaptersRes.data.chapters || []
    questions.value = questionsRes.data.questions || []
    results.value = resultsRes.data.results || []
  } catch (e) {
    error.value = 'Failed to fetch admin data'
    users.value = []
    quizzes.value = []
    subjects.value = []
    chapters.value = []
    questions.value = []
    results.value = []
  } finally {
    loading.value = false
  }
}

onMounted(fetchAllData)

</script>

<style scoped>
.admin-quiz-section {
  padding: 2rem 0;
}
.table th, .table td {
  vertical-align: middle;
}
</style>
