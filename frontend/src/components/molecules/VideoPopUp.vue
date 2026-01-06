<template>
  <v-card :title="props.project?.name">
    <video :src="videoURL" controls autoplay playsinline></video>
    <v-card-actions>
      <v-btn @click="downloadVideo">Download</v-btn>
      <v-btn @click="emit('cancel')">Exit</v-btn>
    </v-card-actions>
  </v-card>
</template>
<script setup lang="ts">
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { BACKEND_ENDPOINT, type Project, type Frame } from '../../stores/socketState'
const emit = defineEmits(['cancel'])
const props = defineProps<{
  project: Project | undefined
  frames: Frame[] | undefined
}>()
const videoURL = ref('')
onMounted(async () => {
  try {
    if (!props.frames) return
    if (!props.project) return

    // Fill gaps between frames with the previous frame
    const frames_with_gaps: Frame[] = []
    for (const [index, frame] of props.frames.entries()) {
      const nextFrameNumber = props.frames[index + 1]?.frameNumber || (frame.frameNumber + 1)
      const gapSize = nextFrameNumber - frame.frameNumber

      for (let i = 0; i < gapSize; i++) {
        frames_with_gaps.push(frame)
      }
    }

    const urls = frames_with_gaps.map((frame) => frame.url)
    const fps = props.project.fps
    const resolution = `${props.project.width}x${props.project.height}`
    const response = await axios.post(
      BACKEND_ENDPOINT + '/render-video',
      { urls, fps, resolution },
      {
        responseType: 'blob',
      },
    )

    videoURL.value = URL.createObjectURL(response.data)
    console.log(response.data)
  } catch (err) {
    console.error('Register failed:', err)
  }
})

// Function to download the video using the url
function downloadVideo() {
  if (!videoURL.value) return
  const link = document.createElement('a')
  link.href = videoURL.value
  link.download = `${props.project?.name || 'video'}.mp4`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}
</script>
