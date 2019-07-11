<template>
  <v-container grid-list-xl>
    <v-layout row wrap justify-center class="my-0">
      <v-flex xs12 sm12 md9 lg9 xl9>
        <v-card height="100%">
          <v-card-title style="font-size: 16px">
            Process
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              append-icon="search"
              label="Search"
              single-line
              hide-details
            ></v-text-field>
          </v-card-title>
          <v-data-table
            :headers="headers"
            :items="list_process"
            :search="search"
            :pagination.sync="pagination"
          >
            <template v-slot:items="props">
              <!-- <td><span class="v-stepper__step__step success"><i class="material-icons"></i></span></td> -->
              <td style="font-size: 15px">{{ props.item.process_name }}</td>
              <!-- <td>{{ props.item.channel_name }}</td> -->
              <td style="font-size: 15px">
                <div v-if="props.item.process_status === 1">
                  <v-chip color="primary" text-color="white" style="font-size: 15px">Running</v-chip>
                </div>
                <div v-if="props.item.process_status === 2">
                  <v-chip color="grey" text-color="white" style="font-size: 15px">Stopped</v-chip>
                </div>
                <div v-if="props.item.process_status === 0">
                  <v-chip color="success" text-color="white" style="font-size: 15px">Init</v-chip>
                </div>
                <div v-if="props.item.process_status === 3">
                  <v-chip color="error" text-color="white" style="font-size: 15px">Error</v-chip>
                </div>
              </td>
              <td>
                <div v-if="props.item.process_status !== 1 & props.item.process_status !== 3">
                  <v-btn @click="start_process(props.item.process_id)" color="success">Start</v-btn>
                </div>
                <div v-if="props.item.process_status === 3">
                  <v-btn @click="start_process_error(props.item)" color="error">Start</v-btn>
                </div>
                <div v-if="props.item.process_status === 1">
                  <v-btn @click="stop_process(props.item.process_id)" color="warning">Stop</v-btn>
                </div>
              </td>

              <td class="text-xs-right" style="width:200px;">
                <v-icon small @click="view_info_process(props.item)">search</v-icon>&nbsp;
                <v-icon small @click="data_edit_process(props.item)">edit</v-icon>&nbsp;
                <v-icon small @click="delete_process(props.item)">delete</v-icon>
              </td>
            </template>
          </v-data-table>
          <div class="text-xs-right mr-4">
            <Add_Process></Add_Process>
          </div>
        </v-card>
      </v-flex>
      <v-flex xs12 sm12 md3 lg3 xl3>
        <div class="v-card v-sheet theme--light" style="margin-top:2.9%;height: 800px; ">
          <v-layout row>
            <v-flex xs8 sm8 md8 lg8 xl8>
              <v-card-text style="font-size: 16px">Process Information</v-card-text>
            </v-flex>
          </v-layout>

          <v-layout wrap justify-center>
            <v-flex xs12 md10>
              <v-text-field v-model="v_process_name" label="Process name" readonly></v-text-field>
            </v-flex>
            <v-flex xs12 md10>
              <v-text-field v-model="v_process_status" label="Status" readonly></v-text-field>
            </v-flex>
            <v-flex xs12 md10>
              <!-- <v-text-field v-model="v_process_camera" label="Camera" readonly></v-text-field> -->
              <v-select
                v-bind:items="listCamera_edit"
                v-model="v_process_camera"
                label="Camera"
                item-text="camera_name"
                item-value="camera_id"
                chips
                readonly
              ></v-select>
            </v-flex>
            <v-flex xs12 md10>
              <!-- <v-text-field v-model="v_process_group_people" label="Group People" readonly></v-text-field> -->
              <v-select
                v-bind:items="listGroup_edit"
                v-model="v_process_group_people"
                label="Group people"
                item-text="people_group_code"
                item-value="people_group_id"
                multiple
                chips
                readonly
                
              ></v-select>
            </v-flex>
          </v-layout>
        </div>
      </v-flex>
      <!-- dialog edit process-->
      <v-dialog v-model="dialog_edit_process" persistent max-width="700px">
        <v-card>
          <v-card-title>
            <v-layout row wrap>
              <v-flex xs6 sm6 lg4 xl4 md4 mt-2>
                <span style="margin-left: 20px; font-size: 20px">
                  <b>Edit Process</b>
                </span>
              </v-flex>
            </v-layout>
          </v-card-title>

          <v-card-text class="pa-0">
            <v-container grid-list-md>
              <!-- <div style="font-size: 16px">{{ $t(`project.all_project`) }}</div> -->
              <v-form ref="form" @submit.prevent="submit_edit_process">
                <v-layout wrap row>
                  <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                    <b>Process Name</b>
                  </v-flex>
                  <v-text-field
                    v-if="dialog_edit_process"
                    :autofocus="'autofocus'"
                    xs7
                    sm7
                    label="Enter Process Name"
                    v-model="process_name_edit"
                    :error-messages="ProcessNameError"
                    required
                    @input="$v.process_name_edit.$touch()"
                    @blur="$v.process_name_edit.$touch()"
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
                      v-bind:items="listCamera_edit"
                      v-model="camera_edit"
                      label="choose group"
                      item-text="camera_name"
                      item-value="camera_id"
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
                      v-bind:items="listGroup_edit"
                      v-model="list_group_edit"
                      label="choose group people"
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
                    <div id="editorWrapper" style="margin-top: 15px">
                      <div id="editor"/>
                    </div>
                  </v-flex>
                </v-layout>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    color="blue darken-1"
                    flat
                    @click="close_dialog_edit_process"
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
    </v-layout>
  </v-container>
</template>

<script>
import { validationMixin } from "vuelidate";
import { mapActions, mapMutations, mapState } from "vuex";
import { required, maxLength, minLength } from "vuelidate/lib/validators";
import Add_Process from "./Add_Process";
import ace from "ace-builds";
import "ace-builds/webpack-resolver";
export default {
  mixins: [validationMixin],
  validations: {
    process_name_edit: {
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
      v_process_name: "",
      v_process_status: "",
      v_process_camera: "",
      v_process_group_people: [],

      list_group_edit: [],
      process_id_tmp: "",
      camera_edit: "",
      process_name_edit: "",
      dialog_edit_process: false,
      pagination: {
        rowsPerPage: 10
      },
      name_camera_id: "",
      name_group: "",
      search: "",
      headers: [
        {
          text: "Process name",
          align: "left",
          width: "300px",
          value: "process_name",
          sortable: false
        },
        // { text: "Channel name", value: "channel_name", sortable: false },
        {
          text: "Status",
          value: "status",
          sortable: false,
          width: "200px"
        },
        {
          text: "Action",
          value: "action",
          sortable: false,
          width: "200px"
        },
        {
          text: "Edit",
          value: "edit",
          sortable: false,
          width: "100px",
          align: "right"
        }
      ]
    };
  },
  components: {
    Add_Process
  },
  created() {
    var data = { project_id: JSON.parse(localStorage.getItem("project_id")) };
    this.$store
      .dispatch("get_list_process", data)
      .then(resp4 => {
        console.log("get list process thanh cong", resp4);
      })
      .catch(err4 => {
        console.log(err4);
      });
    this.$store
      .dispatch("process_get_all_group", data)
      .then(resp => {
        console.log("get all group thanh cong: ", resp);
      })
      .catch(err => {
        console.log(err);
      });
    this.$store
      .dispatch("get_all_camera", data)
      .then(resp2 => {
        console.log("get all camera thanh cong: ", resp2);
      })
      .catch(err2 => {
        console.log(err2);
      });
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
  computed: mapState({
    ProcessNameError() {
      const errors = [];
      if (!this.$v.process_name_edit.$dirty) return errors;
      !this.$v.process_name_edit.required &&
        errors.push("Camera name is required.");
      // this.fail_create === "code_fail" && errors.push("Code already exits");
      // for (let i = 0; i < this.process_name_edit.length; i++) {
      //   if (this.process_name_edit[i] === " ")
      //     errors.push("Person code must not have space");
      // }
      !this.$v.process_name_edit.maxLength &&
        errors.push("Camera name must be at most 30 characters long");
      !this.$v.process_name_edit.minLength &&
        errors.push("Camera name must be at least 2 characters long");
      return errors;
    },
    list_group: state => state.res_group_camera.list_group_camera,
    list_process: state => state.abc_process.list_process,
    listGroup_edit() {
      console.log("danh sach group people", this.$store.getters.Process_ListGroup)
      return this.$store.getters.Process_ListGroup;
    },
    listCamera_edit() {
      let list_temp = this.$store.getters.ListCamera;
      // console.log("danh sach camera", list_temp)
      // let list_return = [];
      // for (let i = 0; i < list_temp.length; i++) {
      //   list_return.push(list_temp[i].camera_name);
      // }
      // return list_return;
      return list_temp;
    },
    authProject() {
      return localStorage.getItem("project") != null;
    },
    nameProject() {
      return JSON.parse(localStorage.getItem("project")).project_name;
    },
    function_id() {
      console.log("anhvan1995");
      var func = JSON.parse(localStorage.getItem("all_function"));
      if (func === null) {
        return 0;
      }
      for (let i = 0; i < func.length; i++) {
        if (func[i].function_id === 1) {
          return 1;
        }
      }
      return 0;
    }
  }),
  methods: {
    start_process_error: function(item)
    {
      
      this.$confirm("Camera đã bị tắt hoạt động, vui lòng truy cập resource camera để khởi động lại", {
        title: "Khởi động process lỗi "
      }).then(res => {
        console.log('alo nghe ne:', item)
      });
    },
    view_info_process: function(item) {
      // console.log("cho trung ", item)
      this.v_process_name = item.process_name;
      if (item.process_status === 0) {
        this.v_process_status = "Init";
      } else if (item.process_status === 1) {
        this.v_process_status = "Running";
      } else if (item.process_status === 2) {
        this.v_process_status = "Stopped";
      } else if (item.process_status === 3) {
        this.v_process_status = "Error";
      }
      let camera_name_tmp;
      for (let t = 0; t < this.$store.state.res_camera.listCamera.length; t++) {
        if (
          item.camera_id_id ===
          this.$store.state.res_camera.listCamera[t].camera_id
        ) {
          camera_name_tmp = this.$store.state.res_camera.listCamera[t]
            .camera_name;
        }
      }

      var res = item.people_group_id.substring(
        1,
        item.people_group_id.length - 1
      );
      var tmp = res.split(',').map(x=>parseInt(x))
      let group_name_tmp = [];
      group_name_tmp.push("[");
      for (let i = 0; i < tmp.length; i++) {
        for (let t = 0; t < this.$store.state.res_people.group.length; t++) {
          if (tmp[i] == this.$store.state.res_people.group[t].people_group_id) {
            group_name_tmp.push(
              this.$store.state.res_people.group[t].people_group_code,
              ", "
            );
            console.log("test", group_name_tmp);
          }
        }
      }
      group_name_tmp.push("]");
      // this.v_process_camera = camera_name_tmp;
      this.v_process_camera = item.camera_id_id
      // console.log("trung cam mom:", tmp)
      this.v_process_group_people = tmp;
      console.log("abc", item);
    },
    async data_edit_process(item) {
      console.log("Trung cho dien: ", item)
      let camera_name_tmp;
      for (let t = 0; t < this.$store.state.res_camera.listCamera.length; t++) {
        if (
          item.camera_id_id ===
          this.$store.state.res_camera.listCamera[t].camera_id
        ) {
          camera_name_tmp = this.$store.state.res_camera.listCamera[t]
            .camera_name;
        }
      }

      var res = item.people_group_id.substring(
        1,
        item.people_group_id.length - 1
      );
      var tmp = res.split(',').map(x=>parseInt(x))
      let group_name_tmp = [];
      group_name_tmp.push("[");
      for (let i = 0; i < tmp.length; i++) {
        for (let t = 0; t < this.$store.state.res_people.group.length; t++) {
          if (tmp[i] == this.$store.state.res_people.group[t].people_group_id) {
            group_name_tmp.push(
              this.$store.state.res_people.group[t].people_group_code,
              ", "
            );
            console.log("test", group_name_tmp);
          }
        }
      }
      group_name_tmp.push("]");
      let data = {
        process_id: item.process_id
      };

      this.$store
        .dispatch("get_process", data)
        .then(resp => {
          console.log("get process xong : ", resp);
        })
        .catch(err => {
          console.log(err);
        });

      this.dialog_edit_process = true;
      this.list_group_edit = tmp;
      // console.log("trung cho dien 2", tmp)
      this.name_camera_id = camera_name_tmp;
      // this.camera_edit = item.camera_id;
      this.camera_edit = item.camera_id_id 
      this.name_group = group_name_tmp;
      this.process_name_edit = item.process_name;
      this.process_id_tmp = item.process_id;
      // var ll =await JSON.parse(item.process_config);
      // console.log('ssssssssssssssss',ll);
      // var t=JSON.parse(ll)
      // console.log('t',t)
      this.editor.setValue(
        JSON.stringify(item.process_config, null, "\t", '"')
      );
    },
    close_dialog_edit_process() {
      this.people_group_fail = false;
      this.process_name_fail = false;
      this.camera_fail = false;
      this.dialog_edit_process = false;
    },
    async submit_edit_process() {
      var data = {
        // process_id:2,
        // process_status:0,
        process_id: this.process_id_tmp,
        process_name: this.process_name_edit,
        camera_id: this.camera_edit,
        people_group_id: this.list_group_edit,
        process_config: await JSON.parse(this.editor.getValue()),
        project_id: JSON.parse(localStorage.getItem("project_id"))
      };
      console.log("data update process ", this.process_name_edit);
      if (this.camera_edit == "") {
        this.camera_fail = true;
      }
      if (this.list_group_edit.length == 0) {
        this.people_group_fail = true;
      }
      if (this.process_name_edit == "") {
        console.log('sai')
        this.process_name_fail = true;
      }
      if (
        this.camera_edit != "" &&
        this.list_group_edit.length != 0 &&
        this.process_name_edit != ""
      ) {
        this.$store
          .dispatch("update_process", data)
          .then(resp => {
            this.dialog_edit_process = false;
            this.a1 = [];
            this.a2 = [];
            this.process_name = [];
            this.people_group_fail = false;
            this.process_name_fail = false;
            this.camera_fail = false;
            this.$v.$reset();
            console.log("update process xong : ", resp);
          })
          .catch(err => {
            console.log(err);
          });
      }
    },
    delete_process: function(item) {
      const index = this.list_process.indexOf(item);
      let camera_id_tmp;
      for (
        let t = 0;
        t < this.$store.state.abc_process.list_process.length;
        t++
      ) {
        if (
          item.process_name ===
          this.$store.state.abc_process.list_process[t].process_name
        ) {
          camera_id_tmp = this.$store.state.abc_process.list_process[t]
            .process_id;
        }
      }
      console.log("id_", camera_id_tmp);
      let data = {
        process_id: camera_id_tmp
      };
      this.$confirm("Are you sure you want to delete this process?", {
        title: "Delete Process"
      }).then(res => {
        if (res === true) {
          this.list_process.splice(index, 1) &&
            this.$store.dispatch("delete_process", data).then(resp => {});
        }
      });
      // confirm("Are you sure you want to delete this person?") &&
      //   this.desserts.splice(index, 1) &&
      //   this.$store.dispatch("delete_person", data).then(resp => {
      //     console.log(resp);
      //     // location.reload();
      //   });
    },
    start_process: function(process_id) {
      let data = {
        process_id: process_id
      };
      this.$confirm("Are you sure you want to start this process ?", {
        title: "Start process"
      }).then(res => {
        if (res === true) {
          this.$store.dispatch("start_process", data).then(resp => {});
          console.log("id_", process_id);
        }
      });
    },
    stop_process: function(process_id) {
      let data = {
        process_id: process_id
      };
      this.$confirm("Are you sure you want to stop this process ?", {
        title: "Stop process"
      }).then(res => {
        if (res === true) {
          this.$store.dispatch("stop_process", data).then(resp => {});
          console.log("id_", process_id);
        }
      });
    }
  }
};
</script>
<style >
.v-chip--disabled{
  background-color: #3B7ECA !important;
  color: white !important;
}
</style>
