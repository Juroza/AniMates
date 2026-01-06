<template>
  <v-btn size="x-large" variant="text" class="buttons big-text-btn text-none" @click="exportFrames">
    [<v-icon icon="$export" class="mr-2" />Export]
  </v-btn>
</template>

<script setup lang="ts">
import JSZip from 'jszip'
import { saveAs } from 'file-saver'
import type { Frame } from '../../stores/socketState'

const props = defineProps<{
  frames: Frame[]
}>()

async function exportFrames() {
  console.group('[Export ZIP]')

  if (!props.frames || props.frames.length === 0) {
    console.error('No frames to export')
    console.groupEnd()
    return
  }

  const zip = new JSZip()
  let added = 0

  for (const frame of props.frames) {
    if (!frame.url || !frame.frameName) {
      console.warn('Skipping invalid frame:', frame)
      continue
    }

    try {
      const res = await fetch(frame.url)
      if (!res.ok) throw new Error(`HTTP ${res.status}`)

      const blob = await res.blob()
      if (!blob.size) throw new Error('Empty blob')

      zip.file(`${frame.frameName}.png`, blob)
      added++

      console.log(`Added ${frame.frameName}.png`)
    } catch (err) {
      console.error(`Failed to fetch ${frame.frameName}`, err)
    }
  }

  if (added === 0) {
    console.error('ZIP aborted — no valid frames added')
    console.groupEnd()
    return
  }

  const zipBlob = await zip.generateAsync({ type: 'blob' })
  saveAs(zipBlob, 'frames_export.zip')

  console.log(`ZIP generated with ${added} frame(s)`)
  console.groupEnd()
}
</script>
