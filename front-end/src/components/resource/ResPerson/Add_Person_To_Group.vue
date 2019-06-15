<template>
  <v-dialog v-model="dialog_add_person_to_group" persistent max-width="500px">
    <template v-slot:activator="{ on }">
      <v-btn fab small color="primary" style="width: 28px ; height: 28px" v-on="on"  @click="getAllGroup">
        <v-icon>add</v-icon>
      </v-btn>
    </template>
    <v-card>
      <v-card-title>
        <v-layout row wrap>
          <v-flex xs12 sm12 mt-2>
            <span style="margin-left: 10px; font-size: 20px">
              <b>{{$t(`res_person.add_person_to_group`) }}</b>
            </span>
          </v-flex>
        </v-layout>
      </v-card-title>

      <v-card-text class="pa-0">
        <v-container grid-list-md>
          <!-- <div style="font-size: 16px">{{ $t(`project.all_project`) }}</div> -->
          <v-form ref="form" @submit.prevent="add_person_to_group">
            <v-layout wrap row>
              <v-flex xs3 sm3 pt-4 style="font-size: 17px">
                <b>{{$t(`res_person.group`) }}</b>
              </v-flex>
              <v-flex xs8 sm8>
                <v-select
                  v-bind:items="ListGroup"
                  v-model="a1"
                  :label="$t('res_person.choose_group')"
                  autocomplete
                  multiple
                  chips    
                ></v-select>
              </v-flex>
            </v-layout>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="blue darken-1"
                flat
                @click="dialog_add_person_to_group = false"
                style="font-size: 16px"
              >{{$t(`res_person.cancel`) }}</v-btn>
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
import { required, maxLength } from "vuelidate/lib/validators";
export default {
  mixins: [validationMixin],
  validations: {
    group: { required}
  },
  data() {
    return {
      dialog_add_person_to_group: false,
      person_code: "",
      a1: [],
      valid: false
    };
  },
  components: {
    VueUploadMultipleImage
  },
  methods: {
      getAllGroup() {
      var data = {project_id :JSON.parse(localStorage.getItem("project_id")) }
      this.$store
      .dispatch("get_all_group", data)
          .then(resp => {
            console.log("get all group thanh cong: ", resp);
          })
          .catch(err => {
            console.log(err);
          });
    },
    add_person_to_group() {
      // console.log(this.person_code), console.log(this.images);

    },
  },
  computed: {
    
    ListGroup () {
      return this.$store.getters.ListGroup
    }

  }
};
</script>
