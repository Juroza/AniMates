<template>
  <p>{{ state.currentFrame?.strokeRecord }}</p>
  <p>{{ state.currentFrame?.projectName }}</p>
  <p>{{ state.currentFrame?.url }}</p>
</template>

<script setup lang="ts">
import { useSocket } from '../stores/socketState'

const { state } = useSocket()
</script>
