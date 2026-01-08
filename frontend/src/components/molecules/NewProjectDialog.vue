<template>
  <v-card :title="props.project ? 'Edit Project' : 'Create Project'" class="pa-6">
    <v-label class="pa-2">Owner: {{ props.owner?.username }}</v-label>
    <v-text-field label="Project Name" v-model="projectName"
    :error="hasProject"
    :errorMessages="hasProject ? 'This project already exists!' : []"
    ></v-text-field>
    <v-switch color="primary" v-model="projectPrivate" label="Private Access"></v-switch>
    <v-label>Resolution</v-label>
    <v-number-input
      v-model="projectWidth"
      label="Width"
      :disabled="!!props.project"
    ></v-number-input>

    <v-number-input
      v-model="projectHeight"
      label="Height"
      :disabled="!!props.project"
    ></v-number-input>
    <v-number-input
      v-model="projectFPS"
      :reverse="false"
      controlVariant="default"
      label="FPS"
      :hideInput="false"
      :inset="false"
    ></v-number-input>
    <v-select
      v-if="projectPrivate"
      v-model="invitedUsers"
      :items="props.users"
      label="Users"
      chips
      multiple
    ></v-select>
    <v-card-actions>
      <v-btn @click="cancel">Cancel</v-btn>
      <v-btn @click="submitProject" :disabled="projectName.length == 0">Submit</v-btn>
    </v-card-actions>
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
  type User,
} from '../../stores/socketState'
const emit = defineEmits(['submitProject', 'cancel'])
const props = defineProps<{
  users: string[] | undefined
  owner: User | undefined
  project: Project | undefined
}>()

const error = ref(false)
const invitedUsers = ref<string[]>([])
const projectName = ref('')
const projectPrivate = ref(true)
const projectWidth = ref(1980)
const projectHeight = ref(1080)
const projectFPS = ref(10)
var hasProject = false;
import { watch } from 'vue'

watch(
  () => props.project,
  (project) => {
    if (!project) return

    projectName.value = project.name
    projectPrivate.value = project.private
    invitedUsers.value = [...project.users]
    projectWidth.value = project.width
    projectHeight.value = project.height
    projectFPS.value = project.fps
  },
  { immediate: true },
)
function cancel() {
  emit('cancel')
}
async function submitProject() {
  try {
    if (props.owner?.username == undefined) {
      return
    }
    if (props.owner?.password == undefined) {
      return
    }
    const currentDateTime = new Date()
    if (!props.project) {
      const response = await axios.post(BACKEND_ENDPOINT + '/create-new-project', {
        name: projectName.value,
        owner: props.owner.username,
        isPrivate: projectPrivate.value,
        users: invitedUsers.value,
        width: projectWidth.value,
        height: projectHeight.value,
        fps: projectFPS.value,
        datetime_created: currentDateTime.toISOString().replace('Z', ''),
        datetime_modified: currentDateTime.toISOString().replace('Z', ''),
        frameCount: 0,
      })
      if (!response.data.result) {
        error.value = true
        console.log('rong')
        hasProject = true
      } else {
        error.value = false
        console.log('right')
        hasProject = false
        const getUsersresponse = await axios.post<getUsersProjectsResponse>(
          BACKEND_ENDPOINT + '/get-users-project',
          {
            username: props.owner.username,
          },
        )
        console.log(getUsersresponse.data)

        setClientUser({
          id: undefined,
          username: props.owner.username,
          password: props.owner.password,
          myProjects: getUsersresponse.data['my-projects'],
          collabProjects: getUsersresponse.data['collab-projects'],
        })
        emit('submitProject')
      }
      console.log(response.data)
    } else {
      const response = await axios.post(BACKEND_ENDPOINT + '/edit-project', {
        name: projectName.value,
        owner: props.owner.username,
        isPrivate: projectPrivate.value,
        users: invitedUsers.value,
        width: projectWidth.value,
        height: projectHeight.value,
        fps: projectFPS.value,
        datetime_created: props.project.datetime_created,
        datetime_modified: props.project.datetime_modified,
        frameCount: 0,
        id: props.project.id,
        frames: props.project.frames,
      })
      if (!response.data.result) {
        error.value = true
        console.log('rong')
      } else {
        error.value = false
        console.log('right')
        const getUsersresponse = await axios.post<getUsersProjectsResponse>(
          BACKEND_ENDPOINT + '/get-users-project',
          {
            username: props.owner.username,
          },
        )
        console.log(getUsersresponse.data)

        setClientUser({
          id: undefined,
          username: props.owner.username,
          password: props.owner.password,
          myProjects: getUsersresponse.data['my-projects'],
          collabProjects: getUsersresponse.data['collab-projects'],
        })
        emit('submitProject')
      }
      console.log(response.data)
    }
  } catch (err) {
    console.error(err)
    error.value = true
  }
}
</script>
<style lang="css">
.dialog {
  padding-left: 40px;
}
</style>
