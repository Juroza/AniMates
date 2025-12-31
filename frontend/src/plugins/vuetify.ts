import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi-svg'
import { mdiPlus, mdiDelete, mdiPencil, mdiChevronRight, mdiChevronLeft } from '@mdi/js'
export default createVuetify({
  icons: {
    defaultSet: 'mdi',
    aliases: {
      ...aliases,
      plus: mdiPlus,
      delete: mdiDelete,
      pencil: mdiPencil,
      right: mdiChevronRight,
      left: mdiChevronLeft,
    },
    sets: { mdi },
  },
})
