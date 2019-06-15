<template>
  <v-menu offset-y origin="center center" :nudge-bottom="10" transition="scale-transition">
    <v-btn icon large flat slot="activator">
     <v-icon>language</v-icon>
    </v-btn>
    <v-list class="pa-0">
      <v-toolbar card dense color="transparent">
        <v-toolbar-title><h4>{{$t(`language`)}}</h4></v-toolbar-title>
      </v-toolbar>
      <v-list-tile v-for="(item,index) in items" :key="index" @click="changeLanguage(item.lang)">
        <v-list-tile-action v-if="item.icon">
          <flag :iso="item.icon"></flag>
        </v-list-tile-action>
        <v-list-tile-content>
          <v-list-tile-title>{{ item.title }}</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
    </v-list>
  </v-menu>
</template>
<script>
import language from '@/api/language'
import {Trans} from '@/plugins/Translation'

export default {
  name: 'langx',
  data: () => ({
    items: language
  }),
  computed: {
    supportedLanguages () {
      return Trans.supportedLanguages
    },
    currentLanguage () {
      return Trans.currentLanguage
    }
  },
  methods: {
    // handleClick (value) {
    //   console.log(value)
    // },
    changeLanguage (value) {
      const lang = value
      const to = this.$router.resolve({params: {lang}})
      // console.log("lang: ", lang)
      // console.log("to: ", to)
      // console.log("to2 : ", Trans.currentLanguage)
      return Trans.changeLanguage(lang).then(() => {
        this.$router.push(to.location)
      })
    },
    isCurrentLanguage (lang) {
      return lang === this.currentLanguage
    }
  }
}
</script>
