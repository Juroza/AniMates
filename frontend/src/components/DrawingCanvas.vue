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
              <!-- <v-btn
                :color="mode === 'fill' ? 'success' : ''"
                variant="outlined"
                @click="setMode('fill')"
                id="fill_button"
              >
                🪣 Fill
              </v-btn> -->
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
          <div class="canvas-wrapper" ref="wrapper">
            <canvas
              id="rendering"
              ref="canvas"
              class="canvas-layer"
              :width="canvas_width"
              :height="canvas_height"
            ></canvas>
            <canvas
              id="drawing"
              ref="drawingCanvas"
              class="canvas-layer"
              :width="canvas_width"
              :height="canvas_height"
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
import { ref, onMounted, onUnmounted } from 'vue'
import Atrament, { MODE_DRAW, MODE_ERASE, MODE_FILL, MODE_DISABLED } from 'atrament';
// import fill from 'atrament/fill';
// import { floodFill, hexToRgba } from './utils/floodFill'
import { fi } from 'vuetify/locale';
import { useSocket } from '../stores/socketState';

// References
const wrapper = ref<HTMLDivElement | null>(null)
const canvas = ref<HTMLCanvasElement | null>(null)
const drawingCanvas = ref<HTMLCanvasElement | null>(null)
// The layer for rendering completed actions
let renderLayer: Atrament | null = null
// The layer for registering actions as they happen
let drawLayer: Atrament | null = null
const modeMap = {
  "draw": MODE_DRAW,
  "erase": MODE_ERASE,
  "fill": MODE_FILL,
  "disabled": MODE_DISABLED
}

// Socket connection
const { socket } = useSocket()

// State
const canvas_width = ref<number>(0)
const canvas_height = ref<number>(0)
const color = ref<string>('#000000')
const weight = ref<number>(3)
const smoothing = ref<number>(0.85)
const mode = ref<'draw' | 'erase' | 'fill'>('draw')
const isDirty = ref<boolean>(false)
const strokeCount = ref<number>(0)
const actions = ref<{ date: Date, type: "stroke" | "fill" | "clear", action: unknown }[]>([])

// Initialize Atrament
onMounted(() => {
  if (!canvas.value || !drawingCanvas.value || !wrapper.value) return


  // Binding the dimensions of the canvas to the wrapper
  const wrapper_rect = wrapper.value.getBoundingClientRect()
  canvas_width.value = Math.floor(wrapper_rect.width)
  canvas_height.value = Math.floor(wrapper_rect.height)

  renderLayer = new Atrament(canvas.value, {
    width: canvas_width.value,
    height: canvas_height.value,
    color: color.value,
  })

  drawLayer = new Atrament(drawingCanvas.value, {
    width: canvas_width.value,
    height: canvas_height.value,
    color: color.value,
    // fill: fill,
  })

  drawLayer.recordStrokes = true
  renderLayer.recordPaused = false

  // Setup event listeners
  renderLayer.addEventListener('dirty', () => {
    isDirty.value = true
  })

  renderLayer.addEventListener('clean', () => {
    isDirty.value = false
  })


  // drawLayer.addEventListener('pointerdown', (eventData: PointerEvent) => {
  //   if (mode.value !== 'fill' || !renderLayer) return

  //   if (!renderLayer.recordPaused) {
  //     const renderRect = canvas.value!.getBoundingClientRect()
  //     const drawRect = drawingCanvas.value!.getBoundingClientRect()

  //     // Calculate coordinates relative to renderLayer
  //     const offsetX = eventData.clientX - drawRect.left
  //     const offsetY = eventData.clientY - drawRect.top

  //     const x = renderRect.left + offsetX
  //     const y = renderRect.top + offsetY

  //     actions.value.push({
  //       date: new Date(),
  //       type: 'fill',
  //       action: { x ,y , color: color.value }
  //     })

  //     const eventClone = new PointerEvent(eventData.type, {
  //       bubbles: true,
  //       cancelable: true,
  //       clientX: x,
  //       clientY: y,
  //       button: eventData.button,
  //       buttons: eventData.buttons,
  //       pointerType: eventData.pointerType,
  //       pressure: eventData.pressure,
  //       width: eventData.width,
  //       height: eventData.height,
  //       tiltX: eventData.tiltX,
  //       tiltY: eventData.tiltY,
  //       isPrimary: eventData.isPrimary,
  //     })

  //     renderFill(eventClone)
  //   }
  // })

  // drawLayer.addEventListener('fillstart', (x: number, y: number) => {
  //   if (!renderLayer.recordPaused) {
  //     actions.value.push({
  //       date: new Date(),
  //       type: "fill",
  //       action: { x: x, y: y, color: drawLayer.color } })

  //   renderFill(x, y, drawLayer!.color)
  //   }
  // })

  // drawLayer.addEventListener('fillend', () => {
  //   drawLayer!.clear()
  // })

  drawLayer.addEventListener('strokerecorded', ({ stroke }) =>
  {
    if (!(mode.value === 'fill')) {
      // Send the stroke to the server
      // socket.emit('drawing:action', {
      //   date: new Date(),
      //   type: "stroke",
      //   action: stroke
      // })
    }
  })

  drawLayer.addEventListener('strokeend', () =>
  {
    if (mode.value === 'draw' || mode.value === 'erase') {
      drawLayer!.clear()
    }
  })


  // Initial setup
  setMode(mode.value)
  updateColor()
  updateWeight()
  updateSmoothing()

  // Handle confirmed actions recieved from the server
  const handleActionConfirmed = (confirmedAction) => {
    console.log('Received confirmed action from server:', confirmedAction.type)

    actions.value.push(confirmedAction)

    if (confirmedAction.type === 'stroke') {
      renderStroke(confirmedAction.action)
      strokeCount.value++
    } else if (confirmedAction.type === 'clear') {
      renderLayer!.clear()
      strokeCount.value = 0
    }
  }

  // Set up socket listeners
  // socket.on('drawing:action-confirmed', handleActionConfirmed)

  // Request all existing actions when component mounts
  // socket.emit('drawing:get-actions')

})

// Cleanup on unmount
onUnmounted(() => {
  // socket.off('drawing:action-confirmed', handleActionConfirmed)
})

// Control functions
const updateColor = () => {
  if (!renderLayer) return
  renderLayer.color = color.value
  drawLayer.color = color.value
}

const updateWeight = () => {
  if (!renderLayer) return
  renderLayer.weight = weight.value
  drawLayer.weight = weight.value
}

const updateSmoothing = () => {
  if (!renderLayer) return
  renderLayer.smoothing = smoothing.value
  drawLayer.smoothing = smoothing.value
}

const setMode = (newMode: 'draw' | 'erase' | 'fill') => {
  if (!renderLayer || !drawLayer) return

  mode.value = newMode

  if (newMode === 'fill') {
    renderLayer.mode = MODE_DISABLED
    drawLayer.mode = MODE_FILL
  } else if (newMode === 'draw') {
    renderLayer.mode = MODE_DISABLED
    drawLayer.mode = MODE_DRAW
  } else {
    renderLayer.mode = MODE_DISABLED
    drawLayer.mode = MODE_ERASE
  }
}

const clearCanvas = () => {
  if (!renderLayer) return

  // Send clear action to the server
  // socket.emit('drawing:action', {
  //   date: new Date(),
  //   type: "clear",
  //   action: null
  // })
}

// This function is inspired by Atrament library example code: https://github.com/jakubfiala/atrament/tree/854c4c560ce2ff9d18788166fd24aa516cf05408?tab=readme-ov-file#fill-startend
const renderStroke = (stroke) => {
  const originalSettings = {
    mode: mode.value,
    weight: renderLayer!.weight,
    smoothing: renderLayer!.smoothing,
    color: renderLayer!.color,
    adaptiveSmoothing: renderLayer.adaptiveSmoothing
  }
  // Disable recording while rendering
  renderLayer!.recordPaused = true
  drawLayer!.recordPaused = true

  // Preparing render canvas settings
  const segments = stroke.segments.slice()
  renderLayer!.mode = modeMap[mode.value]
  renderLayer!.weight = stroke.weight
  renderLayer!.smoothing = stroke.smoothing
  renderLayer!.color = stroke.color
  renderLayer!.adaptiveSmoothing = stroke.adaptiveSmoothing

  // Drawing the stroke
  const startPoint = segments.shift().point
  renderLayer!.beginStroke(startPoint.x, startPoint.y)

  let prevPoint = startPoint
  while (segments.length > 0) {
    const segment = segments.shift()
    const { x, y } = renderLayer.draw(segment.point.x, segment.point.y, prevPoint.x, prevPoint.y, segment.pressure)

    prevPoint = { x, y };
  }
  renderLayer.endStroke(prevPoint.x, prevPoint.y)


  renderLayer!.recordPaused = false
  drawLayer!.recordPaused = false

  // Restore original settings
  setMode(originalSettings.mode)
  renderLayer!.weight = originalSettings.weight
  renderLayer!.smoothing = originalSettings.smoothing
  renderLayer!.color = originalSettings.color
  renderLayer!.adaptiveSmoothing = originalSettings.adaptiveSmoothing
}

// const renderFill = (x: number, y: number, fillColor: string) => {
//   if (!renderLayer) return
//   renderLayer!.recordPaused = true

//   const ctx = renderLayer.context
//   if (!ctx) {
//     renderLayer!.recordPaused = false
//     return
//   }
//   floodFill(ctx, Math.floor(x), Math.floor(y), hexToRgba(fillColor))


//   renderLayer!.recordPaused = false
// }


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
  width: 800px;
  height: 600px;
  max-width: 100%;
  margin: 20px 0;
  border: 2px solid #ddd;
  border-radius: 8px;
  display: inline-block;
  background-color: white;
}

.canvas-layer {
  position:absolute;
  top:0px;
  left:0px;
  width: 100%;
  height: 100%;
  display: block;
  cursor: crosshair;
  touch-action: none;
}

.drawing-canvas {
  border:3px solid #444;
}

#rendering { z-index: 1; }
#drawing   { z-index: 2; }

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
