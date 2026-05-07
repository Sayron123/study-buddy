<script setup>
import Chatbar from './Chatbar.vue'
import Navbar from './Navbar.vue'
import Sidebar from './Sidebar.vue'
import { ref, computed, watch, onMounted } from 'vue'
import api from '../api'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const messages = ref([])
const isLoading = ref(false)
const route = useRoute()
const chatId = computed(() => route.params.id)
const authStore = useAuthStore()

onMounted(loadChat)
watch(chatId, loadChat)

async function loadChat() {
  messages.value = []
  if (!chatId.value) return
  try {
    const response = await api.get(`/chats/${chatId.value}`)
    messages.value = response.data.messages.flatMap(m => [
      { role: 'user', content: m.question },
      { role: 'ai', content: m.answer}
    ])
  }catch (error){
    console.error('Failed to lead chat:', error)
  }
}

const handleSend  = async (userMessage) => {
  messages.value.push({ role: 'user', content: userMessage })
  isLoading.value = true

  try {
    const response = await api.post(`/chats/${chatId.value}/ask`, {
      question: userMessage,
    })
    messages.value.push({ role: 'ai', content: response.data.answer })
    authStore.addTokens(response.data.tokens_used)

    // Auto-title after first message
    if(messages.value.length === 2) {
      await api.patch(`/chats/${chatId.value}/title` , {
        title: userMessage.slice(0, 40)
      })
      window.dispatchEvent(new CostumEvent('reload-chats'))
    }

  }catch(error){
    console.error('Chat failed:', error)
  }finally {
    isLoading.value = false
  }
}
</script>

<template>
  <aside class="h-screen w-72 fixed left-0 top-0 overflow-y-auto bg-slate-100 dark:bg-slate-900 z-50 flex flex-col gap-y-1 p-6 font-manrope text-sm font-medium">
    <Sidebar />
  </aside>

  <main class="ml-72 flex-1 flex flex-col h-screen relative bg-slate-50 dark:bg-slate-950 transition-colors duration-300">    
    <Navbar />

    <!-- Chat Section -->
    <section class="flex-1 overflow-y-auto px-6 py-10 space-y-8 scroll-smooth bg-slate-50 dark:bg-slate-950 transition-colors duration-300">     
        <!-- AI Welcome State -->
        <div v-if="messages.length === 0" class="text-center py-10 spave-y-4">
          <div class="w-16 h-16 bg-gradient-to-br from-primary to-tertiary rounded-2xl mx-auto flex items-center justify-center shadow-xl shadow-primary/20">
            <span class="material-symbols-outlined text-white text-3xl" style="font-variation-settings: 'FILL' 1;">auto_fix_high</span>
          </div>
          <h2 class="text-3xl font-headline font-extrabold text-slate-900 dark:text-slate-100 tracking-tight">
            How can I assist your learning today?
          </h2>
          <p class="text-slate-500 dark:text-slate-400 max-w-md mx-auto">
            Your cognitive sanctuary is ready. We can analyze complex proofs, summarize readings, or practice flashcards.
          </p>
        </div>

        <!-- Messages -->
         <div v-for="(msg, index) in messages" :key="index">

        <!-- User Message -->
        <div v-if="msg.role === 'user'" class="flex justify-end">
          <div class="max-w-[80%] bg-primary text-white px-6 py-4 rounded-2x1 rounded-tr shadow-lg shadow-primary/10">
            <p class="text-[15px] leading-relaxed">{{  msg.content }}</p>
          </div>
        </div>
        <!-- AI Messsage-->
        <div v-else class="flex justify-start items-start gap-4">
          <div class="w-10 h-10 rounded-xl bg-secondary-container flex items-center justify-center flex-shrink-0">
            <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">smart_toy</span>
          </div>
          <div class="max-w-[85%] bg-white dark:bg-slate-800 border border-slate-100 p-6 rounded-3x1 rounded-tl-none shadow-xl">
            <p class="text-slate-700 dark:text-slate-300 leading-relaxed">{{ msg.content }}</p>
          </div>
        </div>

      </div>

        <!-- Loading indicator -->
        <div v-if="isLoading" class="flex justify-start items-start gap-4">
          <div class="w-10 h-10 rounded-xl bg-secondary-container flex items-center justif-center">
            <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">smart_toy</span>
          </div>
          <div class="bg-white dark:bg-slate-800 border border-slate-100 px-6 py-4 rounded-3xl rounded-tl-none">
            <p class="text-slate-400 text-sm">Thinking...</p>
          </div>
        </div>
      

        <div class="h-24"></div>
        <Chatbar @send="handleSend"/>

    
    </section>
  </main>
</template>


