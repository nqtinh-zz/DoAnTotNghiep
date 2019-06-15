<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog2" max-width="700px">
      <template v-slot:activator="{ on }">
        <v-btn
          v-if="name !== ''"
          style="text-transform: none !important; width:auto;margin-left: 0px; margin-right:100px"
          color="#1565C0"
          dark
          v-on="on"
          @click="select"
        >{{name}}<v-icon>keyboard_arrow_down</v-icon></v-btn>
        <v-btn
          v-else
          style="text-transform: none !important; width:auto;margin-right:100px"
          color="#1565C0"
          dark
          v-on="on"
          @click="select"
        >{{$t(`toolbar.select_project`) }}<v-icon>keyboard_arrow_down</v-icon></v-btn>
      </template>
      <v-card>
        <v-card-title>
          <v-layout row wrap>
            <v-flex xs6 sm6 lg4 xl4 md4 mt-2>
              <span style="margin-left: 20px; font-size: 20px">{{ $t(`toolbar.select_project`) }}</span>
            </v-flex>
            <v-flex xs6 sm6 lg4 xl4 md4>
              <router-link style="text-decoration: none;" to="/new-project">
                <v-btn
                  color="#1565C0"
                  style="margin-left: 300px ; font-size: 15px"
                  dark
                  flat
                  @click="dialog2 = false"
                >{{ $t(`project.new_project`) }}</v-btn>
              </router-link>
            </v-flex>
          </v-layout>
          <v-flex xs12 sm6 md6 style="margin-left: 20px">
            <v-text-field
              :label="$t('toolbar.search')"
              prepend-inner-icon="search"
              single-line
              hide-details
              v-model="search"
            ></v-text-field>
          </v-flex>
        </v-card-title>

        <v-card-text class="pa-0">
          <v-container grid-list-md>
            <div style="font-size: 16px">{{ $t(`project.all_project`) }}</div>
            <v-data-table :headers="headers" :items="desserts" class="elevation-1" :search="search">
              <template v-slot:items="props">
                <tr
                  v-if="props.item.project_code !== project_code"
                  @click="check_open(props.item.project_code,props.item.project_name )"
                >
                  <td class="text-xs-left">{{ props.item.project_name }}</td>
                  <td class="text-xs-right">{{ props.item.project_code }}</td>
                  <td class="text-xs-right">
                    <!-- <v-icon small class="mr-2" >edit</v-icon> -->
                    <v-icon small @click="deleteItem(props.item)">delete</v-icon>
                  </td>
                </tr>
                <tr
                  v-else
                  style="background: #EEEEEE; "
                  @click="check_open(props.item.project_code,props.item.project_name )"
                >
                  <td class="text-xs-left">{{ props.item.project_name }}</td>
                  <td class="text-xs-right">{{ props.item.project_code }}</td>
                  <td class="text-xs-right">
                    <!-- <v-icon small class="mr-2" >edit</v-icon> -->
                    <v-icon small @click="deleteItem(props.item)">delete</v-icon>
                  </td>
                </tr>
              </template>
            </v-data-table>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click="dialog2 = false">{{$t(`function.cancel`) }}</v-btn>
          <v-btn color="blue darken-1" flat @click="open">{{$t(`function.open`) }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</template>
<script>
export default {
  data() {
    return {
      search: "",
      dialog2: false,
      headers: [
        {
          text: "Name project",
          align: "left",
          sortable: false,
          value: "project_name"
        },
        { text: "Project code", align: "right", value: "project_code" },
        { text: "Actions", align: "right", value: "name", sortable: false }
      ],
      project_name: "",
      project_id: "",
      desserts: [],
      user_id: "",
      project_code: "",
      name: "",
      background: "none"
    };
  },
  created: function() {
    if (localStorage.getItem("project") != null) {
      this.name = JSON.parse(localStorage.getItem("project")).project_name;
    }
  },
  methods: {
    select: function() {
      this.$store
        .dispatch("get_all_project")
        .then(resp => {
          this.desserts = resp.data.data;
          // console.log("sai roi kia Tinh' : ", resp.data.data)
        })
        .catch(err => {
          console.log(err);
        });
    },
    check_open: function(code, name) {
      if (this.background === "none") {
        this.background = "red";
      } else this.background = "none";
      console.log("check open");
      this.project_code = code;
      this.project_name = name;
    },
    open: function() {
      this.select_name = true;
      let data = {
        project_code: this.project_code,
        project_name: this.project_name
      };
      this.$store
        .dispatch("choose_project", data)
        .then(async resp => {
          localStorage.setItem("project_id", resp.data.data.project_id);
          this.project_id = JSON.parse(localStorage.getItem("project_id"));
          let datax = {
            project_id: this.project_id
          };
          await this.$store
            .dispatch("get_all_function", datax)
            .then(resp => {
              localStorage.setItem(
                "all_function",
                JSON.stringify(resp.data.data)
              );
              this.functions = JSON.parse(localStorage.getItem("all_function"));
            })
            .catch(err => {
              console.log(err);
            });
          location.reload();
        })
        .catch(err => {
          console.log(err);
        });
    },
    deleteItem: function(item) {
      const index = this.desserts.indexOf(item);
      confirm(this.$t(`function.are_you_sure`)) &&
        this.desserts.splice(index, 1) &&
        this.$store.dispatch("delete_project", item).then(resp => {
          console.log(resp);
          if (
            item.project_code ===
            JSON.parse(localStorage.getItem("project")).project_code
          ) {
            localStorage.removeItem("project"),
              localStorage.removeItem("project_id");
            localStorage.removeItem("all_function");
            localStorage.removeItem("secret_key");
          }
          location.reload();
        });
    }
  }
};
</script>
