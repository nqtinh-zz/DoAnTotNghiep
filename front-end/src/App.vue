<template>
  <v-app class="back_ground">
    <v-content>
     <router-view></router-view>
    </v-content>
  </v-app>
</template>
<script>
export default {
  name: 'App',
  created: function () {
    this.$http.interceptors.response.use(undefined, function (err) {
      return new Promise(function (resolve, reject) {
        if (err.status === 401 && err.config && !err.config.__isRetryRequest) {
          this.$store.dispatch('logout')
        }
        throw err
      })
    })
  }
}
</script>
<style>
.back_ground{
  background-color: #FAFAFA!important
}
</style>

