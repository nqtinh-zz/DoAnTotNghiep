<template>
  <v-flex xs12 sm12 md3 lg3 xl3>
    <div class="v-card v-sheet theme--light" style="margin-left:42% !important;margin-bottom:15%;height: 100%;width:95% ">
      <v-layout row>
        <v-flex xs4 sm4 md4 lg4 xl4>
          <v-card-text style="font-size: 16px">Res Group</v-card-text>
        </v-flex>
      </v-layout>
      <v-layout row justify-center>
        <v-flex xs7 sm7 md7 lg7 xl7>
          <v-select
            v-bind:items="listGroup"
            v-model="a1_group_person"
            :label="$t('res_person.choose_group')"
            autocomplete
            persistent-hint
            multiple
            chips
          ></v-select>
        </v-flex>
        <v-flex xs3 sm3 md3 lg3 xl3>
          <v-btn
            style="margin-top:22px"
            @click="search_group()"
            dark
            color="primary"
          >{{$t(`res_person.search`) }}</v-btn>
        </v-flex>
      </v-layout>
      <v-container id="scroll-target" class="scroll-y">
        <v-layout
          row
          wrap
          style="height: 625px;margin-top:5%; max-width:100%
            overflow:auto;"
        >
          <v-layout row wrap>
            <v-layout  v-if="search_gr===true" row wrap>
              <v-flex xs6 sm6 md6 lg6 xl6 v-for="(item,index) in arr_search" :key="index">
                <v-btn
                  class="click_choose"
                  :style="{ backgroundColor: item.people_group_color }"
                  style=" text-transform: none !important;color:white;height:75px; width:100%"
                  @contextmenu.prevent.stop="openContext($event, item)"
                >{{item.people_group_code}}</v-btn>
              
              </v-flex>
            </v-layout>
            <v-layout
              
              v-if="search_gr===false ||check_search===true"
              row
              wrap
            >
              <v-flex xs6 sm6 md6 lg6 xl6>
                <v-dialog v-model="dialog2" persistent max-width="600px">
                  <div v-if="dialog2 === true">{{check_color2}}</div>
                  <template v-slot:activator="{ on }">
                    <v-btn
                      style=" text-transform: none !important;height:75px; color:white; width:100%"
                      dark
                      color="indigo"
                      @click="check_color()"
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
                            <b>{{$t(`res_person.add_group`) }}</b>
                          </span>
                        </v-flex>
                      </v-layout>
                    </v-card-title>
                    <v-card-text class="pa-0">
                      <v-container grid-list-md>
                        <v-form ref="form">
                          <v-layout wrap row>
                            <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                              <b>{{$t(`res_person.group_code`) }}</b>
                            </v-flex>
                            <v-text-field
                              xs7
                              sm7
                              :label="$t('res_person.group_code')"
                              autofocus
                              v-if="dialog2"
                              v-model="people_group_code"
                              :error-messages="groupcodeErrors"
                              required
                              @input="$v.people_group_code.$touch()"
                              @blur="$v.people_group_code.$touch()"
                            ></v-text-field>&nbsp;
                            <v-flex xs1 sm1></v-flex>
                          </v-layout>

                          <v-layout wrap row>
                            <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                              <b>{{$t(`res_person.group_name`) }}</b>
                            </v-flex>
                            <v-text-field
                              :label="$t('res_person.group_name')"
                              v-model="people_group_name"
                              :error-messages="groupnameErrors"
                              required
                              @input="$v.people_group_name.$touch()"
                              @blur="$v.people_group_name.$touch()"
                            ></v-text-field>&nbsp;
                            <v-flex xs1 sm1></v-flex>
                          </v-layout>

                          <v-layout wrap row>
                            <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                              <b>{{$t(`res_person.group_color`) }}</b>
                            </v-flex>
                            <v-flex xs7 sm7>
                              <v-text-field
                                type="text"
                                class="form-control"
                                v-model="colorValue"
                                @focus="showPicker()"
                                @input="updateFromInput"
                              />
                              <chrome-picker
                                :value="colors"
                                @input="updateFromPicker"
                                v-if="displayPicker"
                              />
                            </v-flex>

                            <v-flex xs1 sm1>
                              <span class="input-group-addon color-picker-container">
                                <span
                                  class="current-color"
                                  :style="'background-color: ' + colorValue"
                                  @click="togglePicker()"
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
                        @click="cancel_dialog2"
                      >{{$t(`res_person.cancel`) }}</v-btn>
                      <v-btn
                        color="blue darken-1"
                        flat
                        @click="submit_group"
                      >{{$t(`res_person.ok`) }}</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-flex>

              <v-flex xs6 sm6 md6 lg6 xl6 v-for="(item,index) in list_group" :key="index">
                <v-btn
                  class="click_choose"
                  :style="{ backgroundColor: item.people_group_color }"
                  style=" text-transform: none !important;color:white;height:75px;width:100%"
                  @contextmenu.prevent.stop="openContext($event, item)"
                >{{item.people_group_code}}</v-btn>
              </v-flex>
            </v-layout>
          </v-layout>
          <v-dialog v-if="check_edit===true" v-model="dialog3" persistent max-width="600px">
            <v-card>
              <v-card-title>
                <v-layout row wrap>
                  <v-flex xs6 sm6 lg4 xl4 md4 mt-2>
                    <span style="margin-left: 20px; font-size: 20px">
                      <b>{{$t(`res_person.edit_group`) }}</b>
                    </span>
                  </v-flex>
                </v-layout>
              </v-card-title>
              <v-card-text class="pa-0">
                <v-container grid-list-md>
                  <v-form ref="form">
                    <v-layout wrap row>
                      <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                        <b>{{$t(`res_person.group_code`) }}</b>
                      </v-flex>
                      <v-text-field
                        :label="{people_group_name}"
                        v-model="people_group_code"
                        :error-messages="groupcodeErrors"
                        required
                        @input="$v.people_group_code.$touch()"
                        @blur="$v.people_group_code.$touch()"
                      ></v-text-field>&nbsp;
                      <v-flex xs1 sm1></v-flex>
                    </v-layout>
                    <div v-if="edit_fail === true">
                        <v-flex
                          style="margin-left: 135px; color: red"
                        > Group code đã tồn tại, vui lòng nhập lại.</v-flex>
                      </div>
                    <v-layout wrap row>
                      <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                        <b>{{$t(`res_person.group_name`) }}</b>
                      </v-flex>
                      <v-text-field
                        :label="{people_group_code}"
                        v-model="people_group_name"
                        :error-messages="groupnameErrors"
                        required
                        @input="$v.people_group_name.$touch()"
                        @blur="$v.people_group_name.$touch()"
                      ></v-text-field>&nbsp;
                      <v-flex xs1 sm1></v-flex>
                    </v-layout>
                    <v-layout wrap row>
                      <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                        <b>{{$t(`res_person.group_color`) }}</b>
                      </v-flex>
                      <v-flex xs7 sm7>
                        <v-text-field
                          type="text"
                          class="form-control"
                          v-model="colorValue"
                          @focus="showPicker()"
                          @input="updateFromInput"
                        />
                        <chrome-picker
                          :value="colors"
                          @input="updateFromPicker"
                          v-if="displayPicker"
                        />
                      </v-flex>

                      <v-flex xs1 sm1>
                        <span class="input-group-addon color-picker-container">
                          <span
                            class="current-color"
                            :style="'background-color: ' + colorValue"
                            @click="togglePicker()"
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
                >{{$t(`res_person.cancel`) }}</v-btn>
                <v-btn
                  color="blue darken-1"
                  flat
                  @click="submit_edit_group"
                >{{$t(`res_person.ok`) }}</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <div></div>
        </v-layout>
      </v-container>
    </div>

    <vue-simple-context-menu
      :elementId="'myFirstMenu'"
      :options="optionsArray1"
      ref="vueSimpleContextMenu1"
      @option-clicked="optionClicked1"
    ></vue-simple-context-menu>
  </v-flex>
</template>
<script>
import VueSimpleContextMenu from "./vue-simple-context-menu";
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
    people_group_code: {
      required,
      minLength: minLength(2),
      maxLength: maxLength(8)
    },
    people_group_name: {
      required,
      minLength: minLength(5),
      maxLength: maxLength(30)
    }
  },
  // name: 'group_person',
  data() {
    return {
      optionsArray1: [
        {
          name: this.$t(`res_person.edit_group`),
          slug: "edit"
        },
        {
          name: this.$t(`res_person.remove_group`),
          slug: "remove"
        }
      ],
      check_search: false,
      colorValue: "",
      displayPicker: false,
      arr_search: [],
      search_gr: false,
      a1_group_person: [],
      choose_item: "",
      check_edit: false,
      // dialog2: false,
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
      people_group_name: "",
      people_group_code: "",
      project_id: "",
      people_group_color: "",
      search: "",
      edit_fail:false
    };
  },
  mounted() {
    // EventBus.$on('EVENT_NAME', function (payLoad) {
    //   console.log("event-bus")
    //   console.log(dialog2)
    //   // this.open_dialog_add()
    // });

    this.setColor(this.color || "#000000");
  },
  created: function() {
    this.$store
      .dispatch("get_all_people_group", {
        project_id: JSON.parse(localStorage.getItem("project_id"))
      })
      .then(resp => {
        console.log("hi");
      })
      .catch(err => {
        console.log(err);
      });
  },
  computed: mapState({
    dialog2: state => state.res_group.dialog2,
    list_group: state => state.res_group.listGroup,
    color_listGroup() {
      var color_listGroup = [];
      for (let i = 0; i < this.$store.state.res_group.listGroup.length; i++) {
        color_listGroup.push(
          this.$store.state.res_group.listGroup[i].people_group_color
        );
      }
      return color_listGroup;
    },
    listGroup() {
      var listGroup = [];
      for (let i = 0; i < this.$store.state.res_group.listGroup.length; i++) {
        listGroup.push(
          this.$store.state.res_group.listGroup[i].people_group_code
        );
      }
      return listGroup;
    },
    groupnameErrors() {
      const errors = [];
      if (!this.$v.people_group_name.$dirty) return errors;
      !this.$v.people_group_name.maxLength &&
        errors.push("Name must be at most 30 characters long");
      !this.$v.people_group_name.minLength &&
        errors.push("Goup name must be at least 5 characters long");
      !this.$v.people_group_name.required && errors.push("Name is required.");
      return errors;
    },
    groupcodeErrors() {
      const errors = [];
      if (!this.$v.people_group_code.$dirty) return errors;
      !this.$v.people_group_code.minLength &&
        errors.push("Goup name must be at least 2 characters long");
      !this.$v.people_group_code.maxLength &&
        errors.push("Group code must be at most 8 characters long");
      !this.$v.people_group_code.required &&
        errors.push("Group code is required.");
      return errors;
    },
    check_color2() {
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
      this.setColor(temp_color);
      this.displayPicker = false;
      this.people_group_name = "";
      this.people_group_code = "";
      this.$router.push({ path: "resperson", query: { addperson: "private" } });
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
        this.updateColors(val);
        this.$emit("input", val);
        //document.body.style.background = val;
      }
    }
  },
  methods: {
    cancel_dialog2() {
      console.log("da toi day");
      this.$store.state.res_group.dialog2 = false;
      this.$v.$reset();
    },
    optionClicked1(event) {
      console.log(event);
      if (event.option.slug === "edit")
        this.edit_group(
          event.item.people_group_id,
          event.item.people_group_code,
          event.item.people_group_name,
          event.item.people_group_color
        );
      if (event.option.slug === "remove")
        this.remove_group(
          event.item.people_group_id,
          event.item.people_group_code,
          event.item.people_group_name,
          event.item.people_group_color
        );
    },
    openContext(event, item) {
      this.$refs.vueSimpleContextMenu1.showMenu(event, item);
      console.log(item);
    },
    check_color() {
      this.$store.state.res_group.dialog2 = true;
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
      this.setColor(temp_color);
      this.displayPicker = false;
      this.people_group_name = "";
      this.people_group_code = "";
      this.$router.push({ path: "resperson", query: { addperson: "private" } });
      return "abc";
    },
    setColor(color) {
      this.updateColors(color);
      this.colorValue = color;
    },
    updateColors(color) {
      if (color.slice(0, 1) === "#") {
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
    showPicker() {
      document.addEventListener("click", this.documentClick);
      this.displayPicker = true;
    },
    hidePicker() {
      document.removeEventListener("click", this.documentClick);
      this.displayPicker = false;
    },
    togglePicker() {
      this.displayPicker ? this.hidePicker() : this.showPicker();
    },
    updateFromInput() {
      this.updateColors(this.colorValue);
    },
    updateFromPicker(color) {
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
    // test01 () {
    //   console.log("Nguyen Neirt")
    //   EventBus.$emit('EVENT_NAME', payLoad);
    // },
    documentClick(e) {
      var el = this.$refs.colorpicker,
        target = e.target;
      if (el !== target || !el.contains(target)) {
        this.hidePicker();
      }
    },
    submit_group() {
      this.$v.$touch();
      if (this.$v.$pending || this.$v.$error) return null;
      else {
        console.log(this.colors.hex);
        this.$store
          .dispatch("add_group", {
            project_id: JSON.parse(localStorage.getItem("project_id")),
            people_group_name: this.people_group_name.trim(),
            people_group_code: this.people_group_code.trim(),
            people_group_color: this.colors.hex
          })
          .then(resp => {
            console.log(resp.data);
            this.$store.state.res_group.dialog2 = false;
          })
          .catch(err => {
            console.log(err);
          });
      }
      this.$v.$reset();
    },
    remove_group(id, code, name, color) {
      let data = {
        choose_group_id: id,
        choose_group_code: code,
        choose_group_name: name,
        choose_group_color: color
      };
      this.$store.dispatch("choose_group", data).then(resp1 => {
        let data2 = {
          people_group_id: this.$store.state.res_group.choose_group
            .choose_group_id,
          project_id: localStorage.getItem("project_id")
        };
        const index = this.list_group.indexOf(localStorage.getItem("group_id"));
        this.$confirm("Are you sure you want to delete this group?").then(
          res => {
            if (res === true) {
              this.$store.dispatch("del_group", data2).then(resp => {
                //reload lai person
                if (resp.data.code === 0) {
                  let data_reload = {
                    project_id: JSON.parse(localStorage.getItem("project_id"))
                  };
                  this.$store
                    .dispatch("reload_list_person", data_reload)
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
          }
        );
        // confirm("Are you sure you want to delete this item?") &&
        //   this.list_group.splice(index, 1) &&
        //   this.$store.dispatch("del_group", data2).then(resp => {
        //     //reload lai person
        //     if (resp.data.code === 0) {
        //       let data_reload = {
        //         project_id: JSON.parse(localStorage.getItem("project_id"))
        //       };
        //       this.$store
        //         .dispatch("reload_list_person", data_reload)
        //         .then(resp2 => {
        //           console.log("reload thanh cong: ", resp2);
        //         })
        //         .catch(err2 => {
        //           console.log(err2);
        //         });
        //     }
        //     console.log(resp.data);
        //     console.log("xong");
        //   });
      });
    },
    edit_group(id, code, name, color) {
      let data = {
        choose_group_id: id,
        choose_group_code: code,
        choose_group_name: name,
        choose_group_color: color
      };
      console.log(this.check_edit);
      this.edit_fail = false;
      this.check_edit = true;
      this.dialog3 = true;
      this.$store.dispatch("choose_group", data).then(resp => {
        (this.people_group_name = this.$store.state.res_group.choose_group.choose_group_name),
          (this.people_group_code = this.$store.state.res_group.choose_group.choose_group_code),
          this.setColor(
            this.$store.state.res_group.choose_group.choose_group_color
          );
      });
      this.$router.push({ path: "resperson", query: { edit: "", id: id } });
    },
    submit_edit_group() {
      this.$v.$touch();
      if (this.$v.$pending || this.$v.$error) return null;
      else {
        this.$store
          .dispatch("update_people_group", {
            project_id: localStorage.getItem("project_id"),
            people_group_id: this.$store.state.res_group.choose_group
              .choose_group_id,
            people_group_name: this.people_group_name.trim(),
            people_group_code: this.people_group_code.trim(),
            people_group_color: this.colors.hex
          })
          .then(resp => {
            //reload person
            if (resp.data.code === 0) {
              this.check_edit = false;
              this.dialog3 = false;
              this.edit_fail = false;
              this.check_search = true;
              this.a1_group_person = [];
              this.arr_search = [];
              this.people_group_name = "";
              this.people_group_code = "";
              let data_reload = {
                project_id: JSON.parse(localStorage.getItem("project_id"))
              };
              this.$store
                .dispatch("reload_list_person", data_reload)
                .then(resp2 => {
                  console.log("reload thanh cong: ", resp2);
                })
                .catch(err2 => {
                  console.log(err2);
                });
            }
            else{
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
      this.$v.$reset();
      this.$router.push({ path: "resperson" });
    },
    search_group() {
      this.arr_search = [];
      this.search_gr = true;
      if (this.a1_group_person.length !== 0) {
        this.check_search = false;
        console.log("aaaa");
        for (let i = 0; i < this.a1_group_person.length; i++) {
          for (let j = 0; j < this.list_group.length; j++) {
            if (
              this.list_group[j].people_group_code === this.a1_group_person[i]
            ) {
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


