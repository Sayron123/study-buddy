<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router';
import { useRouter } from 'vue-router'
import Sidebar from './Sidebar.vue';
import Navbar from './Navbar.vue';
import api from '../api'

const router = useRouter()
const route = useRoute()
const quizId = ref(route.params.id)

//DATA
const quizTitle = ref('')
const questions = ref([])
const notes = ref('')

//Quiz session state 
const mode = ref('idle')
const currentIndex = ref(0)
const selectedAnswer = ref(null)
const isChecking = ref(false)
const isCorrect = ref(null)
const correctAnswer = ref(null)
const score = ref(0)
const isGenerating = ref(false)

onMounted(async () => {
    const response = await api.get(`/quizzes/${quizId.value}`)
    quizTitle.value = response.data.title
    questions.value = response.data.questions
    if(questions.value.length > 0 ) {
        mode.value = 'taking'
        window.dispatchEvent(new Event('reload-quizzes'))
    }
})


watch(() => route.params.id, async (newId) => {
  if(newId) {
    quizId.value = newId
    const response = await api.get(`/quizzes/${newId}`)
    quizTitle.value = response.data.title
    questions.value = response.data.questions
    selectedAnswer.value = null
    isCorrect.value = null
    correctAnswer.value = null
    currentIndex.value = 0
    score.value = 0 
    mode.value = questions.value.length > 0 ? 'taking' : 'idle'
  }
})
const generateQuiz = async() => {
    if(!notes.value.trim()) return 
    isGenerating.value = true
    try {
        const response = await api.post('/quizzes/generate', {
            notes: notes.value
        })
        quizId.value = response.data.id
        router.replace(`/quizzes/${response.data.id}`)
        window.dispatchEvent(new Event('reload-quizzes'))
        questions.value = response.data.questions
        quizTitle.value = response.data.title
        currentIndex.value = 0
        score.value = 0
        selectedAnswer.value = null 
        isCorrect.value = null
        mode.value = 'taking'
    }catch(error){
        console.error('Failed to generate quiz:' ,error)
    }finally {
        isGenerating.value = false
    }
}

const submitAnswer = async(choice) => {
    if(selectedAnswer.value) return
    isChecking.value = true
    selectedAnswer.value = choice 

    const response = await api.post(`/quizzes/${quizId.value}/submit-answer`, {
        question_index: currentIndex.value,
        user_answer: choice
    })

    isCorrect.value = response.data.is_correct
    correctAnswer.value = response.data.correct_answer
    if(response.data.is_correct) score.value++
    isChecking.value = false
}

const nextQuestion = () => {
    selectedAnswer.value = null
    isCorrect.value = null
    correctAnswer.value = null

    if(currentIndex.value + 1 >= questions.value.length) {
        mode.value = 'results'
    }else {
        currentIndex.value++
    }
}

const retake = () => {
    currentIndex.value = 0
    score.value = 0 
    selectedAnswer.value = null
    isCorrect.value = null 
    correctAnswer.value = null
    mode.value = 'taking'
}
</script>

<template>
  <aside class="h-screen w-72 fixed left-0 top-0 overflow-y-auto bg-slate-100 dark:bg-slate-900 z-50 flex flex-col gap-y-1 p-6 font-manrope text-sm font-medium">
    <Sidebar />
  </aside>

  <main class="ml-72 flex-1 flex flex-col h-screen relative bg-slate-50 dark:bg-slate-950 transition-colors duration-300">
    <Navbar />

    <section class="flex-1 overflow-y-auto px-6 py-10">
      <div class="max-w-3xl mx-auto space-y-8">

        <!-- Title -->
        <h1 class="text-3xl font-extrabold text-slate-900 dark:text-slate-100">
          {{ quizTitle || 'New Quiz' }}
        </h1>

        <!-- IDLE MODE — paste notes -->
        <div v-if="mode === 'idle'" class="space-y-4">
          <p class="text-slate-500">Paste your notes below and AI will generate 10 questions for you!</p>
          <textarea
            v-model="notes"
            rows="8"
            placeholder="Paste your study notes here..."
            class="w-full rounded-2xl border border-slate-200 dark:border-slate-700 p-4 text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-primary/20 resize-none"          ></textarea>
          <button
            @click="generateQuiz"
            :disabled="isGenerating"
            class="w-full py-3 rounded-full bg-primary text-white font-bold hover:opacity-90 transition-all"
          >
            {{ isGenerating ? 'Generating...' : '✨ Generate Quiz' }}
          </button>
        </div>

        <!-- TAKING MODE — one question at a time -->
        <div v-else-if="mode === 'taking'" class="space-y-6">

          <!-- Progress -->
          <div class="flex items-center justify-between">
            <span class="text-sm font-bold text-slate-500">
              Question {{ currentIndex + 1 }} of {{ questions.length }}
            </span>
            <span class="text-sm font-bold text-primary">
              Score: {{ score }}
            </span>
          </div>

          <!-- Progress Bar -->
          <div class="w-full h-2 bg-slate-200 rounded-full">
            <div
              class="h-2 bg-primary rounded-full transition-all duration-500"
              :style="{ width: ((currentIndex) / questions.length * 100) + '%' }"
            ></div>
          </div>

          <!-- Question Card -->
          <div class="bg-white/5 dark:bg-slate-800 rounded-3xl shadow-xl p-10 text-center">
            <p class="text-xl font-bold text-slate-900 dark:text-slate-100">
              {{ questions[currentIndex].question }}
            </p>
          </div>

          <!-- Choices -->
          <div class="grid grid-cols-1 gap-3">
            <button
              v-for="(text, letter) in questions[currentIndex].choices"
              :key="letter"
              @click="submitAnswer(letter)"
              :disabled="selectedAnswer !== null"
              :class="[
                'w-full py-4 px-6 rounded-2xl border-2 font-bold text-left transition-all text-slate-800 dark:text-slate-100',
                selectedAnswer === null || isChecking
                  ? 'border-slate-300 dark:border-slate-600 hover:border-primary hover:text-primary'
                  : letter === correctAnswer
                    ? '!border-green-500 !bg-green-900 !text-green-300'
                    : letter === selectedAnswer
                      ? '!border-red-400 !bg-red-900 !text-red-300'
                      : 'border-slate-200 dark:border-slate-600 text-slate-400'
              ]"
            >
              <span class="mr-3 font-extrabold">{{ letter }}.</span>{{ text }}
            </button>
          </div>

          <!-- Feedback + Next -->
          <div v-if="selectedAnswer && !isChecking" class="space-y-4">
            <p :class="isCorrect ? 'text-green-600 font-bold text-center' : 'text-red-500 font-bold text-center'">
              {{ isCorrect ? '✅ Correct!' : `❌ Wrong — correct answer is ${correctAnswer}` }}
            </p>
            <button
              @click="nextQuestion"
              class="w-full py-3 rounded-full bg-primary text-white font-bold hover:opacity-90 transition-all"
            >
              {{ currentIndex + 1 >= questions.length ? 'See Results' : 'Next Question →' }}
            </button>
          </div>

        </div>

        <!-- RESULTS MODE — final score -->
        <div v-else-if="mode === 'results'" class="text-center py-20 space-y-6">
          <p class="text-6xl">🎉</p>
          <h2 class="text-3xl font-extrabold text-slate-900 dark:text-slate-100">Quiz Complete!</h2>
          <p class="text-xl text-slate-500">
            You got <span class="text-primary font-extrabold">{{ score }}</span> out of
            <span class="font-extrabold">{{ questions.length }}</span> correct
          </p>
          <div class="flex gap-4 justify-center">
            <button
              @click="retake"
              class="px-8 py-3 rounded-full bg-primary text-white font-bold hover:opacity-90 transition-all"
            >
              🔁 Retake Quiz
            </button>
            <button
              @click="mode = 'idle'; questions = []"
              class="px-8 py-3 rounded-full border-2 border-slate-300 text-slate-600 font-bold hover:border-primary hover:text-primary transition-all"
            >
              📝 New Quiz
            </button>
          </div>
        </div>

      </div>
    </section>
  </main>
</template>