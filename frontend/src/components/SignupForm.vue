<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth';
import api from '../api'
import { ref } from 'vue'

const fullName = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const agreedToTerms = ref(false)

const router = useRouter()
const authStore = useAuthStore()

const handleSignup = async () => {
  if(password.value !== confirmPassword.value) {
    alert('Password do not match!')
    return
  }

  try{
    await api.post('/register', {
      full_name: fullName.value,
      email: email.value,
      password: password.value,
    })
    const response = await api.post('/login', {
      email: email.value,
      password: password.value,
    })
    authStore.setToken(response.data.access_token)
    router.push('/dashboard')
  } catch (error) {
    console.log('Signup failed:', error)
  }
}
</script>

<template>
  <div class="bg-background min-h-screen overflow-hidden text-on-surface relative">

    <div class="absolute top-[-10%] left-[-10%] w-[50vw] h-[50vw] rounded-full bg-primary-container floating-shape"></div>
    <div class="absolute bottom-[-20%] right-[-10%] w-[60vw] h-[60vw] rounded-full bg-secondary-container floating-shape"></div>
    <div class="absolute top-[20%] right-[10%] w-[30vw] h-[30vw] rounded-full bg-tertiary floating-shape opacity-20"></div>

    <main class="relative z-10 w-full min-h-screen flex flex-col md:flex-row items-center justify-between px-6 md:px-20 lg:px-32 py-12">

      <div class="w-full md:w-1/2 flex flex-col items-start gap-8 mb-12 md:mb-0">
        <div class="space-y-2">
          <span class="text-xs uppercase tracking-[0.2em] font-semibold text-primary/60 font-label">The Cognitive Sanctuary</span>
          <h1 class="text-6xl md:text-8xl font-extrabold tracking-tighter leading-[0.9] text-on-background">
            Liwanag
          </h1>
        </div>
      </div>

      <div class="w-full md:w-[460px] relative">
        <div class="absolute -top-12 -right-12 w-32 h-32 bg-primary-container/20 rounded-full blur-2xl"></div>

        <div class="flex flex-col gap-4">
          <form class="flex flex-col gap-4" @submit.prevent="handleSignup">

            <div class="glass-effect shadow-[0_20px_40px_rgba(11,28,48,0.04)] transition-all hover:scale-[1.01] duration-500 rounded-2xl px-4 py-3 relative border border-outline-variant/10 group">
              <label class="absolute -top-2 left-4 px-1 bg-white/50 backdrop-blur-sm text-[10px] uppercase tracking-widest font-bold text-primary/70 font-label leading-none">
                Full Name
              </label>
              <div class="flex items-center gap-3">
                <input
                  v-model="fullName"
                  type="text"
                  placeholder="John Doe"
                  required
                  class="w-full bg-transparent border-none p-0 text-lg font-medium focus:ring-0 placeholder:text-outline-variant/50 text-on-surface"
                />
                <span class="material-symbols-outlined text-primary/40 text-xl" style="font-variation-settings: 'FILL' 1;">person</span>
              </div>
            </div>

            <div class="glass-effect shadow-[0_20px_40px_rgba(11,28,48,0.04)] transition-all hover:scale-[1.01] duration-500 rounded-2xl px-4 py-3 relative border border-outline-variant/10 group">
              <label class="absolute -top-2 left-4 px-1 bg-white/50 backdrop-blur-sm text-[10px] uppercase tracking-widest font-bold text-primary/70 font-label leading-none">
                Email Address
              </label>
              <div class="flex items-center gap-3">
                <input
                  v-model="email"
                  type="email"
                  placeholder="john@example.com"
                  required
                  class="w-full bg-transparent border-none p-0 text-lg font-medium focus:ring-0 placeholder:text-outline-variant/50 text-on-surface"
                />
                <span class="material-symbols-outlined text-primary/40 text-xl" style="font-variation-settings: 'FILL' 1;">mail</span>
              </div>
            </div>

            <div class="glass-effect shadow-[0_20px_40px_rgba(11,28,48,0.04)] transition-all hover:scale-[1.01] duration-500 rounded-2xl px-4 py-3 relative border border-outline-variant/10 group">
              <label class="absolute -top-2 left-4 px-1 bg-white/50 backdrop-blur-sm text-[10px] uppercase tracking-widest font-bold text-primary/70 font-label leading-none">
                Password
              </label>
              <div class="flex items-center gap-3">
                <input
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="••••••••••••"
                  required
                  class="w-full bg-transparent border-none p-0 text-lg font-medium focus:ring-0 placeholder:text-outline-variant/50 text-on-surface"
                />
                <button
                  type="button"
                  class="focus:outline-none"
                  :aria-label="showPassword ? 'Hide password' : 'Show password'"
                  @click="showPassword = !showPassword"
                >
                  <span class="material-symbols-outlined text-primary/40 text-xl hover:text-primary/70 transition-colors cursor-pointer">
                    {{ showPassword ? 'visibility_off' : 'visibility' }}
                  </span>
                </button>
              </div>
            </div>

            <div class="glass-effect shadow-[0_20px_40px_rgba(11,28,48,0.04)] transition-all hover:scale-[1.01] duration-500 rounded-2xl px-4 py-3 relative border border-outline-variant/10 group">
              <label class="absolute -top-2 left-4 px-1 bg-white/50 backdrop-blur-sm text-[10px] uppercase tracking-widest font-bold text-primary/70 font-label leading-none">
                Confirm Password
              </label>
              <div class="flex items-center gap-3">
                <input
                  v-model="confirmPassword"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  placeholder="••••••••••••"
                  required
                  class="w-full bg-transparent border-none p-0 text-lg font-medium focus:ring-0 placeholder:text-outline-variant/50 text-on-surface"
                />
                <button
                  type="button"
                  class="focus:outline-none"
                  :aria-label="showConfirmPassword ? 'Hide password' : 'Show password'"
                  @click="showConfirmPassword = !showConfirmPassword"
                >
                  <span class="material-symbols-outlined text-primary/40 text-xl hover:text-primary/70 transition-colors cursor-pointer">
                    {{ showConfirmPassword ? 'visibility_off' : 'visibility' }}
                  </span>
                </button>
              </div>
            </div>

            <div class="flex items-center gap-3 px-1 mt-2">
              <input
                v-model="agreedToTerms"
                id="terms"
                type="checkbox"
                required
                class="w-5 h-5 rounded border-outline-variant/30 text-primary focus:ring-primary/20 bg-white/50 cursor-pointer"
              />
              <label for="terms" class="text-xs font-medium text-on-surface-variant cursor-pointer">
                By signing up I agree with
                <a href="#" class="text-primary underline hover:text-tertiary transition-colors duration-300">terms and conditions</a>
              </label>
            </div>

            <button
              type="submit"
              class="group relative w-full rounded-full bg-primary overflow-hidden shadow-[0_20px_50px_rgba(0,64,161,0.2)] active:scale-95 transition-all duration-300 h-12 mt-2"
            >
              <div class="absolute inset-0 bg-gradient-to-r from-primary to-tertiary transition-transform duration-500 group-hover:scale-105"></div>
              <div class="relative flex items-center justify-center gap-4 text-on-primary">
                <span class="text-xl font-bold tracking-tight">Enter the Sanctuary</span>
                <span class="material-symbols-outlined transition-transform duration-300 group-hover:translate-x-2">arrow_forward</span>
              </div>
            </button>

            <div class="flex items-center gap-4 mt-4">
              <div class="h-px flex-grow bg-outline-variant/20"></div>
              <span class="text-[10px] font-bold tracking-[0.2em] text-outline/60 whitespace-nowrap uppercase">Or Continue With</span>
              <div class="h-px flex-grow bg-outline-variant/20"></div>
            </div>

            <div class="flex justify-center">
              <button type="button" class="w-full rounded-2xl glass-effect flex items-center justify-center gap-3 hover:bg-surface-container-lowest transition-colors shadow-sm h-14 border border-outline-variant/10">
                <svg class="w-6 h-6 text-[#1877F2]" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                </svg>
                <span class="text-sm font-bold text-on-surface/80">Continue with Facebook</span>
              </button>
            </div>

            <div class="text-center mt-4">
              <span class="text-sm text-on-surface-variant/70">Already have an account? </span>
              <RouterLink to="/login" class="text-sm text-primary font-bold hover:underline underline-offset-4">Login</RouterLink>
            </div>

          </form>
        </div>
      </div>
    </main>

  </div>
</template>

<style scoped>
.glass-effect {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
}
.floating-shape {
  filter: blur(60px);
  opacity: 0.4;
  pointer-events: none;
  z-index: 0;
}
</style>