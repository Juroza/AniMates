<template>
  <h1 class="title">Welcome, {{ state.clientUser?.username }}!</h1>
  <v-container fluid class="my-5">
    <v-row>
      <v-col cols="auto" class="d-flex flex-column align-start">
        <v-btn class="buttons" size="x-large" variant="text">
          <v-icon icon="$plus" />

          New Project
        </v-btn>
        <v-btn class="buttons" size="x-large" variant="text">
          <v-icon icon="$delete" />

          Delete Project
        </v-btn>
        <v-btn class="buttons" size="x-large" variant="text">
          <v-icon icon="$pencil" />

          Edit Project
        </v-btn>
        <v-btn class="anim-button" size="xx-large" variant="text">
          <v-icon icon="$pencil" />

          [AniMate!]
        </v-btn>
      </v-col>
      <ProjectList
        :projects="state.clientUser?.myProjects"
        title="My Projects"
        :selected-project="selectedProject"
        @update:selected-project="selectedProject = $event"
      >
      </ProjectList>
      <ProjectList
        :projects="state.clientUser?.collabProjects"
        title="Collaboration Projects"
        :selected-project="selectedProject"
        @update:selected-project="selectedProject = $event"
      >
      </ProjectList>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ProjectList from '../components/molecules/ProjectList.vue'
import { useSocket } from '../stores/socketState'

const { state } = useSocket()
const selectedProject = ref('')
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
