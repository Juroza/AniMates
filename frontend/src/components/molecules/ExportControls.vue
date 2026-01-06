<template>
  <v-btn size="x-large" variant="text" class="buttons big-text-btn text-none" @click="exportFrames">
    [<v-icon icon="$export" class="mr-2" />Export]
  </v-btn>
</template>

<script setup lang="ts">
import { FFmpeg } from '@ffmpeg/ffmpeg'
import { fetchFile } from '@ffmpeg/util'
import { saveAs } from 'file-saver'
import { useSocket, getImageFramebyName, type Frame } from '../../stores/socketState'

const { state } = useSocket()

const props = defineProps<{
  frames: Frame[]
}>()

const ffmpeg = new FFmpeg()

async function exportFrames() {
  console.group('[Export MP4]')

  if (!props.frames || props.frames.length === 0) {
    console.error('No frames to export')
    console.groupEnd()
    return
  }

  if (!ffmpeg.loaded) {
    console.log('Loading FFmpeg...')
    await ffmpeg.load()
  }

  let written = 0

  for (let i = 0; i < props.frames.length; i++) {
    const frame = props.frames[i]

    if (!frame) return

    if (!frame.url) {
      console.warn('Skipping invalid frame:', frame)
      continue
    }

    try {
      const filename = `frame_${String(written).padStart(4, '0')}.png`
      await ffmpeg.writeFile(filename, await fetchFile(frame.url))
      written++
    } catch (err) {
      console.error(`Failed to write frame ${i}`, err)
    }
  }

  console.log(`Encoding ${written} frames to MP4...`)

  await ffmpeg.exec([
    '-framerate', String(state!.currentProject?.fps),
    '-i', 'frame_%04d.png',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-movflags', 'faststart',
    'output.mp4'
  ])

  if (written === 0) {
    console.error('No valid frames written')
    console.groupEnd()
    return
  }

  const data = await ffmpeg.readFile('output.mp4')

  const buffer = data instanceof Uint8Array
    ? data.buffer.slice(data.byteOffset, data.byteOffset + data.byteLength)
    : new TextEncoder().encode(data).buffer

  saveAs(
    new Blob([buffer], { type: 'video/mp4' }),
    'frames_export.mp4'
  )
}
</script>
