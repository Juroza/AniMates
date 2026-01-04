// =========================== socketState.ts (native WebSockets) ===========================
import { reactive } from 'vue'
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

const URL_HTTP = import.meta.env.DEV ? 'http://localhost:8080' : undefined
export const BACKEND_ENDPOINT = import.meta.env.DEV ? 'http://localhost:8080' : ''

// For WebSocket URL:
const WS_URL = import.meta.env.DEV
  ? 'ws://localhost:8080' // if you set wss path like /ws then: ws://localhost:8080/ws
  : (() => {
      // in production, derive ws(s) from current page
      const proto = location.protocol === 'https:' ? 'wss:' : 'ws:'
      return `${proto}//${location.host}`
    })()

// -------------------- Minimal event-emitter wrapper over WebSocket --------------------
type Handler = (data: any) => void
const handlers: Record<string, Set<Handler>> = {}

function on(event: string, cb: Handler) {
  if (!handlers[event]) handlers[event] = new Set()
  handlers[event].add(cb)
}
function off(event: string, cb: Handler) {
  handlers[event]?.delete(cb)
}

function emitLocal(event: string, data: any) {
  for (const cb of handlers[event] ?? []) cb(data)
}

// reconnect settings (similar to your socket.io config)
const reconnect = {
  enabled: true,
  delay: 1000,
  maxDelay: 5000,
  attempts: 5,
}

let ws: WebSocket | null = null
let attempt = 0
let manuallyClosed = false

function connect() {
  manuallyClosed = false
  ws = new WebSocket(WS_URL)

  ws.onopen = () => {
    state.connected = true
    attempt = 0
    console.log('WS connected to:', WS_URL)

    // If you want: auto re-join current frame after reconnect
    if (state.currentFrame?.frameName) {
      joinFrameSession()
    }
  }

  ws.onmessage = (evt: MessageEvent) => {
    // All server messages are JSON { event, data }
    try {
      const msg = JSON.parse(typeof evt.data === 'string' ? evt.data : '')
      const { event, data } = msg || {}
      if (!event) return
      emitLocal(event, data)
    } catch (e) {
      // ignore bad messages
    }
  }

  ws.onerror = (err) => {
    console.error('WS error:', err)
  }

  ws.onclose = () => {
    state.connected = false
    console.log('WS disconnected')

    if (!reconnect.enabled || manuallyClosed) return
    if (attempt >= reconnect.attempts) return

    attempt++
    const backoff = Math.min(reconnect.delay * attempt, reconnect.maxDelay)
    window.setTimeout(() => connect(), backoff)
  }
}

connect()

function send(event: string, data: any) {
  if (!ws || ws.readyState !== WebSocket.OPEN) return
  ws.send(JSON.stringify({ event, data }))
}

// -------------------- Your existing REST helper (unchanged) --------------------
export async function getImageFramebyName(frameNameIn: string | undefined): Promise<Frame> {
  const frameName = frameNameIn ?? 'i-guess-bro.jpg'
  if (!frameNameIn) {
    const response = await axios.get<getImageURLbyNameResponse>(
      BACKEND_ENDPOINT + '/get-frame-url',
      {
        params: { name: frameName },
      },
    )
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

    if ((res.data.strokeRecord as any)?.length == 0) {
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

// -------------------- WS event handlers to match your old socket.io ones --------------------
on('frameDataRetrieval', (payload: any) => {
  if (!state.currentFrame) return
  if (payload.frameName !== state.currentFrame.frameName) return

  const strokes = normalizeStrokeRecord(payload.strokeRecord)
  patchCurrentFrame({
    frameNumber: payload.frameNumber,
    projectName: payload.projectName,
  })
  setCurrentFrameStrokeRecord(strokes)
})

on('drawing:action-confirmed', (payload: any) => {
  if (!state.currentFrame) return
  if (payload.frameName !== state.currentFrame.frameName) return

  if (payload.type === 'stroke' && payload.stroke) {
    state.currentFrame.strokeRecord.push(payload.stroke as Stroke)
    state.currentFrame.strokeRecord = [...state.currentFrame.strokeRecord]
  } else if (payload.type === 'clear') {
    setCurrentFrameStrokeRecord([])
  }
})

on('drawing:actions-snapshot', (payload: any) => {
  if (!state.currentFrame) return
  if (payload.frameName !== state.currentFrame.frameName) return

  setCurrentFrameStrokeRecord(normalizeStrokeRecord(payload.strokeRecord))
  patchCurrentFrame({ frameNumber: payload.frameNumber })
})

// -------------------- exposed API (like your composable) --------------------
export function setClientUser(user: User) {
  if (state.clientUser) Object.assign(state.clientUser, user)
  else state.clientUser = user
}

export function setCurrentProject(project: Project | undefined) {
  state.currentProject = project
}

export function joinFrameSession() {
  const frameName = state.currentFrame?.frameName
  if (!frameName) return

  setCurrentFrameStrokeRecord([])

  send('joinFrame', { frameName })
  send('drawing:get-actions', { frameName })
}

export function useSocket() {
  return {
    state,

    // keep the same surface area as before
    socket: {
      // compat layer for your existing calls in components:
      emit: (event: string, data?: any) => send(event, data),
      on: (event: string, cb: Handler) => on(event, cb),
      off: (event: string, cb: Handler) => off(event, cb),
      disconnect: () => {
        manuallyClosed = true
        ws?.close()
      },
      get readyState() {
        return ws?.readyState
      },
    },

    send: (event: string, payload: any) => send(event, payload),
    on,
    off,
  }
}
