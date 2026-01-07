<template>
  <v-card :title="`Info`" class="pa-6">
    <v-btn id="currentUsers" @click="seeCurrentUsers">See Current Users</v-btn>
    <v-btn id="help" @click="help">Help</v-btn>
    <v-btn id="close" @click="close">Close</v-btn>
  </v-card>
</template>
<script setup lang="ts">
const emit = defineEmits(['seeCurrentUsers', 'help', 'close'])
function seeCurrentUsers() {
  emit("seeCurrentUsers")
}
function help() {
  emit("help")
}
function close() {
  emit("close")
}
</script>
<style lang="css">
  #currentUsers {
    align-self: center;
  }
  #help {
    align-self: center;
  }
  #close {
    align-self: center;
  }
</style>
