<template>
  <v-col>
    <h3>{{ props.title }}</h3>
    <v-divider :thickness="7"></v-divider>
    <v-list>
      <v-list-item v-if="props.projects?.length === 0">
        <v-list-item-title
          id="defaultString"
        ><b><i>{{ props.defaultString }}</i></b></v-list-item-title>
      </v-list-item>
      <v-list-item v-else
        color="primary"
        v-for="project in props.projects"
        :key="project.name"
        :value="project.name"
        :active="project.name === selectedProject"
        @click="emit('update:selectedProject', project.name)"
      >
        <v-list-item-title>{{ project.name }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-col>
</template>
<script setup lang="ts">
/// <reference types="../../../node_modules/.vue-global-types/vue_3.5_0.d.ts" />
import type { Project } from '../../stores/socketState'
const props = defineProps<{
  projects: Project[] | undefined
  defaultString: string | undefined
  title: string | undefined
  selectedProject: string | undefined
}>()
const emit = defineEmits(['update:selectedProject'])
</script>
<style>
  #defaultString {
    color: #606060;
    text-align: center;
    text-wrap: inherit;
  }
</style>
