<template>
  <v-card class="pa-8" width="100%">
    <v-card-title class="text-h6">Frame Options</v-card-title>

    <v-divider class="my-4" />

    <!-- ADD FRAME -->
    <v-sheet
      class="option-row mb-4 pa-1"
      rounded="lg"
      elevation="6"
      color="surface"
      tabindex="0"
      @click="onAddFrame"
      @keydown.enter="onAddFrame"
    >
      <v-row align="center">
        <v-col cols="3">
          <span class="option-label">Add frame</span>
        </v-col>
        <v-col cols="4">
          <v-number-input
            v-model="addFrame"
            :min="totalFrames + 1"
            density="compact"
            hide-details
            @click.stop
            @keydown.enter.stop
          />
        </v-col>
      </v-row>
    </v-sheet>

    <!-- DUPLICATE FRAME -->
    <v-sheet
      class="option-row mb-4 pa-1"
      rounded="lg"
      elevation="6"
      color="surface"
      tabindex="0"
      @click="onDuplicateFrame"
      @keydown.enter="onDuplicateFrame"
    >
      <v-row align="center">
        <v-col cols="3">
          <span class="option-label">Duplicate frame</span>
        </v-col>
        <v-col cols="4">
          <v-number-input
            v-model="duplicateFrame"
            :min="1"
            :max="totalFrames"
            density="compact"
            hide-details
            @click.stop
            @keydown.enter.stop
          />
        </v-col>
      </v-row>
    </v-sheet>

    <!-- MOVE FRAME -->
    <v-sheet
      class="option-row mb-4 pa-1"
      rounded="lg"
      elevation="6"
      color="surface"
      tabindex="0"
      @click="onMoveFrame"
      @keydown.enter="onMoveFrame"
    >
      <v-row align="center">
        <v-col cols="3">
          <span class="option-label">Move frame</span>
        </v-col>

        <v-col cols="4">
          <v-number-input
            v-model="moveFrom"
            :min="1"
            :max="totalFrames"
            density="compact"
            hide-details
            @click.stop
            @keydown.enter.stop
          />
        </v-col>

        <v-col cols="1" class="px-0 d-flex justify-center align-center">
          <span class="option-label">to</span>
        </v-col>

        <v-col cols="4" class="pl-0">
          <v-number-input
            v-model="moveTo"
            :min="1"
            :max="totalFrames"
            density="compact"
            hide-details
            @click.stop
            @keydown.enter.stop
          />
        </v-col>
      </v-row>
    </v-sheet>

    <!-- DELETE FRAME -->
    <v-sheet
      class="option-row mb-4 pa-1"
      rounded="lg"
      elevation="6"
      color="surface"
      tabindex="0"
      @click="onDeleteFrame"
      @keydown.enter="onDeleteFrame"
    >
      <v-row align="center">
        <v-col cols="3">
          <span class="option-label">Delete frame</span>
        </v-col>
        <v-col cols="4">
          <v-number-input
            v-model="deleteFrame"
            :min="1"
            :max="totalFrames"
            density="compact"
            hide-details
            @click.stop
            @keydown.enter.stop
          />
        </v-col>
      </v-row>
    </v-sheet>

    <v-card-actions class="justify-center mt-8">
      <v-btn variant="text" @click="cancel">Cancel</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
import axios from 'axios'
import { ref, computed, watch } from 'vue'
import {
  BACKEND_ENDPOINT,
  type getUsersProjectsResponse,
  type Project,
  setClientUser,
  setCurrentProject,
  useSocket,
} from '../../stores/socketState'

const props = defineProps<{
  project: Project | undefined
  username: string | undefined
}>()

const emit = defineEmits(['done', 'cancel'])
const { state } = useSocket()

const totalFrames = computed(() => props.project?.frames.length ?? 0)

const addFrame = ref(totalFrames.value + 1)
const duplicateFrame = ref(1)
const moveFrom = ref(1)
const moveTo = ref(1)
const deleteFrame = ref(1)

const error = ref(false)

watch(totalFrames, (n) => {
  addFrame.value = n + 1
  deleteFrame.value = Math.min(deleteFrame.value, n)
})

function cancel() {
  emit('cancel')
}

async function onAddFrame() {
  await createNewFrame()
  cancel()
}

async function onDeleteFrame() {
  if (totalFrames.value <= 1) return
  await deleteSelectedFrame()
  cancel()
}

async function onDuplicateFrame() {
  console.warn('not implemented yet')
}

async function onMoveFrame() {
  console.warn('not implemented yet')
}

async function createNewFrame() {
  if (!props.project || !props.username) return
  if (addFrame.value < totalFrames.value + 1) return

  try {
    const response = await axios.post(BACKEND_ENDPOINT + '/add-frame-to-project', {
      projectName: props.project.name,
      strokeRecord: [],
      frameNumber: addFrame.value,
    })

    if (!response.data.result) {
      error.value = true
      return
    }

    await refreshProject()
  } catch (err) {
    console.error(err)
    error.value = true
  }
}

async function deleteSelectedFrame() {
  if (!props.project || !props.username) return

  const index = deleteFrame.value - 1
  const frameName = props.project.frames[index]

  if (!frameName) {
    console.warn('Frame does not exist')
    return
  }

  try {
    const response = await axios.post(BACKEND_ENDPOINT + '/delete-frame', {
      name: frameName,
    })

    if (!response.data.result) {
      error.value = true
      return
    }

    await refreshProject()
  } catch (err) {
    console.error(err)
    error.value = true
  }
}

async function refreshProject() {
  const res = await axios.post<getUsersProjectsResponse>(BACKEND_ENDPOINT + '/get-users-project', {
    username: props.username,
  })

  setClientUser({
    id: undefined,
    username: props.username!,
    password: props.username!,
    myProjects: res.data['my-projects'],
    collabProjects: res.data['collab-projects'],
  })

  const updated =
    res.data['my-projects'].find((p) => p.name === props.project?.name) ||
    res.data['collab-projects'].find((p) => p.name === props.project?.name)

  setCurrentProject(updated ?? state.currentProject)
  emit('done')
}
</script>

<style scoped>
.option-label {
  font-size: 1rem;
  font-weight: 500;
  opacity: 0.9;
}
.option-row {
  cursor: pointer;
  transition: background-color 0.15s ease;
}
.option-row:hover {
  background-color: rgba(255, 255, 255, 0.04);
}
.option-row:active {
  background-color: rgba(255, 255, 255, 0.08);
}
.option-row:hover .option-label {
  font-weight: 600;
}
</style>
