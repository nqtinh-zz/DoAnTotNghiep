<template>
  <v-app id="error">
      <v-container fluid fill-height>
        <v-layout align-center justify-center row>
          <div class="text-md-center">
            <h1 class="errorCode">404</h1>
            <h2 class="my-3 headline ">{{ $t(`common.link_error`) }}</h2>
            <div>
              <v-btn @click="link_to_dashboard" color="secondary">{{ $t(`common.go_to_dashboard`) }}</v-btn>
            </div>
          </div>
        </v-layout>
      </v-container>
  </v-app>
</template>

<script>
export default {
  methods:{
    link_to_dashboard(){
      this.$router.push('/home')
    }
  }
}
</script>

<style>
  .d {
    margin: 0 auto;
    width: 25% !important;
  }
  .errorCode {

    text-align: center;
    vertical-align: middle;
    font-size: 170px;
    line-height: 170px;
    font-weight: 800;
    color: #424242 ;
    text-shadow: rgba(61,61,61,.3) 1px 1px, rgba(61,61,61,.2) 2px 2px, rgba(61,61,61,.3) 3px 3px;
  }
</style>
