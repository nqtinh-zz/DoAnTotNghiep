<template>
  <v-dialog v-model="dialog_import_person" persistent max-width="700px">
    <template v-slot:activator="{ on }">
      <v-btn
        @click="getAllGroup_Import"
        style="text-transform: none !important; "
        color="#1565C0"
        dark
        v-on="on"
      >{{$t(`res_person.import`) }}</v-btn>
    </template>
    <v-card>
      <v-card-title>
        <v-layout row wrap>
          <v-flex xs6 sm6 lg4 xl4 md4 mt-2>
            <span style="margin-left: 20px; font-size: 20px">
              <b>{{$t(`res_person.import_person`) }}</b>
            </span>
          </v-flex>
        </v-layout>
      </v-card-title>

      <v-card-text class="pa-0">
        <v-container grid-list-md>
          <!-- <div style="font-size: 16px">{{ $t(`project.all_project`) }}</div> -->

          <v-layout wrap row>
            <v-flex xs3 sm3 pt-4 style="font-size: 17px">
              <b>{{$t(`res_person.folder`) }}</b>
            </v-flex>
            <div v-if="btn_upload === true">
              <label
                class="custom-file-upload"
                style="color: white; background: #3177C7; margin-top: 20px; width: 70px;"
              >
                <i class="material-icons" style="margin-left: 14px;margin-top: 5px;">cloud_upload</i>
                <input
                  type="file"
                  id="id_folder"
                  @change="uploadFolder"
                  style="width: 100px"
                  webkitdirectory
                  directory
                  multiple
                >
              </label>
            </div>
            <div v-if="btn_edit === true" style="margin-top: 20px">
              <v-btn
                color="blue darken-1"
                flat
                @click="show_data_import"
                style="font-size: 16px"
              >{{$t(`res_person.click_show_all`) }}</v-btn>
            </div>
            <div v-if="btn_chip === true" style="margin-top: 20px">
              <div
                style="float: left; margin-top: 2px;text-transform: uppercase;"
                v-for="(one_person,index1) in this.data_import_person"
                :key="index1"
              >
                <v-chip
                  text-color="black"
                  close
                  @input="onClose_vchip_import(one_person)"
                >{{one_person.person_code}}</v-chip>
              </div>
            </div>
          </v-layout>
          <v-layout wrap row pt-2></v-layout>
          <v-layout wrap row>
            <v-flex xs3 sm3 pt-4 style="font-size: 17px">
              <b>{{$t(`res_person.group`) }}</b>
            </v-flex>
            <v-flex xs8 sm8>
              <v-select
                v-model="arr_group_import"
                v-bind:items="listGroup"
                :label="$t('res_person.choose_group')"
                multiple
                chips
                persistent-hint
              >
                <template v-slot:prepend-item>
                  <v-list-tile ripple @click="New_Group_Select">
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
          <v-layout wrap row pt-2 v-if="check_import === true">
            <v-progress-linear :indeterminate="true"></v-progress-linear>
          </v-layout>
          <v-card-actions>
            <v-spacer></v-spacer>

            <v-btn color="blue darken-1" flat @click="cacel_Import" style="font-size: 16px">{{$t(`res_person.cancel`) }}</v-btn>
            <v-btn
              color="blue darken-1"
              flat
              style="font-size: 16px; margin-right: 5px"
              @click="submit_Import"
            >{{$t(`res_person.ok`) }}</v-btn>
          </v-card-actions>
        </v-container>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
<script>
import { mapState } from "vuex";
import { forEach, cloneDeep } from "lodash";
import VueUploadMultipleImage from "vue-upload-multiple-image";
import { validationMixin } from "vuelidate";
import { required, maxLength } from "vuelidate/lib/validators";
import Vue from "vue";
// import EventBus from './event-bus';
export default {
  mixins: [validationMixin],
  validations: {
    person_code: { required, maxLength: maxLength(30) }
  },
  props: {
    dataImages: {
      type: Array,
      default: () => {
        return [];
      }
    }
  },
  // name: 'import_dialog',
  data() {
    return {
      check_import: false,
      formData: new FormData(),
      test_formdata: {},
      dialog_import_person: false,
      check_button: false,
      import: [],
      data_import_person: [],
      data_import_person2: [],
      add_fail: false,
      images: [],
      btn_upload: true,
      btn_edit: false,
      btn_chip: false,
      arr_group_import: [],
      test_edit: false
    };
  },

  components: {},
  methods: {
    New_Group_Select() {
      // console.log("Nguyen Tien Trien")
      // this.$store.state.ResGroup.submit_group
      // this.cacel_Import()
      // EventBus.$emit('EVENT_NAME', 'abc');
      this.dialog_import_person = false;
      this.$store.state.res_group.dialog2 = true;
      // console.log('ssssssssssss',this.$store.state.res_group.dialog2)
    },
    // abc() {
    //   console.log("vo day r anh ")
    // },
    createImage(files) {
      for (let i = 0; i < files.length; i++) {
        let reader = new FileReader();
        let formData = new FormData();
        formData.append("file", files[i]);
        reader.onload = e => {
          let dataURI = e.target.result;
          if (dataURI) {
            if (!this.images.length) {
              let temp = files[i].webkitRelativePath.split("/");

              if (temp.length === 3) {
                var temp_name = temp[1];
              }
              if (temp.length === 2) {
                var temp_name = temp[0];
              }
              this.images.push({
                file: files[i],
                name: temp_name,
                path: dataURI,
                highlight: 1,
                default: 1
              });
              this.currentIndexImage = 0;
            } else {
              let temp = files[i].webkitRelativePath.split("/");

              if (temp.length === 3) {
                var temp_name = temp[1];
              }
              if (temp.length === 2) {
                var temp_name = temp[0];
              }
              this.images.push({
                file: files[i],
                name: temp_name,
                path: dataURI,
                highlight: 0,
                default: 0
              });
            }
            this.$emit(
              "upload-success",
              formData,
              this.images.length - 1,
              this.images
            );
          }
          // this.count_import = this.count_import +1
          // console.log('this.count_import',this.count_import)
        };
        reader.readAsDataURL(files[i]);
      }

      console.log("Day ne truoc");
    },
    uploadFolder(e) {
      let files = e.target.files || e.dataTransfer.files;
      if (!files.length) {
        return false;
      }
      console.log("file.length", files.length);
      // forEach(files, (value, index) => {
      //   this.createImage(value);
      // });
      // for (let i = 0; i < files.length; i++) {
      //   this.createImage(files[i]);
      //   console.log("create image");
      //   // console.log(this.images)
      //   // if(this.count_import === files.length)
      //   // {
      //   //   console.log("Nguyen Tuie trien")
      //   //   this.bool_import = true
      //   // }
      // }
      this.createImage(files);
      if (document.getElementById(this.id_folder)) {
        document.getElementById(this.id_folder).value = [];
      }

      this.check_button = true;

      console.log(this.check_button);
      console.log("day ne:  ", this.images);
      // console.log("typeof trc khi dispatch: ", typeof this.images);
      this.btn_edit = true;
      this.btn_upload = false;
      // this.show_data_import();
    },
    show_data_import() {
      for (let i = 0; i < this.images.length; i++) {
        var temp_name = this.images[i].name;
        var temp_file = [];
        var temp_path = [];
        for (let j = i; j < this.images.length; j++) {
          if (this.images[j].name === this.images[i].name) {
            temp_path.push(this.images[j].path);
            temp_file.push(this.images[j].file);
          } else {
            i = j - 1;
            break;
          }
          if (j === this.images.length - 1) {
            i = j + 1;
          }
        }
        var temp_object = {
          file: temp_file,
          person_code: temp_name,
          images: temp_path,
          group: [],
          project_id: JSON.parse(localStorage.getItem("project_id"))
        };

        this.data_import_person.push(temp_object);
        // temp_name = ''
        // temp_path = []
      }

      // console.log("day ne 2: ", this.data_import_person);

      // console.log("ssssssssssssssssss", this.data_import_person.length);
      // for (let m = 0; m < this.data_import_person.length; m++) {
      //   for (let t = 0; t < this.data_import_person[m].file.length; t++) {
      //     this.formData.append(
      //       this.data_import_person[m].person_code,
      //       this.data_import_person[m].file[t]
      //     );
      //   }
      // }
      // this.formData.append("project_id", localStorage.getItem("project_id"));
      // this.formData.append("group", this.arr_group_import);
      console.log(this.formData.getAll("group"));
      this.btn_chip = true;
      this.btn_edit = false;
      this.test_edit = true;
    },
    submit_Import() {
      this.check_import = true;
      
      if (this.test_edit === false) {
        console.log("ngtt");
        this.show_data_import();
        this.test_edit = false;
      }
      console.log("day ne 2: ", this.data_import_person);

      console.log("ssssssssssssssssss", this.data_import_person.length);
      for (let m = 0; m < this.data_import_person.length; m++) {
        for (let t = 0; t < this.data_import_person[m].file.length; t++) {
          this.formData.append(
            this.data_import_person[m].person_code,
            this.data_import_person[m].file[t]
          );
        }
      }
      this.formData.append("project_id", localStorage.getItem("project_id"));
      this.formData.append("group", this.arr_group_import);
      this.$store
        .dispatch("import_person", this.formData)
        .then(resp => {
          (this.images = []),
            (this.import = []),
            (this.data_import_person = []),
            (this.add_fail = true),
            (this.check_button = false);
          (this.dialog_import_person = false),
            (this.btn_upload = true),
            (this.btn_edit = false),
            (this.arr_group_import = []),
            (this.formData = new FormData());
          // console.log("da import thanh cong")
          // console.log(resp)
          this.check_import = false;
          console.log(resp.data);
        })
        .catch(err => {
          console.log(err);
        });
    },
    cacel_Import() {
      (this.images = []),
        (this.import = []),
        (this.data_import_person = []),
        (this.check_button = false);
      this.dialog_import_person = false;
      this.btn_upload = true;
      this.btn_edit = false;
      this.arr_group_import = [];
      this.check_import = false;
    },
    getAllGroup_Import() {
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
    onClose_vchip_import: function(one_person) {
      var temp = 0;
      for (let i = 0; i < this.data_import_person.length; i++) {
        if (one_person.person_code === this.data_import_person[i].person_code) {
          temp = i;
          break;
        }
      }
      this.data_import_person.splice(temp, 1);
      if (this.data_import_person.length === 0) {
        this.btn_upload = true
        this.images = []
        this.import = []
        this.arr_group_import = []
      }
    }
  },
  computed: mapState({
    listGroup() {
      return this.$store.getters.ListGroup;
    },
    list_images() {
      return this.$store.state.res_camera.images_import;
    }
  })
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
