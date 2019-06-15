import axios from 'axios'
import HTTP_API from '../../../api/config';
const state = {
  status: ''
}

const mutations = {
  get_success_avatar (state, data) {
    state.status = 'get_success_avatar'
    state.data = data
  },
  set_success_avatar (state, data) {
    state.status = 'set_success_avatar'
    state.data = data
  }
}

const actions = {
  change_password({
    commit
  },data_change){
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/user/change-password`,
        data: data_change,
        method: 'POST'
      })
        .then(resp => {
          
          resolve(resp)
        })
        .catch(err => {
          console.log(err)
        })
    })
  },
  get_profile ({
    commit
  }) {
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/user/profile`,
        method: 'GET'
      })
        .then(resp => {
          
          resolve(resp)
        })
        .catch(err => {
          console.log(err)
        })
    })
},
  get_avatar ({
    commit
  }) {
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/user/get-avatar`,
        method: 'GET'
      })
        .then(resp => {
          commit('get_success_avatar')
          resolve(resp)
        })
        .catch(err => {
          console.log(err)
        })
    })
},
    set_avatar ({
        commit
        },data) {
        return new Promise((resolve, reject) => {
            axios({
            url: `${HTTP_API}/api/user/profile`,
            method: 'PUT',
            data: data,
            })
            .then(resp => {
                commit('set_success_avatar')
                resolve(resp)
            })
            .catch(err => {
                console.log(err)
            })
        })
    }
  
}
const getters = {
  functionStatus: state => state.status
}
export default {
  state,
  getters,
  actions,
  mutations
}
