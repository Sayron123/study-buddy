<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
import api from '../api'

const router = useRouter()
const authStore = useAuthStore();

const recentChats = ref([])
const recentFlashcards =  ref([])
const recentAssignments = ref([])
const recentQuizzes = ref([])
const activity = ref([])



onMounted(async () => {
    const response = await api.get('/me')
    authStore.setUser(response.data)

    const  [chats, flashcards, assignments,  quizzes, activityRes] = await Promise.all([
      api.get('/chats'),
      api.get('/flashcards'),
      api.get('/assignments'),
      api.get('/quizzes'),
      api.get('/activity'),
    ])

    recentChats.value = chats.data.chats.slice(0, 3)
    recentFlashcards.value = flashcards.data.flashcards.slice(0, 3)
    recentAssignments.value = assignments.data.assignments.slice(0, 3)
    recentQuizzes.value = quizzes.data.quizzes.slice(0, 3)
    activity.value = activityRes.data.activity
})
</script>

<template>
  <div class="pt-6 min-h-screen p-10 space-y-6 bg-slate-50 dark:bg-slate-950 transition-colors duration-300">

    <!-- Welcome Hero -->
    <section class="grid grid-cols-12 gap-6 max-w-7xl mx-auto">

      <!-- Hero Card -->
        <div class="col-span-8 p-10 rounded-3xl relative overflow-hidden text-white shadow-2xl shadow-primary/20 hero-card">        <div class="relative z-10 space-y-4">
          <div class="flex items-center gap-2 text-white w-fit px-3 py-1 rounded-full text-xs font-bold uppercase tracking-widest"
            style="background: linear-gradient(90deg, #14B8A6 0%, rgba(20, 184, 166, 0) 100%);">
            <span class="material-symbols-outlined text-sm">bolt</span>
            AI Companion Active
          </div>
          <h2 class="text-4xl font-black tracking-tight leading-tight">
            Welcome back, {{ authStore.user?.email?.split('@')[0] }}.<br/>Ready for deep focus?
          </h2>
          <p class="text-white/80 max-w-md leading-relaxed">
            Your AI study buddy Liwanag is ready to help you learn, review, and grow.
          </p>
          <div class="pt-4">
            <button 
              @click="router.push('/chat/' + (recentChats[0]?._id || ''))"
              class="hero-btn bg-white/20 backdrop-blur-sm border border-white/30 text-white px-6 py-3 rounded-xl font-bold text-sm flex items-center gap-2 hover:bg-white/30 transition-all">
              <span class="material-symbols-outlined">auto_awesome</span>
              Talk to Liwanag
            </button>
          </div>
        </div>
        <div class="absolute right-0 top-0 w-1/2 h-full opacity-20 pointer-events-none">
          <div class="w-full h-full bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-white via-transparent to-transparent scale-150"></div>
        </div>
      </div>

      <!-- Progress Card -->
        <div class="col-span-4 relative p-8 rounded-3xl flex flex-col overflow-hidden"
  style="background: rgba(255,255,255,0.25); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.4); box-shadow: 0 8px 32px rgba(0,0,0,0.08);">
  
  <div class="absolute top-[-20px] right-[-20px] w-32 h-32 rounded-full opacity-30 blob-1" style="background: #6366f1; filter: blur(30px);"></div>
  <div class="absolute bottom-[-20px] left-[-20px] w-40 h-40 rounded-full opacity-20 blob-2" style="background: #14b8a6; filter: blur(40px);"></div>

  <h3 class="relative z-10 text-2xl font-black text-slate-800 dark:text-white tracking-tight mb-6">Progress</h3>

  <!-- Bar Chart -->
      <div class="relative z-10 flex items-end justify-between gap-2 h-32">
        <div
          v-for="day in activity"
          :key="day.date"
          class="flex flex-col items-center gap-2 flex-1"
        >
          <div class="w-full rounded-xl transition-all duration-700 bar"
            :style="{
              height: day.count === 0 ? '8px' : (day.count * 20) + 'px',
              maxHeight: '96px',
              background: day.isToday ? 'linear-gradient(180deg, #6366f1, #0056D2)' : 'rgba(99,102,241,0.25)',
              boxShadow: day.isToday ? '0 4px 15px rgba(99,102,241,0.4)' : 'none'
            }"
          ></div>
          <span class="text-[10px] font-bold" :class="day.isToday ? 'text-primary' : 'text-slate-400'">
            {{ day.day }}
          </span>
        </div>
      </div>

      <!-- Max count label -->
      <p class="relative z-10 text-xs text-slate-400 mt-4 text-center">
        {{ activity.reduce((a, b) => a + b.count, 0) }} total activities this week
      </p>
</div>
    </section>

    <!-- Recent Items Grid -->
    <div class="grid grid-cols-12 gap-6 max-w-7xl mx-auto">

      <!-- Recent Chats -->
      <div class="col-span-6 space-y-3">
        <h3 class="text-lg font-extrabold text-slate-800 dark:text-white">Recent Chats</h3>
        <div v-if="recentChats.length === 0" 
          class="bg-white/60 dark:bg-slate-900/60 backdrop-blur-2xl p-6 rounded-2xl border border-white dark:border-slate-700/50 text-slate-400 text-sm italic shadow-lg">
          No chats yet. Start a conversation!
        </div>
        <div
          v-for="chat in recentChats"
          :key="chat._id"
          @click="router.push(`/chat/${chat._id}`)"
          class="cursor-pointer bg-white/60 dark:bg-slate-900/60 backdrop-blur-2xl p-5 rounded-2xl border border-white dark:border-slate-700/50 hover:border-primary/40 hover:shadow-lg hover:shadow-primary/10 transition-all shadow-md flex items-center gap-4"
        >
          <div class="w-9 h-9 rounded-xl bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center flex-shrink-0">
            <span class="material-symbols-outlined text-primary text-lg">chat</span>
          </div>
          <p class="font-semibold text-sm text-slate-800 dark:text-white truncate">{{ chat.title }}</p>
        </div>
      </div>

      <!-- Recent Flashcards -->
      <div class="col-span-6 space-y-3">
        <h3 class="text-lg font-extrabold text-slate-800 dark:text-white">Recent Flashcards</h3>
        <div v-if="recentFlashcards.length === 0"
          class="bg-white/60 dark:bg-slate-900/60 backdrop-blur-2xl p-6 rounded-2xl border border-white dark:border-slate-700/50 text-slate-400 text-sm italic shadow-lg">
          No flashcards yet. Create a set!
        </div>
        <div
          v-for="fs in recentFlashcards"
          :key="fs._id"
          @click="router.push(`/flashcards/${fs._id}`)"
          class="cursor-pointer bg-white/60 dark:bg-slate-900/60 backdrop-blur-2xl p-5 rounded-2xl border border-white dark:border-slate-700/50 hover:border-secondary/40 hover:shadow-lg hover:shadow-secondary/10 transition-all shadow-md flex items-center gap-4"
        >
          <div class="w-9 h-9 rounded-xl bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center flex-shrink-0">
            <span class="material-symbols-outlined text-secondary text-lg">style</span>
          </div>
          <p class="font-semibold text-sm text-slate-800 dark:text-white truncate">{{ fs.title }}</p>
        </div>
      </div>

      <!-- Recent Assignments -->
      <div class="col-span-6 space-y-3">
        <h3 class="text-lg font-extrabold text-slate-800 dark:text-white">Recent Assignments</h3>
        <div v-if="recentAssignments.length === 0"
          class="bg-white/60 dark:bg-slate-900/60 backdrop-blur-2xl p-6 rounded-2xl border border-white dark:border-slate-700/50 text-slate-400 text-sm italic shadow-lg">
          No assignments yet.
        </div>
        <div
          v-for="a in recentAssignments"
          :key="a._id"
          @click="router.push(`/assignments/${a._id}`)"
          class="cursor-pointer bg-white/60 dark:bg-slate-900/60 backdrop-blur-2xl p-5 rounded-2xl border border-white dark:border-slate-700/50 hover:border-tertiary/40 hover:shadow-lg hover:shadow-tertiary/10 transition-all shadow-md flex items-center gap-4"
        >
          <div class="w-9 h-9 rounded-xl bg-teal-100 dark:bg-teal-900/30 flex items-center justify-center flex-shrink-0">
            <span class="material-symbols-outlined text-tertiary text-lg">assignment</span>
          </div>
          <p class="font-semibold text-sm text-slate-800 dark:text-white truncate">{{ a.title }}</p>
        </div>
      </div>

      <!-- Recent Quizzes -->
      <div class="col-span-6 space-y-3">
        <h3 class="text-lg font-extrabold text-slate-800 dark:text-white">Recent Quizzes</h3>
        <div v-if="recentQuizzes.length === 0"
          class="bg-white/60 dark:bg-slate-900/60 backdrop-blur-2xl p-6 rounded-2xl border border-white dark:border-slate-700/50 text-slate-400 text-sm italic shadow-lg">
          No quizzes yet. Generate one!
        </div>
        <div
          v-for="q in recentQuizzes"
          :key="q.id"
          @click="router.push(`/quizzes/${q.id}`)"
          class="cursor-pointer bg-white/60 dark:bg-slate-900/60 backdrop-blur-2xl p-5 rounded-2xl border border-white dark:border-slate-700/50 hover:border-error/40 hover:shadow-lg hover:shadow-error/10 transition-all shadow-md flex items-center gap-4"
        >
          <div class="w-9 h-9 rounded-xl bg-red-100 dark:bg-red-900/30 flex items-center justify-center flex-shrink-0">
            <span class="material-symbols-outlined text-error text-lg">quiz</span>
          </div>
          <p class="font-semibold text-sm text-slate-800 dark:text-white truncate">{{ q.title }}</p>
        </div>
      </div>

    </div>
  </div>
</template>
 
<style scoped>
.hero-card {
  background: linear-gradient(135deg, #0056D2, #0ea5e9, #6366f1);
  background-size: 300% 300%;
  animation: gradientShift 6s ease infinite;
}

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.hero-btn {
  position: relative;
  overflow: hidden;
}

.hero-btn::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -75%;
  width: 50%;
  height: 200%;
  background: linear-gradient(
    to right,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.4) 50%,
    rgba(255, 255, 255, 0) 100%
  );
  transform: skewX(-20deg);
  transition: none;
}

.hero-btn:hover::after {
  animation: shine 0.6s ease forwards;
}

@keyframes shine {
  0% { left: -75%; }
  100% { left: 125%; }
}

.blob-1 {
  animation: blobMove1 8s ease-in-out infinite;
  filter: blur(30px);
}

.blob-2 {
  animation: blobMove2 10s ease-in-out infinite;
  filter: blur(40px);
}

@keyframes blobMove1 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(-20px, 20px) scale(1.2); }
}

@keyframes blobMove2 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(20px, -20px) scale(1.1); }
} 


</style>