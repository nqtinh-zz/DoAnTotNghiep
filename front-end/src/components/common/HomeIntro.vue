<template>
  <div>
    <Header_Intro></Header_Intro>
    <v-layout row wrap>
      <v-flex xs12>
        <v-parallax
          src
          style="background: linear-gradient(to bottom, #1867c0, #5CBBF6) "
          height="400"
        >
          <v-layout column align-center justify-center class="white--text">
            <img
              src="https://fit.uit.edu.vn/attachments/article/4644/FUJINET1.png"
              alt="Vuetify.js"
              height="100"
            ><br/>
            <h1
              class="white--text mt-2 mb-2 display-1 text-xs-center"
            >{{ $t(`intro.get_start_fcc`) }}</h1>
            <!-- <div class="subheading mb-3 text-xs-center">....</div> -->
            <router-link to="/signin">
              <v-btn style="text-decoration: none;color:white" class="blue lighten-2 mt-5" dark large >{{ $t(`intro.start`) }}</v-btn>
              <!-- class="blue lighten-2 mt-5" dark large -->
            </router-link>
          </v-layout>
        </v-parallax>
      </v-flex>

      <v-flex xs12>
        <v-layout column wrap class="my-5" align-center>
          <v-flex xs12 sm4 class="my-3">
            <div class="text-xs-center">
              <h2 class="headline">{{ $t(`intro.main_product`) }}</h2>
              <!-- <span class="subheading">
                Cras facilisis mi vitae nunc
              </span>-->
            </div>
          </v-flex>
          <v-flex xs12 sm4>
            <v-container grid-list-xl>
              <v-layout row wrap align-center>
                <v-flex xs12 sm12 md4 lg4 xl4>
                  <v-card  class="elevation-0 transparent">
                    <v-card-text class="text-xs-center">
                      <v-icon x-large class="blue--text text--lighten-2">lock_open</v-icon>
                    </v-card-text>
                    <v-card-title primary-title class="layout justify-center">
                      <div class="headline text-xs-center">{{ $t(`common.fsmart_door`) }}</div>
                    </v-card-title>
                    <v-card-text style="font-size: 16px">
                      {{ $t(`intro.intro_fsmart_door`) }}
                      <router-link to="/fsmartdoor" style="text-decoration: none;" @click.native="scrollToTop">
                        <a>{{ $t(`intro.more`) }}</a>
                      </router-link>
                    </v-card-text>
                  </v-card>
                </v-flex>
                <v-flex xs12 sm12 md4 lg4 xl4>
                  <v-card class="elevation-0 transparent">
                    <v-card-text class="text-xs-center">
                      <v-icon x-large class="blue--text text--lighten-2">notifications_none</v-icon>
                    </v-card-text>
                    <v-card-title primary-title class="layout justify-center">
                      <div class="headline text-xs-center">{{ $t(`common.fire_detect`) }}</div>
                    </v-card-title>
                    <v-card-text style="font-size: 16px">
                      {{ $t(`intro.intro_f_escape`) }}
                      <router-link to="/FSmartEscape" style="text-decoration: none;" @click.native="scrollToTop">
                        <a>{{ $t(`intro.more`) }}</a>
                      </router-link>
                    </v-card-text>
                  </v-card>
                </v-flex>
                <v-flex xs12 sm12 md4 lg4 xl4>
                  <v-card class="elevation-0 transparent">
                    <v-card-text class="text-xs-center">
                      <v-icon x-large class="blue--text text--lighten-2">transfer_within_a_station</v-icon>
                    </v-card-text>
                    <v-card-title primary-title class="layout justify-center">
                      <div class="headline text-xs-center">{{ $t(`common.people_couting`) }}</div>
                    </v-card-title>
                    <v-card-text style="font-size: 16px">
                      {{ $t(`intro.intro_people_couting`) }}
                      <router-link to="/FSmartPeopleCounting" style="text-decoration: none;" @click.native="scrollToTop">
                        <a>{{ $t(`intro.more`) }}</a>
                      </router-link>
                    </v-card-text>
                  </v-card>
                </v-flex>
                
              </v-layout>
            </v-container>
          </v-flex>
        </v-layout>
      </v-flex>

      <v-flex xs12 style="background: #F5F5F5">
        <v-container grid-list-xl>
          <v-layout row wrap justify-center class="my-5">
            <v-flex xs12 sm5>
              <v-card class="elevation-0 transparent">
                <v-card-title primary-title class="layout justify-center">
                  <div class="headline">{{ $t(`intro.company_info`) }}</div>
                </v-card-title>
                <v-card-text>
                  Công ty Cổ phần FUJINET SYSTEMS được thành lập ngày 01/10/1996, chủ yếu cung cấp máy tính cho các công ty Nhật ở Hồ Chí Minh.
                  Ngày 06/09/2000: Thành lập Công ty TNHH Mạng Máy Tính Phú Sĩ (Fujinet Co., Ltd.) chuyên phát triển phần mềm cho thị trường Nhật Bản.
                  Ngày 01/09/2015: Công ty Fujinet chuyển đổi thành Công ty Cổ phần Fujinet Systems.
                  Công ty kinh doanh các lĩnh vực: Phát triển phần mềm: Lập trình Web Application, Lập trình Smart Phone Aplication
                  Kỹ sư onsite tại Nhật: Phát triển lập trình Offshore;
                  Phần mềm đóng gói: Phát triển hệ thống ERP;
                  Tích hợp hệ thống: Thiết kế, vận hành, bảo trì hệ thống mạng;
                  Thiết kế AutoCAD: Tạo bản vẽ kiến trúc bằng 3DSMAX, tạo phối cảnh 3D
                </v-card-text>
              </v-card>
            </v-flex>
            <v-flex xs12 sm5 offset-sm1>
              <v-card class="elevation-0 transparent">
                <v-card-title primary-title class="layout justify-center">
                  <div class="headline">{{ $t(`intro.contact_us`) }}</div>
                </v-card-title>
                <v-card-text>Liên hệ với chúng tôi để cùng hợp tác và phát triển.</v-card-text>
                <v-list class="transparent">
                  <v-list-tile>
                    <v-list-tile-action>
                      <v-icon class="blue--text text--lighten-2">phone</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                      <v-list-tile-title>(84-28) 3847-7000</v-list-tile-title>
                    </v-list-tile-content>
                  </v-list-tile>
                  <v-list-tile>
                    <v-list-tile-action>
                      <v-icon class="blue--text text--lighten-2">place</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                      <v-list-tile-title>Tòa nhà Waseco, Khu B, Tầng 1, Phòng 101, số 10 Phổ Quang, Phường 2, Quận Tân Bình, Thành phố Hồ Chí Minh.</v-list-tile-title>
                    </v-list-tile-content>
                  </v-list-tile>
                  <v-list-tile>
                    <v-list-tile-action>
                      <v-icon class="blue--text text--lighten-2">email</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                      <v-list-tile-title>info@fujinet.net</v-list-tile-title>
                    </v-list-tile-content>
                  </v-list-tile>
                </v-list>
              </v-card>
            </v-flex>
          </v-layout>
        </v-container>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
import Profile from "../users/profile.vue";
import Signin from "../users/SignIn.vue";
import SelectProject from "../project/SelectProject.vue";
// import AppEvents from '../../event.js'
import Header_Intro from "./Header_Intro"
import menu from "../../api/menu.js";
export default {
  name: "HomeIntro",
  data: () => ({
    dialog: false,
    drawer: false,
    items: menu,
    snackbar: {
      show: false,
      text: "",
      color: ""
    }
  }),
  computed: {
    isLoggedIn: function() {
      console.log(this.$store.getters.isLoggedIn);
      return this.$store.getters.isLoggedIn;
    }
  },

  methods: {
    logout: function() {
      this.$store.dispatch("logout").then(() => {
        this.$router.push("/signin");
      });
    },
    scrollToTop() {
                window.scrollTo(0,0);
           }
  },
  components: {
    Profile,
    Signin,
    SelectProject,
    Header_Intro
  }
};
</script>

<style lang="scss" scoped>
// @import "./favison/css/bootstrap.css";
// @import "./favison/css/themify-icons.css";
// @import "./favison/vendors/fontawesome/css/all.min.css";
// @import "./favison/vendors/owl-carousel/owl.carousel.min.css";
// @import "./favison/vendors/animate-css/animate.css";
// @import "./favison/css/style.css";
// @import "./favison/css/responsive.css";
.v-content__wrap {
  max-width: 120%;
}
// a {  text-decoration: none;}
// .container {
//     max-width: 1500px !important;
// }
</style>

