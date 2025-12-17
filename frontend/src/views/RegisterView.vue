<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="auto">
        <RegisterInput
          @handle-register="handleRegister"
          v-model:error="error"
          v-model:username="username"
          v-model:password="password"
          v-model:errorMessage="errorMessage"
        ></RegisterInput>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'

import RegisterInput from '../components/molecules/RegisterInput.vue'
import axios from 'axios'
import { BACKEND_ENDPOINT } from '../stores/socketState'
import router from '../router'

const username = ref('')
const password = ref('')
const error = ref(false)
const errorMessage = ref('')

async function handleRegister() {
  try {
    const response = await axios.post(BACKEND_ENDPOINT + '/register', {
      username: username.value,
      password: password.value,
    })
    if (!response.data.result) {
      error.value = true
      errorMessage.value = response.data.msg
      console.log('rong')
    } else {
      error.value = false
      router.push('home')
    }
    console.log('Register response:', response.data)
  } catch (err) {
    console.error('Register failed:', err)
    error.value = true
  }
}
</script>
