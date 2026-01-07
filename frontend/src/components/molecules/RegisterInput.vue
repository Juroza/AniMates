<template>
  <v-container class="input-container">
    <v-col style="gap: 40px">
      <div class="text-h4 font-weight-bold mb-8">Register</div>
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
        <v-btn class="register-btn" @click="register"> Register </v-btn>
      </v-row>
    </v-col>
  </v-container>
</template>

<script setup lang="ts">
const props = defineProps<{
  errorMessage: string
  username: string
  password: string
  error: boolean
}>()
const emit = defineEmits(['update:username', 'update:password', 'handleRegister'])
function register() {
  emit('handleRegister')
}
</script>
<style lang="css" scoped>
.input-container {
  justify-content: center;
  align-items: center;

  text-align: center;
}
.title {
  font-size: large;
  margin: 40px;
}
</style>
