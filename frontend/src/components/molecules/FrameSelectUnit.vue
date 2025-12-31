<template>
  <v-container class="thumb" :style="{ transform: `rotateY(${props.rotation}deg)` }">
    <v-label
      id="cover"
      :style="{
        transform: `rotateY(${props.rotation}deg)`,
        ...shadowStyle,
      }"
      >{{ frame?.frameNumber }}</v-label
    >

    <img
      id="cover"
      :src="frame?.url"
      @click="select"
      :style="{
        transform: `rotateY(${props.rotation}deg)`,
        ...shadowStyle,
      }"
  /></v-container>
</template>
<script setup lang="ts">
import { type Frame } from '../../stores/socketState'

const props = defineProps<{
  frame: Frame | undefined
  rotation: number
}>()
const emit = defineEmits(['selected'])
function select() {
  emit('selected', props.frame)
}
import { computed } from 'vue'

const shadowStyle = computed(() => {
  const r = props.rotation

  // Clamp so it doesn't go crazy
  const clamped = Math.max(-60, Math.min(60, r))

  // Horizontal shadow moves opposite to rotation
  const x = -clamped * 0.8

  // Vertical shadow slightly increases with angle
  const y = 20 + Math.abs(clamped) * 0.3

  // Blur increases with distance
  const blur = 40 + Math.abs(clamped) * 0.6

  return {
    boxShadow: `${x}px ${y}px ${blur}px rgba(0,0,0,0.35)`,
  }
})
</script>

<style lang="css">
/*
Source - https://stackoverflow.com/q
Posted by Eric Gutiérrez Llopis, modified by community. See post 'Timeline' for change history
Retrieved 2025-12-31, License - CC BY-SA 3.0
*/

.thumb {
  perspective: 600px;
}

#cover {
  width: 60%;
  max-width: 300px;
  display: block;
  margin: auto;
  transform-style: preserve-3d;
}
</style>
