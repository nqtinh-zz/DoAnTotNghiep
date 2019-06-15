<template>
  <div>
    <Home></Home>
    <v-toolbar>
      <v-toolbar-title class="ml-0 pl-4">{{ $t(`dashboard.title`) }}</v-toolbar-title>
    </v-toolbar>

    <v-container grid-list-md text-xs-center>
      <v-flex xs12 sm10 offset-sm1>
        <v-layout row wrap>
          <!-- cot 1 -->
          <v-flex>
            <v-card xs12 md3 class="grow">
              <v-card-title primary-title>
                <div>
                  <div class="headline">
                    <i class="material-icons">widgets</i>
                    {{ $t(`dashboard.info_project`) }}
                  </div>
                  <br>
                  <div style="margin-top:10px">
                    <div style="float:left;margin-left: 30px;">{{ $t(`dashboard.project_id`) }}</div>
                    <br>
                    <div
                      style="float:left;margin-left: 30px; color: rgba(0,0,0,.66)"
                    >{{project.project_id}}</div>
                  </div>
                  <br>
                  <div style="margin-top:10px">
                    <div style="float:left;margin-left: 30px">{{ $t(`dashboard.project_name`) }}</div>
                    <br>
                    <div
                      style="float:left;margin-left: 30px; color: rgba(0,0,0,.66)"
                    >{{project.project_name}}</div>
                  </div>
                  <br>
                  <div style="margin-top:10px">
                    <div style="float:left;margin-left: 30px">{{ $t(`dashboard.project_code`) }}</div>
                    <br>
                    <div
                      style="float:left;margin-left: 30px; color: rgba(0,0,0,.66)"
                    >{{project.project_code}}</div>
                  </div>
                </div>
              </v-card-title>
              <hr>
            </v-card>

            <v-card xs12 md3 class="grow" style="margin-top: 25px">
              <v-card-title primary-title>
                <div>
                  <div class="headline" style="float: left">
                    <i class="material-icons">subject</i>
                    {{ $t(`dashboard.function`) }}
                  </div>
                  <br>
                  <!-- <div style="margin-top:10px">
                    <div style="float:left;margin-left: 30px">{{ $t(`dashboard.function_name`) }}: {{ item.function_name }}</div>
                  </div>-->
                  <div style="margin-top: 20px">
                    <ul v-for="(item,index) in functions" :key="index">
                      <li style="float:left">
                        <div
                          style="float:left;margin-left: 30px"
                        >{{ $t(`dashboard.function_name`) }}: {{ item.function_name }}</div>
                      </li>
                    </ul>
                  </div>
                </div>
              </v-card-title>
            </v-card>
          </v-flex>
          <!-- cot 2 -->
          <v-flex style="margin-left:30px">
            <v-card xs12 md3 class="grow">
              <v-card-title primary-title>
                <div>
                  <div class="headline" style="float:left">
                    <i class="material-icons">perm_identity</i>
                    Hướng dẫn
                  </div>
                  <br>
                  <div style="margin-top:28px">
                    <div style="float:left;margin-left: 30px;">
                      <i class="material-icons">create</i>
                    </div>
                    <div style="float:left;margin-left: 20px; ">Khởi tạo dự án</div>
                  </div>
                  <br>
                  <div style="margin-top:18px">
                    <div style="float:left;margin-left: 30px;">
                      <i class="material-icons">account_balance</i>
                    </div>
                    <div style="float:left;margin-left: 20px; ">Đăng ký sử dụng, thanh toán ứng dụng</div>
                  </div>
                  <br>
                  <div style="margin-top:18px">
                    <div style="float:left;margin-left: 30px;">
                      <i class="material-icons">done_all</i>
                    </div>
                    <div style="float:left;margin-left: 20px; ">Demo khởi tạo và sử dụng ứng dụng</div>
                  </div>
                  <br>
                  <div style="margin-top:18px">
                    <div style="float:left;margin-left: 30px;">
                      <i class="material-icons">slow_motion_video</i>
                    </div>
                    <div style="float:left;margin-left: 20px; ">Các vấn đề thường gặp</div>
                  </div>
                  <br>
                  <div style="margin-top:18px">
                    <div style="float:left;margin-left: 30px;">
                      <i class="material-icons">perm_phone_msg</i>
                    </div>
                    <div style="float:left;margin-left: 20px; ">Liên hệ, giải đáp thắc mắc</div>
                  </div>
                </div>
              </v-card-title>
            </v-card>
          </v-flex>
          <!-- cot 3 -->
          <v-flex style="margin-left:30px">
            <v-card xs12 md3 class="grow">
              <v-card-title primary-title>
                <div>
                  <div class="headline" style="float: left">
                    <i class="material-icons">mail</i>
                    Thông báo lỗi
                  </div>
                  <br>
                  <div style="margin-top:28px">
                    <div style="float:left;margin-left: 30px;">
                      <i class="material-icons">how_to_vote</i>
                    </div>
                    <div
                      style="float:left;margin-left: 20px; "
                    >Vui lòng gửi lỗi cho chúng tôi tại đây</div>
                  </div>
                  <br>
                  <div style="margin-top:28px">
                    <div style="float:left;margin-left: 30px;">
                      <i class="material-icons">save_alt</i>
                    </div>
                    <div style="float:left;margin-left: 20px; ">Các phiên bản cập nhật</div>
                  </div>
                </div>
              </v-card-title>
            </v-card>
            <v-card xs12 md3 class="grow" style="margin-top: 25px">
              <v-card-title primary-title>
                <div>
                  <div class="headline" style="float:left">
                    <i class="material-icons">line_weight</i>
                    Tài liệu
                  </div>
                  <br>
                  <div style="margin-top:28px">
                    <!-- <div style="float:left;margin-left: 30px;">
                      <i class="material-icons">create</i>
                    </div>-->
                    <div style="float:left;margin-left: 20px; ">Tổng quan ứng dụng F.Smart Door</div>
                  </div>
                  <br>
                  <div style="margin-top:18px">
                    <!-- <div style="float:left;margin-left: 30px;">
                      <i class="material-icons">account_balance</i>
                    </div>-->
                    <div style="float:left;margin-left: 20px; ">Tổng quan ứng dụng F.Escape</div>
                  </div>
                  <br>
                  <div style="margin-top:18px">
                    <!-- <div style="float:left;margin-left: 30px;">
                      <i class="material-icons">done_all</i>
                    </div>-->
                    <div
                      style="float:left;margin-left: 20px; "
                    >Tổng quan ứng dụng F.Smart People Couting</div>
                  </div>
                  <br>
                  <div style="margin-top:18px">
                    <!-- <div style="float:left;margin-left: 30px;">
                      <i class="material-icons">slow_motion_video</i>
                    </div>-->
                    <div style="float:left;margin-left: 20px; ">Tìm hiểu về F.Cloud Console</div>
                  </div>
                  <br>
                  <div style="margin-top:18px">
                    <!-- <div style="float:left;margin-left: 30px;">
                      <i class="material-icons">perm_phone_msg</i>
                    </div>-->
                    <div
                      style="float:left;margin-left: 20px; "
                    >Tìm hiểu thêm về các ứng dụng AI thuộc Fujinet</div>
                  </div>
                </div>
              </v-card-title>
              <hr>
            </v-card>
          </v-flex>
        </v-layout>
      </v-flex>
    </v-container>
  </div>
</template>

<script>
import Home from "../common/Home.vue";
export default {
  name: "Dashboard",
  data: function() {
    return {
      project: {
        project_name: "",
        project_code: "",
        project_id: ""
      },
      functions: []
    };
  },
  created: function() {
    if (localStorage.getItem("project") !== null) {
      this.project.project_name = JSON.parse(
        localStorage.getItem("project")
      ).project_name;

      this.project.project_code = JSON.parse(
        localStorage.getItem("project")
      ).project_code;
      this.project.project_id = JSON.parse(localStorage.getItem("project_id"));
      let data = {
        project_id: this.project.project_id
      };
      this.$store
        .dispatch("get_all_function", data)
        .then(resp => {
          localStorage.setItem("all_function", JSON.stringify(resp.data.data));
          this.functions = JSON.parse(localStorage.getItem("all_function"));
        })
        .catch(err => {
          console.log(err);
        });
    }
  },

  components: {
    Home
  }
};
</script>
