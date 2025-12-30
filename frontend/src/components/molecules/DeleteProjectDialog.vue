<template>
  <v-card :title="`Delete ${props.projectName}`" subtitle="Are you sure?" class="pa-6">
    <v-card-actions>
      <v-btn @click="cancel">Cancel</v-btn>
      <v-btn class="dlt-btn" @click="deleteProject">
        <v-icon icon="$delete" />
        Delete</v-btn
      >
    </v-card-actions>
  </v-card>
</template>
<script setup lang="ts">
import axios from 'axios'
import { ref } from 'vue'
import {
  BACKEND_ENDPOINT,
  type getUsersProjectsResponse,
  setClientUser,
  type User,
} from '../../stores/socketState'
const emit = defineEmits(['submitProject', 'cancel'])
const props = defineProps<{
  owner: User | undefined
  projectName: string | undefined
}>()
const error = ref(false)

function cancel() {
  emit('cancel')
}
async function deleteProject() {
  try {
    if (props.owner?.username == undefined) {
      return
    }
    if (props.owner?.password == undefined) {
      return
    }
    const response = await axios.post(BACKEND_ENDPOINT + '/delete-project', {
      name: props.projectName,
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
.dlt-btn {
  background-color: red;
  color: white;
}
</style>
