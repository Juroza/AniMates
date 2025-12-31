import { reactive, onMounted, onUnmounted } from 'vue'
import { io } from 'socket.io-client'
import router from '../router'
import { fa } from 'vuetify/locale'
import axios from 'axios'
export type Project = {
  name: string
  ownerName: string
  private: boolean
  users: string[]
  width: number
  height: number
  fps: number
  datetime_created: string
  datetime_modified: string
  frameCount: number
  id: string
}
export type Frame = {
  frameNumber: number
  frameName: string
  url: string
}
export type User = {
  username: string
  password: string
  myProjects: Project[] | undefined
  collabProjects: Project[] | undefined
  id: string | undefined
}
export interface getAllUsersResponse {
  id: string
  username: string
}
export interface getImageURLbyNameResponse {
  url: string
}
export interface getUsersProjectsResponse {
  'my-projects': Project[]
  'collab-projects': Project[]
}
type clientStateData = {
  connected: boolean
  clientUser: User | undefined
  currentProject: Project | undefined
}
const state: clientStateData = reactive({
  connected: false,
  clientUser: undefined,
  currentProject: undefined,
})
const URL = import.meta.env.DEV ? 'http://localhost:8080' : undefined
export const BACKEND_ENDPOINT = import.meta.env.DEV ? 'http://localhost:8080' : ''
export async function getImageFramebyName(frame: Frame | undefined): Promise<Frame> {
  const frameName = frame?.frameName ?? 'i-guess-bro.jpg'
  const frameNumber = frame?.frameNumber ?? 1
  const response = await axios.get<getImageURLbyNameResponse>(BACKEND_ENDPOINT + '/get-frame-url', {
    params: { name: frameName },
  })
  console.log('response')
  console.log(response.statusText)
  console.log(response.data)
  return {
    frameName,
    frameNumber,
    url: response.data.url,
  }
}
const socket = io(URL, {
  autoConnect: true,
})
socket.on('connect', () => {
  state.connected = true
})
export function setClientUser(user: User) {
  if (state.clientUser) {
    Object.assign(state.clientUser, user)
  } else {
    state.clientUser = user
  }
}
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
