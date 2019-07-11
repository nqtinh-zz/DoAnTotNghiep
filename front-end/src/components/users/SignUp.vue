<template>
  <div id="app">
    <v-app>
      <main>
        <v-container fluid fill-height class="loginOverlay">
          <v-layout flex align-center justify-center mt-5>
            <v-flex xs12 sm6 elevation-6>
              <v-layout row wrap>
                <v-flex xs12 sm12 lg12 xl12 md12>
                  <v-toolbar class="pt-4 blue darken-4" style="padding:10px">
                    <v-toolbar-title class="white--text">
                      <h2>F.Cloud Console</h2>
                      <div>{{$t(`signup.title`) }}</div>
                    </v-toolbar-title>
                  </v-toolbar>
                </v-flex>
              </v-layout>
              <div>
                <div style="float: left;margin-left: 35px;margin-top: 25px;">
                  <v-form ref="form" @submit.prevent="register">
                    <v-layout row wrap>
                      <v-flex xs6 sm6 lg4 xl4 md4>
                        <v-text-field
                          v-model="firstname"
                          :label="$t('signup.first_name')"
                          :error-messages="firstnameErrors"
                          required
                          @input="$v.firstname.$touch()"
                          @blur="$v.firstname.$touch()"
                        ></v-text-field>
                      </v-flex>
                      <v-flex xs6 sm6 lg1 xl1 md1></v-flex>
                      <v-flex xs6 sm6 lg4 xl4 md4>
                        <v-text-field
                          v-model="lastname"
                          :label="$t('signup.last_name')"
                          :error-messages="lastnameErrors"
                          required
                          @input="$v.lastname.$touch()"
                          @blur="$v.lastname.$touch()"
                        ></v-text-field>
                      </v-flex>
                    </v-layout>
                    <v-flex xs6 sm6 lg9 xl9 md9>
                      <v-text-field
                        xs12
                        md6
                        ml-6
                        :label="$t('signup.username')"
                        v-model="name"
                        :error-messages="nameErrors"
                        required
                        @input="$v.name.$touch()"
                        @blur="$v.name.$touch()"
                      ></v-text-field>
                    </v-flex>
                    <v-flex xs6 md9>
                      <v-text-field
                        :label="$t('signup.email')"
                        v-model="email"
                        :error-messages="emailErrors"
                        required
                        @input="$v.email.$touch()"
                        @blur="$v.email.$touch()"
                      ></v-text-field>
                    </v-flex>

                    <v-layout row wrap>
                      <v-flex xs6 md4>
                        <v-text-field
                          v-model="password"
                          ref="password"
                          :append-icon="show1 ? 'visibility' : 'visibility_off'"
                          :rules="[rules.required, rules.min]"
                          :type="show1 ? 'text' : 'password'"
                          name="input-10-1"
                          :label="$t('signup.password')"
                          hint="At least 8 characters"
                          @click:append="show1 = !show1"
                          :error-messages="passwordErrors"
                          required
                          @input="$v.password.$touch()"
                          @blur="$v.password.$touch()"
                        ></v-text-field>
                      </v-flex>
                      <v-flex xs6 md1></v-flex>
                      <v-flex xs6 md4>
                        <v-text-field
                          v-model="password_confirm"
                          :append-icon="show2 ? 'visibility' : 'visibility_off'"
                          :rules="[rules.required, rules.confirm]"
                          :type="show2 ? 'text' : 'password'"
                          name="input-10-2"
                          :label="$t('signup.confirm_password')"
                          hint="At least 8 characters"
                          value="wqfasds"
                          class="input-group--focused"
                          @click:append="show2 = !show2"
                          :error-messages="password_confirmErrors"
                          required
                          @input="$v.password_confirm.$touch()"
                          @blur="$v.password_confirm.$touch()"
                        ></v-text-field>
                      </v-flex>
                    </v-layout>
                    <v-layout row wrap>
                      <v-flex xs9 sm9 lg9 xl9 md9>
                        <v-checkbox
                          v-model="checkbox"
                          :error-messages="checkboxErrors"
                          required
                          @change="$v.checkbox.$touch()"
                          @blur="$v.checkbox.$touch()"
                        >
                          <template v-slot:label>
                            <div>{{$t(`signup.accept`) }}
                              <v-tooltip bottom>
                                <template v-slot:activator="{ on }">
                                  <a
                                    style="text-decoration: none;"
                                    target="_blank"
                                    href="#"
                                    @click.stop
                                    v-on="on"
                                  >{{$t(`signup.term_condition`) }}</a>
                                </template>Opens in new window
                              </v-tooltip>&nbsp;
                            </div>
                          </template>
                        </v-checkbox>
                      </v-flex>
                    </v-layout>
                    <v-layout row wrap>
                      <v-flex xs6 sm3 lg3 xl3 md3>
                        <div style="margin-top:13px; margin-bottom:30px">
                          <router-link to="/signin" style="text-decoration: none;margin-left:5px;">
                            <a style="font-size:17px">
                              <b>{{$t(`signup.login`) }}</b>
                            </a>
                          </router-link>
                        </div>
                      </v-flex>
                      <v-flex xs6 sm3 lg3 xl3 md3></v-flex>
                      <v-flex xs6 sm3 lg3 xl3 md3>
                        <v-btn
                          style="color:white; margin-left:4px;"
                          type="submit"
                          color="#287AE6"
                        >{{$t(`signup.register`) }}</v-btn>
                      </v-flex>
                    </v-layout>
                  </v-form>
                </div>
                <div
                  style="float: left ;margin-top: 110px"
                >
                  <img
                    src="https://fit.uit.edu.vn/attachments/article/4644/FUJINET1.png"
                    alt
                    width="244"                    
                  >
                </div>
              </div>
            </v-flex>
          </v-layout>
        </v-container>
      </main>
    </v-app>
  </div>
</template>

<script>
import { validationMixin } from 'vuelidate'
import {
  required,
  maxLength,
  email,
  minLength
} from 'vuelidate/lib/validators'
export default {
  mixins: [validationMixin],

  validations: {
    name: { required, minLength: minLength(5), maxLength: maxLength(30) },
    firstname: { required, minLength: minLength(2), maxLength: maxLength(30) },
    lastname: { required, minLength: minLength(2), maxLength: maxLength(30) },
    password: { required, minLength: minLength(8) },
    password_confirm: { required, minLength: minLength(8) },
    email: { required, email },
    checkbox: {
      checked (val) {
        return val
      }
    }
  },
  data () {
    return {
      checkbox: false,
      show1: false,
      show2: false,
      firstname: '',
      lastname: '',
      name: '',
      email: '',
      password: '',
      password_confirm: '',
      fail_register: '',
      rules: {
        required: value => !!value || 'Required.',
        min: v => v.length >= 8 || 'Min 8 characters',
        max: v => v.length <= 30 || 'Max 30 characters',
        emailMatch: () => 'The email and password you entered don`t match',
        confirm: v => v === this.password || 'Password confirm not match'
      },
      // rules_name: {
      //   min: v => v.length > 0 || "Min 1 characters",
      //   max: v => v.length <= 30 || "Max 30 character"
      // },
      emailRules: [
        v => !!v || 'E-mail is required',
        v =>
          /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(v) ||
          'E-mail must be valid'
      ]
    }
  },
  computed: {
    checkboxErrors () {
      const errors = []
      if (!this.$v.checkbox.$dirty) return errors
      !this.$v.checkbox.checked && errors.push(this.$t(`signup.agree`))
      return errors
    },
    nameErrors () {
      const errors = []
      if (!this.$v.name.$dirty) return errors
      !this.$v.name.maxLength &&
        errors.push(this.$t(`signup.nameErrors.most`))
      for (let i = 0; i < this.name.length; i++) {
        if (this.name[i] === ' ') errors.push(this.$t(`signup.nameErrors.check_space`))
      }
      !this.$v.name.minLength &&
        errors.push(this.$t(`signup.nameErrors.least`))
      !this.$v.name.required && errors.push(this.$t(`signup.nameErrors.required`))
      if (this.fail_register === 'username') {
        errors.push(this.$t(`signup.nameErrors.username_exist`))
      }
      return errors
    },
    firstnameErrors () {
      const errors = []
      if (!this.$v.firstname.$dirty) return errors
      !this.$v.firstname.maxLength &&
        errors.push(this.$t(`signup.nameErrors.first_name_most`))
      !this.$v.firstname.minLength &&
        errors.push(this.$t(`signup.nameErrors.first_name_least`))
      !this.$v.firstname.required && errors.push(this.$t(`signup.nameErrors.first_name_required`))
      return errors
    },
    lastnameErrors () {
      const errors = []
      if (!this.$v.lastname.$dirty) return errors
      !this.$v.lastname.maxLength &&
        errors.push(this.$t(`signup.nameErrors.last_name_most`))
      !this.$v.lastname.minLength &&
        errors.push(this.$t(`signup.nameErrors.last_name_least`))
      !this.$v.lastname.required && errors.push(this.$t(`signup.nameErrors.last_name_required`))
      return errors
    },
    password_confirmErrors () {
      const errors = []
      if (!this.$v.password_confirm.$dirty) return errors
      !this.$v.password_confirm.required &&
        errors.push(this.$t(`signup.password_confirm_Errors.required`))
      return errors
    },
    passwordErrors () {
      const errors = []
      if (!this.$v.password.$dirty) return errors
      !this.$v.password.minLength &&
        errors.push(this.$t(`signup.passwordErrors.least`))
      !this.$v.password.required && errors.push(this.$t(`signup.passwordErrors.required`))
      return errors
    },
    emailErrors () {
      const errors = []
      if (!this.$v.email.$dirty) return errors
      !this.$v.email.email && errors.push(this.$t(`signup.emailErrors.format`))
      !this.$v.email.required && errors.push(this.$t(`signup.emailErrors.required`))
      this.fail_register === 'email' && errors.push(this.$t(`signup.emailErrors.exist`))
      return errors
    }
  },
  methods: {
    register: function () {
      if (this.password === this.password_confirm) {
        this.$v.$touch()
        if (this.$v.$pending || this.$v.$error) return null
        else {
          let data = {
            first_name: this.firstname.trim(),
            last_name: this.lastname.trim(),
            username: this.name.trim(),
            email: this.email.trim(),
            password: this.password,
            password_confirm: this.password_confirm
          }
          console.log("nguyen tien trien")
          this.$store
            .dispatch('register', data)
            .then(resp => {
              console.log('data',resp.data)
              if (resp.data.code === 0) {
                this.$router.push('/signin')
              } else {
                if (resp.data.message === 'Email exists') {
                  this.$router.push('/signup')
                  this.fail_register = 'email'
                } else if (resp.data.message === 'Username exists!') {
                  this.$router.push('/signup')
                  this.fail_register = 'username'
                }
              }
            })
            .catch(err => {
              console.log(err)
            })
        }
      } else {
        console.log('password error')
      }
    }
  }
}
</script>
<style>
/* .container {
    max-width: 100% !important;
} */
.container.fluid {
    max-width: 100% !important;
}
</style>
