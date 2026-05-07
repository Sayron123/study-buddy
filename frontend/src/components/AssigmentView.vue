<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Sidebar from './Sidebar.vue'
import Navbar from './Navbar.vue'
import api from '../api'

const route = useRoute()
const router = useRouter()
const assignmentId = computed(() => route.params.id)

const assignment = ref(null)
const sources = ref([])
const newContent = ref('')
const newType = ref('text')
const newLabel = ref('')
const isAdding = ref(false)
const messages = ref([])
const question = ref('')
const isLoading = ref(false)
const imageBase64 = ref(null)
const imagePreview = ref(null)

onMounted(async () => {
  const response = await api.get(`/assignments/${assignmentId.value}`)
  assignment.value = response.data
  sources.value = response.data.sources.map(s => ({ ...s, checked: true }))
})

const handleImageUpload = (e) => {
  const file = e.target.files[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = () => {
    imagePreview.value = reader.result
    imageBase64.value = reader.result.split(',')[1]
  }
  reader.readAsDataURL(file)
}

const addSource = async () => {
  if (!newContent.value.trim()) return
  isAdding.value = true
  try {
    const response = await api.post(`/assignments/${assignmentId.value}/sources`, {
      type: newType.value,
      content: newContent.value,
      label: newLabel.value
    })
    sources.value.push({ ...response.data.source, checked: true })
    newContent.value = ''
    newLabel.value = ''
  } catch (error) {
    console.error('Failed to add source:', error)
  } finally {
    isAdding.value = false
  }
}

const deleteSource = async (sourceId) => {
  await api.delete(`/assignments/${assignmentId.value}/sources/${sourceId}`)
  sources.value = sources.value.filter(s => s.id !== sourceId)
}

const sendMessage = async () => {
  if (!question.value.trim()) return
  const selectedIds = sources.value.filter(s => s.checked).map(s => s.id)

  messages.value.push({ role: 'user', content: question.value })
  isLoading.value = true
  const q = question.value
  question.value = ''

  try {
    const response = await api.post(`/assignments/${assignmentId.value}/chat`, {
      question: q,
      selected_sources: selectedIds,
      image_base64: imageBase64.value
    })
    messages.value.push({ role: 'ai', content: response.data.answer })
    imageBase64.value = null
    imagePreview.value = null
  } catch (error) {
    console.error('Chat failed:', error)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <aside class="h-screen w-72 fixed left-0 top-0 overflow-y-auto bg-slate-100 dark:bg-slate-900 z-50 flex flex-col gap-y-1 p-6 font-manrope text-sm font-medium">
    <Sidebar />
  </aside>

  <main class="ml-72 flex-1 flex flex-col h-screen relative bg-slate-50 dark:bg-slate-950">
    <Navbar />

    <section class="flex-1 overflow-y-auto px-6 py-10">
      <div class="max-w-6xl mx-auto space-y-8">

        <!-- Title -->
        <h1 class="text-3xl font-extrabold text-slate-900 dark:text-slate-100 text-center">
          {{ assignment?.title || 'New Assignment' }}
        </h1>

        <div class="grid grid-cols-12 gap-8">

          <!-- Left: Sources (3 columns) -->
          <div class="col-span-3 space-y-4">
            <h2 class="text-lg font-bold text-slate-700 dark:text-slate-300">Sources</h2>

            <!-- Add Source Form -->
            <div class="bg-white dark:bg-slate-800 rounded-2xl p-4 space-y-3 border border-slate-200 dark:border-slate-700">
              <p class="text-xs font-bold text-slate-500 uppercase">Link / Notes</p>
              <input
                v-model="newLabel"
                placeholder="Label (optional)"
                class="w-full rounded-xl border border-slate-200 p-2 text-sm text-slate-700 dark:bg-slate-700 dark:text-slate-200 dark:border-slate-600"
              />
              <textarea
                v-model="newContent"
                placeholder="Paste your link or notes here..."
                rows="4"
                class="w-full rounded-xl border border-slate-200 p-2 text-sm text-slate-700 resize-none dark:bg-slate-700 dark:text-slate-200 dark:border-slate-600"
              ></textarea>
              <button
                @click="addSource"
                :disabled="isAdding"
                class="w-full py-2 rounded-full bg-primary text-white font-bold text-sm hover:opacity-90"
              >
                {{ isAdding ? 'Adding...' : '+ Add Source' }}
              </button>
            </div>

            <!-- Sources List -->
            <div class="space-y-2">
              <div
                v-for="source in sources"
                :key="source.id"
                class="bg-white dark:bg-slate-800 rounded-xl p-3 border border-slate-200 dark:border-slate-700 flex items-start gap-3"
              >
                <input type="checkbox" v-model="source.checked" class="mt-1 accent-primary" />
                <div class="flex-1 min-w-0">
                  <p class="text-xs font-bold text-slate-500 uppercase">{{ source.type || 'source' }}</p>
                  <p class="text-sm text-slate-700 dark:text-slate-300 truncate">{{ source.label || source.content }}</p>
                </div>
                <button @click="deleteSource(source.id)" class="text-red-400 hover:text-red-600">
                  <span class="material-symbols-outlined text-sm">close</span>
                </button>
              </div>
              <p v-if="sources.length === 0" class="text-sm text-slate-400 italic">No sources yet. Add one above!</p>
            </div>
          </div>

          <!-- Center: Chat with AI (9 columns) -->
          <div class="col-span-9 space-y-4 flex flex-col">
            <h2 class="text-lg font-bold text-slate-700 dark:text-slate-300 text-center">Chat with AI</h2>

            <!-- Messages -->
            <div class="flex-1 bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-6 space-y-4 min-h-[500px] max-h-[600px] overflow-y-auto">
              <p v-if="messages.length === 0" class="text-sm text-slate-400 italic text-center mt-20">
                Add sources and ask about your assignment!
              </p>
              <div v-for="(msg, i) in messages" :key="i">
                <div v-if="msg.role === 'user'" class="flex justify-end">
                  <div class="bg-primary text-white px-4 py-2 rounded-2xl rounded-tr-none text-sm max-w-[80%]">
                    {{ msg.content }}
                  </div>
                </div>
                <div v-else class="flex justify-start">
                  <div class="bg-slate-100 dark:bg-slate-700 px-4 py-2 rounded-2xl rounded-tl-none text-sm max-w-[80%] text-slate-700 dark:text-slate-200">
                    {{ msg.content }}
                  </div>
                </div>
              </div>
              <div v-if="isLoading" class="flex justify-start">
                <div class="bg-slate-100 dark:bg-slate-700 px-4 py-2 rounded-2xl text-sm text-slate-400">Thinking...</div>
              </div>
            </div>

            <!-- Image Preview -->
            <div v-if="imagePreview" class="relative">
              <img :src="imagePreview" class="w-full h-32 object-cover rounded-xl" />
              <button @click="imageBase64 = null; imagePreview = null" class="absolute top-2 right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs">✕</button>
            </div>

            <!-- Input -->
            <div class="flex gap-2 items-center">
              <label class="cursor-pointer text-slate-400 hover:text-primary">
                <span class="material-symbols-outlined">image</span>
                <input type="file" accept="image/*" class="hidden" @change="handleImageUpload" />
              </label>
              <input
                v-model="question"
                @keyup.enter="sendMessage"
                placeholder="Ask about your assignment..."
                class="flex-1 rounded-full border border-slate-200 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 dark:bg-slate-800 dark:text-slate-200 dark:border-slate-600"
              />
              <button
                @click="sendMessage"
                class="bg-primary text-white px-4 py-2 rounded-full text-sm font-bold hover:opacity-90"
              >
                Send
              </button>
            </div>
          </div>

        </div>
      </div>
    </section>
  </main>
</template>