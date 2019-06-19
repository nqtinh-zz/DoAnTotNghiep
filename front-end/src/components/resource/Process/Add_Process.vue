<template>
  <v-dialog v-model="dialog_add_process" persistent max-width="700px">
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
              <b>Add Process</b>
            </span>
          </v-flex>
        </v-layout>
      </v-card-title>

      <v-card-text class="pa-0">
        <v-container grid-list-md>
          <!-- <div style="font-size: 16px">{{ $t(`project.all_project`) }}</div> -->
          <v-form ref="form" @submit.prevent="add_process">
            <v-layout wrap row>
              <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                <b>Process Name</b>
              </v-flex>
              <v-text-field
                v-if="dialog_add_process"
                :autofocus="'autofocus'"
                xs7
                sm7
                label="Enter Process Name"
                v-model="process_name"
                :error-messages="ProcessNameError"
                required
                @input="$v.process_name.$touch()"
                @blur="$v.process_name.$touch()"
              ></v-text-field>&nbsp;
              <v-flex xs1 sm1></v-flex>
            </v-layout>
            <v-layout wrap row>
              <v-flex xs3 sm3 pt-4 style="font-size: 17px"></v-flex>
              <div v-if="process_name_fail === true">
                <v-flex style="margin-left: 15px; color: red">Process name is required</v-flex>
              </div>
              <v-flex xs1 sm1></v-flex>
            </v-layout>
            <v-layout wrap row>
              <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                <b>Camera</b>
              </v-flex>
              <v-flex xs8 sm8>
                <v-select
                  v-bind:items="listCamera"
                  v-model="a1"
                  label="Choose Camera"
                  
                  chips
                  persistent-hint
                ></v-select>
              </v-flex>
            </v-layout>
            <v-layout wrap row>
              <v-flex xs3 sm3 pt-4 style="font-size: 17px"></v-flex>
              <div v-if="camera_fail === true">
                <v-flex style="margin-left: 15px; color: red">Camera is required</v-flex>
              </div>
              <v-flex xs1 sm1></v-flex>
            </v-layout>
            <v-layout wrap row pt-3>
              <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                <b>People group</b>
              </v-flex>
              <v-flex xs8 sm8>
                <v-select
                  v-bind:items="listGroup"
                  v-model="a2"
                  label="Choose Group"
                  item-text="people_group_code"
                  item-value="people_group_id"
                
                  multiple
                  chips
                  persistent-hint
                ></v-select>
                <!-- <v-autocomplete
                  :items="['Skiing', 'Ice hockey', 'Soccer', 'Basketball', 'Hockey', 'Reading', 'Writing', 'Coding', 'Basejump']"
                  label="Interests"
                  multiple
                ></v-autocomplete>-->
              </v-flex>
            </v-layout>
            <v-layout wrap row>
              <v-flex xs3 sm3 pt-4 style="font-size: 17px"></v-flex>
              <div v-if="people_group_fail === true">
                <v-flex style="margin-left: 15px; color: red">People group is required</v-flex>
              </div>
              <v-flex xs1 sm1></v-flex>
            </v-layout>
            <v-layout wrap row>
              <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                <b>Process config</b>
              </v-flex>
              <v-flex xs8 class="py-0">
                <!-- <h3 class="headline font-weight-medium ma-0">Process config</h3> -->
                <div id="editorWrapper" style="margin-top: 15px; height:300px">
                  <div id="editor"/>
                </div>
              </v-flex>
            </v-layout>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="blue darken-1"
                flat
                @click="close_dialog_process"
                style="font-size: 16px"
              >CANCEL</v-btn>
              <v-btn
                color="blue darken-1"
                flat
                type="submit"
                style="font-size: 16px; margin-right: 5px"
              >Submit</v-btn>
            </v-card-actions>
          </v-form>
        </v-container>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
<script>
import { validationMixin } from "vuelidate";
import { mapActions, mapMutations, mapState } from "vuex";
import { required, maxLength, minLength } from "vuelidate/lib/validators";
import ace from "ace-builds";
import "ace-builds/webpack-resolver";
export default {
  mixins: [validationMixin],
  validations: {
    process_name: {
      required,
      maxLength: maxLength(30),
      minLength: minLength(2)
    }
  },
  data() {
    return {
      process_name_fail: false,
      camera_fail: false,
      people_group_fail: false,
      dialog_add_process: false,
      process_name: "",
      camera_name: "",
      stream_url: "",
      a1: "",
      a2: [],
      valid: false,
      // listGroup: [],
      add_fail: false,
      json: "",
      editor: null,
      process_config: "",
      valid: true
    };
  },
  created() {
    console.log("CREATED ADD NEW CHANNEL");
    console.log(this.channel);
  },
  beforeMount() {
    console.log("BEFORE MOUNTED ADD NEW CHANNEL");
  },
  mounted() {
    console.log("MOUNTED ADD NEW CHANNEL");
    // this.init()
    this.editor = ace.edit("editor", {
      mode: "ace/mode/json",
      selectionStyle: "text",
      showPrintMargin: false,
      theme: "ace/theme/dracula"
    });
    // this.editor.setValue(JSON.stringify(this.channel.process_config, null, '\t'))
    console.log(this.editor);
  },
  updated() {
    console.log("UPDATE ADD NEW CHANNEL");
  },
  destroyed() {
    console.log("DESTROY ADD NEW CHANNEL");
    this.editor.destroy();
    this.editor.container.remove();
  },
  components: {},
  methods: {
    async add_process() {
      let camera_id_tmp;
      for (let t = 0; t < this.$store.getters.ListCamera.length; t++) {
        if (this.a1 === this.$store.getters.ListCamera[t].camera_name) {
          camera_id_tmp = this.$store.getters.ListCamera[t].camera_id;
        }
      }
      console.log("id_", camera_id_tmp);
      var data = {
        // process_id:2,
        // process_status:0,
        process_name: this.process_name,
        camera_id: camera_id_tmp,
        people_group_id: this.a2,
        process_config: await JSON.parse(this.editor.getValue()),
        project_id: JSON.parse(localStorage.getItem("project_id"))
      };
      console.log("data add process ", data);
      if (this.a1 == "") {
        this.camera_fail = true;
      }
      if (this.a2.length == 0) {
        this.people_group_fail = true;
      }
      if (this.process_name == "") {
        this.process_name_fail = true;
      }
      if (this.a1 != "" && this.a2.length != 0 && this.process_name != "") {
        this.$store
          .dispatch("add_process", data)
          .then(resp => {
            this.dialog_add_process = false;
            this.a1 = [];
            this.a2 = [];
            this.process_name = [];
            this.people_group_fail = false;
            this.process_name_fail = false;
            this.camera_fail = false;
            this.$v.$reset();
            console.log("add process xong : ", resp);
          })
          .catch(err => {
            console.log(err);
          });
      }
    },
    close_dialog_process() {
      this.dialog_add_process = false;
      this.people_group_fail = false;
      this.process_name_fail = false;
      this.camera_fail = false;
      this.a1 = [];
      this.a2 = [];
      this.$v.$reset();
    },
    getAllGroup() {
      var data = { project_id: JSON.parse(localStorage.getItem("project_id")) };
      console.log("den day r");
      this.$store
        .dispatch("get_config", data)
        .then(resp3 => {
          console.log("ab cc ss  dd ");
          this.editor.setValue(JSON.stringify(resp3, null, "\t"));
        })
        .catch(err3 => {
          console.log(err3);
        });
    }
  },
  computed:
    // listGroup () {
    //   return this.$store.getters.ListGroup
    // },
    mapState({
      ProcessNameError() {
        const errors = [];
        if (!this.$v.process_name.$dirty) return errors;
        // !this.$v.process_name.required &&
        //   errors.push("Process name is required.");
        // this.fail_create === "code_fail" && errors.push("Code already exits");
        // for (let i = 0; i < this.process_name.length; i++) {
        //   if (this.process_name[i] === " ")
        //     errors.push("Person code must not have space");
        // }
        !this.$v.process_name.maxLength &&
          errors.push("Process name must be at most 30 characters long");
        !this.$v.process_name.minLength &&
          errors.push("Process name must be at least 2 characters long");
        return errors;
      },
      // CameraError() {
      //   const errors = [];
      //   if (!this.$v.a1.$dirty) return errors;
      //   !this.$v.a1.required &&
      //     errors.push("Camera name is required.");

      //   return errors;
      // },
      // PeopleGroupError() {
      //   const errors = [];
      //   if (!this.$v.a2.$dirty) return errors;
      //   !this.$v.a2.required &&
      //     errors.push("People group is required.");

      //   return errors;
      // },
      list_group: state => state.res_group_camera.list_group_camera,
      listGroup() {
        return this.$store.getters.Process_ListGroup;
      },
      listCamera() {
        let list_temp = this.$store.getters.ListCamera;
        let list_return = [];
        for (let i = 0; i < list_temp.length; i++) {
          list_return.push(list_temp[i].camera_name);
        }
        return list_return;
      }
    })
};
</script>
<style lang="sass">
@import url('https://fonts.googleapis.com/css?family=Montserrat|Roboto+Mono')
#editorWrapper
  position: relative
  height: 100%
  max-height: 45vh

  @media (min-height: 600px)
    height: 55vh

  @media (min-height: 900px)
    height: 65vh

  #editor
    font-family: 'Roboto Mono', monospace
    font-size: 14px
    position: absolute
    top: 0
    bottom: 0
    left: 0
    right: 0

</style>
