<template>
  <div v-if="state.currentProject">
    <h1 class="title">Project: {{ state.currentProject.name }}</h1>
    <TimeLineSlider :frames="frames" @select="onFrameSelected" />
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
            <v-btn
              size="xx-large"
              variant="text"
              class="underlined-btn text-none"
              @click="showOptionDialog = true"
            >
              [Options]
            </v-btn>
            <v-btn
            size="xx-large"
            variant="text"
            class="underlined-btn text-none"
            @click="showInfoDialog = true"
            >
              [Info]
            </v-btn>
          </div>
        </v-col>

        <v-spacer />

        <v-col cols="auto">
          <div class="d-flex flex-column align-end">
            <!-- EXPORT CONTROLS -->
            <ExportControls :frames="frames" />

            <v-btn
              @click="showVideoPopup = true"
              size="x-large"
              variant="text"
              class="buttons big-text-btn text-none"
            >
              [<v-icon icon="$play" class="mr-2" />Play]
            </v-btn>
          </div>
        </v-col>
      </v-row>
    </v-footer>
    <v-dialog max-width="500" v-model="showOptionDialog" content-class="pa-5">
      <FrameOptionsDialog
        :project="state.currentProject"
        :username="state.clientUser?.username"
        :key="state.clientUser?.collabProjects?.length"
        @cancel="showOptionDialog = false"
        @done="
          () => {
            showOptionDialog = false
            loadFrames()
          }
        "
      />
    </v-dialog>
    <v-dialog max-width="500" v-model="showInfoDialog" content-class="pa-5">
      <InfoDialog
        @see-current-users="
        () => {
          showCurrentUsersDialog = true
          showInfoDialog = false
        }"
        @help="
        () => {
          showHelpDialog = true
          showInfoDialog = false
        }"
        @close="showInfoDialog = false"
      />
    </v-dialog>
    <v-dialog max-width="500" v-model="showCurrentUsersDialog" content-class="pa-5">
      <CurrentUsersDialog
        :userMap="userMap"
        @close="showCurrentUsersDialog = false"
      />
    </v-dialog>
    <v-dialog max-width="500" v-model="showHelpDialog" content-class="pa-5">
      <HelpDialog
        @close="showHelpDialog = false"
      />
    </v-dialog>
    <v-dialog max-width="500" v-model="showVideoPopup" content-class="pa-5">
      <VideoPopUp @cancel="showVideoPopup = false" :frames="frames" :project="state.currentProject">
      </VideoPopUp>
    </v-dialog>
  </div>
  <div v-else>
    <h1 class="title">No project selected. Please go back to Home.</h1>
    <v-btn @click="router.push('/home')">Back to Home</v-btn>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import router from '../router'

import { useSocket, getImageFramebyName, type Frame } from '../stores/socketState'
import { getUsersOnProject } from '../stores/socketState'
import { setCurrentFrame } from '../stores/socketState'

import TimeLineSlider from '../components/organisms/TimeLineSlider.vue'
import FrameOptionsDialog from '../components/molecules/FrameOptionsDialog.vue'
import ExportControls from '../components/molecules/ExportControls.vue'
import VideoPopUp from '../components/molecules/VideoPopUp.vue'
import InfoDialog from '../components/molecules/InfoDialog.vue'
import CurrentUsersDialog from '../components/molecules/CurrentUsersDialog.vue'
import HelpDialog from '../components/molecules/HelpDialog.vue'
const { state } = useSocket()
const frames = ref<Frame[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const videoURL = ref<string>('')
const showOptionDialog = ref(false)
const showInfoDialog = ref(false)
const showCurrentUsersDialog = ref(false)
const showHelpDialog = ref(false)
const showVideoPopup = ref(false)
const userMap = ref<Map<string, (number|undefined)>>(new Map())
// const allUsers = ref<string[]>([])
async function loadFrames() {
  if (!state.currentProject) return

  loading.value = true
  error.value = null

  try {
    console.log('Frame count:' + state.currentProject.frameCount)
    if (state.currentProject.frames.length !== 0) {
      frames.value = await Promise.all(
        state.currentProject.frames.map((name) => getImageFramebyName(name)),
      )
    } else {
      showOptionDialog.value = true
    }
  } catch {
    error.value = 'Failed to load frames'
    frames.value = []
  } finally {
    loading.value = false
  }
}

watch(
  () => state.currentProject?.name,
  () => {
    loadFrames()
    getUsersOnProject()
    // getAllUsers()
  },
  { immediate: true })

watch(
  () => state.currentUsers,
  () => {
    userMap.value = computeUserMap()
  },
  { deep: true }
)

function onFrameSelected(index: number) {
  setCurrentFrame(frames.value[index])
}

// async function getAllUsers() {
//   try {
//     const response = await axios.post<getAllUsersResponse[]>(BACKEND_ENDPOINT + '/get-all-users')
//     if (!response.data) {
//       console.log('rong')
//     } else {
//       console.log('right')
//       allUsers.value.push(...response.data.map((user) => user.username))
//     }

//   } catch (err) {
//     console.error(err)
//   }
// }

function computeUserMap() {
  // const onlineUsers = state.currentUsers || new Map()
  // const allUsersMap: Map<string, number|undefined> = new Map()

  // for (const user of allUsers.value) {
  //   if (onlineUsers?.has(user)) {
  //     allUsersMap.set(user, onlineUsers.get(user))
  //   } else {
  //     allUsersMap.set(user, undefined)
  //   }
  // }

  // userMap.value = allUsersMap
  // return onlineUsers
  // Create a new Map to ensure Vue reactivity
  if (!state.currentUsers) return new Map()
  return new Map(state.currentUsers)
}
</script>

<style scoped>
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

.buttons {
  font-family: 'Roboto Mono';
  font-weight: 400;
  font-size: 62px;
  margin: 20px;
  height: auto !important;
  min-height: 0 !important;
  padding: 0 !important;
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
