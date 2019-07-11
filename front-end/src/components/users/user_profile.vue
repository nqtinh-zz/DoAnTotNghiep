<template>
  <v-container grid-list-xl>
    <v-layout row wrap justify-center class="my-0">
      <v-flex xs12 sm12 md4 lg4 xl4>
        <div class="v-card v-sheet theme--light" style="height: 500px; ">

        </div>
      </v-flex>
      <v-flex xs12 sm12 md8 lg9 xl8>
        <div class="v-card v-sheet theme--light" style="height: 100%;">
          <v-card-text style="font-size: 16px">{{$t(`profile.edit`) }}</v-card-text>
          
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
</template>
<script>

export default {
  
};
</script>
<style>
</style>
