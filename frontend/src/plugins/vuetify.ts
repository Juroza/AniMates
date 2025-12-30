import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi-svg'
import { mdiPlus, mdiDelete, mdiPencil } from '@mdi/js'
export default createVuetify({
  icons: {
    defaultSet: 'mdi',
    aliases: {
      ...aliases,
      plus: mdiPlus,
      delete: mdiDelete,
      pencil: mdiPencil,
    },
    sets: { mdi },
  },
})
