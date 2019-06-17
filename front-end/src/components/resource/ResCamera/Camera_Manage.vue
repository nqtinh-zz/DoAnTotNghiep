<template>
  <div style="margin-top:2%;width:90%">
    <v-layout row wrap justify-center class="my-0">
      <v-flex xs12 sm12 md9 lg9 xl9>
        <div style="margin-left:3%; width:110%">
        <v-card height="100%">
          <v-card-title style="font-size: 16px">
            Res Camera
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              append-icon="search"
              label="Search"
              single-line
              hide-details
            ></v-text-field>
          </v-card-title>
          <!-- dialog add camera to group -->
          <v-dialog v-model="dialog4" persistent max-width="500px">
            <template v-slot:activator="{ on }"></template>
            <v-card>
              <v-card-title>
                <v-layout row wrap>
                  <v-flex xs12 sm12 mt-2>
                    <span style="margin-left: 10px; font-size: 20px">
                      <b>{{$t(`res_camera.add_camera_to_group`) }}</b>
                    </span>
                  </v-flex>
                </v-layout>
              </v-card-title>

              <v-card-text class="pa-0">
                <v-container grid-list-md>
                  <!-- <div style="font-size: 16px">{{ $t(`project.all_project`) }}</div> -->
                  <!-- @submit.prevent="add_person_to_group" -->
                  <v-form ref="form" @submit.prevent="add_camera_to_group()">
                    <v-layout wrap row>
                      <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                        <b>{{$t(`res_camera.group`) }}</b>
                      </v-flex>
                      <v-flex xs8 sm8 md8 lg8 xl8>
                        <v-select
                          v-bind:items="group_of_camera"
                          v-model="arr_group_camera"
                          :label="$t('res_camera.choose_group')"
                          multiple
                          chips
                          Enables
                          autofocus
                          persistent-hint
                        >
                          <template v-slot:prepend-item>
                            <v-list-tile ripple @click="New_Group_On_Add_Person_To_Group">
                              <v-list-tile-action>
                                <!-- <v-icon :color="selectedFruits.length > 0 ? 'indigo darken-4' : ''">{{ icon }}</v-icon> -->
                              </v-list-tile-action>
                              <v-list-tile-content>
                                <v-list-tile-title>{{$t(`res_camera.new_group`) }}</v-list-tile-title>
                              </v-list-tile-content>
                            </v-list-tile>
                            <v-divider class="mt-2"></v-divider>
                          </template>
                        </v-select>
                      </v-flex>
                    </v-layout>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                        color="blue darken-1"
                        flat
                        @click="close_add_camera_to_group"
                        style="font-size: 16px"
                      >{{$t(`res_camera.cancel`) }}</v-btn>
                      <v-btn
                        color="blue darken-1"
                        flat
                        type="submit"
                        style="font-size: 16px; margin-right: 5px"
                      >{{$t(`res_camera.ok`) }}</v-btn>
                    </v-card-actions>
                  </v-form>
                </v-container>
              </v-card-text>
            </v-card>
          </v-dialog>
          <v-dialog v-model="dialog_selection" persistent max-width="500px">
            <Selection></Selection>
            <v-card>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  color="blue darken-1"
                  flat
                  @click="dialog_selection = false"
                >{{$t(`res_camera.cancel`) }}</v-btn>
                <v-btn color="blue darken-1" flat @click="open">{{$t(`res_camera.submit`) }}</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>

          <!-- /dialog add camera to group -->
          <!-- dialog edit camera -->
          <v-dialog v-model="dialog_edit_camera" persistent max-width="580px">
            <v-card>
              <v-card-title>
                <v-layout row wrap>
                  <v-flex xs6 sm6 lg4 xl4 md4 mt-2>
                    <span style="margin-left: 20px; font-size: 20px">
                      <b>{{$t(`res_camera.edit_camera`) }}</b>
                    </span>
                  </v-flex>
                </v-layout>
              </v-card-title>

              <v-card-text class="pa-0">
                <v-container grid-list-md>
                  <!-- <div style="font-size: 16px">{{ $t(`project.all_project`) }}</div> -->
                  <v-form ref="form" @submit.prevent="edit_camera">
                    <v-layout wrap row>
                      <v-flex xs3 sm3 pt-4 style="margin-left: 20px;font-size: 17px">
                        <b>{{$t(`res_camera.camera_name`) }}</b>
                      </v-flex>
                      <v-text-field
                        xs7
                        sm7
                        :label="$t('res_camera.enter_camera_name')"
                        v-model="camera_name_edit"
                        :error-messages="PersonCodeErrors"
                        required
                        @input="$v.camera_name_edit.$touch()"
                        @blur="$v.camera_name_edit.$touch()"
                      ></v-text-field>&nbsp;
                      <v-flex xs1 sm1></v-flex>
                    </v-layout>
                    <v-layout wrap row>
                      <v-flex xs3 sm3 pt-4 style="margin-left: 20px; font-size: 17px">
                        <b>Stream URL</b>
                      </v-flex>
                      <v-text-field
                        xs7
                        sm7
                        :label="$t('res_camera.enter_stream_url')"
                        v-model="stream_url_edit"
                        required
                      ></v-text-field>&nbsp;
                      <v-flex xs1 sm1></v-flex>
                    </v-layout>
                    <v-layout wrap row>
                      <div v-if="check_edit === true">
                        <v-flex style="margin-left: 15px; color: red">Camera name đã tồn tại</v-flex>
                      </div>
                    </v-layout>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                        color="blue darken-1"
                        flat
                        @click="close_dialog_edit"
                        style="font-size: 16px"
                      >{{$t(`res_camera.cancel`) }}</v-btn>
                      <v-btn
                        color="blue darken-1"
                        flat
                        type="submit"
                        style="font-size: 16px; margin-right: 5px"
                      >{{$t(`res_camera.ok`) }}</v-btn>
                    </v-card-actions>
                  </v-form>
                </v-container>
              </v-card-text>
            </v-card>
          </v-dialog>
          <!-- /dialog edit person -->
          <!-- diaglog view camare-->
          <v-dialog v-model="dialog_view_camera" max-width="1000px">
            <v-card>
              <v-card-title>
                <v-layout row wrap>
                  <v-flex xs6 sm6 lg4 xl4 md4 mt-2>
                    <span style="margin-left: 20px; font-size: 20px">
                      <b>View Camera</b>
                    </span>
                  </v-flex>
                </v-layout>
              </v-card-title>

              <v-card-text class="pa-0">
                <v-container grid-list-md>
                  <!-- <div style="font-size: 16px">{{ $t(`project.all_project`) }}</div> -->
                  <div>
                    <div style="margin-left: 80px; margin-bottom: 15px">
                      <div v-if="check_one_camera === false" style="color: red;text-align: center">Camera không hoạt động vui lòng kiểm tra lại</div>
                      <!-- <div v-if="check_one_camera === true" >
                        <div style="text-align: center">Loading</div>
                      </div> -->
                      <img v-bind:src="src_stream" alt="laichim" width="800px">
                    </div>
                  </div>
                  <v-form ref="form">
                    <v-layout wrap row>
                      <v-flex xs3 sm3 pt-4 style="margin-left: 20px;font-size: 17px">
                        <b>{{$t(`res_camera.camera_name`) }}</b>
                      </v-flex>
                      <v-text-field
                        xs7
                        sm7
                        :label="$t('res_camera.enter_camera_name')"
                        v-model="camera_name_edit"
                        :error-messages="PersonCodeErrors"
                        required
                        @input="$v.camera_name_edit.$touch()"
                        @blur="$v.camera_name_edit.$touch()"
                        readonly
                      ></v-text-field>&nbsp;
                      <v-flex xs1 sm1></v-flex>
                    </v-layout>
                    <v-layout wrap row>
                      <v-flex xs3 sm3 pt-4 style="margin-left: 20px; font-size: 17px">
                        <b>Stream URL</b>
                      </v-flex>
                      <v-text-field
                        xs7
                        sm7
                        :label="$t('res_camera.enter_stream_url')"
                        v-model="stream_url_edit"
                        required
                        readonly
                      ></v-text-field>&nbsp;
                      <v-flex xs1 sm1></v-flex>
                    </v-layout>
                    <v-layout wrap row>
                      <div v-if="check_edit === true">
                        <v-flex style="margin-left: 15px; color: red">Camera name đã tồn tại</v-flex>
                      </div>
                    </v-layout>
                  </v-form>
                </v-container>
              </v-card-text>
            </v-card>
          </v-dialog>
          <!-- / dialog view camera-->
          <v-data-table
            :headers="headers"
            :items="desserts"
            :search="search"
            :pagination.sync="pagination"
          >
            <template v-slot:items="props">
              <td style="font-size: 15px">{{ props.item.camera_name }}</td>
              <tr style="border-bottom: none;">
                <div style="float: left; margin-top: 2px;">
                  <v-btn
                    fab
                    small
                    dark
                    color="#1565C0"
                    style="text-transform: none !important; width: 28px ; height: 28px;"
                    @click="getGroup_ofCamera(props.item)"
                  >
                    <v-icon>add</v-icon>
                  </v-btn>
                </div>
                <div
                  style="float: left; margin-top: 2px;text-transform: uppercase;"
                  v-for="(group,index1) in props.item.group"
                  :key="index1"
                >
                  <v-chip
                    :style="{ backgroundColor: group.camera_group_color}"
                    text-color="white"
                    close
                    @input="onClose(group,props.item)"
                  >{{group.camera_group_name}}</v-chip>
                </div>
              </tr>
              <td>{{ props.item.stream_url }}</td>
              <td>
                <span>
                  <v-switch
                    value
                    input-value="true"
                    color="#3177C7"
                    hide-details
                    @change="choose_selection($event)"
                  ></v-switch>
                </span>
              </td>

              <td>
                <span v-if="props.item.status === false" class="v-stepper__step__step red">
                  <i class="material-icons"></i>
                </span>
                <span v-if="props.item.status === 1" class="v-stepper__step__step grey">
                  <i class="material-icons"></i>
                </span>
                <span v-if="props.item.status === true" class="v-stepper__step__step success">
                  <i class="material-icons"></i>
                </span>
              </td>
              <!-- <td><span class="v-stepper__step__step success"><i class="material-icons"></i></span></td> -->
              <td class="text-xs-right">
                <v-icon small @click="view_data_camera(props.item)">search</v-icon>&nbsp;
                <v-icon small @click="data_edit_camera(props.item)">edit</v-icon>&nbsp;
                <v-icon @click="deleteItem(props.item)" small>delete</v-icon>
              </td>
            </template>
          </v-data-table>
          <div v-if="this.check_button===false" class="text-xs-right mr-4">
            <!-- <label class="custom-file-upload" style="color: white; background: #3177C7">
              IMPORT
              <input
                type="file"
                id="id_folder"
                @change="uploadFolder"
                style="width: 100px"
                webkitdirectory
                directory
                multiple
              >
            </label>-->
            &nbsp;&nbsp;
            <div>
              
              <!-- <div v-if="process_check_status === true" style="float: left">
                <v-progress-circular indeterminate color="primary"></v-progress-circular>
              </div> -->
              <span v-if="process_check_status === true"><v-progress-circular indeterminate color="primary"></v-progress-circular></span>
              <v-btn color="success" @click="check_status()">{{$t(`res_camera.check_status`) }}</v-btn>
              <AddCamera></AddCamera>
            </div>
          </div>
        </v-card>
        </div>
      </v-flex>
      <!-- <v-flex xs12 sm12 md3 lg3 xl3>
         group camera asdfsa df
      </v-flex>-->
      <GroupCamera></GroupCamera>
    </v-layout>
  </div>
</template>

<script>
import { forEach } from "lodash";
// import ResGroup from "./ResGroup";
import ViewCamera from "./View_Camera";
import AddCamera from "./Add_Camera";
import GroupCamera from "./Group_Camera";
import VueUploadMultipleImage from "vue-upload-multiple-image";
import { validationMixin } from "vuelidate";
import { required, maxLength, minLength } from "vuelidate/lib/validators";
import VuetifyConfirm from "vuetify-confirm";
import Selection from "./Selection";
import HTTP_API from "@/api/config.js"
import Vue from "vue";
Vue.use(VuetifyConfirm, {
  buttonTrueText: "Accept",
  buttonFalseText: "Cancel",
  color: "warning",
  icon: "warning",
  title: "Delete Person",
  width: 350,
  property: "$confirm"
});
export default {
  mixins: [validationMixin],
  validations: {
    camera_name_edit: {
      required,
      maxLength: maxLength(30),
      minLength: minLength(2)
    }
  },
  data() {
    return {
      check_one_camera: true,
      process_check_status: false,
      dialog_view_camera: false,
      check_edit: false,
      selection: "",
      dialog_selection: false,
      check_button: false,
      display: "none",
      search: "",
      dialog4: false,
      //cua dialog edit camera
      dialog_edit_camera: false,
      camera_id_edit: "",
      camera_name_edit: "",
      stream_url_edit: "",
      valid: false,
      add_fail: false,
      // /cua dialog edit camera
      arr_group_camera: [],
      camera_id: "",
      pagination: {
        rowsPerPage: 10
      },
      valid: false,
      src_stream: "",
      headers: [
        {
          text: "Camera name",
          align: "left",
          width: "250px",
          value: "camera_name",
          sortable: false
        },
        { text: "Group", value: "people_group_code", sortable: false },
        {
          text: "Stream url",
          value: "stream_url",
          sortable: false,
          width: "200px"
        },
        {
          text: "Selection",
          value: "selection",
          sortable: false,
          width: "100px"
        },
        { text: "Status", value: "status", sortable: false, width: "100px" },
        { text: "Action", value: "action", sortable: false, width: "120px" }
      ]
      // desserts: []
    };
  },
  created: function() {
    this.$store
      .dispatch("get_all_camera", {
        project_id: JSON.parse(localStorage.getItem("project_id"))
      })
      .then(resp => {
        // this.desserts = [...resp.data.data];
        console.log("get all camera: ", resp.data.data);
      })
      .catch(err => {
        console.log(err);
      });
  },
  computed: {
    PersonCodeErrors() {
      const errors = [];
      if (!this.$v.camera_name_edit.$dirty) return errors;
      !this.$v.camera_name_edit.required &&
        errors.push(this.$t(`res_camera.camera_code_Errors.required`));
      // this.fail_create === "code_fail" && errors.push("Code already exits");
      // for (let i = 0; i < this.camera_name_edit.length; i++) {
      //   if (this.camera_name_edit[i] === " ")
      //     errors.push(this.$t(`res_camera.camera_code_Errors.check_space`));
      // }
      !this.$v.camera_name_edit.maxLength &&
        errors.push(this.$t(`res_camera.camera_code_Errors.most`));
      !this.$v.camera_name_edit.minLength &&
        errors.push(this.$t(`res_camera.camera_code_Errors.least`));
      return errors;
    },
    desserts() {
      return this.$store.getters.ListCamera;
    },
    group_of_camera() {
      return this.$store.getters.GroupOfCamera;
    }
  },
  components: {
    AddCamera,
    GroupCamera,
    VueUploadMultipleImage,
    Selection,
    ViewCamera
  },
  methods: {
    check_status() {
      this.process_check_status = true;
      let data = {
        project_id: JSON.parse(localStorage.getItem("project_id"))
      };
      console.log("lksadl lsajdf lksdaf", data);
      this.$store
        .dispatch("check_status", data)
        .then(resp => {
          console.log(resp);
          // console.log("aldkf day ne` 3")
          this.process_check_status = false;
        })
        .catch(err => {
          console.log(err);
        });
    },
    New_Group_On_Add_Person_To_Group() {
      (this.dialog4 = false),
        (this.arr_group_camera = []),
        (this.$store.state.res_group_camera.dialog_add_gr_camera = true);
    },
    choose_selection(event) {
      console.log("nguyen tien trien");
      console.log(`${event}`);
      this.selection = event;
      if (event === false) {
        this.dialog_selection = true;
      }
      console.log(this.selection);
    },
    deleteItem: function(item) {
      const index = this.desserts.indexOf(item);
      let data = {
        camera_id: item.camera_id,
        project_id: JSON.parse(localStorage.getItem("project_id"))
      };
      this.$confirm("Are you sure you want to delete this camera?", {
        title: "Delete Camera"
      }).then(res => {
        if (res === true) {
          this.desserts.splice(index, 1) &&
            this.$store.dispatch("delete_camera", data).then(resp => {});
        }
      });
      // confirm("Are you sure you want to delete this person?") &&
      //   this.desserts.splice(index, 1) &&
      //   this.$store.dispatch("delete_person", data).then(resp => {
      //     console.log(resp);
      //     // location.reload();
      //   });
    },
    getGroup_ofCamera: function(item) {
      this.dialog4 = true;
      // console.log("get group of person: ", item);
      this.camera_id = item.camera_id;
      this.$store
        .dispatch("get_group_of_camera", item)
        .then(resp => {
          console.log(resp);
        })
        .catch(err => {
          console.log(err);
        });
    },
    add_camera_to_group: function(item) {
      // console.log("thoibodi: ",item)
      let data = {
        camera_id: this.camera_id,
        group_arr: this.arr_group_camera,
        project_id: JSON.parse(localStorage.getItem("project_id"))
      };
      console.log("add_person_to_group: ", data);
      this.$store
        .dispatch("add_camera_to_group", data)
        .then(resp => {
          console.log("sau khi add group thanh cong: ", resp);
          if (resp.data.code === 0) {
            this.arr_group_camera = [];
            this.camera_id = "";
            this.dialog4 = false;
          }
          if (resp.data.code === -1) {
            // console.log('áldfksldflfd')
            this.dialog4 = true;
          }
        })
        .catch(err => {
          console.log(err);
        });
    },
    close_add_camera_to_group() {
      (this.dialog4 = false), (this.arr_group_camera = []);
    },
    onClose: function(group, item) {
      console.log("group: ", group);
      console.log("item: ", item);
      let data = {
        camera_group_id: group.camera_group_id,
        camera_id: item.camera_id,
        project_id: group.project_id_id
      };
      this.$confirm("Are you sure you want to delete this group ?", {
        title: "delete group of person"
      }).then(res => {
        if (res === true) {
          this.$store
            .dispatch("delete_one_group_camera", data)
            .then(resp => {
              console.log(resp);
            })
            .catch(err => {
              console.log(err);
            });
        }
      });
    },
    view_data_camera: function(item) {
      this.check_one_camera = true
      let data = item.stream_url;
      // console.log("item ne:", item)
      this.$store
        .dispatch("check_one_status", item.camera_id)
        .then(resp => {
          console.log("ldh", resp)
          if(resp.data.data === false)
          {
            this.check_one_camera = false
          }
          else {
            this.check_one_camera = true
          }
        })
        .catch(err => {
          console.log(err);
        });
      this.src_stream =
        `${HTTP_API}/api/v/project/resources/live-stream?stream_url=` +
        data;
      console.log("alo alo", this.src_stream);
      // console.log("nguyen chi trung 1", item);
      // this.$store
      //   .dispatch("view_camera_url", data)
      //   .then(resp => {
      //     console.log(resp);
      //   })
      //   .catch(err => {
      //     console.log(err);
      //   });
      this.dialog_view_camera = true;
      this.camera_name_edit = item.camera_name;
      this.camera_id_edit = item.camera_id;
      this.stream_url_edit = item.stream_url;
    },
    //edit camera
    data_edit_camera: function(item) {
      this.dialog_edit_camera = true;
      this.camera_name_edit = item.camera_name;
      this.camera_id_edit = item.camera_id;
      this.stream_url_edit = item.stream_url;
    },
    edit_camera() {
      this.$v.$touch();
      if (this.$v.$pending || this.$v.$error) return null;
      else {
        var data = {
          camera_name: this.camera_name_edit,
          stream_url: this.stream_url_edit,
          project_id: JSON.parse(localStorage.getItem("project_id")),
          camera_id: this.camera_id_edit
        };
        // console.log("data_images: ", this.data_images);
        // console.log("edit person", data);
        this.$store
          .dispatch("edit_camera", data)
          .then(resp => {
            console.log("nguye ntien aldkf", resp.data);
            if (resp.data.code === 0) {
              this.dialog_edit_camera = false;
              this.camera_name_edit = "";
              this.stream_url_edit = "";
              this.camera_id_edit = "";
              this.check_edit = false;
            }
            if (resp.data.code === -1) {
              // console.log('áldfksldflfd')
              // this.dialog_edit_camera = false;
              this.check_edit = true;
            }
          })
          .catch(err => {
            console.log("loi", err);
          });
        // console.log("type data images: ",this.images)
      }
      // this.$v.$reset()
    },
    close_dialog_edit() {
      this.dialog_edit_camera = false;
      this.images_edit = [];
      this.person_code_edit = "";
      this.data_images = [];
      this.person_id_edit = "";
      this.check_edit = false;
    }

    // /edit person
  }
};
</script>
<style>
#id_folder {
  display: none;
}
.modal-mask {
  display: none !important;
}
.image-overlay-details {
  position: unset !important;
}
.image-icon-edit[data-v-10e59822] {
  display: none !important;
}
.mark-text-primary {
  display: none !important;
}
.image-overlay {
  background: none !important;
}
.image-icon-info {
  width: 0px !important;
}
.image-primary {
  font-size: 0px !important;
  width: 0px !important;
  background-color: white !important;
}
.custom-file-upload {
  display: inline-block;
  line-height: 2.2em;
  padding: 0 0.62em;
  border: 0px solid #666;
  border-radius: 0.25em;

  box-shadow: inset 0 0 0.1em #fff, 0.2em 0.2em 0.2em rgba(0, 0, 0, 0.1);
  font-family: arial, sans-serif;
  font-size: 1.1em;
}
.css_btn_ntt {
  border-radius: 0.25em;
  font-family: arial, sans-serif;
}
</style>

