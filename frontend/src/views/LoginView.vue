<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="auto">
        <LoginInput
          @handle-login="handleLogin"
          v-model:error="error"
          v-model:username="username"
          v-model:password="password"
          v-model:errorMessage="errorMessage"
        ></LoginInput>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import LoginInput from '../components/molecules/LoginInput.vue'
import axios from 'axios'
import { BACKEND_ENDPOINT } from '../stores/socketState'
import router from '../router'
import { useSocket, setClientUser, User, getUsersProjectsResponse } from '../stores/socketState'

const username = ref('')
const password = ref('')
const error = ref(false)
const errorMessage = ref('')

async function handleLogin() {
  try {
    const response = await axios.post(BACKEND_ENDPOINT + '/login', {
      username: username.value,
      password: password.value,
    })
    if (!response.data.result) {
      error.value = true
      errorMessage.value = response.data.msg
      console.log('rong')
    } else {
      error.value = false
      const getUsersresponse = await axios.post<getUsersProjectsResponse>(
        BACKEND_ENDPOINT + '/get-users-project',
        {
          username: username.value,
        },
      )
      console.log(getUsersresponse.data)
      setClientUser({
        id: undefined,
        username: username.value,
        password: password.value,
        myProjects: getUsersresponse.data['my-projects'],
        collabProjects: getUsersresponse.data['collab-projects'],
      })
      router.push('home')
    }
    console.log('Register response:', response.data)
  } catch (err) {
    console.error('Register failed:', err)
    error.value = true
  }
}
</script>
