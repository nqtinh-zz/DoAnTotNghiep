<template>
  <div>
    <Home></Home>
    <v-container grid-list-xl>
      <v-layout row wrap justify-center>
        <!-- <v-flex xs12 sm12 md4 lg4 xl4>
        <div class="v-card v-sheet theme--light" style="height: 700px; ">
          <UserCard></UserCard>
        </div>
        </v-flex>-->
        <v-flex xs12 sm12 md5 lg5 xl5 mt-5>
          <div class="v-card v-sheet theme--light" style="height: 100%;">
            <v-card-text style="font-size: 16px">{{$t(`change_password.edit`) }}</v-card-text>
            
              <v-flex xs12 md12 ml-3 mr-3>
                <v-text-field
                  value
                  v-model="old_password"
                  :label="$t('change_password.password')"
                  :append-icon="show_old ? 'visibility' : 'visibility_off'"
                  :type="show_old ? 'text' : 'password'"
                  @click:append="show_old = !show_old"
                  :error-messages="old_passwordErrors"
                  required
                  @input="$v.old_password.$touch()"
                  @blur="$v.old_password.$touch()"
                ></v-text-field>
              </v-flex>
              <v-flex xs12 md12 ml-3 mr-3>
                <v-text-field
                  value
                  v-model="new_password"
                  :label="$t('change_password.new_password')"
                  :append-icon="show_new ? 'visibility' : 'visibility_off'"
                  :type="show_new ? 'text' : 'password'"
                  @click:append="show_new = !show_new"
                  :error-messages="new_passwordErrors"
                  required
                  @input="$v.new_password.$touch()"
                  @blur="$v.new_password.$touch()"
                ></v-text-field>
              </v-flex>
              
              <v-flex xs12 md12 ml-3 mr-3>
                <v-text-field
                  value
                  v-model="confirm_password"
                  :append-icon="show_confirm ? 'visibility' : 'visibility_off'"
                  :type="show_confirm ? 'text' : 'password'"
                  @click:append="show_confirm = !show_confirm"
                  :label="$t('change_password.confirm_password')"
                  :rules="[rules.confirm]"
                  :error-messages="confirm_passwordErrors"
                  required
                  @input="$v.confirm_password.$touch()"
                  @blur="$v.confirm_password.$touch()"
                ></v-text-field>
              </v-flex>
              <v-flex xs12 md12 ml-3 mr-3>
                <div v-if="check_change === true"><v-flex
                  style="margin-left: 15px; color: red"
                >{{$t(`change_password.wrong_password`) }}</v-flex></div>
              </v-flex>
              <v-flex xs12 md12 mb-3> 
                <v-layout justify-center>
                  <v-btn
                    color="blue-grey"
                    class="white--text"
                    @click="update_password"
                  >{{$t(`change_password.change_password`) }}</v-btn>
                </v-layout>
              </v-flex>
            
          </div>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>
<script>
import Home from "../../common/Home.vue";
import { validationMixin } from "vuelidate";
import { required, maxLength, minLength } from "vuelidate/lib/validators";
export default {
  mixins: [validationMixin],

  validations: {
    old_password: { required, minLength: minLength(8) },
    confirm_password: { required, minLength: minLength(8) },
    new_password: { required, minLength: minLength(8) }
  },
  data() {
    return {
      check_change: false,
      old_password: "",
      new_password: "",
      confirm_password: "",
      rules: {
        confirm: v => v === this.new_password || "Password confirm not match"
      },
      show_old: false,
      show_new: false,
      show_confirm: false
    };
  },
  computed: {
    old_passwordErrors() {
      const errors = [];
      if (!this.$v.old_password.$dirty) return errors;
      !this.$v.old_password.minLength && errors.push(this.$t(`change_password.passwordErrors.least`));
      !this.$v.old_password.required && errors.push(this.$t(`change_password.passwordErrors.required`));
      return errors;
    },
    new_passwordErrors() {
      const errors = [];
      if (!this.$v.new_password.$dirty) return errors;
      !this.$v.new_password.minLength && errors.push(this.$t(`change_password.new_passwordErrors.least`));
      !this.$v.new_password.required && errors.push(this.$t(`change_password.new_passwordErrors.required`));
      return errors;
    },
    confirm_passwordErrors() {
      const errors = [];
      if (!this.$v.confirm_password.$dirty) return errors;
      !this.$v.confirm_password.required &&
        errors.push(this.$t(`change_password.password_confirm_Errors.required`));
      return errors;
    }
  },
  methods: {
    update_password() {
      if (this.new_password === this.confirm_password) {
        this.$v.$touch();
        if (this.$v.$pending || this.$v.$error) return null;
        else {
          let data = {
            old_password: this.old_password,
            new_password: this.new_password
          };
          console.log("ssss", data);
          this.$store
            .dispatch("change_password", data)
            .then(resp => {
              if (resp.data.code === 0) {
                console.log(resp.data);
                this.$store.dispatch("logout").then(() => {
                  this.$router.push("/");
                });
              }
              else
              {
                this.check_change = true
              }
            })
            .catch(err => {
              console.log(err);
            });
        }
      } else {
        console.log("mat khau khong hop le");
      }
    }
  },
  components: {
    Home
  }
};
</script>
<style>
</style>
