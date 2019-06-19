<template>
    <div>
        <v-toolbar :clipped-left="$vuetify.breakpoint.lgAndUp" color="blue darken-3" dark app fixed>
      <v-toolbar-title style="width: 300px" class="ml-0 pl-3">
        <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
        <router-link style="text-decoration: none;color:white" to="/">F.Cloud Console</router-link>
      </v-toolbar-title>&nbsp;&nbsp;&nbsp;&nbsp;
      <v-text-field
        flat
        solo-inverted
        hide-details
        prepend-inner-icon="search"
        :label="$t('toolbar.search')"
        class="hidden-sm-and-down"
      ></v-text-field>
      <v-spacer></v-spacer>
      <langx></langx>
      <router-link to="/signup">
        <v-btn color="primary" style="width:120px">{{$t(`toolbar.register`)}}</v-btn>
      </router-link>
      <router-link to="/signin">
        <v-btn color="primary" style="width:120px">{{$t(`toolbar.login`)}}</v-btn>
      </router-link>
    </v-toolbar>
    </div>
</template>
<script >
export default {
    
}
</script>
<style lang="scss" scoped>

.v-content__wrap {
  max-width: 120%;
}
</style>
