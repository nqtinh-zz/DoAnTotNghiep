<template>
  <v-flex xs12 sm12 md3 lg3 xl3>
    <div class="v-card v-sheet theme--light" style="margin-left:42% !important;margin-bottom:15%;height: 768px;width:95% ">
      <v-layout row>
        <v-flex xs4 sm4 md4 lg4 xl4>
          <v-card-text style="font-size: 16px">Res Group</v-card-text>
        </v-flex>
      </v-layout>
      
      <v-layout row >
        <v-flex xs7 sm7 md7 lg7 xl7>
          <v-select
            v-bind:items="listGroup"
            v-model="a1"
            :label="$t('res_camera.choose_group')"
            autocomplete
            multiple
            persistent-hint
            chips
          ></v-select>
        </v-flex>
        <v-flex xs1 sm1 md5 lg5 xl5>
          <v-btn
            style="margin-top:22px; width:90%"
            @click="search_group_camera()"
            dark
            color="primary"
          >{{$t(`res_camera.search`) }}</v-btn>
        </v-flex>
      </v-layout>
      
      <v-container id="scroll-target" class="scroll-y">
        <v-layout
          row
          wrap
          style="height: 560px;margin-top:5%; max-width:100%
            overflow:auto;"
        >
          <v-layout row wrap>
            <v-layout style="margin-left:5%" v-if="search_gr===true" row wrap>
              <v-flex xs6 sm6 md6 lg6 xl6 v-for="(item,index) in arr_search" :key="index">
                <v-btn
                  class="click_choose"
                  :style="{ backgroundColor: item.camera_group_color }"
                  style="text-transform: none !important;color:white;height:75px; width:100%"
                  @contextmenu.prevent.stop="openContext_gr_camera($event, item)"
                >{{item.camera_group_name}}</v-btn>
              </v-flex>
            </v-layout>
            <v-layout
              
              v-if="search_gr===false ||check_search===true"
              row
              wrap
            >
              <v-flex xs6 sm6 md6 lg6 xl6>
                <!-- dialog add group -->
                <v-dialog v-model="dialog_add_gr_camera" persistent max-width="600px">
                  <div v-if="dialog_add_gr_camera === true">{{check_color_gr_camera2}}</div>
                  <template v-slot:activator="{ on }">
                    <v-btn
                      style="text-transform: none !important;height:75px; color:white; width:100%"
                      dark
                      color="indigo"
                      @click="check_color_gr_camera()"
                      v-on="on"
                    >
                      <v-icon>add</v-icon>
                    </v-btn>
                  </template>
                  <v-card>
                    <v-card-title>
                      <v-layout row wrap>
                        <v-flex xs6 sm6 lg4 xl4 md4 mt-2>
                          <span style="margin-left: 20px; font-size: 20px">
                            <b>{{$t(`res_camera.add_group`) }}</b>
                          </span>
                        </v-flex>
                      </v-layout>
                    </v-card-title>
                    <v-card-text class="pa-0">
                      <v-container grid-list-md>
                        <v-form ref="form">
                          <!-- <v-layout wrap row>
                            <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                              <b>Group code</b>
                            </v-flex>
                            <v-text-field
                              xs7
                              sm7
                              label="Group code"
                              v-model="camera_group_code"
                              :error-messages="groupcodeErrors"
                              required
                              @input="$v.camera_group_code.$touch()"
                              @blur="$v.camera_group_code.$touch()"
                            ></v-text-field>&nbsp;
                            <v-flex xs1 sm1></v-flex>
                          </v-layout>-->

                          <v-layout wrap row>
                            <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                              <b>{{$t(`res_camera.group_name`) }}</b>
                            </v-flex>
                            <v-text-field
                              v-if="dialog_add_gr_camera"
                              :autofocus="'autofocus'"
                              :label="$t('res_camera.group_name')"
                              v-model="camera_group_name"
                              :error-messages="groupnameErrors"
                              required
                              @input="$v.camera_group_name.$touch()"
                              @blur="$v.camera_group_name.$touch()"
                            ></v-text-field>&nbsp;
                            <v-flex xs1 sm1></v-flex>
                          </v-layout>

                          <v-layout wrap row>
                            <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                              <b>{{$t(`res_camera.group_color`) }}</b>
                            </v-flex>
                            <v-flex xs7 sm7>
                              <v-text-field
                                type="text"
                                class="form-control"
                                v-model="colorValue"
                                @focus="showPicker_gr_camera()"
                                @input="updateFromInput_gr_camera"
                              />
                              <chrome-picker
                                :value="colors"
                                @input="updateFromPicker_gr_camera"
                                v-if="displayPicker"
                              />
                            </v-flex>

                            <v-flex xs1 sm1>
                              <span class="input-group-addon color-picker-container">
                                <span
                                  class="current-color"
                                  :style="'background-color: ' + colorValue"
                                  @click="togglePicker_gr_camera()"
                                ></span>
                              </span>
                            </v-flex>
                          </v-layout>
                        </v-form>
                      </v-container>
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                        color="blue darken-1"
                        flat
                        @click="cancel_dialog_add_gr_camera"
                      >{{$t(`res_camera.cancel`) }}</v-btn>
                      <v-btn
                        color="blue darken-1"
                        flat
                        @click="submit_group_camera"
                      >{{$t(`res_camera.ok`) }}</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
                <!-- /dialog add group -->
              </v-flex>

              <v-flex xs6 sm6 md6 lg6 xl6 v-for="(item,index) in list_group" :key="index">
                <v-btn
                  class="click_choose"
                  :style="{ backgroundColor: item.camera_group_color }"
                  style="text-transform: none !important;color:white;height:75px;width:100%"
                  @contextmenu.prevent.stop="openContext_gr_camera($event, item)"
                >{{item.camera_group_name}}</v-btn>
              </v-flex>
            </v-layout>
          </v-layout>
          <!-- dialog edit group -->
          <v-dialog v-if="check_edit===true" v-model="dialog3" persistent max-width="600px">
            <v-card>
              <v-card-title>
                <v-layout row wrap>
                  <v-flex xs6 sm6 lg4 xl4 md4 mt-2>
                    <span style="margin-left: 20px; font-size: 20px">
                      <b>{{$t(`res_camera.edit_group`) }}</b>
                    </span>
                  </v-flex>
                </v-layout>
              </v-card-title>
              <v-card-text class="pa-0">
                <v-container grid-list-md>
                  <v-form ref="form">
                    <!-- <v-layout wrap row>
                      <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                        <b>Group Code</b>
                      </v-flex>
                      <v-text-field
                        :label="{camera_group_code}"
                        v-model="camera_group_code"
                        :error-messages="groupcodeErrors"
                        required
                        @input="$v.camera_group_code.$touch()"
                        @blur="$v.camera_group_code.$touch()"
                      ></v-text-field>&nbsp;
                      <v-flex xs1 sm1></v-flex>
                    </v-layout>-->
                    <v-layout wrap row>
                      <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                        <b>{{$t(`res_camera.group_name`) }}</b>
                      </v-flex>
                      <v-text-field
                        :label="{camera_group_name}"
                        v-model="camera_group_name"
                        :error-messages="groupnameErrors"
                        required
                        @input="$v.camera_group_name.$touch()"
                        @blur="$v.camera_group_name.$touch()"
                      ></v-text-field>&nbsp;
                      <v-flex xs1 sm1></v-flex>
                    </v-layout>
                    <div v-if="edit_fail === true">
                      <v-flex
                        style="margin-left: 135px; color: red"
                      >{{$t(`res_camera.camera_code_Errors.exits`) }}</v-flex>
                    </div>
                    <v-layout wrap row>
                      <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                        <b>{{$t(`res_camera.group_color`) }}</b>
                      </v-flex>
                      <v-flex xs7 sm7>
                        <v-text-field
                          type="text"
                          class="form-control"
                          v-model="colorValue"
                          @focus="showPicker_gr_camera()"
                          @input="updateFromInput_gr_camera"
                        />
                        <chrome-picker
                          :value="colors"
                          @input="updateFromPicker_gr_camera"
                          v-if="displayPicker"
                        />
                      </v-flex>

                      <v-flex xs1 sm1>
                        <span class="input-group-addon color-picker-container">
                          <span
                            class="current-color"
                            :style="'background-color: ' + colorValue"
                            @click="togglePicker_gr_camera()"
                          ></span>
                        </span>
                      </v-flex>
                    </v-layout>
                  </v-form>
                </v-container>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  color="blue darken-1"
                  flat
                  @click="dialog3 = false , check_edit =false"
                >{{$t(`res_camera.cancel`) }}</v-btn>
                <v-btn
                  color="blue darken-1"
                  flat
                  @click="submit_edit_group_camera"
                >{{$t(`res_camera.ok`) }}</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <!-- /dialog edit group -->
          <div></div>
        </v-layout>
      </v-container>
    </div>

    <vue-simple-context-menu
      :elementId="'myFirstMenu'"
      :options="optionsArray1"
      ref="vueSimpleContextMenu1"
      @option-clicked="optionClicked1_gr_camera"
    ></vue-simple-context-menu>
  </v-flex>
</template>
<script>
import VueSimpleContextMenu from "../ResPerson/vue-simple-context-menu";
import { mapState } from "vuex";
import { VueContext } from "vue-context";
import { Chrome } from "vue-color";
import { validationMixin } from "vuelidate";
import { required, maxLength, minLength } from "vuelidate/lib/validators";
import VuetifyConfirm from "vuetify-confirm";
import Vue from "vue";
Vue.use(VuetifyConfirm, {
  buttonTrueText: "Accept",
  buttonFalseText: "Cancel",
  color: "warning",
  icon: "warning",
  title: "Delete Group",
  width: 350,
  property: "$confirm"
});
export default {
  props: ["color"],
  name: "ResGroup",
  mixins: [validationMixin],
  validations: {
    camera_group_name: {
      required,
      minLength: minLength(5),
      maxLength: maxLength(30)
    }
  },
  data() {
    return {
      optionsArray1: [
        {
          name: this.$t(`res_camera.list_camera`),
          slug: "view"
        },
        {
          name: this.$t(`res_camera.edit_group`),
          slug: "edit"
        },
        {
          name: this.$t(`res_camera.remove_group`),
          slug: "remove"
        }
      ],
      check_search: false,
      colorValue: "",
      displayPicker: false,
      arr_search: [],
      search_gr: false,
      a1: [],
      choose_item: "",
      check_edit: false,
      // dialog_add_gr_camera: false,
      dialog3: false,
      colors: {
        hex: "#FFFFFF",
        hsl: {
          h: 150,
          s: 0.5,
          l: 0.2,
          a: 1
        },
        hsv: {
          h: 150,
          s: 0.66,
          v: 0.3,
          a: 1
        },
        rgba: {
          r: 25,
          g: 77,
          b: 51,
          a: 1
        },
        a: 1
      },
      camera_group_name: "",
      // camera_group_code: "",
      project_id: "",
      camera_group_color: "",
      search: "",
      edit_fail: false
    };
  },
  mounted() {
    this.setColor_gr_camera(this.color || "#000000");
  },
  created: function() {
    this.$store
      .dispatch("get_all_camera_group", {
        project_id: JSON.parse(localStorage.getItem("project_id"))
      })
      .then(resp => {})
      .catch(err => {
        console.log(err);
      });
  },
  computed: mapState({
    dialog_add_gr_camera: state => state.res_group_camera.dialog_add_gr_camera,
    list_group: state => state.res_group_camera.list_group_camera,
    color_listGroup() {
      var color_listGroup = [];
      for (
        let i = 0;
        i < this.$store.state.res_group_camera.list_group_camera.length;
        i++
      ) {
        color_listGroup.push(
          this.$store.state.res_group_camera.list_group_camera[i]
            .camera_group_color
        );
      }
      return color_listGroup;
    },
    listGroup() {
      var listGroup = [];
      for (
        let i = 0;
        i < this.$store.state.res_group_camera.list_group_camera.length;
        i++
      ) {
        listGroup.push(
          this.$store.state.res_group_camera.list_group_camera[i]
            .camera_group_name
        );
      }
      return listGroup;
    },
    groupnameErrors() {
      const errors = [];
      if (!this.$v.camera_group_name.$dirty) return errors;
      !this.$v.camera_group_name.maxLength &&
        errors.push(this.$t(`res_camera.camera_code_Errors.most`));
      !this.$v.camera_group_name.minLength &&
        errors.push(this.$t(`res_camera.camera_code_Errors.least`));
      !this.$v.camera_group_name.required &&
        errors.push(this.$t(`res_camera.camera_code_Errors.required`));
      return errors;
    },
    // groupcodeErrors() {
    //   const errors = [];
    //   if (!this.$v.camera_group_code.$dirty) return errors;
    //   !this.$v.camera_group_code.minLength &&
    //     errors.push("Goup name must be at least 2 characters long");
    //   !this.$v.camera_group_code.maxLength &&
    //     errors.push("Group code must be at most 8 characters long");
    //   !this.$v.camera_group_code.required &&
    //     errors.push("Group code is required.");
    //   return errors;
    // },
    check_color_gr_camera2() {
      let letters = "0123456789ABCDEF";
      let temp_color = "#";
      for (var i = 0; i < 6; i++) {
        temp_color += letters[Math.floor(Math.random() * 16)];
      }
      console.log(this.color_listGroup);
      for (let i = 0; i < this.color_listGroup.length; i++) {
        if (
          temp_color === this.color_listGroup[i] ||
          temp_color === "#FFFFFF"
        ) {
          let letters = "0123456789ABCDEF";
          let temp_color = "#";
          for (var i = 0; i < 6; i++) {
            temp_color += letters[Math.floor(Math.random() * 16)];
          }
          console.log(temp_color);
        }
      }
      this.setColor_gr_camera(temp_color);
      this.displayPicker = false;
      // this.camera_group_code = "";
      this.camera_group_name = "";
      return "";
    }
  }),
  components: {
    "chrome-picker": Chrome,
    VueContext,
    "vue-simple-context-menu": VueSimpleContextMenu
  },
  watch: {
    colorValue(val) {
      if (val) {
        this.updateColors_gr_camera(val);
        this.$emit("input", val);
        //document.body.style.background = val;
      }
    }
  },
  methods: {
    cancel_dialog_add_gr_camera() {
      this.$store.state.res_group_camera.dialog_add_gr_camera = false;
      this.$v.$reset();
    },
    optionClicked1_gr_camera(event) {
      console.log(event);
      if (event.option.slug === "view") {
        console.log("test view", event.item.camera_group_id);
        let data={
          group_id: event.item.camera_group_id,
          project_id: JSON.parse(localStorage.getItem("project_id"))
        }
        this.$store
          .dispatch("camera_group_list_camera", data)
          .then(resp => {
            //reload lai person
            
          });
      }
      if (event.option.slug === "edit")
        this.edit_group_camera(
          event.item.camera_group_id,
          // event.item.camera_group_code,
          event.item.camera_group_name,

          event.item.camera_group_color
        );
      if (event.option.slug === "remove")
        this.remove_group_camera(
          event.item.camera_group_id,
          event.item.camera_group_name,
          // event.item.camera_group_code,
          event.item.camera_group_color
        );
    },
    openContext_gr_camera(event, item) {
      this.$refs.vueSimpleContextMenu1.showMenu(event, item);
      console.log(item);
    },
    check_color_gr_camera() {
      this.$store.state.res_group_camera.dialog_add_gr_camera = true;
      let letters = "0123456789ABCDEF";
      let temp_color = "#";
      for (var i = 0; i < 6; i++) {
        temp_color += letters[Math.floor(Math.random() * 16)];
      }
      console.log(this.color_listGroup);
      for (let i = 0; i < this.color_listGroup.length; i++) {
        if (
          temp_color === this.color_listGroup[i] ||
          temp_color === "#FFFFFF"
        ) {
          let letters = "0123456789ABCDEF";
          let temp_color = "#";
          for (var i = 0; i < 6; i++) {
            temp_color += letters[Math.floor(Math.random() * 16)];
          }
          console.log(temp_color);
        }
      }
      this.setColor_gr_camera(temp_color);
      this.displayPicker = false;
      // this.camera_group_code = "";
      this.camera_group_name = "";
    },
    setColor_gr_camera(color) {
      this.updateColors_gr_camera(color);
      this.colorValue = color;
    },
    updateColors_gr_camera(color) {
      if (color.slice(0, 1) == "#") {
        this.colors = {
          hex: color
        };
      } else if (color.slice(0, 4) == "rgba") {
        var rgba = color.replace(/^rgba?\(|\s+|\)$/g, "").split(","),
          hex =
            "#" +
            (
              (1 << 24) +
              (parseInt(rgba[0]) << 16) +
              (parseInt(rgba[1]) << 8) +
              parseInt(rgba[2])
            )
              .toString(16)
              .slice(1);
        this.colors = {
          hex: hex,
          a: rgba[3]
        };
      }
    },
    showPicker_gr_camera() {
      document.addEventListener("click", this.documentClick_gr_camera);
      this.displayPicker = true;
    },
    hidePicker_gr_camera() {
      document.removeEventListener("click", this.documentClick_gr_camera);
      this.displayPicker = false;
    },
    togglePicker_gr_camera() {
      this.displayPicker
        ? this.hidePicker_gr_camera()
        : this.showPicker_gr_camera();
    },
    updateFromInput_gr_camera() {
      this.updateColors_gr_camera(this.colorValue);
    },
    updateFromPicker_gr_camera(color) {
      this.colors = color;
      if (color.rgba.a == 1) {
        this.colorValue = color.hex;
      } else {
        this.colorValue =
          "rgba(" +
          color.rgba.r +
          ", " +
          color.rgba.g +
          ", " +
          color.rgba.b +
          ", " +
          color.rgba.a +
          ")";
      }
    },
    documentClick_gr_camera(e) {
      var el = this.$refs.colorpicker,
        target = e.target;
      if (el !== target || !el.contains(target)) {
        this.hidePicker_gr_camera();
      }
    },
    submit_group_camera() {
      this.$v.$touch();
      if (this.$v.$pending || this.$v.$error) return null;
      else {
        console.log(this.colors.hex);
        this.$store
          .dispatch("add_group_camera", {
            project_id: JSON.parse(localStorage.getItem("project_id")),
            // camera_group_code: this.camera_group_code.trim(),
            camera_group_name: this.camera_group_name.trim(),
            camera_group_color: this.colors.hex
          })
          .then(resp => {
            console.log(resp.data);
            this.$store.state.res_group_camera.dialog_add_gr_camera = false;
            this.a1 = [];
            this.arr_search = [];
            this.camera_group_name = "";
            // this.camera_group_code = "";
          })
          .catch(err => {
            console.log(err);
          });
      }
      this.$v.$reset();
    },
    remove_group_camera(id, name, color) {
      let data = {
        choose_group_id: id,
        choose_group_name: name,
        choose_group_color: color
      };

      let data2 = {
        camera_group_id: id,
        project_id: localStorage.getItem("project_id")
      };

      const index = this.list_group.indexOf(localStorage.getItem("group_id"));
      this.$confirm("Are you sure you want to delete this group?").then(res => {
        if (res === true) {
          this.$store.dispatch("del_group_camera", data2).then(resp => {
            //reload lai person
            if (resp.data.code === 0) {
              let data_reload = {
                project_id: JSON.parse(localStorage.getItem("project_id"))
              };
              this.$store
                .dispatch("reload_list_camera", data_reload)
                .then(resp2 => {
                  console.log("reload thanh cong: ", resp2);
                })
                .catch(err2 => {
                  console.log(err2);
                });
            }
            console.log(resp.data);
            console.log("xong");
          });
        }
      });
    },
    edit_group_camera(id, name, color) {
      let data = {
        choose_group_id: id,

        choose_group_name: name,
        choose_group_color: color
      };
      this.edit_fail = false;
      console.log(this.check_edit);
      this.check_edit = true;
      this.dialog3 = true;
      this.$store.dispatch("choose_group", data).then(resp => {
        (this.camera_group_name = this.$store.state.res_group.choose_group.choose_group_name),
          this.setColor_gr_camera(
            this.$store.state.res_group.choose_group.choose_group_color
          );
      });
    },
    submit_edit_group_camera() {
      this.$v.$touch();
      if (this.$v.$pending || this.$v.$error) return null;
      else {
        this.$store
          .dispatch("update_camera_group", {
            project_id: localStorage.getItem("project_id"),
            camera_group_id: this.$store.state.res_group.choose_group
              .choose_group_id,
            camera_group_name: this.camera_group_name.trim(),

            camera_group_color: this.colors.hex
          })
          .then(resp => {
            //reload person
            if (resp.data.code === 0) {
              this.check_search = true;
              this.a1 = [];
              this.arr_search = [];
              this.camera_group_name = "";
              let data_reload = {
                project_id: JSON.parse(localStorage.getItem("project_id"))
              };
              this.dialog3 = false;
              this.edit_fail = false;
              this.check_edit = false;
              console.log("ttttttttttttttttttttttttt");
              this.$store
                .dispatch("reload_list_camera", data_reload)
                .then(resp2 => {
                  console.log("reload thanh cong: ", resp2);
                })
                .catch(err2 => {
                  console.log(err2);
                });
            } else {
              this.edit_fail = true;
              console.log("update error");
              this.dialog3 = true;
              this.check_edit = true;
            }
          })
          .catch(err => {
            console.log(err);
          });
      }
    },
    search_group_camera() {
      this.arr_search = [];
      this.search_gr = true;
      if (this.a1.length !== 0) {
        this.check_search = false;
        console.log("aaaa");
        for (let i = 0; i < this.a1.length; i++) {
          for (let j = 0; j < this.list_group.length; j++) {
            if (this.list_group[j].camera_group_name === this.a1[i]) {
              this.arr_search.push(this.list_group[j]);
            }
          }
        }
      } else {
        this.check_search = true;
      }
    }
  }
};
</script>
<style>
.current-color {
  display: inline-block;
  width: 16px;
  height: 16px;
  background-color: #000;
  cursor: pointer;
  margin-top: 75%;
}
</style>


