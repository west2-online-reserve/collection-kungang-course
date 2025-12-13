import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUiStore = defineStore('ui', () => {
  const navExpanded = ref(false)
  const hoveredIndex = ref<number | null>(null)
  const profileOpen = ref(false)
  const topBarCollapsed = ref(false)
  function toggleNav() { navExpanded.value = !navExpanded.value }
  function setHover(i: number | null) { hoveredIndex.value = i }
  function setProfileOpen(v: boolean) { profileOpen.value = v }
  function toggleTopBar() { topBarCollapsed.value = !topBarCollapsed.value }
  return { navExpanded, hoveredIndex, profileOpen, topBarCollapsed, toggleNav, setHover, setProfileOpen, toggleTopBar }
})

