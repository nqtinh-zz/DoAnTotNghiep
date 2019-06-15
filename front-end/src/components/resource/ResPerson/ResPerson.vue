<template>
  <div>
    <div v-if="authProject === false">
      <Home></Home>
      <v-alert
        :value="alert"
        type="success"
        transition="scale-transition"
      >Create new project success!</v-alert>
      <v-flex mt-3 ml-4 mb-1>
        <v-toolbar-title class="ml-0 pl-4">
          <v-icon>add_circle_outline</v-icon>&nbsp; Add Function
        </v-toolbar-title>
      </v-flex>
      <hr>
      <div style="padding-top: 5px; padding-left: 50px">
        <v-flex style="font-size: 16px">Bạn chưa có project, vui lòng chọn hoặc tạo project</v-flex>
        <br>
        <v-form v-model="valid" ref="form" @submit.prevent="create_project">
          <v-flex xs12 sm6 md3>
            <v-text-field
              label="Project code"
              v-model="projectcode"
              :error-messages="codeErrors"
              required
              @input="$v.projectcode.$touch()"
              @blur="$v.projectcode.$touch()"
            ></v-text-field>
          </v-flex>
          <v-flex xs12 sm6 md3>
            <v-text-field
              label="Project name"
              v-model="projectname"
              :error-messages="nameErrors"
              required
              @input="$v.projectname.$touch()"
              @blur="$v.projectname.$touch()"
            ></v-text-field>
          </v-flex>
          <v-btn style="color:white; margin-left:4px;" type="submit" color="#287AE6">CREATE</v-btn>
          <router-link style="text-decoration: none;color:white" to="/">
            <v-btn>CANCEL</v-btn>
          </router-link>
        </v-form>
      </div>
    </div>
    <div v-else-if="function_id !== 1">
      <Home></Home>
      <v-flex mt-3 ml-4 mb-1>
        <v-toolbar-title class="ml-0 pl-4">
          <v-icon>add_circle_outline</v-icon>&nbsp; Add Function
        </v-toolbar-title>
      </v-flex>
      <hr>
      <v-flex mt-3 ml-4 mb-1>
        <v-flex class="ml-0 pl-4" style="font-size: 16px">
          Bạn muốn thêm Function
          <b>F.Smart Door</b> vào Project
          <b>{{nameProject}}</b>
        </v-flex>
        <v-flex class="ml-0 pl-4">
          <v-btn @click="add_function" style="color:white; margin-left:4px;" color="#287AE6">buy now</v-btn>
          
          <v-btn>trial 30 days free</v-btn>
        </v-flex>
      </v-flex>
    </div>
    <div v-else>
      <Home></Home>
      <PersonManage></PersonManage>
    </div>
    <div v-if="this.credit===true">
            <CreditCard></CreditCard>
          </div>
  </div>
</template>

<script>
import CreditCard from "../../function/Credit_Card.vue";
import Home from "../../common/Home.vue";
import PersonManage from "./PersonManage";
import { validationMixin } from "vuelidate";
import { required, maxLength } from "vuelidate/lib/validators";
export default {
  name: "NewProject",
  mixins: [validationMixin],
  validations: {
    projectname: { required, maxLength: maxLength(30) },
    projectcode: { required, maxLength: maxLength(30) }
  },
  // name: 'res_person',
  data() {
    return {
      credit: false,
      alert: false,
      valid: false,
      projectcode: "",
      projectname: "",
      fail_create: ""
    };
  },
  computed: {
    nameErrors() {
      const errors = [];
      if (!this.$v.projectname.$dirty) return errors;
      !this.$v.projectname.required && errors.push("Name is required.");
      !this.$v.projectname.maxLength &&
        errors.push("Name must be at most 30 characters long");
      return errors;
    },
    codeErrors() {
      const errors = [];
      if (!this.$v.projectcode.$dirty) return errors;
      !this.$v.projectcode.required && errors.push("Name is required.");
      this.fail_create === "code_fail" && errors.push("Code already exits");
      for (let i = 0; i < this.projectcode.length; i++) {
        if (this.projectcode[i] === " ")
          errors.push("Code must not have space");
      }
      !this.$v.projectcode.maxLength &&
        errors.push("Code must be at most 30 characters long");
      return errors;
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
  },
  methods: {
    create_project: function() {
      this.$v.$touch();
      if (this.$v.$pending || this.$v.$error) return null;
      else {
      let data = {
        project_code: this.projectcode.trim(),
        project_name: this.projectname.trim()
      };
      this.$store
        .dispatch("create_project_and_choose", data)
        .then(resp => {
          console.log(resp.data);
          if (resp.data.code !== 0) {
            this.fail_create = "code_fail";
          } else {
            this.alert = !this.alert;
            setTimeout(() => {
              location.reload();
            }, 1000);
          }
        })
        .catch(err => {
          console.log(err);
        });
      }
    },
    add_function: function() {
      this.credit = !this.credit;
      console.log("sssssssss", this.credit);
      let data = {
        function_id: 1,
        project_id: JSON.parse(localStorage.getItem("project_id"))
      };
      this.$store.dispatch("add_function_to_project", data).then(async resp => {
        console.log(resp.code);
        let data1 = {
          project_id: JSON.parse(localStorage.getItem("project_id"))
        };
        await this.$store
          .dispatch("get_all_function", data1)
          .then(resp1 => {
            localStorage.setItem(
              "all_function",
              JSON.stringify(resp1.data.data)
            );
            this.functions = JSON.parse(localStorage.getItem("all_function"));
          })
          .catch(err1 => {
            console.log(err1);
          });

        if (resp.code === 0) {
          location.reload()
        }
      });
    }
  },
  components: {
    Home,
    PersonManage,
    CreditCard
  }
};
</script>
