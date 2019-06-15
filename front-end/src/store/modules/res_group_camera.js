import axios from 'axios'
import HTTP_API from '../../api/config';
const state = {
  status: '',
  list_group_camera: [],
  choose_group: '',
  group: ''
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
  get_all_camera_group(state, group) {
    state.status = 'get_all_success_group'
    state.list_group_camera = group
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
  add_group_camera({
    commit
  }, group) {
    return new Promise((resolve, reject) => {
        console.log(group)
      axios({
          url: `${HTTP_API}/api/v/project/resources/camera-group`,
          data: group,
          method: 'POST'
        })
        .then(async resp => {
          commit('add_success_group', group)
          console.log(resp.data)
          await axios({
              url: `${HTTP_API}/api/v/project/resources/camera-group`,
              params: {
                project_id: group.project_id
              },
              method: 'GET'
            })
            .then(resp => {
              commit('get_all_camera_group', resp.data.data)
              resolve(resp)
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
  get_all_camera_group({
    commit
  }, group) {
    return new Promise((resolve, reject) => {
      axios({
          url: `${HTTP_API}/api/v/project/resources/camera-group`,
          params: {
            project_id: group.project_id
          },
          method: 'GET'
        })
        .then(resp => {
          commit('get_all_camera_group', resp.data.data)
          resolve(resp)
        })
        .catch(err => {
          console.log(err)
        })
    })
  },
  del_group_camera({
    commit
  }, group) {
    return new Promise((resolve, reject) => {
      axios({
          url: `${HTTP_API}/api/v/project/resources/camera-group`,
          params: {
            camera_group_id: group.camera_group_id
          },
          method: 'DELETE'
        })
        .then(async resp => {
          commit('del_group', group)
          await axios({
              url: `${HTTP_API}/api/v/project/resources/camera-group`,
              params: {
                project_id: group.project_id
              },
              method: 'GET'
            })
            .then(resp => {
              commit('get_all_camera_group', resp.data.data)
              resolve(resp)
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
  update_people_group_camera({
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
            .then(resp => {
              commit('get_all_people_group', resp.data.data)
              resolve(resp)
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
