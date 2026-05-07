<script setup>
import { useRoute } from 'vue-router';
import SubjectCard from './SubjectCard.vue';

const route = useRoute();


</script>

<template>
  <!-- Logo -->
  <div class="mb-8 px-2">
    <div class="flex items-center gap-3">
      <div class="w-9 h-9 rounded-lg bg-blue-600 flex items-center justify-center text-white shadow-sm">
        <span class="material-symbols-outlined text-xl" style="font-variation-settings: 'FILL' 1;">auto_awesome</span>
      </div>
      <div>
        <h1 class="text-xl font-bold text-slate-900 dark:text-white tracking-tight">Liwanag</h1>
        <p class="text-[9px] uppercase tracking-wider text-slate-500 dark:text-slate-400 font-semibold">AI STUDY BUDDY</p>
      </div>
    </div>
  </div>

  <!-- Nav Links -->
  <nav class="flex-1 space-y-0.5">

    <RouterLink
    to="/dashboard"
    :class="route.path === '/dashboard' ? 'bg-blue-50 text-blue-700' : 'text-slate-700 hover:bg-slate-50'"
    class="rounded-lg py-2.5 px-3 flex items-center gap-3 transition-colors font-medium">
    <span class="material-symbols-outlined text-[20px]">dashboard</span>
    <span>Dashboard</span>
  </RouterLink>

    <SubjectCard />

    <!-- History Section Label -->
    <div class="pt-6 pb-1 px-3 text-[10px] font-bold text-slate-400 uppercase tracking-wider">
      History
    </div>

    <!-- History -->
    <a href="#" class="text-slate-700 hover:bg-slate-50 py-2.5 px-3 flex items-center gap-3 rounded-lg transition-colors font-medium">
      <span class="material-symbols-outlined text-[20px]">history</span>
      <span>History</span>
    </a>

  </nav>

  <!-- Bottom Links -->
  <div class="mt-auto pt-4 border-t border-slate-200 space-y-0.5">
    <a href="#" class="text-slate-700 hover:bg-slate-50 py-2.5 px-3 flex items-center gap-3 rounded-lg transition-colors font-medium">
      <span class="material-symbols-outlined text-[20px]">help</span>
      <span>Help Center</span>
    </a>
    <a href="#" class="text-slate-700 hover:bg-slate-50 py-2.5 px-3 flex items-center gap-3 rounded-lg transition-colors font-medium">
      <span class="material-symbols-outlined text-[20px]">person</span>
      <span>Account</span>
    </a>
  </div>
</template>