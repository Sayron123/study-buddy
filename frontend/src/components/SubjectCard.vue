<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute, RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../api'


const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

onMounted(() => {
  loadChats()
  loadLibraries()
  loadFlashcards()
  loadAssignments()
  loadQuizzes()
  window.addEventListener('reload-chats', loadChats)
  window.addEventListener('reload-quizzes', loadQuizzes)  
})


const sections = ref([  
  { id: 'chat', label: 'Chat', icon: 'chat', isHovered: false, nextId: 1, items: [] },
  { id: 'library', label: 'Library Upload', icon: 'upload_file', isHovered: false, nextId: 1, items: [] },
  { id: 'flashcards', label: 'Flashcards', icon: 'style', isHovered: false, nextId: 1, items: [] },
  { id: 'assignments', label: 'Assignments', icon: 'assignment', isHovered: false, nextId: 1, items: [] },
  { id: 'quizzes', label: 'Quizzes', icon: 'quiz', isHovered: false, nextId: 1, items: [] }

])

const loadChats = async () => {
  try {
    const response = await api.get('/chats')
    const chatSection = sections.value.find(s => s.id === 'chat')
    chatSection.items = response.data.chats.map(chat => ({
      id: chat._id,
      name: chat.title,
      isEditing: false
    }))
  } catch (error) {
    console.error('Failed to load chats:', error)
  }
}

const loadLibraries = async () => {
  try {
    const response = await api.get('/library')
    const librarySection = sections.value.find(s => s.id === 'library')
    librarySection.items = response.data.libraries.map(lib => ({
      id: lib._id,
      name: lib.title,
      isEditing: false
    }))
  }catch(error){
    console.error('Failed to load libraries:', error)
  }
}

const loadFlashcards = async () => {
  try{
    const response = await api.get('/flashcards')
    const flashcardSection = sections.value.find(s => s.id === 'flashcards')
    flashcardSection.items = response.data.flashcards.map(fs => ({
      id: fs._id,
      name: fs.title,
      isEditing: false
    }))
  }catch(error){
    console.error('Failed to load flashcards:', error)
  }
}

const loadAssignments = async () => {
  try {
    const response = await api.get('/assignments')
    const assignmentSection = sections.value.find(s => s.id === 'assignments')
    assignmentSection.items = response.data.assignments.map(a => ({
      id: a._id,
      name: a.title,
      isEditing: false
    }))
  }catch (error) {
    console.error('Failed to load assignments:', error)
  }
}

const loadQuizzes = async () => {
  try {
    const response = await api.get('/quizzes')
    const quizSection = sections.value.find(s => s.id ===  'quizzes')
    quizSection.items = response.data.quizzes.map(q => ({
      id: q.id,
      name: q.title,
      isEditing: false
    }))
  }catch (error) {
    console.error('Failes to load quizzes:', error)
  }
}

watch(() => authStore.token, async(newToken) => {
  if(newToken) {
    await loadChats()
    await loadLibraries()
    await loadFlashcards()
    await loadAssignments()
    await loadQuizzes()
  }
}, { immediate: true })


const handleAdd = async (e, section) => {
  e.stopPropagation()

  if (section.id === 'chat') {
    const response = await api.post('/chats', { title: 'New Chat' })
    const chatId = response.data.id
    section.items.unshift({ id: chatId, name: 'New Chat', isEditing: false })
    router.push(`/chat/${chatId}`)

  }else if (section.id === 'library') {
    const response = await api.post('/library', { title: 'New Library'})
    const libId = response.data.id
    section.items.unshift({ id: libId, name: 'New library', isEditing: false })
    router.push(`/library/${libId}`)

  }else if (section.id === 'flashcards'){
    const response = await api.post('/flashcards', { title: 'New Flashcard Set'})
    const setId = response.data.id
    section.items.unshift({ id: setId, name: 'New Flashcard Set', isEditing: false })
    router.push(`/flashcards/${setId}`)
  
  }else if (section.id === 'assignments'){
    const response = await api.post('/assignments', { title: 'New Assignment'})
    const assignmentId = response.data.id
    section.items.unshift({ id: assignmentId, name: 'New Assignment', isEditing: false }) 
    router.push(`/assignments/${assignmentId}`)
  
  }else if (section.id === 'quizzes'){
    const response = await api.post('/quizzes')
    const quizId = response.data.id
    section.items.unshift({ id: quizId, name: 'New Quiz', isEditing: false })
    router.push(`/quizzes/${quizId}`)

  } else {
    const newItem = { id: section.nextId++, name: '', isEditing: true }
    section.items.unshift(newItem)
    section.isHovered = true
    setTimeout(() => {
      const input = document.querySelector(`.subject-input-${section.id}`)
      if (input) input.focus()
    }, 50)
  }
}

const saveItem = (section, item) => {
  if (item.name.trim() === '') {
    section.items = section.items.filter(i => i.id !== item.id)
  } else {
    item.isEditing = false
  }
}

const handleKeydown = (e, section, item) => {
  if (e.key === 'Enter') saveItem(section, item)
  else if (e.key === 'Escape') {
    if (item.name.trim() === '') section.items = section.items.filter(i => i.id !== item.id)
    else item.isEditing = false
  }
}

const deleteItem = async (section, itemId) => {
  if(section.id === 'chat'){
    try{
      await api.delete(`/chats/${itemId}`)
      if(route.path === `/chat/${itemId}`)
        router.push('/dashboard')
    }catch (error) {
      console.error('Failed to delete chat:', error)
    }
  }else if (section.id === 'library') {
    try {
      await api.delete(`/library/${itemId}`)
      if (route.path === `/library/${itemId}`) {
        router.push('/dashboard')
      }
    } catch (error) {
      console.error('Failed to delete library:', error)
    }
  }else if (section.id === 'flashcards'){
    try {
      await api.delete(`/flashcards/${itemId}`)
      if (route.path === `/flashcards/${itemId}`) {
        router.push('/dashboard')
      }
    }catch (error) {
      console.error('Failed to delete flashcard:', error)
    }
  }else if (section.id === 'assignments') {
    try {
      await api.delete(`/assignments/${itemId}`)
      if (route.path === `/assignments/${itemId}`) {
        router.push('/dashboard')
      }
    }catch (error) {
      console.error('Failed to delete assignment:', error)
    }
  }else if (section.id === 'quizzes') {
    try {
      await api.delete(`/quizzes/${itemId}`)
      router.push('/dashboard')
    }catch(error){
      console.error('Failed to delete quiz:', error)
    }
  }
  section.items = section.items.filter(i => i.id !== itemId)
}

</script>

<template>
  <div v-for="section in sections" :key="section.id" class="group"
    @mouseenter="section.isHovered = true"
    @mouseleave="section.isHovered = false"
  >
    <!-- Section Header -->
    <div class="text-slate-600 dark:text-slate-400 hover:text-blue-600 dark:hover:text-teal-200 py-2 px-4 flex items-center justify-between rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-all cursor-pointer">
      <div class="flex items-center gap-3">
        <span class="material-symbols-outlined">{{ section.icon }}</span>
        <span>{{ section.label }}</span>
      </div>
      <span
        class="material-symbols-outlined cursor-pointer"
        @click="handleAdd($event, section)"
      >
        add
      </span>
    </div>

    <!-- Dropdown Items -->
    <transition
      enter-active-class="transition-all duration-200 ease-out"
      enter-from-class="opacity-0 -translate-y-2 max-h-0"
      enter-to-class="opacity-100 translate-y-0 max-h-96"
      leave-active-class="transition-all duration-150 ease-in"
      leave-from-class="opacity-100 translate-y-0 max-h-96"
      leave-to-class="opacity-0 -translate-y-2 max-h-0"
    >
      <div
        v-show="section.isHovered"
        class="ml-9 mt-1 space-y-1 overflow-hidden"
      >
        <div
          v-for="item in section.items"
          :key="item.id"
          class="group/item relative"
        >
          <!-- Edit Mode -->
          <input
            v-if="item.isEditing"
            v-model="item.name"
            type="text"
            :class="`subject-input-${section.id}`"
            class="block w-full py-1.5 px-3 text-xs text-slate-700 dark:text-slate-300 bg-white dark:bg-slate-800 border-2 border-blue-500 dark:border-teal-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-teal-400"
            :placeholder="`Enter ${section.label.toLowerCase().slice(0, -1)} name...`"
            @blur="saveItem(section, item)"
            @keydown="handleKeydown($event, section, item)"
          />
          <!-- View Mode -->
          <RouterLink
            v-if="!item.isEditing"
            :to="section.id === 'chat' ? `/chat/${item.id}` : section.id === 'library' ? `/library/${item.id}` : section.id === 'flashcards' ? `/flashcards/${item.id}` : section.id === 'assignments' ? `/assignments/${item.id}`: section.id === 'quizzes' ? `/quizzes/${item.id}` : '#'"
            :class="route.path === `/chat/${item.id}` || route.path === `/library/${item.id}` || route.path === `/flashcards/${item.id}` || route.path === `/assignments/${item.id}` || route.path === `/quizzes/${item.id}` ? 'bg-slate-200 dark:bg-slate-700 text-blue-700' : 'text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800'"
            class="flex items-center justify-between py-1.5 px-3 text-xs rounded-lg transition-colors"
            @dblclick.prevent="item.isEditing = true"
          >
            <span class="truncate">{{ item.name }}</span>
            <span
              class="material-symbols-outlined text-xs text-red-500 hover:text-red-700 opacity-0 group-hover/item:opacity-100 transition-opacity flex-shrink-0 ml-1 cursor-pointer"
              @click.prevent="deleteItem(section, item.id)"
            >
              close
            </span>
          </RouterLink>                 
        </div>
        <!-- Empty state -->
        <p
          v-if="section.items.length === 0"
          class="text-[11px] text-slate-400 dark:text-slate-600 px-3 py-1 italic"
        >
          No {{ section.label.toLowerCase() }} yet
        </p>
      </div>
    </transition>
  </div>
</template>