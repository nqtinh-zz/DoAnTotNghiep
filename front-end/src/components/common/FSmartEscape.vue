<template>
  <div>
    <Header_Intro></Header_Intro>
    <section class="about-area area-padding-bottom">
      <div class="container">
        <div class="row">
          <div class="col-lg-6">
            <div class="area-heading">
              <h4>Giới thiệu </h4>

              <p style="font-size: 16px">F.Escape là hệ thống phát hiện và cảnh báo lửa sớm ở các tòa nhà cao tầng. Nó có thể thông báo đến người dùng về các tình huống khẩn cấp khi có cháy xảy ra, cũng như giám sát vị trí nạn nhân bên trong hỏa hoạn và cung cấp thông tin về hướng thoát hiểm trong tòa nhà. Ngoài ra hệ thống còn cung cấp các số liệu, thông tin về nạn nhân, tình hình hỏa hoạn liên tục cho ban quản lí để đưa ra biện pháp ứng phó đúng đắn.</p>
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
          <div class="col-lg-6">
            <div style="margin-top: 70px; margin-left: 40px">
             

 
              <video width="120%" height="120%" controls>
                <source src="./favison/img/banner/FEscape_Demo.mp4" type="video/mp4">
                
              </source>
              </video>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="feature-area area-padding bg_one">
      <div class="container">
        <div class="row align-items-center">
          <div class="offset-lg-6 col-lg-6">
            <div class="area-heading light">
              <h4>Mục đích</h4>
              <p style="font-size: 16px">F.Escape có thể được sử dụng cùng với các camera giám sát đã được lắp đặt tại các tòa nhà, chung cư, khách sạn, cửa hàng…, những nơi cần phải phát hiện sự cố do hỏa hoạn một cách nhanh nhất, để giảm thiểu sự thiệt hại. .</p>
            </div>
            <div class="row">
              <div class="col-">
                <div class="single-feature d-flex">
                  <div class="feature-icon">
                    <i class="ti-layers"></i>
                  </div>
                  <div class="single-feature-content">
                    <h5>Phát hiện và cảnh báo sớm hỏa hoạn.</h5>
                  </div>
                </div>
              </div>
              <div class="col-">
                <div class="single-feature d-flex">
                  <div class="feature-icon">
                    <i class="ti-layers"></i>
                  </div>
                  <div class="single-feature-content">
                    <h5>Cung cấp giải pháp giám sát, theo giỏi tình trạng và giải cứu nạn nhân một cách nhanh chóng.</h5>
                  </div>
                </div>
              </div>
              <div class="col-">
                <div class="single-feature d-flex">
                  <div class="feature-icon">
                    <i class="ti-layers"></i>
                  </div>
                  <div class="single-feature-content">
                    <h5>Giảm thiểu thiệt hại về người và tài sản</h5>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <section class="statics-area area-padding">
      <div class="container">
        <div class="row">
          <div class="col-lg-5">
            <div class="image-box">
              <img src="./favison/img/banner/FEscape_SysArch.png" alt>
            </div>
          </div>

          <div class="offset-lg-1 col-lg-6">
            <div class="area-heading">
              <h4>Bối cảnh sản phẩm</h4>

              <p style="font-size: 16px">F.Escape có thể được sử dụng cùng với các camera giám sát đã được lắp đặt tại các tòa nhà, chung cư, khách sạn, cửa hàng…, những nơi cần phải phát hiện sự cố do hỏa hoạn một cách nhanh nhất, để giảm thiểu sự thiệt hại. .</p>
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
import Header_Intro from "./Header_Intro"
export default {
  name: "HomeIntro",
  data: () => ({}),

  components: {
    Profile,
    Signin,
    SelectProject,
    Header_Intro
  },
  
};
</script>

<style lang="scss" scoped>
@import "./favison/css/bootstrap.css";
@import "./favison/css/themify-icons.css";
@import "./favison/vendors/fontawesome/css/all.min.css";
@import "./favison/vendors/owl-carousel/owl.carousel.min.css";
@import "./favison/vendors/animate-css/animate.css";
@import "./favison/css/style.css";
@import "./favison/css/responsive.css";
.about-area:after{
  background-image: none !important;
  position: relative !important;
}
.area-heading h4 {
    font-family: inherit !important;
}

</style>

