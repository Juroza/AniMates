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
  frames: string[]
}
export type Frame = {
  projectName: string
  strokeRecord: string
  frameNumber: number
  frameName: string
  url: string
}
export interface LoadFrameByNameResponse {
  projectName: string
  strokeRecord: string
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
  currentFrame: Frame | undefined
}
const state: clientStateData = reactive({
  connected: false,
  clientUser: undefined,
  currentProject: undefined,
  currentFrame: undefined,
})
const URL = import.meta.env.DEV ? 'http://localhost:8080' : undefined
export const BACKEND_ENDPOINT = import.meta.env.DEV ? 'http://localhost:8080' : ''
export async function getImageFramebyName(frameNameIn: string | undefined): Promise<Frame> {
  const frameName = frameNameIn ?? 'i-guess-bro.jpg'
  if (!frameNameIn) {
    const response = await axios.get<getImageURLbyNameResponse>(
      BACKEND_ENDPOINT + '/get-frame-url',
      {
        params: { name: frameName },
      },
    )
    console.log('response')
    console.log(response.statusText)
    console.log(response.data)
    return {
      frameName: frameName ?? '',
      frameNumber: 1,
      url: response.data.url,
      strokeRecord: '',
      projectName: state.currentProject?.name ?? '',
    }
  } else {
    const res = await axios.get<LoadFrameByNameResponse>(BACKEND_ENDPOINT + '/load-frame', {
      params: { name: frameName },
    })

    if (res.data.strokeRecord.length == 0) {
      const response = await axios.get<getImageURLbyNameResponse>(
        BACKEND_ENDPOINT + '/get-frame-url',
        {
          params: { name: 'free-frame.png' },
        },
      )

      return {
        frameName: frameName ?? '',
        frameNumber: res.data.frameNumber,
        url: response.data.url,
        projectName: res.data.projectName,
        strokeRecord: res.data.strokeRecord,
      }
    }
    const response2 = await axios.get<getImageURLbyNameResponse>(
      BACKEND_ENDPOINT + '/get-frame-url',
      {
        params: { name: frameName },
      },
    )

    return {
      frameName: frameName ?? '',
      frameNumber: res.data.frameNumber,
      url: response2.data.url,
      projectName: res.data.projectName,
      strokeRecord: res.data.strokeRecord,
    }
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
export function setCurrentProject(project: Project | undefined) {
  state.currentProject = project
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
