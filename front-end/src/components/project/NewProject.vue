<template>
  <div>
    <Home></Home>
    <v-alert :value="alert" type="success" transition="scale-transition">{{$t(`function.add_p_success`) }}</v-alert>
    <v-toolbar>
      <v-toolbar-title class="ml-0 pl-4">{{$t(`function.new_project`) }}</v-toolbar-title>
    </v-toolbar>
    <div style="padding-top: 5px; padding-left: 50px">
      <v-form v-model="valid" ref="form" @submit.prevent="create_project">
        <v-flex xs12 sm6 md3>
          <v-text-field
            :label="$t('function.project_code')"
            v-model="projectcode"
            :error-messages="codeErrors"
            required
            @input="$v.projectcode.$touch()"
            @blur="$v.projectcode.$touch()"
          ></v-text-field>
        </v-flex>
        <v-flex xs12 sm6 md3>
          <v-text-field
            :label="$t('function.project_name')"
            v-model="projectname"
            :error-messages="nameErrors"
            required
            @input="$v.projectname.$touch()"
            @blur="$v.projectname.$touch()"
          ></v-text-field>
        </v-flex>
        <v-btn style="color:white; margin-left:4px;" type="submit" color="#287AE6">{{$t(`function.btn_add`) }}</v-btn>
        <router-link style="text-decoration: none;color:white" to="/">
          <v-btn>{{$t(`function.cancel`) }}</v-btn>
        </router-link>
      </v-form>
    </div>
  </div>
</template>

<script>
import Home from '../common/Home.vue'
import { validationMixin } from 'vuelidate'
import { required, maxLength } from 'vuelidate/lib/validators'
export default {
  name: 'NewProject',
  mixins: [validationMixin],
  validations: {
    projectname: { required , maxLength: maxLength(30)},
    projectcode: { required, maxLength: maxLength(30) }
  },
  data () {
    return {
      alert: false,
      valid: false,
      projectcode: '',
      projectname: '',
      fail_create: ''
    }
  },
  computed: {
    nameErrors () {
      const errors = []
      if (!this.$v.projectname.$dirty) return errors
      !this.$v.projectname.required && errors.push(this.$t(`function.name_requi`))
      !this.$v.projectname.maxLength &&
        errors.push(this.$t(`function.name_30ch`))
      return errors
    },
    codeErrors () {
      const errors = []
      if (!this.$v.projectcode.$dirty) return errors
      !this.$v.projectcode.required && errors.push(this.$t(`function.code_requi`))
      this.fail_create === 'code_fail' && errors.push(this.$t(`function.code_exist`))
      for (let i = 0; i < this.projectcode.length; i++) {
        if (this.projectcode[i] === ' ') errors.push(this.$t(`function.name_space`))
      }
      !this.$v.projectcode.maxLength &&
        errors.push(this.$t(`function.code_30ch`))
      return errors
    }
  },
  methods: {
    create_project: function () {
       this.$v.$touch();
      if (this.$v.$pending || this.$v.$error) return null;
      else {
      let data = {
        project_code: this.projectcode.trim(),
        project_name: this.projectname.trim()
      }
      this.$store
        .dispatch('create_project', data)
        .then(resp => {
          if (resp.data.code !== 0) {
            this.fail_create = 'code_fail'
          } else {
            this.alert = !this.alert
            setTimeout(() => {
              this.$router.push('/')
            }, 1000)
          }
        })
        .catch(err => {
          console.log(err)
        })
      }
    }
  },
  components: {
    Home
  }
}
</script>
