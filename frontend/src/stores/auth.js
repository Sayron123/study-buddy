import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {


    state: () => ({
        token: localStorage.getItem('token'),
        user: null,
        tokensUsed: parseInt(localStorage.getItem('tokensUsed')) || 0,
    }),

    actions: {
        setToken(token) {
            this.token = token
            localStorage.setItem('token', token)
        },
        setUser(user) {
            this.user = user
        },
        logout() {
            this.token = null
            this.user = null
            localStorage.removeItem('token')
        },
        addTokens(count){
            this.tokensUsed += count
            localStorage.setItem('tokensUsed', this.tokensUsed)
        },
        resetToken(){
            this.tokensUsed = 0
            localStorage.removeItem('tokensUsed')
        },
        logout() {
            this.token = null
            this.user = null
            this.tokensUsed = 0
            localStorage.removeItem('token')
            localStorage.removeItem('tokensUsed')
        }
    },
})