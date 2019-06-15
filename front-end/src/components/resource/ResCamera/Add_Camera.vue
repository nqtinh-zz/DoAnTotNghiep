<template>
  <v-dialog v-model="dialog_add_camera" persistent max-width="700px">
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
    <v-card>
      <v-card-title>
        <v-layout row wrap>
          <v-flex xs6 sm6 lg4 xl4 md4 mt-2>
            <span style="margin-left: 20px; font-size: 20px">
              <b>{{$t(`res_camera.add_camera`) }}</b>
            </span>
          </v-flex>
        </v-layout>
      </v-card-title>

      <v-card-text class="pa-0">
        <v-container grid-list-md>
          <!-- <div style="font-size: 16px">{{ $t(`project.all_project`) }}</div> -->
          <v-form ref="form" @submit.prevent="add_camera">
            <v-layout wrap row>
              <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                <b>{{$t(`res_camera.camera_name`) }}</b>
              </v-flex>
              <v-text-field
              v-if="dialog_add_camera"
              :autofocus="'autofocus'"
                xs7
                sm7
                :label="$t('res_camera.enter_camera_name')"
                v-model="camera_name"
                :error-messages="PersonCodeErrors"
                required
                @input="$v.camera_name.$touch()"
                @blur="$v.camera_name.$touch()"
              ></v-text-field>&nbsp;
              <v-flex xs1 sm1></v-flex>
            </v-layout>
            <v-layout wrap row>
              <v-flex xs3 sm3 pt-4 style="font-size: 17px"></v-flex>
              <div v-if="add_fail === true">
                <v-flex
                  style="margin-left: 15px; color: red"
                >{{$t(`res_camera.camera_code_Errors.exits`) }}</v-flex>
              </div>
              <v-flex xs1 sm1></v-flex>
            </v-layout>
            <v-layout wrap row>
              <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                <b>Stream URL</b>
              </v-flex>
              <v-flex xs8 sm8>
                <v-text-field v-model="stream_url" label="Stream URL"></v-text-field>
              </v-flex>
            </v-layout>
            <v-layout wrap row pt-3>
              <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                <b>{{$t(`res_camera.group`) }}</b>
              </v-flex>
              <v-flex xs8 sm8>
                <v-select
                  v-bind:items="listGroup"
                  v-model="a1"
                  :label="$t('res_camera.choose_group')"
                  multiple
                  chips
                  persistent-hint
                >
                  <template v-slot:prepend-item>
                  <v-list-tile ripple @click="New_Group_On_Add_Camera">
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
                <!-- <v-autocomplete
                  :items="['Skiing', 'Ice hockey', 'Soccer', 'Basketball', 'Hockey', 'Reading', 'Writing', 'Coding', 'Basejump']"
                  label="Interests"
                  multiple
                ></v-autocomplete> -->
              </v-flex>
            </v-layout>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" flat @click="close_dialog" style="font-size: 16px">{{$t(`res_camera.cancel`) }}</v-btn>
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
</template>
<script>
import { validationMixin } from "vuelidate";
import { mapState } from "vuex";
import { required, maxLength, minLength } from "vuelidate/lib/validators";
export default {
  mixins: [validationMixin],
  validations: {
    camera_name: { required, maxLength: maxLength(30), minLength: minLength(2) }
  },
  data() {
    return {
      dialog_add_camera: false,
      camera_name: "",
      stream_url: "",
      a1: [],
      valid: false,
      // listGroup: [],
      add_fail: false
    };
  },
  components: {},
  methods: {
    New_Group_On_Add_Camera() {
      this.dialog_add_camera = false
      this.$store.state.res_group_camera.dialog_add_gr_camera =true
    },
    add_camera() {
      this.$v.$touch();
      if (this.$v.$pending || this.$v.$error) return null;
      else {
        var data = {
          camera_name: this.camera_name,
          stream_url: this.stream_url,
          group: this.a1,
          project_id: JSON.parse(localStorage.getItem("project_id"))
        };
        console.log("add_camera", data);
        this.$store
          .dispatch("add_camera", data)
          .then(resp => {
            console.log("da gui thanh cong: ", resp.data.code);
            if (resp.data.code === 0) {
              this.a1 = [];
              this.stream_url = "";
              this.camera_name = "";
              this.dialog_add_camera = false;
            }
            if (resp.data.code === -1) {
              // console.log('áldfksldflfd')
              this.add_fail = true;
            }
          })
          .catch(err => {
            console.log("loi", err);
          });
      }
      this.$v.$reset()      
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
    close_dialog() {
      this.dialog_add_camera = false;
      this.camera_name = "";
      this.stream_url = '';
      this.images = [];
      this.a1 = [];
      this.data_images = [];
      this.add_fail = false;
      this.$v.$reset()
    }
  },
  computed:
    // listGroup () {
    //   return this.$store.getters.ListGroup
    // },
    mapState({
      PersonCodeErrors() {
        const errors = [];
        if (!this.$v.camera_name.$dirty) return errors;
        !this.$v.camera_name.required &&
          errors.push(this.$t(`res_camera.camera_code_Errors.required`));
        // this.fail_create === "code_fail" && errors.push("Code already exits");
        // for (let i = 0; i < this.camera_name.length; i++) {
        //   if (this.camera_name[i] === " ")
        //     errors.push("Person code must not have space");
        // }
        !this.$v.camera_name.maxLength &&
          errors.push(this.$t(`res_camera.camera_code_Errors.most`));
          !this.$v.camera_name.minLength &&
          errors.push(this.$t(`res_camera.camera_code_Errors.least`));
        return errors;
      },
      list_group: state => state.res_group_camera.list_group_camera,
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
