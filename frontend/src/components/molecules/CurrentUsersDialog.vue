<template>
  <v-card :title="`Active Users`" class="pa-6">
    <v-divider :thickness="4"></v-divider>
    <v-list v-if="props.userMap.size > 0">
      <v-list-item
        :color="frameNumber ? `success` : `grey`"
        v-for="[user, frameNumber] in props.userMap.entries()"
        :key="frameNumber ? frameNumber : 0"
        :title="user"
        :subtitle="frameNumber ? `Frame ${frameNumber}` : 'Offline'"
      ></v-list-item>
    </v-list>
    <p v-else > No Current Users</p>
  </v-card>
</template>
<script setup lang="ts">
import { useSocket } from '../../stores/socketState'

const { state } = useSocket()
const props = defineProps<{
  userMap: Map<string, number | undefined>
}>()

</script>
<style lang="css">
p {
  display: flex;
  justify-content: space-between;
}
</style>
