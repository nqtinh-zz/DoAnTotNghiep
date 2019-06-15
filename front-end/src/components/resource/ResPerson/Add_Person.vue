<template >
  <v-dialog v-model="dialog_add_person" persistent max-width="700px">
    <template v-slot:activator="{ on }">
      <v-btn
        @click="getAllGroup"
        style="text-transform: none !important; "
        color="#1565C0"
        dark
        v-on="on"
        fab
        small
      >
        <v-icon>add</v-icon>
      </v-btn>
    </template>
    <v-card @click="off_select">
      <v-card-title>
        <v-layout row wrap>
          <v-flex xs6 sm6 lg4 xl4 md4 mt-2>
            <span style="margin-left: 20px; font-size: 20px">
              <b>{{$t(`res_person.add_person`) }}</b>
            </span>
          </v-flex>
        </v-layout>
      </v-card-title>

      <v-card-text class="pa-0">
        <v-container grid-list-md>
          <!-- <div style="font-size: 16px">{{ $t(`project.all_project`) }}</div> -->
          <v-form ref="form" @submit.prevent="add_person" lazy-validation>
            <v-layout wrap row>
              <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                <b>{{$t(`res_person.person_code`) }}</b>
              </v-flex>
              <v-text-field
                v-if="dialog_add_person"
                xs7
                sm7
                :label="$t('res_person.enter_person_code')"
                v-model="person_code"
                :error-messages="PersonCodeErrors"
                required
                :autofocus="'autofocus'"
                @input="$v.person_code.$touch()"
                @blur="$v.person_code.$touch()"
              ></v-text-field>&nbsp;
              <v-flex xs1 sm1></v-flex>
            </v-layout>
            <v-layout wrap row pt-2>
              <v-flex xs3 sm3 pt-5 style="font-size: 17px">
                <b>{{$t(`res_person.image`) }}</b>
              </v-flex>
              <vue-upload-multiple-image
                @upload-success="uploadImageSuccess"
                @before-remove="beforeRemove"
                @edit-image="editImage"
                @data-change="dataChange"
                :data-images="images"
                idUpload="myIdUpload"
                editUpload="myIdEdit"
              ></vue-upload-multiple-image>
              <div v-if="add_fail == true">
                <v-flex style="margin-left: 15px; color: red">{{$t(`res_person.person_code_Errors.exits`) }}</v-flex>
              </div>
            </v-layout>
            <v-layout wrap row>
              <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                <b>{{$t(`res_person.group`) }}</b>
              </v-flex>
              <v-flex xs8 sm8>
                <v-select
                  v-bind:items="listGroup"
                  v-model="a1_add_person"
                  :label="$t('res_person.choose_group')"
                  persistent-hint
                  multiple
                  chips
                >
                  <template v-slot:prepend-item>
                    <v-list-tile ripple @click="New_Group_On_Add_Person">
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
            <v-layout wrap row pt-2 v-if="check_add_person === true">
              <v-progress-linear :indeterminate="true"></v-progress-linear>
            </v-layout>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" flat @click="close_dialog" style="font-size: 16px">{{$t(`res_person.cancel`) }}</v-btn>
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
</template>
<script>
import VueUploadMultipleImage from "vue-upload-multiple-image";
import { validationMixin } from "vuelidate";
import { required, maxLength, minLength } from "vuelidate/lib/validators";
export default {
  mixins: [validationMixin],
  validations: {
    person_code: { required, maxLength: maxLength(30), minLength: minLength(2) }
  },
  // name: 'add_person',
  data() {
    return {
      check_add_person: false,
      tmp_formData: [],
      right_formData: new FormData(),
      dialog_add_person: false,
      person_code: "",
      images: [],
      a1_add_person: [],
      data_images: [],
      valid: false,
      // listGroup: [],
      add_fail: false
    };
  },
  components: {
    VueUploadMultipleImage
  },
  methods: {
    New_Group_On_Add_Person() {
      this.dialog_add_person = false;
      this.$store.state.res_group.dialog2 = true;
    },
    off_select() {
      console.log("sssssssss");
    },
    add_person() {
      this.$v.$touch();
      if (this.$v.$pending || this.$v.$error) return null;
      else {
        // this.formData.append("project_id", localStorage.getItem("project_id"));
        // this.formData.append("group", this.arr_group_import);
        // this.formData.append("person_code", this.person_code);
        // for (let t = 0; t < this.data_images.length; t++) {
        //   this.formData.append(
        //     'images',
        //     this.data_images[t]
        //   );
        // }
        this.check_add_person = true;
        var data = {
          person_code: this.person_code,
          images: this.data_images,
          group: this.a1_add_person,
          project_id: JSON.parse(localStorage.getItem("project_id"))
        };
        // console.log("add_person", this.formData);
        console.log("type data images: ", this.images);
        // for (var pair of this.tmp_formData.entries()) {
        //   console.log(pair[1]);
        // }
        for (let i = 0; i < this.tmp_formData.length; i++) {
          for (var pair of this.tmp_formData[i].entries()) {
            this.right_formData.append(this.person_code, pair[1]);
          }
        }
        for (var pair of this.right_formData.entries()) {
          console.log(pair[0]);
          console.log(pair[1]);
        }
        this.right_formData.append(
          "project_id",
          localStorage.getItem("project_id")
        );
        this.right_formData.append("person_code",this.person_code)
        this.right;
        this.right_formData.append("group", this.a1_add_person);
        this.$store
          .dispatch("add_person", this.right_formData)
          .then(resp => {
            console.log("da gui thanh cong: ", resp.data.code);
            if (resp.data.code === 0) {
              this.a1_add_person = [];
              this.images = [];
              this.person_code = "";
              this.dialog_add_person = false;
              this.tmp_formData = [];
              this.right_formData = new FormData();
            }
            if (resp.data.code === -1) {
              // console.log('áldfksldflfd')
              this.add_fail = true;
            }
            this.check_add_person = false;
          })
          .catch(err => {
            console.log("loi", err);
          });
      }
      this.$v.$reset();
    },
    getAllGroup() {
      var data = { project_id: JSON.parse(localStorage.getItem("project_id")) };
      this.$store
        .dispatch("get_all_group", data)
        .then(resp => {
          console.log("get all group thanh cong: ", resp);
        })
        .catch(err => {
          console.log(err);
        });
    },
    uploadImageSuccess(formData, index, fileList) {
      this.data_images = [];
      for (let i = 0; i < fileList.length; i++) {
        this.data_images.push(fileList[i].path);
        // let url = fileList[i].path;
        // console.log('ddddd')
        // fetch(url)
        //   .then(res => res.blob())
        //   .then(blob => {
        //     let file = new File([blob], fileList[i].name);
        //     this.tmp_formData.append(this.person_code, file);
        //   });
      }
      this.tmp_formData.push(formData);
      // for (var pair of this.tmp_formData.entries()) {
      //     console.log(pair[1]);
      //   }

      // console.log("sau khi upload anh: ",index)
      console.log("sau khi upload anh: ", fileList);
    },
    beforeRemove(index, done, fileList) {
      console.log("index", index, fileList);
      var r = confirm("remove image");
      if (r == true) {
        done();
      } else {
      }
      this.data_images = [];
      this.tmp_formData = [];
      for (let i = 0; i < fileList.length; i++) {
        this.data_images.push(fileList[i].path);
        //console.log(fileList[i].path)
        let res = fileList[i].path;
        var data = new FormData();

        var arr = res.split(","),
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
        for (var pair of data.entries()) {
          console.log(pair[0]);
          console.log(pair[1]);
        }
      }
    },
    editImage(formData, index, fileList) {
      this.data_images = [];
      for (let i = 0; i < fileList.length; i++) {
        this.data_images.push(fileList[i].path);
      }
      console.log("edit data", index, fileList);
    },
    dataChange(data) {
      console.log(data);
    },
    close_dialog() {
      this.dialog_add_person = false;
      this.person_code = "";
      this.images = [];
      this.a1_add_person = [];
      this.data_images = [];
      this.add_fail = false;
      this.$v.$reset();
      this.check_add_person = false;
      // this.$refs.form.reset()
    }
  },
  computed: {
    PersonCodeErrors() {
      const errors = [];
      if (!this.$v.person_code.$dirty) return errors;
      !this.$v.person_code.required && errors.push(this.$t(`res_person.person_code_Errors.required`));
      // this.fail_create === "code_fail" && errors.push("Code already exits");
      for (let i = 0; i < this.person_code.length; i++) {
        if (this.person_code[i] === " ")
          errors.push(this.$t(`res_person.person_code_Errors.check_space`));
      }
      !this.$v.person_code.maxLength &&
        errors.push(this.$t(`res_person.person_code_Errors.most`));
      !this.$v.person_code.minLength &&
        errors.push(this.$t(`res_person.person_code_Errors.least`));
      return errors;
    },
    listGroup() {
      return this.$store.getters.ListGroup;
    }
  }
};
</script>
<style>
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
</style>
