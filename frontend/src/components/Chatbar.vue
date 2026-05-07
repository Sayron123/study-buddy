<script setup>
import { useAuthStore } from '@/stores/auth'
import { ref } from 'vue'

const emit = defineEmits(['send'])
const showAttachMenu = ref(false)
const message = ref('')
const authStore = useAuthStore()


const toggleAttachMenu = () => {
  showAttachMenu.value = !showAttachMenu.value
}

const handleAttachFile = () => {
  console.log('Attach file clicked')
  showAttachMenu.value = false
  // Add your file upload logic here
}

const handleAttachPhoto = () => {
  console.log('Attach photo clicked')
  showAttachMenu.value = false
  // Add your photo upload logic here
}

const handleAttachDrive = () => {
  console.log('Attach from drive clicked')
  showAttachMenu.value = false
  // Add your drive integration logic here
}

const handleMicClick = () => {
  alert('Please enable microphone access to use voice input.')
  // Or you can use a more elegant notification
  // You can also add actual mic permission logic here
}

const handleSend = () => {
  if (authStore.tokensUsed >= 1500) {
    alert('Daily token limit reached! Please try again tomorrow.')
    return
  }
  if(message.value.trim()) {
    emit('send', message.value)
    message.value = ''
  }
}

// Close menu when clicking outside
const closeMenuOnClickOutside = (e) => {
  if (!e.target.closest('.attach-menu-container')) {
    showAttachMenu.value = false
  }
}
</script>

<template>
  <!-- Chat Bar Area -->
  <div class="absolute bottom-0 left-0 right-0 p-8 pointer-events-none" @click.self="showAttachMenu = false">
    <div class="max-w-4xl mx-auto w-full pointer-events-auto">
      <div class="glass-panel rounded-full p-2 pl-4 pr-3 flex items-center gap-2 bg-white dark:bg-slate-800 border border-white/50 dark:border-slate-700/50 shadow-2xl shadow-blue-900/10 focus-within:ring-4 focus-within:ring-primary/10 transition-all duration-300 relative">

        <!-- Attach Popup Menu -->
        <Transition name="attach-menu">
          <div
            v-if="showAttachMenu"
            class="attach-menu-container absolute bottom-full mb-4 left-0 bg-white dark:bg-slate-800 rounded-2xl shadow-2xl border border-slate-200/50 dark:border-slate-700/50 p-2 min-w-[160px] flex flex-col gap-1 z-50"
          >
            <button
              class="flex items-center gap-3 px-3 py-2 hover:bg-slate-50 dark:hover:bg-slate-700/50 rounded-xl transition-colors text-slate-700 dark:text-slate-300"
              @click="handleAttachFile"
            >
              <span class="material-symbols-outlined text-xl text-primary">attach_file</span>
              <span class="text-sm font-medium">Attach File</span>
            </button>
            <button
              class="flex items-center gap-3 px-3 py-2 hover:bg-slate-50 dark:hover:bg-slate-700/50 rounded-xl transition-colors text-slate-700 dark:text-slate-300"
              @click="handleAttachPhoto"
            >
              <span class="material-symbols-outlined text-xl text-secondary">image</span>
              <span class="text-sm font-medium">Photo</span>
            </button>
            <button
              class="flex items-center gap-3 px-3 py-2 hover:bg-slate-50 dark:hover:bg-slate-700/50 rounded-xl transition-colors text-slate-700 dark:text-slate-300"
              @click="handleAttachDrive"
            >
              <span class="material-symbols-outlined text-xl text-amber-500">add_to_drive</span>
              <span class="text-sm font-medium">Drive</span>
            </button>
          </div>
        </Transition>

        <!-- Add / Attach Toggle Button -->
        <button
          class="attach-menu-container w-10 h-10 flex items-center justify-center text-slate-400 hover:text-primary hover:bg-slate-100 rounded-full transition-all"
          title="Attachments"
          @click="toggleAttachMenu"
        >
          <span
            class="material-symbols-outlined transition-transform duration-200"
            :class="{ 'rotate-45': showAttachMenu }"
          >add</span>
        </button>

        <!-- Mic Button -->
        <button
          class="w-10 h-10 flex items-center justify-center text-slate-400 hover:text-primary hover:bg-slate-100 rounded-full transition-all mr-2"
          title="Voice Input"
          @click="handleMicClick"
        >
          <span class="material-symbols-outlined">mic</span>
        </button>

        <!-- Message Input -->
        <input
          v-model="message"
          class="flex-1 bg-transparent border-none focus:ring-0 text-slate-700 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-500 text-base"
          placeholder="Ask anything about your subjects..."
          type="text"
          @keyup.enter="handleSend"
        />

        <!-- Send Button -->
        <button
          class="bg-primary text-white w-10 h-10 rounded-full flex items-center justify-center hover:scale-105 active:scale-95 transition-all shadow-lg shadow-primary/20"
          @click="handleSend"
        >
          <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">send</span>
        </button>

      </div>
      <div class="flex items-center justify-between px-2 mt-2">
      <p class="text-center text-[10px] text-slate-400 mt-4 font-medium">Liwanag AI can make mistakes. Verify important academic information.</p>
      <div :class="authStore.tokensUsed > 1200 ? 'text-red-500' : 'text-slate-400'" class="text-[10px] font-bold">
        {{  authStore.tokensUsed }} / 1500 tokens
      </div>
      </div>
    </div>

    
  </div>
</template>

<style scoped>
.attach-menu-enter-active,
.attach-menu-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}
.attach-menu-enter-from,
.attach-menu-leave-to {
  opacity: 0;
  transform: translateY(6px);
}
</style>