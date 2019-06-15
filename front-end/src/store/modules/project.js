import axios from 'axios'
import HTTP_API from '../../api/config';
const state = {
  status: '',
  project: localStorage.getItem('project') || ''
}

const mutations = {
  create_success_project (state, project) {
    state.status = 'create_success_project'
    state.project = project
  },
  get_success_project (state, project) {
    state.status = 'get_success_project'
    state.project = project
  },
  choose_success_project (state, project) {
    state.status = 'choose_success_project'
    state.project = project
  },
  delete_success_project (state) {
    state.status = 'delete_success_project'
  }
}

const actions = {
  get_all_project ({
    commit
  }, project) {
    console.log(project)
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/v/project/`,
        data: project,
        method: 'GET'
      })
        .then(resp => {
          commit('get_success_project', project)
          resolve(resp)
        })
        .catch(err => {
          console.log(err)
        })
    })
  },
  choose_project ({
    commit
  }, project) {
    return new Promise((resolve, reject) => {
      console.log(project)
      axios({
        url: `${HTTP_API}/api/v/project/`,
        params:{
          project_code:project.project_code
        },
        method: 'GET'
      })
        .then(resp => {
          localStorage.removeItem('project')
          localStorage.setItem('project', JSON.stringify(project))
          localStorage.setItem('secret_key',resp.data.data.secret_key)
          commit('choose_success_project', project)

          resolve(resp)
        })
        .catch(err => {
          console.log(err)
        })
    })
  },
  create_project ({
    commit
  }, project) {
    console.log(project)
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/v/project/`,
        data: project,
        method: 'POST'
      })
        .then(resp => {
          commit('create_success_project', project)
          resolve(resp)
        })
        .catch(err => {
          console.log(err)
        })
    })
  },
  create_project_and_choose ({
    commit
  }, project) {
    console.log(project)
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/v/project/`,
        data: project,
        method: 'POST'
      })
        .then(resp => {
          commit('create_success_project', project)
          axios({
            url: `${HTTP_API}/api/v/project/`,
            params: {
              project_code : project.project_code
            },
            method: 'GET'
          })
            .then(resp2 => {
              localStorage.removeItem('project')
              localStorage.setItem('project', JSON.stringify(project))
              localStorage.setItem('project_id', resp2.data.data.project_id)
              localStorage.setItem('secret_key',resp2.data.data.secret_key)
              commit('choose_success_project', project)
              // console.log(resp2)
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
  delete_project ({
    commit
  }, project) {
    console.log(project)
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/v/project/`,
        params: {
          project_code : project.project_code
        },
        method: 'DELETE'
      })
        .then(resp => {
          commit('delete_success_project')
          console.log('Da xoa thanh cong')
          resolve(resp)
        })
        .catch(err => {
          console.log(err)
        })
    })
  },
  add_function_to_project ({
    commit
  }, project) {
    console.log(project)
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/v/project/function/`,
        data: project,
        method: 'POST'
      })
        .then(resp => {
          resolve(resp.data)
        })
        .catch(err => {
          console.log(err)
        })
    })
  }

}

const getters = {
  projectStatus: state => state.status,
  project: state => !!state.project,
  nameProject: state => state.project
}
export default {
  state,
  getters,
  actions,
  mutations
}
