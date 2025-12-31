<template>
  <FrameSelectUnit :frame="props.frames[0]" :rotation="-45"></FrameSelectUnit>
</template>

<script setup lang="ts">
import FrameSelectUnit from '../molecules/FrameSelectUnit.vue'
import { type Frame } from '../../stores/socketState'

const props = defineProps<{
  frames: Frame[]
}>()
</script>
