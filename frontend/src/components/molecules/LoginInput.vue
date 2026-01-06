<template>
  <v-container class="input-container">
    <v-col style="gap: 40px">
      <div class="text-h4 font-weight-bold mb-8">Login</div>
      <v-text-field
        class="mb-4"
        label="Username"
        :model-value="props.username"
        @update:model-value="emit('update:username', $event)"
        :error="props.error"
      >
      </v-text-field>
      <v-text-field
        label="Password"
        class="mb-4"
        :model-value="props.password"
        @update:model-value="emit('update:password', $event)"
        :error="props.error"
        :error-messages="props.error ? props.errorMessage : []"
      >
      </v-text-field>
      <v-row style="gap: 90px; align-items: center; /* vertical center */ justify-content: center">
        <v-btn class="register-btn" @click="register">
          Register
          <v-icon icon="$openInNew"></v-icon>
        </v-btn>
        <v-btn class="login-btn" @click="login"> Login </v-btn></v-row
      >
    </v-col>
  </v-container>
</template>

<script setup lang="ts">
import router from '../../router'

const props = defineProps<{
  errorMessage: string
  username: string
  password: string
  error: boolean
}>()
const emit = defineEmits(['update:username', 'update:password', 'handleLogin'])
function login() {
  emit('handleLogin')
}
function register() {
  router.push('/register')
}
</script>

<style lang="css" scoped>
.input-container {
  justify-content: center;
  align-items: center;
  border: 3px solid rgb(0, 0, 0);
  border-radius: 30px;
  text-align: center;
}
.text_input {
  margin: 30px;
}
.title {
  font-size: large;
  margin: 40px;
}
</style>
