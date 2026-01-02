<template>
  <div v-if="state.currentProject">
    <h1 class="title">Project: {{ state.currentProject.name }}</h1>
    <TimeLineSlider :frames="frames" />
    <v-footer app class="pa-0 ma-0" color="transparent">
      <v-row no-gutters class="w-100 px-4 pb-8" align="end">
        <v-col cols="auto">
          <v-btn class="anim-button text-none" variant="text" @click="router.push('/home')">
            [
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="70"
              height="70"
              fill="currentColor"
              class="bi bi-door-open-fill"
              viewBox="0 0 16 16"
            >
              <path
                d="M1.5 15a.5.5 0 0 0 0 1h13a.5.5 0 0 0 0-1H13V2.5A1.5 1.5 0 0 0 11.5 1H11V.5a.5.5 0 0 0-.57-.495l-7 1A.5.5 0 0 0 3 1.5V15zM11 2h.5a.5.5 0 0 1 .5.5V15h-1zm-2.5 8c-.276 0-.5-.448-.5-1s.224-1 .5-1 .5.448.5 1-.224 1-.5 1"
              />
            </svg>

            Leave]
          </v-btn>
        </v-col>

        <v-col cols="auto" class="ml-10">
          <div class="d-flex flex-column align-start">
            <v-btn size="xx-large" variant="text" class="underlined-btn text-none">
              [Options]
            </v-btn>
            <v-btn size="xx-large" variant="text" class="underlined-btn text-none"> [Info] </v-btn>
          </div>
        </v-col>

        <v-spacer></v-spacer>

        <v-col cols="auto">
          <div class="d-flex flex-column align-end">
            <v-btn size="x-large" variant="text" class="buttons big-text-btn text-none">
              [<v-icon icon="$export" class="mr-2" />Export]
            </v-btn>

            <v-btn size="x-large" variant="text" class="buttons big-text-btn text-none">
              [<v-icon icon="$play" class="mr-2" />Play]
            </v-btn>
          </div>
        </v-col>
      </v-row>
    </v-footer>
  </div>
  <div v-else>
    <h1 class="title">No project selected. Please go back to Home.</h1>
    <v-btn @click="router.push('/home')">Back to Home</v-btn>
  </div>
</template>

<script setup lang="ts">
import { useSocket, getImageFramebyName, type Frame } from '../stores/socketState'
import TimeLineSlider from '../components/organisms/TimeLineSlider.vue'
import router from '../router'
import { ref, watch } from 'vue'

const { state } = useSocket()
const frames = ref<Frame[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
async function loadFrames() {
  if (!state.currentProject) return

  loading.value = true
  error.value = null

  try {
    if (state.currentProject.frameCount === 0) {
      frames.value = await Promise.all([
        getImageFramebyName(undefined),
        getImageFramebyName(undefined),
        getImageFramebyName(undefined),
      ])
    } else {
      // TODO: fetch real frame list
      frames.value = []
    }
  } catch {
    error.value = 'iuyg'
    frames.value = []
  } finally {
    loading.value = false
  }
}
watch(
  () => state.currentProject?.name,
  () => loadFrames(),
  { immediate: true },
)
</script>
<style lang="css" scoped>
.title {
  text-decoration: underline;
}
.underlined-btn {
  text-decoration: underline;
  font-family: 'Roboto Mono';
  font-weight: 400;
  font-size: xx-large;
  margin: 20px;
}
.anim-button {
  font-family: 'Roboto Mono';
  font-weight: 400;
  font-size: 70px;
  text-transform: unset !important;
  height: auto !important;
  display: flex;
  align-items: center;
}
.bottom-bar {
  margin-bottom: 1;
  display: flex;
  gap: 16px;
  align-items: center;
  padding: 16px 0;
}
.buttons {
  font-family: 'Roboto Mono';
  font-weight: 400;
  font-size: 62px;
  margin: 20px;
  height: auto !important;
  min-height: 0 !important;
  padding: 0 !important;
}
.buttons :deep(.v-btn__content) {
  line-height: 1 !important;
}
.big-text-btn {
  height: auto !important;
  min-height: 0 !important;
  padding: 0 !important;
  line-height: 1 !important;
}

.big-text-btn :deep(.v-btn__content) {
  padding: 0 !important;
  line-height: 1 !important;
}

.big-text-btn :deep(.v-btn__overlay),
.big-text-btn :deep(.v-btn__underlay) {
  border-radius: 0;
}
</style>
