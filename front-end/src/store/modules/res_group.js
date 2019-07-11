import axios from 'axios'
import HTTP_API from '../../api/config';
const state = {
  status: '',
  listGroup: [],
  choose_group: '',
  group: '',
  dialog2: false
}

const mutations = {
  choose_success_group(state, group) {
    state.status = 'choose_success_group'
    state.choose_group = group
  },
  add_success_group(state, group) {
    state.status = 'add_success_group'
    state.group = group
  },
  reset_success_group(state, group) {
    state.status = 'reset_success_group'
    state.group = group
  },
  get_all_people_group(state, group) {
    state.status = 'get_all_success_group'
    state.listGroup = group
  },
  del_group(state, group) {
    state.status = 'del_success_group'
    state.group = group
  },
  update_people_group(state, group) {
    state.status = 'update_people_group'
    state.group = group
  }
}

const actions = {
  
  test_formdata({
    commit
  }, group) {
    return new Promise((resolve, reject) => {
      axios({
          url: `${HTTP_API}/api/v/project/resources/test`,
          data: group,
          method: 'POST'
        })
        .then(async resp => {
          resolve(resp)
        })
        .catch(err => {
          console.log(err)
        })
    })
  },
  choose_group({
    commit
  }, group) {
    commit('choose_success_group', group)
  },
  reset_group({
    commit
  }, group) {
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/v/project/resources/people-group`,
        params: {
          project_id: group.project_id
        },
        method: 'GET'
      })
      .then(resp => {
        commit('rest_group', resp.data.data)
        resolve(resp)
      })
      .catch(err => {
        console.log(err)
      })
    })
  },
  add_group({
    commit
  }, group) {
    return new Promise((resolve, reject) => {
      axios({
          url: `${HTTP_API}/api/v/project/resources/people-group`,
          data: group,
          method: 'POST'
        })
        .then(async resp => {
          commit('add_success_group', group)
          await axios({
              url: `${HTTP_API}/api/v/project/resources/people-group`,
              params: {
                project_id: group.project_id
              },
              method: 'GET'
            })
            .then(resp2 => {
              commit('get_all_people_group', resp2.data.data)
              resolve(resp2)
            })
            .catch(err => {
              console.log(err)
            })
          resolve(resp)
        })
        .catch(err => {
          console.log(err)
        })
    })
  },
  get_all_people_group({
    commit
  }, group) {
    return new Promise((resolve, reject) => {
      axios({
          url: `${HTTP_API}/api/v/project/resources/people-group`,
          params: {
            project_id: group.project_id
          },
          method: 'GET'
        })
        .then(resp => {
          commit('get_all_people_group', resp.data.data)
          resolve(resp)
        })
        .catch(err => {
          console.log(err)
        })
    })
  },
  del_group({
    commit
  }, group) {
    return new Promise((resolve, reject) => {
      axios({
          url: `${HTTP_API}/api/v/project/resources/people-group`,
          params: {
            people_group_id: group.people_group_id
          },
          method: 'DELETE'
        })
        .then(async resp => {
          commit('del_group', group)
          await axios({
              url: `${HTTP_API}/api/v/project/resources/people-group`,
              params: {
                project_id: group.project_id
              },
              method: 'GET'
            })
            .then(resp2 => {
              commit('get_all_people_group', resp2.data.data)
              resolve(resp2)
            })
            .catch(err => {
              console.log(err)
            })
          resolve(resp)
        })
        .catch(err => {
          console.log(err)
        })
    })
  },
  update_people_group({
    commit
  }, group) {
    return new Promise((resolve, reject) => {
      axios({
          url: `${HTTP_API}/api/v/project/resources/people-group`,
          data: group,
          method: 'PUT'
        })
        .then(async resp => {
          commit('update_people_group', group)
          await axios({
              url: `${HTTP_API}/api/v/project/resources/people-group`,
              params: {
                project_id: group.project_id
              },
              method: 'GET'
            })
            .then(resp2 => {
              commit('get_all_people_group', resp2.data.data)
              resolve(resp2)
            })
            .catch(err => {
              console.log(err)
            })
          resolve(resp)
        })
        .catch(err => {
          console.log(err)
        })
    })
  }
}
const getters = {
  group: state => state.group
}
export default {
  state,
  getters,
  actions,
  mutations
}
