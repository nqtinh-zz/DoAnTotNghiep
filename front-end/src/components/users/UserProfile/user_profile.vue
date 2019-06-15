<template>
<div>
    <Home></Home>
  <v-container grid-list-xl>
    <v-layout row wrap justify-center >
      <!-- <v-flex xs12 sm12 md4 lg4 xl4>
        <div class="v-card v-sheet theme--light" style="height: 700px; ">
          <UserCard></UserCard>
        </div>
      </v-flex> -->
      <v-flex xs12 sm12 md8 lg8 xl8 mt-5>
        <div class="v-card v-sheet theme--light" style="height: 100%;">
          <v-card-text style="font-size: 20px" >{{$t(`profile.edit`) }}</v-card-text>
          <EditProfileForm></EditProfileForm>
        </div>
      </v-flex>
    </v-layout>
  </v-container>
  <!-- <div class="row">
      <div class="col-xl-4 col-lg-5 col-md-6">
        <UserCard></UserCard>
        <MembersCard></MembersCard>
      </div>
      <div class="col-xl-8 col-lg-7 col-md-6">
        <EditProfileForm></EditProfileForm>
      </div>
  </div>-->
   </div>
</template>
<script>
import Home from "../../common/Home.vue";
import UserCard from "./user_card.vue";
import EditProfileForm from './edit_profile.vue'
export default {
  components: {
    Home,
    UserCard,
    EditProfileForm,
  },
};
</script>
<style>
</style>
