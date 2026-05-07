<script setup>
import { useDarkMode } from '@/assets/useDarkMode';
import { useAuthStore } from '@/stores/auth';
import { useRoute, useRouter } from 'vue-router';
import { ref } from 'vue';

const authStore = useAuthStore()
const { isDark, toggleDarkMode } = useDarkMode()
const showSettingsMenu = ref(false)
const router = useRouter()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script> 

<template>
  <!-- TopNavBar Component -->
  <header class="docked full-width top-0 sticky z-40 bg-slate-50/80 dark:bg-slate-950/80 backdrop-blur-xl flex justify-between items-center px-6 py-3 w-full border-b border-slate-200/50 dark:border-slate-800/50 font-manrope antialiased tracking-tight shadow-sm shadow-blue-900/5">
    <div class="flex items-center gap-6 flex-1">
      <div class="relative w-full max-w-xl group">
        <div class="absolute inset-y-0 left-4 flex items-center pointer-events-none text-slate-400 group-focus-within:text-primary transition-colors">
          <span class="material-symbols-outlined">search</span>
        </div>
        <input
          class="w-full pl-12 pr-4 py-2 bg-surface-container-low border-none rounded-full text-sm focus:ring-2 focus:ring-primary/20 focus:bg-white transition-all shadow-inner"
          placeholder="Search knowledge base, notes, or AI memory..."
          type="text"
        />
        <div class="absolute inset-0 rounded-full bg-primary/5 blur-md -z-10 opacity-0 group-focus-within:opacity-100 transition-opacity"></div>
      </div>
    </div>

    <div class="flex items-center gap-3">
      <button class="bg-primary text-on-primary px-4 py-2 rounded-lg text-sm font-semibold flex items-center gap-2 hover:bg-primary-container transition-colors shadow-sm">
        <span class="material-symbols-outlined text-sm">add_circle</span>
        Add Event
      </button>

      <div class="flex items-center gap-1 border-l border-slate-200 ml-2 pl-2">
        <button
          class="p-2 text-slate-500 hover:bg-slate-200/50 rounded-lg transition-colors"
          :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
          @click="toggleDarkMode"
        >
          <span class="material-symbols-outlined">
            {{ isDark ? 'light_mode' : 'dark_mode' }}
          </span>
        </button>
        <button class="p-2 text-slate-500 hover:bg-slate-200/50 rounded-lg transition-colors relative">
          <span class="material-symbols-outlined">notifications</span>
          <span class="absolute top-2 right-2 w-2 h-2 bg-error rounded-full border-2 border-slate-50"></span>
        </button>

     <div class="relative">
        <button
         @click="showSettingsMenu = !showSettingsMenu"
         class="p-2 text-slate-500 hover:bg-slate-200/50 rounded-lg transistion-colors">
        <span class="material-symbols-outlined">settings</span>
        </button>


        <!-- Settings Dropdown -->
        <div v-if="showSettingsMenu" class="absolute right-0 mt-2 w-48 bg-white rounded-x1 shadow-lg border border-slate-100 overflow-hidden z-50">
          <button class="w-full flex items-center gap-3 px-4 py-3 text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors">
            <span class="material-symbols-outlined text-lg">account_circle</span>
            Account
          </button> 
          <button
           @click="handleLogout"
           class="w-full flex items-center gap-3 px-4 py-3 text-sm font-medium text-red-500 hover:bg-red-50 transition-colors">
          <span class="material-symbols-outlined text-lg">logout</span>
            Logout 
          </button>                                                                
        </div>
     </div>
    </div>    
    
      <div class="flex items-center gap-3 ml-4 bg-surface-container-high/40 p-1 pr-3 rounded-full border border-white/50">
        <div class="relative">
          <img
            alt="User profile avatar"
            class="w-8 h-8 rounded-full object-cover"
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuDMXszT70EY_2nox6ufLq7lMA9taHnrB-obLU--bpTZIUfpdaTmc_27f5QbxPJAbh3oLBHPYe8Vg-1nn0fAz2MwSSKTt7cXuJTy5k8zfwHA0Vic0ln7ybdMs9vAGNisHi64dwfCti6E0CuWQgyfuwcqTuAfW9yve3Go2szsZVSMDjlUA2Z95O4WeOCjMArYuYzDdE1TkHXaRoNgWxjZ0ZcyPwAH4wdNFnbsG6SojfpQ0jjmXbQ5PKt8R5rj3vZCwLV5_4ILaCm64GU"
          />
          <span class="absolute bottom-0 right-0 w-2.5 h-2.5 bg-secondary-fixed rounded-full border-2 border-white"></span>
        </div>
        <span class="text-xs font-bold text-slate-700">{{ authStore.user?.email }}</span>
      </div>
    </div>
  </header>
</template>