<template>
  <div id="app">
    <v-app>
      <main>
        <v-container fluid fill-height class="loginOverlay">
          <v-layout align-center justify-center mt-5>
            <v-flex xs12 lg4 md5 sm7 elevation-1 mt-5>
              <v-toolbar class="pt-4 pb-2 blue darken-4">
                <v-toolbar-title class="white--text pb-2">
                  <h2 class="text-xs-center ml-4">F.Cloud Console</h2>
                  <div class="text-xs-center ml-4">{{$t(`signin.title`) }}</div>
                </v-toolbar-title>
              </v-toolbar>
              <v-card height="350">
                <v-card-text class="pt-4">
                  <div
                    v-if="register_success === 'register_success'"
                    style="color: green"
                  >{{$t(`signin.register_successfull`) }}</div>
                  <div>
                    <v-form v-model="valid" ref="form" @submit.prevent="login">
                      <v-text-field
                        :label="$t('signin.username')"
                        v-model="name"
                        :error-messages="nameErrors"
                        required
                        @input="$v.name.$touch()"
                        @blur="$v.name.$touch()"
                      ></v-text-field>&nbsp;
                      <v-text-field
                        :label="$t('signin.password')"
                        v-model="password"
                        min="8"
                        :append-icon="e1 ? 'visibility' : 'visibility_off'"
                        @click:append="e1 = !e1"
                        :type="e1 ? 'text' : 'password'"
                        :error-messages="passwordErrors"
                        required
                        @input="$v.password.$touch()"
                        @blur="$v.password.$touch()"
                      ></v-text-field>
                      <div
                        v-if=" fail_login === true"
                        style="color: red; "
                      >{{$t(`signin.signin_fail`) }} </div>
                      <v-layout justify-space-between mt-4>
                        <div style="margin-top:12px">
                          <a><b style="color: #1976d2 !important">{{$t(`signin.forgot_password`) }}</b></a>
                          &nbsp;&nbsp;&nbsp;
                          <router-link to="/signup">
                            <a><b style="color: #1976d2 !important">{{$t(`signin.create_account`) }}</b></a>
                          </router-link>
                        </div>

                        <v-btn
                          style="color:white; margin-left:4px;"
                          type="submit"
                          color="#287AE6"
                        >{{$t(`signin.login`) }}</v-btn>
                      </v-layout>
                    </v-form>
                  </div>
                </v-card-text>
              </v-card>
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
  minLength
} from 'vuelidate/lib/validators'
export default {
  mixins: [validationMixin],
  validations: {
    name: { required, minLength: minLength(5), maxLength: maxLength(30) },
    password: { required, minLength: minLength(8) }
  },
  data () {
    return {
      valid: false,
      e1: false,
      password: '',
      name: '',
      fail_login: false
    }
  },
  computed: {
    register_success () {
      return this.$store.getters.authStatus
    },
    nameErrors () {
      const errors = []
      if (!this.$v.name.$dirty) return errors
      !this.$v.name.maxLength &&
        errors.push(this.$t(`signin.nameErrors.most`))
      !this.$v.name.minLength &&
        errors.push(this.$t(`signin.nameErrors.least`))
      !this.$v.name.required && errors.push(this.$t(`signin.nameErrors.required`))
      return errors
    },
    passwordErrors () {
      const errors = []
      if (!this.$v.password.$dirty) return errors
      !this.$v.password.minLength &&
        errors.push(this.$t(`signin.passwordErrors.least`))
      !this.$v.password.required && errors.push(this.$t(`signin.passwordErrors.required`))
      return errors
    }
  },
  methods: {
    login () {
      this.$v.$touch()
      if (this.$v.$pending || this.$v.$error) return null
      else {
        this.$store
          .dispatch('login', {
            username: this.name.trim(),
            password: this.password
          })
          .then(response => {
            if (response.data.data.token != null) {
              this.$router.push('/')
            } else {
              this.$router.push('/signup')
            }
          })
          .catch(err => {
            this.fail_login = true
            console.log(err)
          })
      }
    }
  }
}
</script>

<style>
a {
  text-decoration: none;
}
/* .container {
    max-width: 100% !important;
} */
.container.fluid {
    max-width: 100% !important;
}
</style>
