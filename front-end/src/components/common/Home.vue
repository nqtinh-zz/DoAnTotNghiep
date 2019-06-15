<template>
  <div id="Header">
    <div>
      <v-navigation-drawer :clipped="$vuetify.breakpoint.lgAndUp" v-model="drawer" fixed floating app 
      temporary >
        <v-list>
          <!-- <router-link to="/fsmartdoor" style="text-decoration: none; color: #000;"> -->

          <v-list-group>
          <template v-slot:activator>
          <v-list-tile>
            <v-list-tile-action>
              <v-icon>fingerprint</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>{{ $t(`navDrawer.FSmartDoor`) }}</v-list-tile-content>
          </v-list-tile>
          </template>
          <div style="margin-left: 25px;">
          <router-link to="/resperson" style="text-decoration: none; color: #000;">
          <v-list-tile>
            <v-list-tile-action><v-icon>people</v-icon></v-list-tile-action>
            <v-list-tile-content>
                <v-list-tile-content>Res People</v-list-tile-content>
            </v-list-tile-content>
          </v-list-tile>
          </router-link>
          <router-link to="/rescamera" style="text-decoration: none; color: #000;">
          <v-list-tile>
            <v-list-tile-action><v-icon>camera</v-icon></v-list-tile-action>
            <v-list-tile-content>
                <v-list-tile-content>Res Camera</v-list-tile-content>
            </v-list-tile-content>
          </v-list-tile>
          </router-link>
          <router-link to="/process" style="text-decoration: none; color: #000;">
          <v-list-tile>
            <v-list-tile-action><v-icon>slow_motion_video</v-icon></v-list-tile-action>
            <v-list-tile-content>
                <v-list-tile-content>Process</v-list-tile-content>
            </v-list-tile-content>
          </v-list-tile>
          </router-link>
          </div>
          </v-list-group>

          <!-- </router-link> -->
          <router-link to="/firedetect" style="text-decoration: none; color: #000;">
          <v-list-tile>
            <v-list-tile-action>
              <v-icon>location_on</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>{{ $t(`navDrawer.FireDetect`) }}</v-list-tile-content>
          </v-list-tile>
          </router-link>
           <v-list-tile>
            <v-list-tile-action>
              <v-icon>camera</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>{{ $t(`navDrawer.PeopleCouting`) }}</v-list-tile-content>
          </v-list-tile>
          <v-list-tile>
            <v-list-tile-action>
              <v-icon>list</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>{{ $t(`navDrawer.viewStatistic`) }}</v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-navigation-drawer>
      <v-toolbar :clipped-left="$vuetify.breakpoint.lgAndUp" color="blue darken-3" dark app fixed>
        <v-toolbar-title style="width: 300px" class="ml-0 pl-3">
          <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
          <router-link style="text-decoration: none;color:white" to="/" >F.Cloud Console</router-link>

        </v-toolbar-title>

        <v-flex xs12 sm2>
          <SelectProject></SelectProject>
        </v-flex>

        &nbsp;&nbsp;&nbsp;&nbsp;
        <v-text-field
          flat
          solo-inverted
          hide-details
          prepend-inner-icon="search"
          :label="$t('toolbar.search')"
          class="hidden-sm-and-down"
        ></v-text-field>
        <v-spacer></v-spacer>
        <v-btn icon>
          <v-icon>apps</v-icon>
        </v-btn>
        <v-btn icon>
          <v-icon>notifications</v-icon>
        </v-btn>
        <langx></langx>
        <Profile></Profile>
      </v-toolbar>
    </div>
  </div>
</template>

<script>
import Profile from '../users/profile.vue'
import Signin from '../users/SignIn.vue'
import SelectProject from '../project/SelectProject.vue'
// import AppEvents from '../../event.js'
// import menu from "../../api/menu.js";
export default {
  name: 'Home',
  data: () => ({
    dropdown_edit: [
      { text: '100%' },
      { text: '75%' },
      { text: '50%' },
      { text: '25%' },
      { text: '0%' }
    ],
    dialog: false,
    drawer: false,
    // items: menu,
    snackbar: {
      show: false,
      text: '',
      color: ''
    }
  }),
  computed: {
    isLoggedIn: function () {
      return this.$store.getters.isLoggedIn
    }
  },
  methods: {
    logout: function () {
      this.$store.dispatch('logout').then(() => {
        this.$router.push('/')
      })
    }
  },
  components: {
    Profile,
    Signin,
    SelectProject
  }
}
</script>
