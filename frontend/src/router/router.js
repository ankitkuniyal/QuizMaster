import { createRouter, createWebHistory } from 'vue-router';

import Login from '../components/Auth/Login.vue';
import Register from '../components/Auth/Register.vue';
import AdminDashboard from '../components/Admin/AdminDashboard.vue';
import Subjects from '../components/Admin/Subjects.vue';
import UserDashboard from '../components/User/UserDashboard.vue';
import QuestionManagement from '../components/Admin/QuestionManagement.vue';
import Subject from '../components/User/subject.vue';
import TakeQuiz from '../components/User/TakeQuiz.vue';
import Quiz from '../components/Admin/Quiz.vue';



// Add your NotFound or NotAuthorized components if needed
// import NotAuthorized from '../components/NotAuthorized.vue';

const routes = [
  { path: '/', component : Quiz },

  { path: '/login', component: Login },
  { path: '/register', component: Register },

  // User dashboard route
  {
    path: '/dashboard/user/:userid',
    component: UserDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/user/subjects/:userid',
    component: Subject,
    meta: { requiresAuth: true }
  },
  {
    path: '/user/quizzes/:quizid',
    component: TakeQuiz,
    meta: { requiresAuth: true }
  },

  {
    path: '/dashboard/admin',
    component: AdminDashboard,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/dashboard/admin/subjects',
    component: Subjects,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/dashboard/admin/db',
    component: Quiz,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/dashboard/admin/questions/:quizid',
    name: 'QuestionManagement',
    component: QuestionManagement,
    meta: { requiresAuth: true, requiresAdmin: true }
  },

  // { path: '/not-authorized', component: NotAuthorized },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// ✅ Route Guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  let role = null;
  if (token) {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      // role may be directly in payload or in payload.sub
      if (payload && payload.role) {
        role = payload.role;
      } else if (payload && payload.sub && payload.sub.role) {
        role = payload.sub.role;
      }
    } catch (e) {
      role = null;
    }
  }

  if (to.meta.requiresAuth && !token) {
    return next('/login');
  }

  if (to.meta.requiresAdmin && role !== 'admin') {
    // return next('/not-authorized');
    alert('Access denied. Admins only.');
    return next('/login');
  }

  next();
});

export default router;
