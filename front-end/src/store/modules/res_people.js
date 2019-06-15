import axios from 'axios'
import HTTP_API from '../../api/config';
const state = {
  status: '',
  group: [],
  listPeople: [],
  group_of_person: [],
  data_edit_person: '',

}
const mutations = {
  add_person_success(state, listPeople_data) {
    state.status = 'add_person_success'
    state.listPeople = listPeople_data
  },
  get_all_group(state, group_data) {
    state.status = "get_all_group_success"
    state.group = group_data
  },
  get_all_people_success(state, listPeople_data) {
    state.status = "get_all_people_success"
    state.listPeople = listPeople_data
  },
  delete_success_person(state) {
    state.status = "delete_success_person"
  },
  group_of_person(state, group_of_person_data) {
    state.status = "get_group_of_person_success"
    state.group_of_person = group_of_person_data
  },
  get_data_edit_person(state) {
    state.status = "get data edit success"
  }

}
const actions = {
  reload_list_person({
    commit
  }, person) {
    // console.log('data khi gui',person)
    return new Promise((resolve, reject) => {
      //cập nhât danh sach person mới
      axios({
        url: `${HTTP_API}/api/v/project/resources/person`,
        params: {
          project_id: person.project_id
        },
        method: 'GET'
      })
        .then(resp2 => {
          var desserts = [...resp2.data.data]
          commit('get_all_people_success', desserts)
          // resolve(resp)
        })
        .catch(err => {
          console.log(err)
        })
    })
  },
  add_person({
    commit
  }, person) {
    // console.log('data khi gui',person)
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/v/project/resources/person`,
        data: person,
        method: 'POST'
      })
        .then(async resp => {
          //cập nhât danh sach person mới
          await axios({
            url: `${HTTP_API}/api/v/project/resources/person`,
            params: {
              project_id: JSON.parse(localStorage.getItem("project_id"))
            },
            method: 'GET'
          })
            .then(resp2 => {
              var desserts = [...resp2.data.data]
              commit('add_person_success', desserts)
              // resolve(resp)
            })
            .catch(err => {
              console.log(err)
            })

          //console.log("sau khi gui axios: ", resp)
          resolve(resp)
        })
        .catch(err => {
          console.log(err)
        })
    })
  },
  get_all_group({
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
            listGroup.push(temp[i].people_group_code)
          }
          commit('get_all_group', listGroup)
          // resolve(resp)
        })
        .catch(err => {
          console.log(err)
        })
    })
  },
  get_group_of_person({
    commit
  }, data) {
    return new Promise((resolve, reject) => {
      // console.log("projec id la: ", data.project_id_id)
      axios({
        url: `${HTTP_API}/api/v/project/resources/people-group`,
        params: {
          project_id: data.project_id_id
        },
        method: 'GET'
      })
        .then(resp => {
          var listGroup = []
          var temp = resp.data.data
          for (let i = 0; i < temp.length; i++) {
            listGroup.push(temp[i].people_group_code)
          }
          var list_delete = [...data.group]
          for (let i = 0; i < list_delete.length; i++) {
            var temp = list_delete[i].people_group_code
            var index_delete = listGroup.indexOf(temp)
            listGroup.splice(index_delete, 1)
          }
          // var index_delete = listGroup.indexOf(temp)
          // listGroup.splice(index_delete,1)

          commit('group_of_person', listGroup)
          // resolve(resp)
        })
        .catch(err => {
          console.log(err)
        })
    })
  },
  get_all_people({
    commit
  }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/v/project/resources/person`,
        params: {
          project_id: data.project_id
        },
        method: 'GET'
      })
        .then(resp => {
          var desserts = [...resp.data.data];
          commit('get_all_people_success', desserts)

          // resolve(resp)
        })
        .catch(err => {
          console.log(err)
        })
    })
  },
  delete_person({
    commit
  }, person) {
    console.log("peson id:", person)
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/v/project/resources/person`,
        data: person,
        method: 'DELETE'
      })
        .then(resp => {
          commit('delete_success_person')
          // console.log('Da xoa thanh cong')
          resolve(resp)
        })
        .catch(err => {
          console.log(err)
        })
    })
  },

  //chua co backend
  edit_person({
    commit
  }, person) {
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/v/project/resources/person`,
        data: person,
        method: 'PUT'
      })
        .then(resp => {
          axios({
            url: `${HTTP_API}/api/v/project/resources/person`,
            params: {
              project_id: JSON.parse(localStorage.getItem("project_id"))
            },
            method: 'GET'
          })
            .then(resp2 => {
              var desserts = [...resp2.data.data];
              commit('get_all_people_success', desserts)

              // resolve(resp)
            })
            .catch(err2 => {
              console.log(err2)
            })
            resolve(resp)
        })
        .catch(err => {
          console.log(err)
        })
    })
  },
  add_person_to_group({
    commit
  }, data_person) {
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/v/project/resources/add-person-to-group`,
        data: data_person,
        method: 'POST'
      })
        .then(resp => {

          //lay danh sach people lai sau khi them group vao
          axios({
            url: `${HTTP_API}/api/v/project/resources/person`,
            params: {
              project_id: data_person.project_id
            },
            method: 'GET'
          })
            .then(resp2 => {
              var desserts = [...resp2.data.data];
              commit('get_all_people_success', desserts)

              // resolve(resp)
            })
            .catch(err2 => {
              console.log(err2)
            })
          resolve(resp)
          // console.log(resp)
        })
        .catch(err => {
          console.log(err)
        })
    })
  },
  delete_one_group({
    commit
  }, data_group) {
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/v/project/resources/delete-person-from-group`,
        data: data_group,
        method: 'POST'
      })
        .then(resp => {

          //lay danh sach people lai sau khi them group vao
          axios({
            url: `${HTTP_API}/api/v/project/resources/person`,
            params: {
              project_id: data_group.project_id
            },
            method: 'GET'
          })
            .then(resp2 => {
              var desserts = [...resp2.data.data];
              commit('get_all_people_success', desserts)

              // resolve(resp)
            })
            .catch(err2 => {
              console.log(err2)
            })
          // resolve(resp)
          console.log(resp)
        })
        .catch(err => {
          console.log(err)
        })
    })
  },
  get_data_edit_person({
    commit
  }, data_person) {
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/v/project/resources/get-image-person`,
        data: data_person,
        method: 'POST'
      })
        .then(resp => {
          commit("get_data_edit_person")
          resolve(resp)
          console.log(resp)
        })
        .catch(err => {
          console.log(err)
        })
    })
  },
  import_person({
    commit
  }, data_import) {
    return new Promise((resolve, reject) => {
      console.log("data gui xuong import: ",data_import)
      axios({
        url: `${HTTP_API}/api/v/project/resources/import-person`,
        data: data_import,
        method: 'POST'
      })
        .then(resp => {
           //lay danh sach people lai sau khi them group vao
           console.log("DA chay thanh cong vao day roi")
           axios({
            url: `${HTTP_API}/api/v/project/resources/person`,
            params: {
              project_id: JSON.parse(localStorage.getItem("project_id"))
            },
            method: 'GET'
          })
            .then(resp2 => {
              var desserts = [...resp2.data.data];
              commit('get_all_people_success', desserts)

              // resolve(resp)
            })
            .catch(err2 => {
              console.log(err2)
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
  PersonStatus: state => state.status,
  ListGroup: state => state.group,
  ListPeople: state => state.listPeople,
  GroupOfPerson: state => state.group_of_person
}
export default {
  state,
  getters,
  actions,
  mutations
}
