<template>
  <v-card :title="`Frame Options`" class="pa-6">
    <v-number-input
      v-model="newProjectFrameNumber"
      :reverse="false"
      controlVariant="default"
      label="New Frame Number"
      :hideInput="false"
      :inset="false"
    ></v-number-input>
    <v-btn @click="createNewFrame" :disabled="newProjectFrameNumber <= 0"
      ><v-icon icon="$plus" /> New Frame</v-btn
    >
    <v-btn @click="cancel">Cancel</v-btn>
  </v-card>
</template>
<script setup lang="ts">
import axios from 'axios'
import { ref } from 'vue'
import {
  BACKEND_ENDPOINT,
  type getUsersProjectsResponse,
  type Project,
  setClientUser,
  setCurrentProject,
  useSocket,
} from '../../stores/socketState'
const newProjectFrameNumber = ref(0)
const error = ref(false)
const props = defineProps<{
  project: Project | undefined
  username: string | undefined
}>()
function cancel() {
  emit('cancel')
}
const emit = defineEmits(['done', 'cancel'])
const { state } = useSocket()
async function createNewFrame() {
  try {
    const response = await axios.post(BACKEND_ENDPOINT + '/add-frame-to-project', {
      projectName: props.project?.name,
      strokeRecord: [],
      frameNumber: newProjectFrameNumber.value,
    })
    if (!response.data.result) {
      error.value = true
      console.log('rong')
    } else {
      error.value = false
      console.log('right')
      if (!props.username) {
        return undefined
      }
      const getUsersresponse = await axios.post<getUsersProjectsResponse>(
        BACKEND_ENDPOINT + '/get-users-project',
        {
          username: props.username,
        },
      )
      console.log('response from frame')
      console.log(getUsersresponse.data)

      setClientUser({
        id: undefined,
        username: props.username,
        password: props.username,
        myProjects: getUsersresponse.data['my-projects'],
        collabProjects: getUsersresponse.data['collab-projects'],
      })
      const updated =
        getUsersresponse.data['my-projects'].find((p) => p.name === props.project?.name) ||
        getUsersresponse.data['collab-projects'].find((p) => p.name === props.project?.name)

      setCurrentProject(updated ?? state.currentProject)

      emit('done')
    }
    console.log(response.data)
  } catch (err) {
    console.error(err)
    error.value = true
  }
}
</script>
