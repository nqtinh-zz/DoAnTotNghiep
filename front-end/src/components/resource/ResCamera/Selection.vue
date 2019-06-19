<template>
  <v-layout row justify-center>
    
      
      <v-card>
        <v-card-title>
          <v-layout row wrap>
            <v-flex xs12 sm12 lg12 xl12 md4 mt-2>
              <span style="margin-left: 20px; font-size: 20px">List Process Of Camera</span>
            </v-flex>
            <!-- <v-flex xs6 sm6 lg4 xl4 md4>
              <v-text-field
              style="margin-left: 20px"
              :label="$t('toolbar.search')"
              prepend-inner-icon="search"
              single-line
              hide-details
              v-model="search"
            ></v-text-field>
            <div></div>
            </v-flex> -->
          </v-layout>
         
        </v-card-title>

        <v-card-text class="pa-0">
          <v-container grid-list-md>
            
            <v-data-table :headers="headers" :items="list_process" class="elevation-1" :search="search">
              <template v-slot:items="props">
                <tr
                >
                  <td class="text-xs-left">{{ props.item.process_name }}</td>
                  <td class="text-xs-right" v-if="props.item.process_status === 0">Init</td>
                  <td class="text-xs-right" v-if="props.item.process_status === 1">Running</td>
                  <td class="text-xs-right" v-if="props.item.process_status === 2">Stopped</td>
                  <td class="text-xs-right" v-if="props.item.process_status === 3">Error</td>
                </tr>
                
              </template>
            </v-data-table>
          </v-container>
        </v-card-text>
        
      </v-card>
      
    
  </v-layout>
</template>
<script>
import { mapActions, mapMutations, mapState } from "vuex";
export default {
  data() {
    return {
      search: "",
      dialog2: true,
      headers: [
        {
          text: "Process Name",
          align: "left",
          sortable: false,
          value: "process_name"
        },
        
        { text: "Status", align: "right", value: "name", sortable: false }
      ],
      process_name: "",
      project_id: "",
      desserts: [],
      user_id: "",
      
      name: "",
      background: "none"
    };
  },
  computed: mapState({
    list_process: state => state.abc_process.list_process,
  }),
  created: function() {
    // var data = { project_id: JSON.parse(localStorage.getItem("project_id")) };
    // this.$store
    //   .dispatch("get_list_process", data)
    //   .then(resp4 => {
    //     console.log("get list process thanh cong", resp4);
    //   })
    //   .catch(err4 => {
    //     console.log(err4);
    //   });
  },
  methods: {
    
  }
};
</script>
