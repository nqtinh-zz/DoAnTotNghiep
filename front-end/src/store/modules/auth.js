import axios from 'axios'
import JwtDecode from 'jwt-decode'
import setAuthToken from '../../utils/setAuthToken'
import  router  from '../../router/index'
import HTTP_API from '../../api/config';
const state = {
  status: '',
  token: localStorage.getItem('token') || '',
  user: {}
}

const mutations = {
  auth_request (state) {
    state.status = 'loading'
  },
  auth_success_token (state, token) {
    state.status = 'success'
    state.token = token
  },
  auth_success_user (state, user) {
    state.status = 'success'
    state.user = user
  },
  auth_error (state) {
    state.status = 'error'
  },
  register (state) {
    state.status = 'register_success'
  },
  logout (state) {
    state.status = ''
    state.token = ''
    state.user = {}
  }
}

const actions = {
  register ({
    commit
  }, user) {
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/user/signup`,
        data: user,
        method: 'POST'
      })
        .then(resp => {
          if (resp.data.code !== -1) {
            commit('register')
          }
          resolve(resp)
        })
        .catch(err => {
          
          console.log(err)
        })
    })
  },
  login ({
    commit
  }, user) {
    return new Promise((resolve, reject) => {
      commit('auth_request')
      axios({
        url: `${HTTP_API}/api/user/login`,
        data: user,
        method: 'POST'
      })
        .then(resp => {
          const token = resp.data.data.token
          const user = JwtDecode(token)
          localStorage.setItem('token', token)
          localStorage.setItem('expiration_date', resp.data.data.expiration_date)
          setAuthToken(token)
          commit('auth_success_token', token)
          commit('auth_success_user', user)
          resolve(resp)
        })
        .catch(err => {
          
          commit('auth_error')
          localStorage.removeItem('token')
          reject(err)
        })
    })
  },
  logout ({
    commit
  }) {
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/user/logout`,
        method: 'GET'
      })
        .then(data => {
          commit('logout')
          localStorage.clear()
          setAuthToken()
          resolve()
        })
        .catch(err => {
          
          console.log(err)
        })
    })
  }
}

const getters = {
  isLoggedIn: state => !!state.token,
  authStatus: state => state.status
}
export default {
  state,
  getters,
  actions,
  mutations
}
