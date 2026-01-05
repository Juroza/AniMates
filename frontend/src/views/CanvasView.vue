<template>
  <div class="drawing-container">
    <v-card class="mx-auto">
      <v-card-title>Drawing</v-card-title>
      <v-card-text>
        <div class="side-by-side">
          <div class="toolbar-container-left">
            <!-- <div class="back-button">

            </div> -->
            <div class="toolbar-left">
              <v-btn
                :color="mode === 'draw' ? 'primary' : ''"
                variant="outlined"
                @click="setMode('draw')"
                id="draw_button"
              >
                ✏️ Draw
              </v-btn>
              <v-btn
                :color="mode === 'erase' ? 'error' : ''"
                variant="outlined"
                @click="setMode('erase')"
                id="erase_button"
              >
                ⌫ Erase
              </v-btn>
              <!-- <v-btn
                :color="mode === 'fill' ? 'success' : ''"
                variant="outlined"
                @click="setMode('fill')"
                id="fill_button"
              >
                🪣 Fill
              </v-btn> -->
              <v-btn color="warning" variant="outlined" id="clear_button"> 🗑️ Clear </v-btn>

              <div class="info-section">
                <p><strong>Status:</strong> {{ isDirty ? '✏️ Drawing...' : '⭐ Ready' }}</p>
                <p><strong>Strokes:</strong> {{ strokeCount }}</p>
              </div>
            </div>
          </div>
          <div
            class="canvas-wrapper"
            ref="wrapper"
            :style="{
              width: displayWidth + 'px',
              height: displayHeight + 'px',
              '--canvas-scale': scale,
            }"
          >
            <canvas
              ref="canvas"
              class="canvas-layer"
              :width="projectWidth"
              :height="projectHeight"
            ></canvas>

            <canvas
              ref="drawingCanvas"
              class="canvas-layer"
              :width="projectWidth"
              :height="projectHeight"
            ></canvas>
          </div>

          <div class="toolbar-container-right">
            <div class="toolbar-right">
              <div class="control-group">
                <label for="color-picker">Color:</label>
                <input id="color-picker" v-model="color" type="color" @change="updateColor" />
              </div>

              <div class="control-group">
                <label for="brush-size">Brush Size: {{ weight }}px</label>
                <input
                  id="brush-size"
                  v-model.number="weight"
                  type="range"
                  min="1"
                  max="50"
                  @change="updateWeight"
                />
              </div>

              <div class="control-group">
                <label for="smoothing">Smoothing: {{ smoothing.toFixed(2) }}</label>
                <input
                  id="smoothing"
                  v-model.number="smoothing"
                  type="range"
                  min="0.1"
                  max="2"
                  step="0.1"
                  @change="updateSmoothing"
                />
              </div>
            </div>
          </div>
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>
<!-- =========================== CanvasView.vue (only the websocket bits changed) =========================== -->
<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import Atrament, { MODE_DRAW, MODE_ERASE, MODE_FILL, MODE_DISABLED } from 'atrament'
import { useSocket, joinFrameSession } from '../stores/socketState'
import type { Stroke } from '../stores/socketState'

const wrapper = ref<HTMLDivElement | null>(null)
const canvas = ref<HTMLCanvasElement | null>(null)
const drawingCanvas = ref<HTMLCanvasElement | null>(null)
let pngInterval: number | null = null

let renderLayer: InstanceType<typeof Atrament> | null = null
let drawLayer: InstanceType<typeof Atrament> | null = null

const modeMap = {
  draw: MODE_DRAW,
  erase: MODE_ERASE,
  fill: MODE_FILL,
  disabled: MODE_DISABLED,
}

const { state, socket } = useSocket()

// canvas scaling
const MAX_DISPLAY_SIZE = 900

const projectWidth = computed(() => state.currentProject!.width)
const projectHeight = computed(() => state.currentProject!.height)

const scale = computed(() =>
  Math.min(MAX_DISPLAY_SIZE / projectWidth.value, MAX_DISPLAY_SIZE / projectHeight.value, 1),
)

const displayWidth = computed(() => projectWidth.value * scale.value)
const displayHeight = computed(() => projectHeight.value * scale.value)

const strokes = computed(() => state.currentFrame?.strokeRecord ?? [])

watch(
  () => state.currentFrame?.frameName,
  (frameName) => {
    if (!frameName) return
    socket.emit('drawing:get-actions', { frameName })
  },
  { immediate: true },
)

watch(
  strokes,
  (newStrokes) => {
    if (!renderLayer) return
    renderLayer.clear()
    newStrokes.forEach((s) => renderStroke({ stroke: s }))
    strokeCount.value = newStrokes.length
  },
  { deep: true, immediate: true },
)

const canvas_width = ref<number>(0)
const canvas_height = ref<number>(0)
const color = ref<string>('#000000')
const weight = ref<number>(3)
const smoothing = ref<number>(0.85)
const mode = ref<'draw' | 'erase' | 'fill' | 'disabled'>('draw')
const isDirty = ref<boolean>(false)
const strokeCount = ref<number>(0)

onMounted(() => {
  if (state.currentFrame?.frameName) joinFrameSession()
  if (!canvas.value || !drawingCanvas.value || !wrapper.value) return

  renderLayer = new Atrament(canvas.value, {
    width: projectWidth.value,
    height: projectHeight.value,
    color: color.value,
  })

  drawLayer = new Atrament(drawingCanvas.value, {
    width: projectWidth.value,
    height: projectHeight.value,
    color: color.value,
  })

  drawLayer.recordStrokes = true
  renderLayer.recordPaused = false

  renderLayer.addEventListener('dirty', () => (isDirty.value = true))
  renderLayer.addEventListener('clean', () => (isDirty.value = false))

  drawLayer.addEventListener('strokerecorded', ({ stroke }: { stroke: Stroke }) => {
    const frameName = state.currentFrame?.frameName
    if (!frameName) return
    if (mode.value === 'fill') return

    stroke.mode = mode.value

    socket.emit('drawing:action', {
      frameName,
      date: new Date().toISOString(),
      type: 'stroke',
      stroke,
    })
  })

  drawLayer.addEventListener('strokeend', () => {
    if (mode.value === 'draw' || mode.value === 'erase') drawLayer!.clear()
  })

  setMode(mode.value)
  updateColor()
  updateWeight()
  updateSmoothing()

  // IMPORTANT CHANGE: native WS cannot JSON-send ArrayBuffer reliably.
  // So we convert blob -> base64 and send { png: base64 }.
  pngInterval = window.setInterval(() => {
    if (!renderLayer) return

    renderLayer.canvas.toBlob(async (blob: Blob | null) => {
      if (!blob) return

      const arrayBuffer = await blob.arrayBuffer()
      const bytes = new Uint8Array(arrayBuffer)

      // convert to base64
      let binary = ''
      const chunkSize = 0x8000
      for (let i = 0; i < bytes.length; i += chunkSize) {
        binary += String.fromCharCode(...bytes.subarray(i, i + chunkSize))
      }
      const base64 = btoa(binary)

      socket.emit('frame:png', {
        frameName: state.currentFrame?.frameName,
        png: base64,
      })
    }, 'image/png')
  }, 2000)
})

onUnmounted(() => {
  if (pngInterval !== null) {
    clearInterval(pngInterval)
    pngInterval = null
  }
})

const updateColor = () => {
  if (!renderLayer || !drawLayer) return
  renderLayer.color = color.value
  drawLayer.color = color.value
}

const updateWeight = () => {
  if (!renderLayer || !drawLayer) return
  renderLayer.weight = weight.value
  drawLayer.weight = weight.value
}

const updateSmoothing = () => {
  if (!renderLayer || !drawLayer) return
  renderLayer.smoothing = smoothing.value
  drawLayer.smoothing = smoothing.value
}

const setMode = (newMode: 'draw' | 'erase' | 'fill' | 'disabled') => {
  if (!renderLayer || !drawLayer) return
  mode.value = newMode
  renderLayer.mode = MODE_DISABLED
  drawLayer.mode = modeMap[newMode]
}

const renderStroke = ({ stroke }: { stroke: Stroke }) => {
  const originalSettings = {
    mode: mode.value,
    weight: renderLayer!.weight,
    smoothing: renderLayer!.smoothing,
    color: renderLayer!.color,
    adaptiveSmoothing: renderLayer!.adaptiveSmoothing,
  }

  renderLayer!.recordPaused = true
  drawLayer!.recordPaused = true

  const segments = stroke.segments.slice()
  if (segments.length === 0) return

  const safeMode = stroke.mode && stroke.mode in modeMap ? stroke.mode : 'draw'

  renderLayer!.mode = modeMap[safeMode]
  renderLayer!.weight = stroke.weight
  renderLayer!.smoothing = stroke.smoothing
  renderLayer!.color = stroke.color ?? stroke.colour ?? '#000000'
  renderLayer!.adaptiveSmoothing = stroke.adaptiveSmoothing ?? stroke.adaptiveStroke ?? false

  const startSeg = segments.shift()
  if (!startSeg) return
  const startPoint = startSeg.point
  renderLayer!.beginStroke(startPoint.x, startPoint.y)

  let prevPoint = startPoint
  while (segments.length > 0) {
    const seg = segments.shift()
    if (!seg) break
    const { x, y } = renderLayer!.draw(
      seg.point.x,
      seg.point.y,
      prevPoint.x,
      prevPoint.y,
      seg.pressure,
    )
    prevPoint = { x, y }
  }
  renderLayer!.endStroke(prevPoint.x, prevPoint.y)

  renderLayer!.recordPaused = false
  drawLayer!.recordPaused = false

  setMode(originalSettings.mode)
  renderLayer!.weight = originalSettings.weight
  renderLayer!.smoothing = originalSettings.smoothing
  renderLayer!.color = originalSettings.color
  renderLayer!.adaptiveSmoothing = originalSettings.adaptiveSmoothing
}
</script>

<style scoped>
.drawing-container {
  padding: 20px;
  margin: 0 auto;
}
.side-by-side {
  display: flex;
  flex-direction: row;

  gap: 10px;
  justify-content: space-around;
  align-items: center;
}

.toolbar-left {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-right: 20px;
}

.toolbar-right {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-left: 20px;
}

.toolbar-container-left {
  border-right: 2px solid #ddd;
  /* border-radius: 4px; */
  max-height: none;
}

.toolbar-container-right {
  border-left: 2px solid #ddd;
  /* border-radius: 2px; */
  max-height: none;
}

.canvas-wrapper {
  position: relative;
  max-width: 100%;
  margin: 20px 0;
  border: 2px solid #ddd;
  border-radius: 8px;
  display: inline-block;
  background-color: white;
}

.canvas-layer {
  position: absolute;
  top: 0px;
  left: 0px;
  width: 100%;
  height: 100%;
  display: block;
  cursor: crosshair;
  touch-action: none;
}

.drawing-canvas {
  border: 3px solid #444;
}

#rendering {
  z-index: 1;
}
#drawing {
  z-index: 2;
}

.control-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.control-group label {
  margin-bottom: 5px;
  font-weight: 600;
}

.control-group input[type='color'] {
  width: 50px;
  height: 40px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.control-group input[type='range'] {
  width: 100%;
  height: 6px;
}

.info-section {
  margin-top: 20px;
  padding: 15px;
  background-color: #e3f2fd;
  border-radius: 8px;
}

.info-section p {
  margin: 5px 0;
  font-size: 14px;
}
</style>
