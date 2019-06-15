<template>
  <div>
    <v-flex>
      <v-card>
        <v-img
          src="https://picsum.photos/350/165?random"
          height="auto"
          contain
          class="grey darken-4"
        ></v-img>
      </v-card>
    </v-flex>

    <v-layout wrap justify-center="">
      <v-flex xs12 md4>
        <v-btn color="blue-grey" class="white--text">
          Change Image
          <!-- <v-icon right dark>cloud_upload</v-icon> -->
        </v-btn>
      </v-flex>
    </v-layout>
  </div>
</template>
<script>
export default {
  data() {
    return {
      //   details: [
      //     {
      //       title: "12",
      //       subTitle: "Files"
      //     },
      //     {
      //       title: "2GB",
      //       subTitle: "Used"
      //     },
      //     {
      //       title: "24,6$",
      //       subTitle: "Spent"
      //     }
      //   ]
    };
  },
  methods: {
    getClasses(index) {
      var remainder = index % 3;
      if (remainder === 0) {
        return "col-lg-3 offset-lg-1";
      } else if (remainder === 2) {
        return "col-lg-4";
      } else {
        return "col-lg-3";
      }
    }
  }
};
</script>
<style>
</style>
