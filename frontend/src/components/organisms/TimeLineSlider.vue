<template>
  <v-container fluid class="pa-0 ma-0 carousel-wrapper">
    <v-row align="center" no-gutters class="carousel-row">
      <v-col cols="auto" class="z-nav">
        <v-btn icon :disabled="atStart" @click="scrollByItems(-1)" variant="text" density="compact">
          <v-icon icon="$left" />
        </v-btn>
      </v-col>

      <v-col class="flex-grow-1 overflow-visible">
        <div ref="strip" class="frame-strip" @scroll="onScroll">
          <div class="spacer"></div>

          <div
            v-for="(frame, i) in props.frames"
            :key="frame.frameNumber ?? i"
            :ref="(el) => setItemRef(el, i)"
            class="item-container"
            :style="getWrapperStyle(i)"
          >
            <FrameSelectUnit
              :frame="frame"
              :rotation="calculateRotation(i)"
              @selected="scrollToIndex(i)"
            />
          </div>

          <div class="spacer"></div>
        </div>
      </v-col>

      <v-col cols="auto" class="z-nav">
        <v-btn icon :disabled="atEnd" @click="scrollByItems(1)" variant="text" density="compact">
          <v-icon icon="$right" />
        </v-btn>
      </v-col>
    </v-row>

    <div class="text-center text-caption text-grey mt-1">
      {{ selectedIndex + 1 }} / {{ props.frames.length }}
    </div>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import FrameSelectUnit from '../molecules/FrameSelectUnit.vue'
import { type Frame } from '../../stores/socketState'

const props = defineProps<{ frames: Frame[] }>()
const strip = ref<HTMLDivElement | null>(null)
const itemEls = ref<(HTMLElement | null)[]>([])
const selectedIndex = ref(0)
const atStart = ref(true)
const atEnd = ref(false)

// Constants
const MAX_ROTATION = 55
const CENTER_SCALE = 1.25
const SIDE_SCALE = 0.85

function setItemRef(el: any, i: number) {
  if (el) itemEls.value[i] = el
}

/**
 * Returns 0 if it is the selected index, otherwise returns distance
 */
function getNormalizedDistance(index: number): number {
  // HARD LOCK: If it's the selected one, it must be 0 (flat)
  if (index === selectedIndex.value) return 0

  const scroller = strip.value
  const el = itemEls.value[index]
  if (!scroller || !el) return 0

  const sRect = scroller.getBoundingClientRect()
  const eRect = el.getBoundingClientRect()
  const sCenter = sRect.left + sRect.width / 2
  const eCenter = eRect.left + eRect.width / 2

  return (eCenter - sCenter) / eRect.width
}

function calculateRotation(index: number): number {
  const dist = getNormalizedDistance(index)
  if (dist === 0) return 0 // Guaranteed flat for selectedIndex

  const sign = Math.sign(dist)
  const absDist = Math.abs(dist)

  // Power function makes adjacent frames tilt away more naturally
  return Math.max(Math.min(sign * Math.pow(absDist, 1.1) * MAX_ROTATION, 60), -60)
}

function getWrapperStyle(index: number) {
  const dist = getNormalizedDistance(index)
  const absDist = Math.abs(dist)

  // Force center scale if it's the selected index
  const scaleValue =
    index === selectedIndex.value
      ? CENTER_SCALE
      : Math.max(CENTER_SCALE - absDist * (CENTER_SCALE - SIDE_SCALE), SIDE_SCALE)

  return {
    zIndex: index === selectedIndex.value ? 100 : Math.round(50 - absDist * 10),
    transform: `scale(${scaleValue})`,
    transition: 'transform 0.15s ease-out', // Slightly slower ease makes rotation snap feel better
    willChange: 'transform',
  }
}

function updateState() {
  if (!strip.value) return

  const sRect = strip.value.getBoundingClientRect()
  const sCenter = sRect.left + sRect.width / 2

  let bestIdx = 0
  let minDiff = Infinity

  itemEls.value.forEach((el, i) => {
    if (!el) return
    const eRect = el.getBoundingClientRect()
    const eCenter = eRect.left + eRect.width / 2
    const diff = Math.abs(eCenter - sCenter)
    if (diff < minDiff) {
      minDiff = diff
      bestIdx = i
    }
  })

  selectedIndex.value = bestIdx
  atStart.value = strip.value.scrollLeft <= 5
  atEnd.value = strip.value.scrollLeft >= strip.value.scrollWidth - strip.value.clientWidth - 5
}

function onScroll() {
  requestAnimationFrame(updateState)
}

function scrollToIndex(i: number) {
  const scroller = strip.value
  if (!scroller || !itemEls.value[i]) return

  scroller.style.scrollSnapType = 'none'
  const targetScroll =
    itemEls.value[i]!.offsetLeft + itemEls.value[i]!.offsetWidth / 2 - scroller.clientWidth / 2

  scroller.scrollTo({ left: targetScroll, behavior: 'smooth' })

  setTimeout(() => {
    if (scroller) scroller.style.scrollSnapType = 'x mandatory'
  }, 500)
}

function scrollByItems(dir: number) {
  const next = Math.max(0, Math.min(props.frames.length - 1, selectedIndex.value + dir))
  scrollToIndex(next)
}

onMounted(async () => {
  await nextTick()
  updateState()
  window.addEventListener('resize', updateState)
})
onBeforeUnmount(() => window.removeEventListener('resize', updateState))
</script>

<style scoped>
.carousel-wrapper {
  max-width: none !important;
  height: fit-content;
  overflow: visible;
}

.carousel-row {
  height: 200px; /* Adjust this to match your component height */
  margin: 0 !important;
}

.frame-strip {
  display: flex;
  align-items: center;
  overflow-x: auto;
  overflow-y: visible;
  scroll-snap-type: x mandatory;
  scrollbar-width: none;
  padding: 10px 0;
  -webkit-overflow-scrolling: touch;
  height: 100%;
}

.frame-strip::-webkit-scrollbar {
  display: none;
}

.item-container,
.spacer {
  flex: 0 0 33.333%;
  width: 33.333%;
}

.item-container {
  display: flex;
  justify-content: center;
  align-items: center;
  scroll-snap-align: center;
  overflow: visible;
}

.z-nav {
  z-index: 150;
}
</style>
