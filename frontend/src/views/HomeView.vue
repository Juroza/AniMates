<template>
  <h1 class="title">Welcome, {{ state.clientUser?.username }}!</h1>
  <v-container fluid class="my-5">
    <v-row>
      <v-col cols="auto" class="d-flex flex-column align-start">
        <v-btn class="buttons" size="x-large" variant="text" @click="showCreateNewProject = true">
          <v-icon icon="$plus" />

          New Project
        </v-btn>
        <v-btn
          :disabled="selectedProject == ''"
          class="buttons"
          size="x-large"
          variant="text"
          @click="showDeleteProject = true"
        >
          <v-icon icon="$delete" />

          Delete Project
        </v-btn>
        <v-btn
          :disabled="selectedProject == ''"
          class="buttons"
          size="x-large"
          variant="text"
          @click="showEditProject = true"
        >
          <v-icon icon="$pencil" />

          Edit Project
        </v-btn>
        <v-btn
          :disabled="selectedProject == ''"
          class="anim-button"
          size="xx-large"
          variant="text"
          @click="router.push({ name: 'timeline' })"
        >
          <v-icon icon="$pencil" />

          [AniMate!]
        </v-btn>
      </v-col>
      <ProjectList
        :projects="state.clientUser?.myProjects"
        title="My Projects"
        :selected-project="selectedProject"
        @update:selected-project="selectedProject = selectedProject === $event ? '' : $event"
      >
      </ProjectList>
      <ProjectList
        :key="state.clientUser?.myProjects?.length"
        :projects="state.clientUser?.collabProjects"
        title="Collaboration Projects"
        :selected-project="selectedProject"
        @update:selected-project="selectedProject = selectedProject === $event ? '' : $event"
      >
      </ProjectList>
    </v-row>
    <v-dialog max-width="500" v-model="showCreateNewProject" content-class="pa-5">
      <NewProjectDialog
        :key="state.clientUser?.collabProjects?.length"
        :users="users"
        :owner="state.clientUser"
        :project="undefined"
        @cancel="showCreateNewProject = false"
        @submit-project="showCreateNewProject = false"
      >
      </NewProjectDialog>
    </v-dialog>
    <v-dialog max-width="500" v-model="showDeleteProject" content-class="pa-5">
      <DeleteProjectDialog
        :owner="state.clientUser"
        :project-name="selectedProject"
        @cancel="showDeleteProject = false"
        @submit-project="showDeleteProject = false"
      >
      </DeleteProjectDialog>
    </v-dialog>
    <v-dialog max-width="500" v-model="showEditProject" content-class="pa-5">
      <NewProjectDialog
        :key="state.clientUser?.collabProjects?.length"
        :users="users"
        :owner="state.clientUser"
        :project="selectedProjectFull"
        @cancel="showEditProject = false"
        @submit-project="showEditProject = false"
      >
      </NewProjectDialog>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import ProjectList from '../components/molecules/ProjectList.vue'
import { BACKEND_ENDPOINT, useSocket, type getAllUsersResponse } from '../stores/socketState'
import DeleteProjectDialog from '../components/molecules/DeleteProjectDialog.vue'
import axios from 'axios'
import NewProjectDialog from '../components/molecules/NewProjectDialog.vue'
import router from '../router'

const { state } = useSocket()
const selectedProject = ref('')
const selectedProjectFull = computed(() => {
  const a = state.clientUser?.myProjects?.filter((proj) => proj.name === selectedProject.value)
  if (!a) {
    const b = state.clientUser?.collabProjects?.filter(
      (proj) => proj.name === selectedProject.value,
    )
    if (!b) {
      return undefined
    }
    return b[0]
  }
  return a[0]
})
watch(
  selectedProjectFull,
  (newProject) => {
    state.currentProject = newProject ?? undefined
  },
  { immediate: true },
)
const showCreateNewProject = ref(false)
const showDeleteProject = ref(false)
const showEditProject = ref(false)
const users = ref<string[]>([''])
onMounted(() => {
  getAllUsers()
})
async function getAllUsers() {
  try {
    const response = await axios.post<getAllUsersResponse[]>(BACKEND_ENDPOINT + '/get-all-users')
    if (!response.data) {
      console.log('rong')
    } else {
      console.log('right')
      users.value = response.data.map((user) => user.username)
    }

    console.log(response.data)
  } catch (err) {
    console.error(err)
  }
}
</script>
<style lang="css">
.title {
  font-family: 'Roboto Mono';
  font-weight: 400;
  size: 84px;
  font-size: 50px;
  margin: 20px;
}
.buttons {
  font-family: 'Roboto Mono';
  font-weight: 400;
  font-size: xx-large;
  margin: 20px;
}
.anim-button {
  font-family: 'Roboto Mono';
  font-weight: 400;
  font-size: 70px;
  margin-top: 90px;
}
</style>
