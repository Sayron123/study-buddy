<script setup> 
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router';
import Sidebar from './Sidebar.vue';
import Navbar from './Navbar.vue';
import api from '../api'

const route = useRoute()
const setId = computed(() => route.params.id)

const flashcardSet = ref(null)
const cards = ref([])
const content = ref('')
const isGenerating = ref(false)
const isFlipped = ref(false)
const currentIndex = ref(0)
const score = ref({ correct: 0, wrong: 0 })

onMounted(async () => {
    const response = await api.get(`/flashcards/${setId.value}`)
    flashcardSet.value = response.data
    cards.value = response.data.cards
    content.value = response.data.content
})

const generateCards = async () => {
    if(!content.value.trim()) return
    isGenerating.value = true
    try { 
        const response = await api.post(`/flashcards/${setId.value}/generate`, {
            content: content.value
        })
        cards.value = response.data.cards
        currentIndex.value = 0
        isFlipped.value = false 
        score.value = { correct: 0, wrong: 0 }
    }catch(error) {
        console.error('Failed to generate:', error)
    }finally {
        isGenerating.value = false 
    }
}

const flipCard = () => {
    isFlipped.value = !isFlipped.value
}

const nextCard = (correct) => {
    if(correct) score.value.correct++
    else score.value.wrong++
    isFlipped.value = false
    currentIndex.value++
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
          {{ flashcardSet?.title || 'Flashcard Set' }}
        </h1>

        <!-- Content Input -->
        <div v-if="cards.length === 0" class="space-y-4">
          <p class="text-slate-500">Paste your notes below and AI will generate flashcards for you!</p>
          <textarea
            v-model="content"
            rows="8"
            placeholder="Paste your study notes here..."
            class="w-full rounded-2xl border border-slate-200 p-4 text-slate-700 focus:outline-none focus:ring-2 focus:ring-primary/20 resize-none"
          ></textarea>
          <button
            @click="generateCards"
            :disabled="isGenerating"
            class="w-full py-3 rounded-full bg-primary text-white font-bold hover:opacity-90 transition-all"
          >
            {{ isGenerating ? 'Generating...' : '✨ Generate Flashcards' }}
          </button>
        </div>

        <!-- Flashcard Study Mode -->
        <div v-else class="space-y-6">

          <!-- Score -->
          <div class="flex items-center gap-4">
            <span class="text-sm font-bold text-slate-500">{{ currentIndex }} / {{ cards.length }} cards</span>
            <span class="text-green-500 font-bold">✅ {{ score.correct }}</span>
            <span class="text-red-500 font-bold">❌ {{ score.wrong }}</span>
            <button @click="cards = []; currentIndex = 0" class="ml-auto text-xs text-primary font-bold hover:underline">
              Regenerate
            </button>
          </div>

          <!-- Finished State -->
          <div v-if="currentIndex >= cards.length" class="text-center py-20 space-y-4">
            <p class="text-4xl">🎉</p>
            <h2 class="text-2xl font-extrabold text-slate-900">Done!</h2>
            <p class="text-slate-500">✅ {{ score.correct }} correct — ❌ {{ score.wrong }} wrong</p>
            <button @click="currentIndex = 0; isFlipped = false; score = { correct: 0, wrong: 0 }" class="px-6 py-3 rounded-full bg-primary text-white font-bold">
              Study Again
            </button>
          </div>

          <!-- Flashcard -->
          <div v-else class="space-y-6">
            <div
              @click="flipCard"
              class="cursor-pointer bg-white dark:bg-slate-800 rounded-3xl shadow-xl p-12 text-center min-h-[250px] flex items-center justify-center transition-all hover:shadow-2xl"
            >
              <div>
                <p class="text-xs uppercase tracking-widest text-slate-400 mb-4">
                  {{ isFlipped ? 'Answer' : 'Question' }}
                </p>
                <p class="text-2xl font-bold text-slate-900 dark:text-slate-100">
                  {{ isFlipped ? cards[currentIndex].answer : cards[currentIndex].question }}
                </p>
                <p v-if="!isFlipped" class="text-xs text-slate-400 mt-6">Click to reveal answer</p>
              </div>
            </div>

            <!-- Action Buttons -->
            <div v-if="isFlipped" class="flex gap-4">
              <button
                @click="nextCard(false)"
                class="flex-1 py-3 rounded-full border-2 border-red-300 text-red-500 font-bold hover:bg-red-50 transition-all"
              >
                ❌ Still Learning
              </button>
              <button
                @click="nextCard(true)"
                class="flex-1 py-3 rounded-full bg-green-500 text-white font-bold hover:bg-green-600 transition-all"
              >
                ✅ Got It!
              </button>
            </div>
          </div>

        </div>
      </div>
    </section>
  </main>
</template>