<template>
  <div class="drawing-container">
    <v-card class="mx-auto">
      <v-card-title>Atrament Drawing Demo</v-card-title>
      <v-card-text>
        <div class="side-by-side">
          <div class="toolbar-container-left">
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
              <v-btn
                :color="mode === 'fill' ? 'success' : ''"
                variant="outlined"
                @click="setMode('fill')"
                id="fill_button"
              >
                🪣 Fill
              </v-btn>
              <v-btn
              color="warning"
              variant="outlined"
              @click="clearCanvas"
              id="clear_button"
              >
                🗑️ Clear
              </v-btn>

              <div class="info-section">
                <p>
                  <strong>Status:</strong> {{ isDirty ? '✏️ Drawing...' : '⭐ Ready' }}
                </p>
                <p><strong>Strokes:</strong> {{ strokeCount }}</p>
                <p><strong>Actions:</strong> {{ actions.length }}</p>
              </div>
            </div>
          </div>
          <div class="canvas-wrapper">
            <canvas
              id="sketchpad"
              ref="canvas"
              class="drawing-canvas"
              width="canvas_width"
              height="canvas_height"
            ></canvas>
          </div>

          <div class="toolbar-container-right">
            <div class="toolbar-right">
              <div class="control-group">
                <label for="color-picker">Color:</label>
                <input
                  id="color-picker"
                  v-model="color"
                  type="color"
                  @change="updateColor"
                />
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

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Atrament, { MODE_DRAW, MODE_ERASE, MODE_FILL, MODE_DISABLED } from 'atrament'
import fill from 'atrament/fill';

// References
const canvas = ref<HTMLCanvasElement | null>(null)
let atrament: Atrament | null = null

// State
const canvas_width = ref<number>(800)
const canvas_height = ref<number>(600)
const color = ref<string>('#000000')
const weight = ref<number>(3)
const smoothing = ref<number>(0.85)
const mode = ref<'draw' | 'erase' | 'fill'>('draw')
const isDirty = ref<boolean>(false)
const strokeCount = ref<number>(0)
const actions = ref<{ date: Date, type: "stroke" | "fill" | "clear", action: unknown }[]>([])

// Initialize Atrament
onMounted(() => {
  if (!canvas.value) return

  atrament = new Atrament(canvas.value, {
    width: canvas_width.value,
    height: canvas_height.value,
    color: color.value,
    fill: fill,
  })
  atrament.recordStrokes = true
  atrament.recordPaused = false

  // Setup event listeners
  atrament.addEventListener('dirty', () => {
    isDirty.value = true
  })

  atrament.addEventListener('clean', () => {
    isDirty.value = false
  })

  atrament.addEventListener('strokeend', () => {
    strokeCount.value++
  })

  atrament.addEventListener('strokerecorded', ({ stroke }) =>
  {
    if (!atrament.recordPaused) {
      actions.value.push({ date: new Date(), type: "stroke", action: stroke })
    }
  })

  atrament.addEventListener('fillstart', ({ x, y }) => {
    if (!atrament.recordPaused) {
      actions.value.push({
        date: new Date(),
        type: "fill",
        action: {
          x: x,
          y: y,
          color: atrament.color
        }
      })
    }
  })


  // Initial setup
  updateColor()
  updateWeight()
  updateSmoothing()
})

// Control functions
const updateColor = () => {
  if (!atrament) return
  atrament.color = color.value
}

const updateWeight = () => {
  if (!atrament) return
  atrament.weight = weight.value
}

const updateSmoothing = () => {
  if (!atrament) return
  atrament.smoothing = smoothing.value
}

const setMode = (newMode: 'draw' | 'erase' | 'fill') => {
  if (!atrament) return
  mode.value = newMode
  atrament.mode = newMode === 'draw' ? MODE_DRAW : newMode === 'erase' ? MODE_ERASE : MODE_FILL

}

const clearCanvas = () => {
  if (!atrament) return
  atrament.clear()
  strokeCount.value = 0
  if (!atrament.recordPaused) {
      actions.value.push({ date: new Date(), type: "clear", action: null })
  }
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
  margin: 20px 0;
  border: 2px solid #ddd;
  border-radius: 8px;
  display: inline-block;
  background-color: white;
}

.drawing-canvas {
  display: block;
  border-radius: 6px;
  cursor: crosshair;
  touch-action: none;
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
