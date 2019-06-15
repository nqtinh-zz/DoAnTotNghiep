<template>
  
</template>
<script>
import JSMpeg from 'jsmpeg-player'
export default {
  props: {
    stream_url: {
      type: String,
      default: null
    },
    channel_id: {
      type: Number,
      default: null
    }
  },
  data () {
    return {
      player: null,
      video: {},
      canvas: {}
    }
  },
  watch: {
    stream_url (val) {
      console.log('camera showing update url', val)
      if (this.player) {
        console.log('*****Đang có player chạy')
        this.player.destroy()
      }
      this.player = new JSMpeg.Player(val, { canvas: this.video, preserveDrawingBuffer: true })
    }
  },
  updated () {
    console.log('***** update video')
  },
  created () {
    console.log('***** created video')
  },
  mounted () {
    console.log('***** mounted video')
    if (this.stream_url) {
      console.log('mounted video')
      this.video = this.$refs.videoWrapper
      this.player = new JSMpeg.Player(this.stream_url, { canvas: this.video, preserveDrawingBuffer: true })
      console.log(this.player)
      this.player.play()
      console.log('play video')
    }
  },
  destroyed () {
    if (this.player) {
      this.player.destroy()
      console.log('camera showing destroy', this.stream_url)
    }
  },
  methods: {}
}
</script>
<style lang="scss">
    .camera-channel{
        background-color: lightgrey;
        width: 100%;
  }
</style>
