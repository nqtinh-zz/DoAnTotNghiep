import axios from 'axios'
import HTTP_API from '../../api/config';
const state = {
  status: ''
}

const mutations = {
  get_success_function (state, data) {
    state.status = 'get_success_function'
    state.data = data
  }
}

const actions = {
  get_all_function ({
    commit
  }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/v/project/function/`,
        params:{
          project_id :data.project_id
        },
        method: 'GET'
      })
        .then(resp => {
          commit('get_success_function', data)
          resolve(resp)
        })
        .catch(err => {
          console.log(err)
        })
    })
  }
}
const getters = {
  functionStatuss: state => state.status
}
export default {
  state,
  getters,
  actions,
  mutations
}
