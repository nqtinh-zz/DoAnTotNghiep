<template>
  
    <v-menu offset-y origin="center center" :nudge-bottom="10" transition="scale-transition">
      <v-btn icon large flat slot="activator">
        <v-avatar v-if="this.check_avatarr===false" size="38px">
          <img
            src='../users/UserProfile/avatar.jpg'
          >
        </v-avatar>
        <v-avatar v-else size="38px">
          <v-img
            :src="avatar"
          ></v-img>
        </v-avatar>
      </v-btn>
      <v-list class="pa-0">
        <v-list-tile @click="profile">
          <v-icon>{{ $t(`icon_account.profile`) }}</v-icon>&nbsp;&nbsp;&nbsp;
          <v-list-tile-title>{{$t(`toolbar.profile`)}}</v-list-tile-title>
        </v-list-tile>
        <v-list-tile @click="change_password">
          <v-icon>{{ $t(`icon_account.change_password`) }}</v-icon>&nbsp;&nbsp;&nbsp;
          <v-list-tile-title>{{$t(`toolbar.change_password`)}}</v-list-tile-title>
        </v-list-tile>
        <v-list-tile>
          <v-icon>{{ $t(`icon_account.setting`) }}</v-icon>&nbsp;&nbsp;&nbsp;
          <v-list-tile-title>{{$t(`toolbar.setting`)}}</v-list-tile-title>
        </v-list-tile>
        
        <v-list-tile @click="logout">
          <v-icon>{{ $t(`icon_account.logout`) }}</v-icon>&nbsp;&nbsp;&nbsp;
          <v-list-tile-title>{{$t(`toolbar.logout`)}}</v-list-tile-title>
        </v-list-tile>
      </v-list>
    </v-menu>
 
</template>

<script>
export default {
  name: "Profile",
  data() {
    return {
      avatar:'',
      check_avatarr: false,
    };
  },
  created() {
    this.$store
      .dispatch("get_avatar")
      .then(resp => {
        // this.desserts = [...resp.data.data];
        console.log("get avatar dashboard ", resp.data);
        if (resp.data.code === 0) {
          this.check_avatarr = true;
          let res=resp.data.data
          let res2 = res.replace("b'", "");
          let res3 = res2.replace("'", "");
          this.avatar=res3
          //console.log(this.avatar)
        }
        else{
          this.check_avatarr = false
        }
      })
      .catch(err => {
        console.log(err);
      });
  },
  methods: {
    logout: function() {
      this.$store.dispatch("logout").then(() => {
        this.$router.push("/");
      });
    },
    profile: function() {
      this.$router.push("/profile");
    },
    change_password: function(){
      this.$router.push("/change_password")
    }
  }
};
</script>
<style scoped>
</style>
