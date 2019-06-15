export default [
  {
    name: 'APP_LOGIN_SUCCESS',
    callback: function (e) {
      this.$router.push({ path: 'dashboard' })
    }
  },
  {
    name: 'APP_LOGOUT',
    callback: function (e) {
      this.snackbar = {
        show: true,
        color: 'green',
        text: 'Logout successfully.'
      }
      this.$router.replace({ path: '/signin' })
    }
  }
]
