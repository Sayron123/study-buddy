import { createRouter, createWebHistory } from "vue-router";
import LoginForm from "./components/LoginForm.vue";
import SignupForm from "./components/SignupForm.vue";
import DashboardView from "./components/DashboardView.vue"
import ChatWindow from "./components/ChatWindow.vue";
import LibraryView from "./components/LibraryView.vue";
import FlashcardView from "./components/FlashcardView.vue";
import AssigmentView from "./components/AssigmentView.vue";
import QuizView from "./components/QuizView.vue";

const routes = [
    { path: '/', redirect: '/login'},
    { path: '/login', component: LoginForm},
    { path: '/Signup', component: SignupForm},
    { path: '/dashboard', component: DashboardView},
    { path: '/chat/:id', component: ChatWindow},
    { path: '/library/:id', component: LibraryView},
    { path: '/flashcards/:id' , component: FlashcardView},
    { path: '/assignments/:id', component: AssigmentView},
    { path: '/quizzes/:id', component: QuizView, meta: { requireAuth: true }}
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: routes,
})

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token')
    if ((to.path === '/dashboard' || to.path.startsWith('/chat/') || to.path.startsWith('/library/') || to.path.startsWith('/flashcard') || to.path.startsWith('/assignment') || to.path.startsWith('/quizzes')) && !token) {
        next('/login')
    }else {
        next()
    }
})

export default router