import { reactive, onMounted, onUnmounted } from 'vue'
import { io } from 'socket.io-client'
import router from '../router'
import { fa } from 'vuetify/locale'
type User = {
  username: string
  password: string
  id: string | undefined
}
type clientStateData = {
  connected: boolean
  clientUser: User | undefined
}
const state: clientStateData = reactive({
  connected: false,
  clientUser: undefined,
})
const URL = import.meta.env.DEV ? 'http://localhost:8080' : undefined
export const BACKEND_ENDPOINT = import.meta.env.DEV ? 'http://localhost:8080' : ''

const socket = io(URL, {
  autoConnect: true,
})
socket.on('connect', () => {
  state.connected = true
})
export function useSocket() {
  // Component-level lifecycle (optional)
  onMounted(() => {
    console.log('Socket composable mounted')
  })

  onUnmounted(() => {
    console.log('Socket composable unmounted')
  })

  function send(event: string, payload: string) {
    socket.emit(event, payload)
  }

  function on(event: string, callback: () => void) {
    socket.on(event, callback)

    onUnmounted(() => {
      socket.off(event, callback)
    })
  }

  return {
    state,
    socket,
    send,
    on,
  }
}
