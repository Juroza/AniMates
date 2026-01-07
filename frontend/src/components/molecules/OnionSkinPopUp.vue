<template>
  <v-dialog v-model="open" max-width="460">
    <v-card>
      <v-card-title class="d-flex justify-space-between align-center">
        Onion Skin Settings
        <v-btn icon variant="text" @click="close">
          <v-icon icon="$close" />
        </v-btn>
      </v-card-title>

      <v-card-text>
        <v-switch v-model="enabled" label="Enable onion skin" inset />

        <v-divider class="my-3" />

        <v-row>
          <v-col cols="6">
            <v-text-field
              v-model.number="prev"
              label="Prev"
              type="number"
              :min="0"
              :max="framesBehind"
              :disabled="!enabled"
              :error="enabled && prev > framesBehind"
              :error-messages="prevError"
              @update:modelValue="userTouched = true"
              @blur="clampPrev"
            />
          </v-col>

          <v-col cols="6">
            <v-text-field
              v-model.number="next"
              label="Next"
              type="number"
              :min="0"
              :max="framesAhead"
              :disabled="!enabled"
              :error="enabled && next > framesAhead"
              :error-messages="nextError"
              @update:modelValue="userTouched = true"
              @blur="clampNext"
            />
          </v-col>
        </v-row>

        <v-divider class="my-3" />

        <!-- Opacity slider (0–100) -->
        <div class="d-flex align-center">
          <div class="mr-4" style="width: 80px">Opacity</div>

          <!-- KEY FIX: use v-model bound to a defined ref -->
          <v-slider
            v-model="opacity"
            :min="0"
            :max="100"
            :step="1"
            :disabled="!enabled"
            thumb-label
            class="flex-grow-1"
            @update:modelValue="userTouched = true"
          />

          <div class="ml-4" style="width: 50px; text-align: right">{{ opacity }}%</div>
        </div>

        <p class="text-caption text-grey mt-2">
          Available: {{ framesBehind }} behind · {{ framesAhead }} ahead
        </p>
      </v-card-text>

      <v-card-actions class="justify-end">
        <v-btn variant="text" @click="close">Cancel</v-btn>
        <v-btn color="primary" variant="elevated" :disabled="!canApply" @click="apply">
          Apply
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'

type OnionSettings = { enabled: boolean; prev: number; next: number; opacity: number }

const props = defineProps<{
  modelValue: boolean
  framesBehind: number
  framesAhead: number
  value: OnionSettings
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', v: boolean): void
  (e: 'apply', v: OnionSettings): void
}>()

const open = computed({
  get: () => props.modelValue,
  set: (v: boolean) => emit('update:modelValue', v),
})

// Local editable state (THESE MUST EXIST for slider to work)
const enabled = ref(false)
const prev = ref(0)
const next = ref(0)
const opacity = ref(100)
const userTouched = ref(false)

watch(
  () => open.value,
  (v) => {
    if (!v) return
    enabled.value = props.value.enabled
    prev.value = props.value.prev
    next.value = props.value.next
    opacity.value = props.value.opacity
    userTouched.value = false
  },
)

/**
 * If availability changes while open:
 * - untouched => snap to max (but keep saved enabled/opacity)
 * - touched   => clamp only
 */
watch(
  () => [props.framesBehind, props.framesAhead],
  () => {
    if (!open.value) return

    if (!userTouched.value) {
      // if user hasn't changed numbers, auto-max them (optional behaviour)
      prev.value = props.framesBehind
      next.value = props.framesAhead
    } else {
      clampPrev()
      clampNext()
    }
  },
)

const prevError = computed(() =>
  enabled.value && prev.value > props.framesBehind ? `Max is ${props.framesBehind}` : '',
)

const nextError = computed(() =>
  enabled.value && next.value > props.framesAhead ? `Max is ${props.framesAhead}` : '',
)

const canApply = computed(() => {
  if (!enabled.value) return true
  return prev.value <= props.framesBehind && next.value <= props.framesAhead
})

function clampPrev() {
  if (!Number.isFinite(prev.value)) prev.value = 0
  prev.value = Math.max(0, Math.min(prev.value, props.framesBehind))
}
function clampNext() {
  if (!Number.isFinite(next.value)) next.value = 0
  next.value = Math.max(0, Math.min(next.value, props.framesAhead))
}

function close() {
  open.value = false
}

function apply() {
  // Defensive: if enabled, ensure within bounds
  if (enabled.value && (prev.value > props.framesBehind || next.value > props.framesAhead)) return

  const payload: OnionSettings = {
    enabled: enabled.value,
    prev: enabled.value ? prev.value : 0,
    next: enabled.value ? next.value : 0,
    opacity: opacity.value, // always keep, even if disabled
  }

  emit('apply', payload)
  close()
}
</script>
