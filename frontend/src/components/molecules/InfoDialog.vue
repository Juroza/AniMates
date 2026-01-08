<template>
  <v-card class="pa-6">
    <h2>Info</h2>
    <v-divider :thickness="5"></v-divider>
    <br/>
    <div class="button_holder">
      <v-btn class="button"
        id="currentUsers"
        variant="tonal"
        @click="seeCurrentUsers"
      >
        See Current Users
      </v-btn>
      <v-btn class="button"
        id="help"
        variant="tonal"
        @click="help"
      >
        Help
      </v-btn>
      <v-btn class="button"
        id="close"
        variant="tonal"
        @click="close"
      >
        Close
      </v-btn>
    </div>
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
.button_holder {
  width: 100%;
  align-content: right;
}
.button {
  min-width: min-content;
  width: 100%;
}

</style>
