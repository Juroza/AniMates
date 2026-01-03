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
export type StrokeSegment = {
  point: { x: number; y: number }
  time: number
  pressure: number
}

export type Stroke = {
  segments: StrokeSegment[]
  mode: string
  weight: number
  smoothing: number
  color?: string
  colour?: string
  adaptiveSmoothing?: boolean
  adaptiveStroke?: boolean
}
export type Frame = {
  projectName: string
  strokeRecord: Stroke[]
  frameNumber: number
  frameName: string
  url: string
}
export interface LoadFrameByNameResponse {
  projectName: string
  strokeRecord: Stroke[] | string
  frameNumber: number
  frameName: string
  url: string
}
function normalizeStrokeRecord(input: unknown): Stroke[] {
  if (!input) return []
  if (Array.isArray(input)) return input as Stroke[]
  if (typeof input === 'string') {
    try {
      const parsed = JSON.parse(input)
      return Array.isArray(parsed) ? (parsed as Stroke[]) : [parsed as Stroke]
    } catch {
      return []
    }
  }

  return [input as Stroke]
}
export function setCurrentFrame(frame: Frame | undefined) {
  state.currentFrame = frame
}

export function patchCurrentFrame(patch: Partial<Frame>) {
  if (!state.currentFrame) return
  Object.assign(state.currentFrame, patch)
}

export function setCurrentFrameStrokeRecord(strokes: Stroke[]) {
  if (!state.currentFrame) return

  state.currentFrame.strokeRecord = [...strokes]
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
      strokeRecord: [],
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
        strokeRecord: normalizeStrokeRecord(res.data.strokeRecord),
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
      strokeRecord: normalizeStrokeRecord(res.data.strokeRecord),
    }
  }
}

const socket = io(URL, {
  autoConnect: true,
  reconnection: true,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 5000,
  reconnectionAttempts: 5,
})

socket.on('connect', () => {
  state.connected = true
  console.log('Socket connected to:', URL)
})
socket.on('frameDataRetrieval', (payload: any) => {
  if (!state.currentFrame) return
  if (payload.frameName !== state.currentFrame.frameName) return

  const strokes = normalizeStrokeRecord(payload.strokeRecord)
  patchCurrentFrame({
    frameNumber: payload.frameNumber,
    projectName: payload.projectName,
  })
  setCurrentFrameStrokeRecord(strokes)
})

socket.on('drawing:action-confirmed', (payload: any) => {
  if (!state.currentFrame) return
  if (payload.frameName !== state.currentFrame.frameName) return

  if (payload.type === 'stroke' && payload.stroke) {
    state.currentFrame.strokeRecord.push(payload.stroke as Stroke)
    state.currentFrame.strokeRecord = [...state.currentFrame.strokeRecord]
  } else if (payload.type === 'clear') {
    setCurrentFrameStrokeRecord([])
  }
})

socket.on('drawing:actions-snapshot', (payload: any) => {
  if (!state.currentFrame) return
  if (payload.frameName !== state.currentFrame.frameName) return

  setCurrentFrameStrokeRecord(normalizeStrokeRecord(payload.strokeRecord))
  patchCurrentFrame({ frameNumber: payload.frameNumber })
})

socket.on('connect_error', (error) => {
  state.connected = false
  console.error('Socket connection failed:', error)
})

socket.on('disconnect', () => {
  state.connected = false
  console.log('Socket disconnected')
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
export function joinFrameSession() {
  const frameName = state.currentFrame?.frameName
  if (!frameName) return

  setCurrentFrameStrokeRecord([])

  socket.emit('joinFrame', { frameName })
  socket.emit('drawing:get-actions', { frameName })
}

export function useSocket() {
  // Component-level lifecycle (optional)
  // onMounted(() => {
  //   console.log('Socket composable mounted')
  // })

  // onUnmounted(() => {
  //   console.log('Socket composable unmounted')
  // })

  function send(event: string, payload: string) {
    socket.emit(event, payload)
  }

  function on(event: string, callback: (data: any) => void) {
    socket.on(event, callback)
    // onUnmounted(() => {
    //   socket.off(event, callback)
    // })
  }

  function off(event: string, callback: (data: any) => void) {
    socket.off(event, callback)
  }

  return {
    state,
    socket,
    send,
    on,
    off,
  }
}
