<template>
  <div>
    <v-container grid-list-xl>
      <v-layout row wrap justify-center class="my-0">
        <v-flex xs12 sm12 md8 lg8 xl8>
          <v-card height="100%">
            <v-card-title style="font-size: 16px">
              Res Person
              <v-btn @click="refresh_list_person" flat icon color="indigo">
                <v-icon>cached</v-icon>
              </v-btn>

              <v-spacer></v-spacer>
              <v-text-field
                v-model="search"
                append-icon="search"
                :label="$t('toolbar.search')"
                single-line
                hide-details
              ></v-text-field>
            </v-card-title>
            <!-- dialog add person to group -->
            <v-dialog v-model="dialog4" persistent max-width="500px">
              <template v-slot:activator="{ on }"></template>
              <v-card>
                <v-card-title>
                  <v-layout row wrap>
                    <v-flex xs12 sm12 mt-2>
                      <span style="margin-left: 10px; font-size: 20px">
                        <b>{{$t(`res_person.add_person_to_group`) }}</b>
                      </span>
                    </v-flex>
                  </v-layout>
                </v-card-title>

                <v-card-text class="pa-0">
                  <v-container grid-list-md>
                    <!-- <div style="font-size: 16px">{{ $t(`project.all_project`) }}</div> -->
                    <!-- @submit.prevent="add_person_to_group" -->
                    <v-form ref="form" @submit.prevent="add_person_to_group()">
                      <v-layout wrap row>
                        <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                          <b>{{$t(`res_person.group`) }}</b>
                        </v-flex>
                        <v-flex xs8 sm8 md8 lg8 xl8>
                          <v-select
                            v-bind:items="group_of_person"
                            v-model="arr_group"
                            :label="$t('res_person.choose_group')"
                            persistent-hint
                            multiple
                            chips
                          >
                            <template v-slot:prepend-item>
                              <v-list-tile ripple @click="New_Group_On_Person">
                                <v-list-tile-action>
                                  <!-- <v-icon :color="selectedFruits.length > 0 ? 'indigo darken-4' : ''">{{ icon }}</v-icon> -->
                                </v-list-tile-action>
                                <v-list-tile-content>
                                  <v-list-tile-title>{{$t(`res_person.new_group`) }}</v-list-tile-title>
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
                          @click="close_add_person_to_group"
                          style="font-size: 16px"
                        >{{$t(`res_person.cancel`) }}</v-btn>
                        <v-btn
                          color="blue darken-1"
                          flat
                          type="submit"
                          style="font-size: 16px; margin-right: 5px"
                        >{{$t(`res_person.ok`) }}</v-btn>
                      </v-card-actions>
                    </v-form>
                  </v-container>
                </v-card-text>
              </v-card>
            </v-dialog>
            <!-- /dialog add person to group -->
            <!-- dialog edit person -->
            <v-dialog v-model="dialog_edit_person" persistent max-width="700px">
              <v-card>
                <v-card-title>
                  <v-layout row wrap>
                    <v-flex xs6 sm6 lg4 xl4 md4 mt-2>
                      <span style="margin-left: 20px; font-size: 20px">
                        <b>{{$t(`res_person.edit_person`) }}</b>
                      </span>
                    </v-flex>
                  </v-layout>
                </v-card-title>

                <v-card-text class="pa-0">
                  <v-container grid-list-md>
                    <!-- <div style="font-size: 16px">{{ $t(`project.all_project`) }}</div> -->
                    <v-form ref="form" @submit.prevent="edit_person">
                      <v-layout wrap row>
                        <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                          <b>{{$t(`res_person.person_code`) }}</b>
                        </v-flex>
                        <v-text-field
                          xs7
                          sm7
                          :label="$t('res_person.enter_person_code')"
                          v-model="person_code_edit"
                          :error-messages="PersonCodeErrors"
                          required
                          @input="$v.person_code_edit.$touch()"
                          @blur="$v.person_code_edit.$touch()"
                        ></v-text-field>&nbsp;
                        <v-flex xs1 sm1></v-flex>
                      </v-layout>
                      <v-layout wrap row v-if="check_edit === true">
                        <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                          <b></b>
                        </v-flex>
                        <v-flex
                          xs7
                          sm7
                          style="color: red"
                        >{{$t(`res_person.person_code_Errors.exits`) }}</v-flex>&nbsp;
                        <v-flex xs1 sm1></v-flex>
                      </v-layout>
                      <v-layout wrap row pt-2>
                        <v-flex xs3 sm3 pt-5 style="font-size: 17px">
                          <b>{{$t(`res_person.image`) }}</b>
                        </v-flex>
                        <vue-upload-multiple-image
                          @upload-success="uploadImageSuccess_edit"
                          @before-remove="beforeRemove_edit"
                          @edit-image="editImage_edit"
                          @data-change="dataChange_edit"
                          :data-images="images_edit"
                          idUpload="myIdUpload1"
                          editUpload="myIdEdit1"
                        ></vue-upload-multiple-image>
                        <!-- <div v-if="add_fail == true">
                        <v-flex
                          style="margin-left: 15px; color: red"
                        >Person code trùng, vui lòng nhập lại.</v-flex>
                        </div>-->
                      </v-layout>
                      <v-layout wrap row pt-2 v-if="check_process === true">
                        <v-progress-linear :indeterminate="true"></v-progress-linear>
                      </v-layout>

                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                          color="blue darken-1"
                          flat
                          @click="close_dialog_edit"
                          style="font-size: 16px"
                        >{{$t(`res_person.cancel`) }}</v-btn>
                        <v-btn
                          color="blue darken-1"
                          flat
                          type="submit"
                          style="font-size: 16px; margin-right: 5px"
                        >{{$t(`res_person.ok`) }}</v-btn>
                      </v-card-actions>
                    </v-form>
                  </v-container>
                </v-card-text>
              </v-card>
            </v-dialog>
            <!-- /dialog edit person -->
            <v-data-table
              :headers="headers"
              :items="desserts"
              :search="search"
              :pagination.sync="pagination"
            >
              <template v-slot:items="props">
                <td style="font-size: 15px">{{ props.item.person_code }}</td>
                <tr style="border-bottom: none;">
                  <div style="float: left; margin-top: 2px;">
                    <v-btn
                      fab
                      small
                      dark
                      color="#1565C0"
                      style="text-transform: none !important; width: 28px ; height: 28px;"
                      @click="getGroup_ofPerson(props.item)"
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
                      :style="{ backgroundColor: group.people_group_color}"
                      text-color="white"
                      close
                      @input="onClose(group,props.item)"
                    >{{group.people_group_code}}</v-chip>
                  </div>
                </tr>
                <td class="text-xs-right">
                  <v-icon small @click="data_edit_person(props.item)">edit</v-icon>&nbsp;
                  <v-icon @click="deleteItem(props.item)" small>delete</v-icon>
                </td>
              </template>
            </v-data-table>
            <div class="text-xs-right mr-4">
              <Import_Person></Import_Person>&nbsp;&nbsp;
              <!-- dialog add person-->
              <AddPerson></AddPerson>
              <!-- /dialog  add person-->
            </div>
          </v-card>
        </v-flex>
        <ResGroup></ResGroup>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import { forEach } from "lodash";
import ResGroup from "./ResGroup";
import AddPerson from "./Add_Person";
import Import_Person from "./Import_Person";
import VueUploadMultipleImage from "vue-upload-multiple-image";
import { validationMixin } from "vuelidate";
import { required, maxLength, minLength } from "vuelidate/lib/validators";
import VuetifyConfirm from "vuetify-confirm";
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
    person_code_edit: {
      required,
      maxLength: maxLength(30),
      minLength: minLength(2)
    }
  },
  // name: 'person_manage',
  data() {
    return {
      check_edit: false,
      check_process: false,
      tmp_formData: [],
      right_formData: new FormData(),
      check_button: false,
      display: "none",
      search: "",
      dialog4: false,
      //cua dialog edit person
      dialog_edit_person: false,
      person_id_edit: "",
      person_code_edit: "",
      images_edit: [],
      data_images: [],

      import: [],
      data_import_person: [],
      valid: false,
      add_fail: false,
      // /cua dialog edit person
      arr_group: [],
      person_id: "",
      pagination: {
        rowsPerPage: 10
      },
      valid: false,
      headers: [
        {
          text: this.$t(`res_person.person_code`),
          align: "left",
          width: "200px",
          value: "person_code",
          sortable: false
        },
        {
          text: this.$t(`res_person.group`),
          value: "people_group_code",
          sortable: false
        },
        {
          text: this.$t(`res_person.action`),
          value: "action",
          sortable: false,
          width: "100px"
        }
      ]
      // desserts: []
    };
  },
  created: function() {
    this.$store
      .dispatch("get_all_people", {
        project_id: JSON.parse(localStorage.getItem("project_id"))
      })
      .then(resp => {
        // this.desserts = [...resp.data.data];
        console.log("get all people: ", resp.data.data);
      })
      .catch(err => {
        console.log(err);
      });
  },
  computed: {
    PersonCodeErrors() {
      const errors = [];
      if (!this.$v.person_code_edit.$dirty) return errors;
      !this.$v.person_code_edit.required &&
        errors.push(this.$t(`res_person.person_code_Errors.required`));
      // this.fail_create === "code_fail" && errors.push("Code already exits");
      for (let i = 0; i < this.person_code_edit.length; i++) {
        if (this.person_code_edit[i] === " ")
          errors.push(this.$t(`res_person.person_code_Errors.check_space`));
      }
      !this.$v.person_code_edit.maxLength &&
        errors.push(this.$t(`res_person.person_code_Errors.most`));
      !this.$v.person_code_edit.minLength &&
        errors.push(this.$t(`res_person.person_code_Errors.least`));
      return errors;
    },
    desserts() {
      return this.$store.getters.ListPeople;
    },
    group_of_person() {
      return this.$store.getters.GroupOfPerson;
    }
  },
  components: {
    AddPerson,
    ResGroup,
    VueUploadMultipleImage,
    Import_Person
  },
  methods: {
    refresh_list_person() {
      this.$store
        .dispatch("get_all_people", {
          project_id: JSON.parse(localStorage.getItem("project_id"))
        })
        .then(resp => {
          // this.desserts = [...resp.data.data];
          console.log("get all people: ", resp.data.data);
        })
        .catch(err => {
          console.log(err);
        });
    },
    New_Group_On_Person() {
      this.dialog4 = false;
      this.arr_group = [];
      this.$store.state.res_group.dialog2 = true;
    },
    deleteItem: function(item) {
      const index = this.desserts.indexOf(item);
      let data = {
        person_id: item.person_id,
        project_id: JSON.parse(localStorage.getItem("project_id"))
      };
      this.$confirm("Are you sure you want to delete this person?", {
        title: "Delete Person"
      }).then(res => {
        if (res === true) {
          this.desserts.splice(index, 1) &&
            this.$store.dispatch("delete_person", data).then(resp => {});
        }
      });
      // confirm("Are you sure you want to delete this person?") &&
      //   this.desserts.splice(index, 1) &&
      //   this.$store.dispatch("delete_person", data).then(resp => {
      //     console.log(resp);
      //     // location.reload();
      //   });
    },
    getGroup_ofPerson: function(item) {
      this.dialog4 = true;
      console.log("get group of person: ", item);
      this.person_id = item.person_id;
      this.$store
        .dispatch("get_group_of_person", item)
        .then(resp => {
          console.log(resp);
        })
        .catch(err => {
          console.log(err);
        });
    },
    add_person_to_group: function(item) {
      // console.log("thoibodi: ",item)
      let data = {
        person_id: this.person_id,
        group_arr: this.arr_group,
        project_id: JSON.parse(localStorage.getItem("project_id"))
      };
      // console.log('add_person_to_group: ',data)
      this.$store
        .dispatch("add_person_to_group", data)
        .then(resp => {
          console.log("sau khi add group thanh cong: ", data);
          if (resp.data.code === 0) {
            this.arr_group = [];
            this.person_id = "";
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
    close_add_person_to_group() {
      (this.dialog4 = false), (this.arr_group = []);
    },
    onClose: function(group, item) {
      console.log("group: ", group);
      console.log("item: ", item);
      let data = {
        people_group_id: group.people_group_id,
        person_id: item.person_id,
        project_id: group.project_id_id
      };
      this.$confirm("Are you sure you want to delete this group ?", {
        title: "delete group of person"
      }).then(res => {
        if (res === true) {
          this.$store
            .dispatch("delete_one_group", data)
            .then(resp => {
              console.log(resp);
            })
            .catch(err => {
              console.log(err);
            });
        }
      });

      // this.$store
      //   .dispatch("delete_one_group", data)
      //   .then(resp => {
      //     console.log(resp);
      //   })
      //   .catch(err => {
      //     console.log(err);
      //   });
    },
    //edit person
    uploadImageSuccess_edit(formData, index, fileList) {
      this.data_images = [];
      for (let i = 0; i < fileList.length; i++) {
        this.data_images.push(fileList[i].path);
      }
      console.log("data_image loi ne: ", this.images_edit);
    },
    beforeRemove_edit(index, done, formData, fileList) {
      console.log("index", index, fileList);
      var r = confirm("remove image");
      if (r == true) {
        done();
      } else {
      }
      this.data_images = [];
      for (let i = 0; i < fileList.length; i++) {
        this.data_images.push(fileList[i].path);
      }
    },
    editImage_edit(formData, index, fileList) {
      this.data_images = [];
      for (let i = 0; i < fileList.length; i++) {
        this.data_images.push(fileList[i].path);
      }
      console.log("edit data", formData, index, fileList);
    },
    dataChange_edit(data) {
      console.log(data);
    },
    data_edit_person: function(item) {
      this.dialog_edit_person = true;
      this.person_code_edit = item.person_code;
      this.person_id_edit = item.person_id;
      this.$store
        .dispatch("get_data_edit_person", { person_id: item.person_id })
        .then(resp => {
          let list_image = [...resp.data.data];
          for (let i = 0; i < list_image.length; i++) {
            let res = list_image[i];
            let res2 = res.replace("b'", "");
            let res3 = res2.replace("'", "");
            let temp_image = {
              default: 0,
              highlight: 0,
              name: "img_lights.jpg",
              path: res3
            };
            this.images_edit.push(temp_image);
          }
          console.log("data get image", this.images_edit);
        });
      // console.log("edit person: ", item)
    },
    edit_person() {
      this.$v.$touch();
      if (this.$v.$pending || this.$v.$error) return null;
      else {
        var temp = [];
        if (this.images_edit.length !== 0) {
          // console.log("ab1111111111111111111")
          for (let i = 0; i < this.images_edit.length; i++) {
            temp[i] = this.images_edit[i].path;
          }
        } else {
          // console.log("ab000000000000000000000")

          for (let i = 0; i < this.data_images.length; i++) {
            temp[i] = this.data_images[i];
          }
        }

        for (var pair of this.right_formData.entries()) {
          console.log(pair[0]);
          console.log(pair[1]);
        }
        // console.log('bbbb222222222222222220',temp)
        for (let z = 0; z < temp.length; z++) {
          var data = new FormData();
          var arr = temp[z].split(","),
            mime = arr[0].match(/:(.*?);/)[1],
            bstr = atob(arr[1]),
            n = bstr.length,
            u8arr = new Uint8Array(n);
          while (n--) {
            u8arr[n] = bstr.charCodeAt(n);
          }
          var file = new File([u8arr], "tinhsan", { type: mime });
          data.append("image_data", file);
          //console.log(file);

          this.tmp_formData.push(data);
        }
        for (let i = 0; i < this.tmp_formData.length; i++) {
          for (var pair of this.tmp_formData[i].entries()) {
            this.right_formData.append(this.person_code_edit, pair[1]);
          }
        }
        this.right_formData.append(
          "project_id",
          JSON.parse(localStorage.getItem("project_id"))
        );
        this.right_formData.append("person_code", this.person_code_edit);
        this.right_formData.append("person_id", this.person_id_edit);
        var data = {
          person_code: this.person_code_edit,
          images: temp,
          project_id: JSON.parse(localStorage.getItem("project_id")),
          person_id: this.person_id_edit
        };
        console.log("data_images: ", this.data_images);
        console.log("edit person", data);
        this.check_process = true;
        this.$store
          .dispatch("edit_person", this.right_formData)
          .then(resp => {
            // console.log(resp.data.code,'adasdffd')
            if (resp.data.code === 0) {
              this.dialog_edit_person = false;
              this.images_edit = [];
              this.person_code_edit = "";
              this.data_images = [];
              (this.tmp_formData = []),
                (this.right_formData = new FormData()),
                (this.person_id_edit = "");
              this.check_edit = false;
            }
            if (resp.data.code === -1) {
              // console.log('áldfksldflfd')
              //  this.images_edit = [];
              // this.person_code_edit = "";
              // this.data_images = [];
              (this.tmp_formData = []), (this.right_formData = new FormData());
              this.check_edit = true;
              // this.person_id_edit = "";
              // this.dialog_edit_person = false;
            }
            this.check_process = false;
          })
          .catch(err => {
            console.log("loi", err);
          });
        // console.log("type data images: ",this.images)
      }
      // this.$v.$reset()
    },
    close_dialog_edit() {
      this.dialog_edit_person = false;
      this.images_edit = [];
      this.person_code_edit = "";
      this.data_images = [];
      this.person_id_edit = "";
      this.check_process = false;
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
.image-container {
  width: 350px !important;
  height: 200px !important;
}
.show-image .show-img {
  max-height: 185px !important;
  max-width: 300px !important;
}
.preview-image .centered {
  left: 47% !important;
  top: 70% !important;
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

