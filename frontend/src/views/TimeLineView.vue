<template>
  <div v-if="state.currentProject">
    <h1 class="title">Project: {{ state.currentProject.name }}</h1>
    <TimeLineSlider :frames="frames" />
  </div>
  <div v-else>
    <h1 class="title">No project selected. Please go back to Home.</h1>
    <v-btn @click="router.push('/home')">Back to Home</v-btn>
  </div>
</template>

<script setup lang="ts">
import { useSocket, getImageFramebyName, type Frame } from '../stores/socketState'
import TimeLineSlider from '../components/organisms/TimeLineSlider.vue'
import router from '../router'
import { ref, watch } from 'vue'

const { state } = useSocket()
const frames = ref<Frame[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
async function loadFrames() {
  if (!state.currentProject) return

  loading.value = true
  error.value = null

  try {
    if (state.currentProject.frameCount === 0) {
      frames.value = await Promise.all([
        getImageFramebyName(undefined),
        getImageFramebyName(undefined),
        getImageFramebyName(undefined),
      ])
    } else {
      // TODO: fetch real frame list
      frames.value = []
    }
  } catch {
    error.value = 'iuyg'
    frames.value = []
  } finally {
    loading.value = false
  }
}
watch(
  () => state.currentProject?.name,
  () => loadFrames(),
  { immediate: true },
)
</script>
