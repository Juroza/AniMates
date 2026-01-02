import { socket } from '@/plugins/socket'
import DrawingCanvas from '@/components/DrawingCanvas.vue'
const { onMounted, onUnmounted } from 'vue'

const projectId = 'placeholder-project-id' // Replace with actual project ID logic

onMounted(() => {
  socket.connect()
  socket.emit('join-room', projectId)
})

onUnmounted(() => {
  socket.emit('leave-room', projectId)
  socket.disconnect()
})