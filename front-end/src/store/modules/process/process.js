import axios from 'axios'
import router from '../../../router/index'
import HTTP_API from '../../../api/config';
const state = {
  status: '',
  config: {},
  group: [],
  list_process: [],
}
const mutations = {
  get_all_group(state, group_data) {
    state.status = "get_all_group_success"
    state.group = group_data
  },
  get_list_process_success(state, list_process_data) {
    state.status = "get_list_process_success"
    state.list_process = list_process_data
  }
}
const actions = {

  process_get_all_group({
    commit
  }, data) {
    return new Promise((resolve, reject) => {
      axios({
          url: `${HTTP_API}/api/v/project/resources/people-group`,
          params: {
            project_id: data.project_id
          },
          method: 'GET'
        })
        .then(resp => {
          var listGroup = []
          var temp = resp.data.data
          for (let i = 0; i < temp.length; i++) {
            let data_temp = {
              people_group_id: temp[i].people_group_id,
              people_group_code: temp[i].people_group_code
            }
            listGroup.push(data_temp)
          }
          commit('get_all_group', listGroup)
          resolve(resp)
        })
        .catch(err => {
          
          console.log(err)
        })
    })
  },
  get_config({
    commit
  }, data) {
    return new Promise((resolve, reject) => {
      axios({
          url: `${HTTP_API}/api/v/project/channel/get-default-config`,

          method: 'GET'
        })
        .then(resp => {
          console.log("data config ne': ", resp.data.data)
          resolve(resp.data.data)
        })
        .catch(err => {
          
          console.log(err)
        })
    })
  },
  get_process({
    commit
  }, data) {
    return new Promise((resolve, reject) => {
      axios({
          url: `http://127.0.0.1:8000/api/v/project/channel/get-process`,
          params: {
            process_id: data.process_id
          },
          method: 'GET'
        })
        .then(resp => {
          console.log("get process ne': ", resp.data.data)
          resolve(resp)
        })
        .catch(err => {
          
          console.log(err)
        })
    })
  },
  add_process({
    commit
  }, data_add_process) {
    return new Promise((resolve, reject) => {
      axios({
          url: `${HTTP_API}/api/v/project/channel/create-process`,
          data: data_add_process,
          method: 'POST'
        })
        .then(resp => {
          console.log("data add process': ", resp)
          axios({
            url: `${HTTP_API}/api/v/project/channel/get-process-list`,
            params: {
              project_id : JSON.parse(localStorage.getItem("project_id"))
            },
            method: 'GET'
          })
          .then(resp2 => {
            console.log("data get list process: ", resp2.data)
            commit("get_list_process_success", resp2.data.data)
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
  update_process({
    commit
  }, data_add_process) {
    return new Promise((resolve, reject) => {
      axios({
          url: `${HTTP_API}/api/v/project/channel/update-process`,
          data: data_add_process,
          method: 'PUT'
        })
        .then(resp => {
          console.log("data update process': ", resp)
          axios({
            url: `${HTTP_API}/api/v/project/channel/get-process-list`,
            params: {
              project_id : JSON.parse(localStorage.getItem("project_id"))
            },
            method: 'GET'
          })
          .then(resp2 => {
            console.log("data get list process: ", resp2.data)
            commit("get_list_process_success", resp2.data.data)
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
  get_list_process({
    commit
  }, data) {
    return new Promise((resolve, reject) => {
      axios({
          url: `${HTTP_API}/api/v/project/channel/get-process-list`,
          params: {
            project_id : JSON.parse(localStorage.getItem("project_id"))
          },
          method: 'GET'
        })
        .then(resp => {
          console.log("data get list process: ", resp.data)
          commit("get_list_process_success", resp.data.data)
          resolve(resp)
        })
        .catch(err => {
          
          console.log(err)
        })
    })
  },
  get_process_of_camera({
    commit
  }, data) {
    return new Promise((resolve, reject) => {
      axios({
          url: `${HTTP_API}/api/v/project/channel/get-process-list`,
          params: {
            project_id : JSON.parse(localStorage.getItem("project_id"))
          },
          method: 'GET'
        })
        .then(resp => {
          console.log("data get list process: ", resp.data)
          let arr_list_process = []
          for(let i=0;i<resp.data.data.length;i++)
          {
            if(resp.data.data[i].camera_id_id === data)
            {
              arr_list_process.push(resp.data.data[i])
            }
          }
          console.log("mang process of camera", arr_list_process)
          commit("get_list_process_success", arr_list_process)
          resolve(resp)
        })
        .catch(err => {
          
          console.log(err)
        })
    })
  },
  delete_process({
    commit
  }, data_add_process) {
    return new Promise((resolve, reject) => {
      axios({
          url: `${HTTP_API}/api/v/project/channel/delete-process`,
          params: {
            process_id: data_add_process.process_id
          },
          method: 'DELETE'
        })
        .then(resp => {
          console.log("data add process': ", resp)
          resolve(resp)
        })
        .catch(err => {
          
          console.log(err)
        })
    })
  },
  start_process({
    commit
  }, data_start_process) {
    return new Promise((resolve, reject) => {
      axios({
          url: `${HTTP_API}/api/v/project/channel/start-process`,
          params: {
            process_id: data_start_process.process_id
          },
          method: 'PUT'
        })
        .then(resp => {
          console.log("data start process': ", resp)
          for(let i=0;i<state.list_process.length; i++)
          {
            if(data_start_process.process_id===state.list_process[i].process_id)
            {
              state.list_process[i].process_status=resp.data.data.process_status
            }
          }
          resolve(resp)
        })
        .catch(err => {
          
          console.log(err)
        })
    })
  },
  stop_process({
    commit
  }, data_stop_process) {
    return new Promise((resolve, reject) => {
      axios({
          url: `${HTTP_API}/api/v/project/channel/stop-process`,
          params: {
            process_id: data_stop_process.process_id
          },
          method: 'PUT'
        })
        .then(resp => {
          console.log("data stop process': ", resp)
          for(let i=0;i<state.list_process.length; i++)
          {
            if(data_stop_process.process_id===state.list_process[i].process_id)
            {
              state.list_process[i].process_status=resp.data.data.process_status
            }
          }
          resolve(resp)
        })
        .catch(err => {
          
          console.log(err)
        })
    })
  },
}
const getters = {
  Process_ListGroup: state => state.group,
}
export default {
  state,
  getters,
  actions,
  mutations
}
