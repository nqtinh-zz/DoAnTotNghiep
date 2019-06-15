<template>
  <v-container grid-list-xl>
    <v-layout wrap justify-space-between>
      <v-flex xs12 md5 mt-5>
        <v-layout justify-center>
          <v-flex
            v-if="this.check_avatar===false"
            xs12
            sm6
            md8
            align-center
            justify-center
            layout
            text-xs-center
          >
            <!-- <v-avatar :size="220" color="grey lighten-4">
              <img src="./avatar.jpg" class="uploading-image" alt="avatar">
            </v-avatar>-->
            <v-hover>
              <v-avatar
                style="position: relative;"
                :size="220"
                color="grey lighten-4"
                slot-scope="{ hover }"
              >
                <!-- <img :src="previewImage" class="uploading-image" alt="avatar"> -->
                <label v-if="hover&& previewImage!==null" style="position: absolute;opacity: 0.5;">
                  <div
                    style="position: absolute; margin-left:55px; margin-top:90px; opacity: 1 !important; color:white; font-size:20px"
                  >{{$t(`profile.change_avatar`) }}</div>
                  <img
                    style="width:220px;height:220px"
                    :src="previewImage"
                    class="uploading-image"
                    alt="avatar"
                  >

                  <input
                    type="file"
                    id="id_folder"
                    accept="image/jpeg"
                    @change="uploadImage"
                    style="width: 0px"
                  >
                </label>
                <label
                  v-else-if="hover&& previewImage===null"
                  style="position: absolute;opacity: 0.5;"
                >
                  <div
                    style="position: absolute; margin-left:55px; margin-top:90px; opacity: 1 !important; color:white; font-size:20px"
                  >{{$t(`profile.change_avatar`) }}</div>
                  <img
                    style="width:220px;height:220px"
                    src="./avatar.jpg"
                    class="uploading-image"
                    alt="avatar"
                  >

                  <input
                    type="file"
                    id="id_folder"
                    accept="image/jpeg"
                    @change="uploadImage"
                    style="width: 0px"
                  >
                </label>
                <label v-else-if="previewImage===null" style="position: absolute;">
                  <img
                    style="width:220px;height:220px"
                    src="./avatar.jpg"
                    class="uploading-image"
                    alt="avatar"
                  >

                  <!-- <input
                type="file"
                id="id_folder"
                accept="image/jpeg"
                @change="uploadImage"
                style="width: 0px"
                  >-->
                </label>
                <label v-else-if="previewImage!==null" style="position: absolute;">
                  <img
                    style="width:220px;height:220px"
                    :src="previewImage"
                    class="uploading-image"
                    alt="avatar"
                  >

                  <!-- <input
                type="file"
                id="id_folder"
                accept="image/jpeg"
                @change="uploadImage"
                style="width: 0px"
                  >-->
                </label>
              </v-avatar>
            </v-hover>
          </v-flex>
          <v-flex v-else xs12 sm6 md8 align-center justify-center layout text-xs-center>
            <v-hover>
              <v-avatar
                style="position: relative;"
                :size="220"
                color="grey lighten-4"
                slot-scope="{ hover }"
              >
                <!-- <img :src="previewImage" class="uploading-image" alt="avatar"> -->
                <label v-if="hover" style="position: absolute;opacity: 0.5;">
                  <div
                    style="position: absolute; margin-left:55px; margin-top:90px; opacity: 1 !important; color:white; font-size:20px"
                  >{{$t(`profile.change_avatar`) }}</div>
                  <img
                    style="width:220px;height:220px"
                    :src="previewImage"
                    class="uploading-image"
                    alt="avatar"
                  >

                  <input
                    type="file"
                    id="id_folder"
                    accept="image/jpeg"
                    @change="uploadImage"
                    style="width: 0px"
                  >
                </label>
                <label v-else style="position: absolute;">
                  <img
                    style="width:220px;height:220px"
                    :src="previewImage"
                    class="uploading-image"
                    alt="avatar"
                  >

                  <!-- <input
                type="file"
                id="id_folder"
                accept="image/jpeg"
                @change="uploadImage"
                style="width: 0px"
                  >-->
                </label>
              </v-avatar>
            </v-hover>
          </v-flex>
        </v-layout>
        <!-- <v-layout justify-center mt-3>
          <v-flex xs12 sm6 md8 align-center justify-center layout text-xs-center>
            <v-btn @click="update_avatar" color="blue-grey" class="white--text">
              Update avatar
            </v-btn>
          </v-flex>
        </v-layout>-->
      </v-flex>
      <!-- change infor -->
      <v-flex xs12 md7>
        <v-flex xs12 md12>
          <v-layout wrap justify-space-between>
            <v-flex xs12 md6>
              <v-text-field v-model="username" :label="$t('profile.username')"  readonly></v-text-field>
            </v-flex>
            <v-flex xs12 md6>
              <v-text-field v-model="email" :label="$t('profile.email')" readonly></v-text-field>
            </v-flex>
            <v-flex xs12 md12>
              <v-text-field v-model="company" :label="$t('profile.company')"></v-text-field>
            </v-flex>
          </v-layout>
        </v-flex>
        <v-flex xs12 md12>
          <v-layout wrap justify-space-between>
            <v-flex xs12 md6>
              <v-text-field v-model="first_name" :label="$t('profile.first_name')"></v-text-field>
            </v-flex>
            <v-flex xs12 md6>
              <v-text-field v-model="last_name" :label="$t('profile.last_name')"></v-text-field>
            </v-flex>
          </v-layout>
        </v-flex>
        <v-flex xs12 md12>
          <v-layout wrap justify-space-between>
            <v-flex xs12 md12>
              <v-text-field v-model="address" :label="$t('profile.address')"></v-text-field>
            </v-flex>
          </v-layout>
        </v-flex>
        <v-layout wrap justify-center>
          <v-flex xs12 md3>
            <v-btn @click="update_profile" color="blue-grey" class="white--text">
              {{$t(`profile.update`) }}
              <!-- <v-icon right dark>cloud_upload</v-icon> -->
            </v-btn>
          </v-flex>
        </v-layout>
      </v-flex>
    </v-layout>

    <br>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      email: '',
      first_name: "",
      last_name: "",
      address: "",
      company: "",
      hover_avatar: false,
      check_avatar: false,
      previewImage: null,
      formData: new FormData()
    };
  },
  computed: {},
  created() {
    this.$store
      .dispatch("get_avatar")
      .then(resp => {
        // this.desserts = [...resp.data.data];
        // console.log("get avatar ", resp.data);
        if (resp.data.code === 0) {
          this.check_avatar = true;
          let res = resp.data.data;
          let res2 = res.replace("b'", "");
          let res3 = res2.replace("'", "");
          this.previewImage = res3;
          //console.log(this.previewImage)
          this.previewImage = res3;
          // console.log(this.previewImage);
        }
      })
      .catch(err => {
        console.log(err);
      });
      this.$store
      .dispatch("get_profile")
      .then(resp => {
        // this.desserts = [...resp.data.data];
        console.log("get profile ", resp.data);
        if (resp.data.code === 0) {
          this.first_name = resp.data.data.first_name
          this.last_name = resp.data.data.last_name
          this.username = resp.data.data.username
          this.email = resp.data.data.email
          this.company= resp.data.data.company
          this.address = resp.data.data.address
          
        }
      })
      .catch(err => {
        console.log(err);
      });
  },
  methods: {
    uploadImage(e) {
      const image = e.target.files[0];
      const reader = new FileReader();
      reader.readAsDataURL(image);
      reader.onload = e => {
        this.previewImage = e.target.result;
        console.log(this.previewImage);
      };
    },
    update_profile() {
      if (this.previewImage !== null) {
        let res = this.previewImage;
        var arr = res.split(","),
          mime = arr[0].match(/:(.*?);/)[1],
          bstr = atob(arr[1]),
          n = bstr.length,
          u8arr = new Uint8Array(n);
        while (n--) {
          u8arr[n] = bstr.charCodeAt(n);
        }
        var file = new File([u8arr], "avatar", { type: mime });
        this.formData.append("avatar", file);
      }
      for (var pair of this.formData.entries()) {
        console.log(pair[0]);
        console.log(pair[1]);
      }
      this.formData.append("first_name", this.first_name);
      this.formData.append("last_name", this.last_name);
      this.formData.append("company", this.company);
      this.formData.append("address", this.address);
      this.$store
        .dispatch("set_avatar", this.formData)
        .then(resp => {
          // this.desserts = [...resp.data.data];
          this.formData = new FormData();
          console.log("set avatar ", resp.data);
          location.reload();
        })
        .catch(err => {
          console.log(err);
        });
    }
  }
};
</script>
