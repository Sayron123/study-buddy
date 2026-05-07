<!-- ScrollDown.vue -->
<script setup>
import { onMounted, onUnmounted } from 'vue'

function updateThumb() {
  const main = document.querySelector('main')
  if (!main) return

  const track = document.getElementById('scroll-track')
  const thumb = document.getElementById('scroll-thumb')
  if (!track || !thumb) return

  const scrollTop = main.scrollTop
  const scrollHeight = main.scrollHeight - main.clientHeight
  const progress = scrollHeight > 0 ? scrollTop / scrollHeight : 0

  const trackHeight = track.clientHeight
  const thumbHeight = thumb.clientHeight
  thumb.style.top = (progress * (trackHeight - thumbHeight)) + 'px'
}

function onTrackClick(e) {
  const main = document.querySelector('main')
  const track = document.getElementById('scroll-track')
  if (!main || !track) return

  const rect = track.getBoundingClientRect()
  const ratio = (e.clientY - rect.top) / track.clientHeight
  main.scrollTo({ top: ratio * (main.scrollHeight - main.clientHeight), behavior: 'smooth' })
}

onMounted(() => {
  const main = document.querySelector('main')
  if (main) main.addEventListener('scroll', updateThumb)
  updateThumb()
})

onUnmounted(() => {
  const main = document.querySelector('main')
  if (main) main.removeEventListener('scroll', updateThumb)
})
</script>

<template>
  <div
    id="scroll-track"
    @click="onTrackClick"
    class="fixed right-3 top-1/2 -translate-y-1/2 z-50 flex flex-col items-center"
    style="width: 4px; height: 60vh; background: rgba(255,255,255,0.1); border-radius: 999px; cursor: pointer;"
  >
    <div
      id="scroll-thumb"
      style="
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        width: 4px;
        height: 40px;
        background: rgba(255,255,255,0.5);
        border-radius: 999px;
        top: 0;
        transition: background 0.2s;
      "
    />
    <!-- Arrow at bottom -->
    <div style="
      position: absolute;
      bottom: -18px;
      left: 50%;
      transform: translateX(-50%);
      width: 0; height: 0;
      border-left: 5px solid transparent;
      border-right: 5px solid transparent;
      border-top: 7px solid rgba(255,255,255,0.4);
    " />
  </div>
</template>