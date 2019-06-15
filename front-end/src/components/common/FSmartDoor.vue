<template>
  <div>
    <v-toolbar :clipped-left="$vuetify.breakpoint.lgAndUp" color="blue darken-3" dark app fixed>
      <v-toolbar-title style="width: 300px" class="ml-0 pl-3">
        <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
        <a style="text-decoration: none;color:white" href="/">F.Cloud Console</a>
      </v-toolbar-title>&nbsp;&nbsp;&nbsp;&nbsp;
      <v-text-field
        flat
        solo-inverted
        hide-details
        prepend-inner-icon="search"
        :label="$t('toolbar.search')"
        class="hidden-sm-and-down"
      ></v-text-field>
      <v-spacer></v-spacer>
      <langx></langx>
      <a href="/signup">
        <v-btn color="primary" style="width:120px">{{$t(`toolbar.register`)}}</v-btn>
      </a>
      <a href="/signin">
        <v-btn color="primary" style="width:120px">{{$t(`toolbar.login`)}}</v-btn>
      </a>
    </v-toolbar>
    <section class="about-area area-padding-bottom">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-lg-6">
            <div class="area-heading">
              <h4>Giới thiệu</h4>
              

              <p style="font-size: 16px">
                Hiện nay, công nghệ trí thông minh nhân tạo (A.I.) phát triển rất mạnh mẽ, và đang trở nên ngày càng hữu dụng. Hơn nữa, nhờ vào sự phát triển của một số mô hình A.I., mà ta có thể áp dụng công nghệ A.I. này trên nhiều lĩnh vực như kinh tế, giao thông, xây dựng, tài chính…
                Đặc biệt, với những kĩ thuật mới, công nghệ mới, và nguồn dữ liệu về hình ảnh rất dồi dào, công nghệ Deep Learning (một phần nhỏ của A.I.) đang là một trong những xu thế dẫn đầu hiện nay. Chính vì thế, bằng cách sử dụng những kĩ thuật, công nghệ mới này, chúng tôi đã phát triển một hệ thống nhận diện danh tính của người dùng, thông qua hình ảnh ghi được từ camera giám sát.
              </p>
            </div>
            <!-- <div class="row">
              <div class="col-md-6 col-lg-6">
                <div class="single-about">
                  <div class="about-icon">
                    <i class="ti-thought"></i>
                  </div>
                  <div class="single-about-content">
                    <h5>Cloud Compatibility</h5>
                    <p>There earth face earth behold. She stars made void two given and also our own grass days. Greater</p>
                  </div>
                </div>
              </div>
              <div class="col-md-6 col-lg-6">
                <div class="single-about">
                  <div class="about-icon">
                    <i class="ti-truck"></i>
                  </div>
                  <div class="single-about-content">
                    <h5>On Time Delivery</h5>
                    <p>There earth face earth behold. She stars made void two given and also our own grass days. Greater</p>
                  </div>
                </div>
              </div>
            </div> -->
          </div>
        </div>
      </div>
    </section>

    <section class="feature-area area-padding bg_one">
      <div class="container">
        <div class="row align-items-center">
          <div class="offset-lg-6 col-lg-6">
            <div class="area-heading light">
              <h4>
                Mục đích
              </h4>
              <p style="font-size: 16px">F.SmartDoor là một hệ thống hỗ trợ cho phép vào cửa dựa vào danh tính của nhân viên bằng công nghệ nhận diện khuôn mặt. Qua đó, nó có thể giúp việc chấm công, quản lý người ra vào cửa được thực hiện thuận tiện và dễ dàng. </p>
            </div>
            <!-- <div class="row">
              <div class="col-">
                <div class="single-feature d-flex">
                  <div class="feature-icon">
                    <i class="ti-layers"></i>
                  </div>
                  <div class="single-feature-content">
                    <h5>Add New Project</h5>
                    <p>There earth face earth behold. She stars made void two given and also our own grass days. Greater</p>
                  </div>
                </div>
              </div>
              <div class="col-">
                <div class="single-feature d-flex">
                  <div class="feature-icon">
                    <i class="ti-layers"></i>
                  </div>
                  <div class="single-feature-content">
                    <h5>Generating Leads</h5>
                    <p>There earth face earth behold. She stars made void two given and also our own grass days. Greater</p>
                  </div>
                </div>
              </div>
            </div> -->
          </div>
        </div>
      </div>
    </section>
    <section class="statics-area area-padding">
      <div class="container">
        <div class="row">
          <div class="col-lg-5">
            <div class="image-box">
              <img src="./favison/img/banner/FSmartDoor_SysArch.png" alt>
            </div>
          </div>

          <div class="offset-lg-1 col-lg-6">
            <div class="area-heading">
              <h4>
                Bối cảnh sản phẩm
              </h4>
              

              <p style="font-size: 16px">F.SmartDoor là hệ thống sẽ giúp cho các công việc như chấm công, giám sát nhân viên trở nên nhanh chóng và hiệu quả hơn. Ngoài ra, F.Smart Door còn hỗ trợ cho khách vãng lai liên hệ với người quản lý thông qua gọi video call.</p>
            </div>
            <div class="single-data">
              <i class="ti-paint-bucket"></i>
              <p style="font-size: 16px">Đăng kí thông tin nhận diện cho nhân viên</p>
            </div>
            <div class="single-data">
              <i class="ti-check-box"></i>
              <p style="font-size: 16px">Nhận diện, hiển thị thông tin của nhân viên.</p>
            </div>
            <div class="single-data">
              <i class="ti-ruler-pencil"></i>
              <p style="font-size: 16px">Ghi nhận thời gian ra, vào của nhân viên</p>
            </div>
            <div class="single-data">
              <i class="ti-ruler-pencil"></i>
              <p style="font-size: 16px">Cho phép khách vãng lai liên hệ với người quản lý thông qua video call</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import Profile from "../users/profile.vue";
import Signin from "../users/SignIn.vue";
import SelectProject from "../project/SelectProject.vue";
// import AppEvents from '../../event.js'
import menu from "../../api/menu.js";
export default {
  name: "HomeIntro",
  data: () => ({}),

  components: {
    Profile,
    Signin,
    SelectProject
  }
};
</script>

<style lang="css">
@import "./favison/css/bootstrap.css";
@import "./favison/css/themify-icons.css";
@import "./favison/vendors/fontawesome/css/all.min.css";
@import "./favison/vendors/owl-carousel/owl.carousel.min.css";
@import "./favison/vendors/animate-css/animate.css";
@import "./favison/css/style.css";
@import "./favison/css/responsive.css";
.about-area:after{
  background-image: url(./favison/img/banner/FSmartDoor_OpStep_FaceRecognition.png) !important;
}
.feature-area:after{
  background-image: url(./favison/img/banner/FSmartDoor_OpStep_FaceRegistration.png) !important;
  width: 50%;
  height:100%;
}
.area-heading h4 {
    font-family: inherit !important;
}

</style>

