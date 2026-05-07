<script setup>
import Layout from './layout.vue';
import Navbar from './Navbar.vue';
import Sidebar from './Sidebar.vue';

</script>
<template>
  
     <aside class="h-screen w-72 fixed left-0 top-0 overflow-y-auto bg-slate-100 dark:bg-slate-900 z-50 flex flex-col gap-y-1 p-6 font-manrope text-sm font-medium">
    <Sidebar />
  </aside>

  <main class="ml-72 flex-1 flex flex-col h-screen relative bg-slate-50 dark:bg-slate-950 transition-colors duration-300">    
    <Navbar />
    <Layout />
  </main>
</template>

