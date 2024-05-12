import { defineStore } from 'pinia'

export const useCommonStore = defineStore('storage', {
  state: () => {
    return {
      apiUrl: import.meta.env.VITE_API_URL,
      langcode: 'en',
    }
  },
  actions: {
    
  },
})
