import axios from 'axios'
import router from '../../../router/index'
import HTTP_API from '../../../api/config';
const state = {
  status: '',
  group: [],
  listCamera: [],
  group_of_camera: [],
  data_edit_person: '',
  // images_import: [],

}
const mutations = {
  add_camera_success(state, listCamera_data) {
    state.status = 'add_camera_success'
    state.listCamera = listCamera_data
  },
  // get_all_group(state, group_data) {
  //   state.status = "get_all_group_success"
  //   state.group = group_data
  // },
  get_all_camera_success(state, listCamera_data) {
    state.status = "get_all_camera_success"
    state.listCamera = listCamera_data
  },
  delete_success_camera(state) {
    state.status = "delete_success_camera"
  },
  group_of_camera(state, group_of_camera_data) {
    state.status = "get_group_of_camera_success"
    state.group_of_camera = group_of_camera_data
  },
  camera_group_list_camera(state, group) {
    state.status = 'camera_group_list_camera'
    state.group = group
  }
  // check_list_camera(state, import_img) {
  //   state.status = "check_list_camera_success"
  //   state.images_import = import_img
  //   console.log('ttttttttttttt', import_img)
  // }
}
const actions = {
  stop_camera({
    commit
  }, data) {
    // console.log('data khi gui',person)
    return new Promise((resolve, reject) => {
      //cập nhât danh sach person mới
      axios({
        url: `${HTTP_API}/api/v/project/resources/turn-off-camera`,
        params: {
          camera_id: data
        },
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
  start_camera({
    commit
  }, data) {
    // console.log('data khi gui',person)
    return new Promise((resolve, reject) => {
      //cập nhât danh sach person mới
      axios({
        url: `${HTTP_API}/api/v/project/resources/turn-on-camera`,
        params: {
          camera_id: data
        },
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


  // },
  // view_camera_url({
  //   commit
  // }, data_leader) {
  //   // console.log('data khi gui',person)
  //   return new Promise((resolve, reject) => {
  //     //cập nhât danh sach person mới
  //     // console.log("cho m ne 1")
  //     axios({
  //       url: `${HTTP_API}/api/v/project/resources/live-stream`,
  //       params: {
  //         stream_url: data_leader
  //       },
  //       method: 'GET',
  //       adapter: require('axios/lib/adapters/http'),
  //       responseType: 'stream', 
  //     })
  //       .then(resp => {
  //         console.log("âlksdflasfjalsfsalfdkl")
  //         console.log("cho may ne`: ",resp)
  //         // resolve(resp)
  //       })
  //       .catch(err => {
          
  //         console.log(err)
  //       })
    
  //   })
  // },
  reload_list_camera({
    commit
  }, camera) {
    // console.log('data khi gui',person)
    return new Promise((resolve, reject) => {
      //cập nhât danh sach person mới
      axios({
        url: `${HTTP_API}/api/v/project/resources/camera`,
        params: {
          project_id: camera.project_id
        },
        method: 'GET'
      })
        .then(resp2 => {
          var desserts = [...resp2.data.data]
          commit('get_all_camera_success', desserts)
          resolve(resp2)
        })
        .catch(err => {
          
          console.log(err)
        })
    })
  },
  check_one_status({
    commit
  }, data_check) {
    console.log('data check one camera',data_check)
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/v/project/resources/check-camera`,
        
        params: {
          camera_id: data_check
        },
        
        method: 'GET'
      })
        .then(resp => {
          // console.log("check one status camera", resp)
          // for(let i =0 ;i< state.listCamera.length;i++)
          // {
          //   state.listCamera[i].status = resp.data.data[i].status
          // }
          // console.log('ngiu7en quyanh tinh',state.listCamera)
          // console.log('data check tra ve', resp.data)
          resolve(resp)
        })
        .catch(err => {
          
          console.log(err)
        })
    })
  },
  check_status({
    commit
  }, data_check) {
    console.log('data check',data_check)
    return new Promise((resolve, reject) => {
      //cập nhât danh sach person mới
      axios({
        url: `${HTTP_API}/api/v/project/resources/check-camera-url`,
        
        params: {
          project_id: data_check.project_id
        },
        
        method: 'GET'
      })
        .then(resp => {
          
          for(let i =0 ;i< state.listCamera.length;i++)
          {
            state.listCamera[i].status = resp.data.data[i].status
          }
          console.log('ngiu7en quyanh tinh',state.listCamera)
          console.log('data check tra ve', resp.data)
          resolve(resp)
        })
        .catch(err => {
          
          console.log(err)
        })
    })
  },
  add_camera({
    commit
  }, camera) {
    // console.log('data khi gui',person)
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/v/project/resources/camera`,
        data: camera,
        method: 'POST'
      })
        .then(async resp => {
          //cập nhât danh sach person mới
          await axios({
            url: `${HTTP_API}/api/v/project/resources/camera`,
            params: {
              project_id: camera.project_id
            },
            method: 'GET'
          })
            .then(resp2 => {
              var desserts = [...resp2.data.data]
              commit('add_camera_success', desserts)
              resolve(resp2)
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
  // get_all_group({
  //   commit
  // }, data) {
  //   return new Promise((resolve, reject) => {
  //     axios({
  //       url: `${HTTP_API}/api/v/project/resources/people-group`,
  //       params: {
  //         project_id: data.project_id
  //       },
  //       method: 'GET'
  //     })
  //       .then(resp => {
  //         var listGroup = []
  //         var temp = resp.data.data
  //         for (let i = 0; i < temp.length; i++) {
  //           listGroup.push(temp[i].people_group_code)
  //         }
  //         commit('get_all_group', listGroup)
  //         // resolve(resp)
  //       })
  //       .catch(err => {
  //         console.log(err)
  //       })
  //   })
  // },
  get_group_of_camera({
    commit
  }, data) {
    return new Promise((resolve, reject) => {
      // console.log("projec id la: ", data.project_id_id)
      axios({
        url: `${HTTP_API}/api/v/project/resources/camera-group`,
        params: {
          project_id: data.project_id_id
        },
        method: 'GET'
      })
        .then(resp => {
          var listGroup = []
          var temp = resp.data.data
          for (let i = 0; i < temp.length; i++) {
            listGroup.push(temp[i].camera_group_name)
          }
          var list_delete = [...data.group]
          for (let i = 0; i < list_delete.length; i++) {
            var temp = list_delete[i].camera_group_name
            var index_delete = listGroup.indexOf(temp)
            listGroup.splice(index_delete, 1)
          }
          // var index_delete = listGroup.indexOf(temp)
          // listGroup.splice(index_delete,1)

          commit('group_of_camera', listGroup)
          resolve(resp)
        })
        .catch(err => {
          
          console.log(err)
        })
    })
  },
  get_all_camera({
    commit
  }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/v/project/resources/camera`,
        params: {
          project_id: data.project_id
        },
        method: 'GET'
      })
        .then(resp => {
          var desserts = [...resp.data.data];
          commit('get_all_camera_success', desserts)
          console.log('get all camera',desserts)
          resolve(resp)
        })
        .catch(err => {
          
          console.log(err)
        })
    })
  },
  delete_camera({
    commit
  }, camera) {
    console.log("peson id:", camera)
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/v/project/resources/camera`,
        data: camera,
        method: 'DELETE'
      })
        .then(resp => {
          commit('delete_success_camera')
          // console.log('Da xoa thanh cong')
          resolve(resp)
        })
        .catch(err => {
          
          console.log(err)
        })
    })
  },

  //chua co backend
  edit_camera({
    commit
  }, camera) {
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/v/project/resources/camera`,
        data: camera,
        method: 'PUT'
      })
        .then(resp => {
          
          axios({
            url: `${HTTP_API}/api/v/project/resources/camera`,
            params: {
              project_id: camera.project_id
            },
            method: 'GET'
          })
            .then(resp2 => {
              var desserts = [...resp2.data.data];
              commit('get_all_camera_success', desserts)

              resolve(resp2)
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
  add_camera_to_group({
    commit
  }, data_camera) {
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/v/project/resources/add-camera-to-group`,
        data: data_camera,
        method: 'POST'
      })
        .then(resp => {
          console.log(resp)
          //lay danh sach people lai sau khi them group vao
          axios({
            url: `${HTTP_API}/api/v/project/resources/camera`,
            params: {
              project_id: data_camera.project_id
            },
            method: 'GET'
          })
            .then(resp2 => {
              var desserts = [...resp2.data.data];
              commit('get_all_camera_success', desserts)

              resolve(resp2)
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
  delete_one_group_camera({
    commit
  }, data_group) {
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/v/project/resources/delete-camera-from-group`,
        data: data_group,
        method: 'POST'
      })
        .then(resp => {

          //lay danh sach people lai sau khi them group vao
          axios({
            url: `${HTTP_API}/api/v/project/resources/camera`,
            params: {
              project_id: data_group.project_id
            },
            method: 'GET'
          })
            .then(resp2 => {
              var desserts = [...resp2.data.data];
              commit('get_all_camera_success', desserts)

              resolve(resp2)
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
  camera_group_list_camera({
    commit
  }, data_group) {
    return new Promise((resolve, reject) => {
      axios({
        url: `${HTTP_API}/api/v/project/resources/camera-group-list-camera`,
        data: data_group,
        params: {
          group_id: data_group.group_id
        },
        method: 'GET'
      })
        .then(resp => {
          var desserts = [...resp.data.data];
          commit('get_all_camera_success', desserts)
          resolve(resp)
          console.log(resp)
        })
        .catch(err => {
          
          console.log(err)
        })
    })
  },
  // import_person({
  //   commit
  // }, data_import) {
  //   return new Promise((resolve, reject) => {
  //     axios({
  //       url: `${HTTP_API}/api/v/project/resources/import-person`,
  //       data: data_import,
  //       method: 'POST'
  //     })
  //       .then(resp => {
  //          //lay danh sach people lai sau khi them group vao
  //          //console.log("DA chay thanh cong vao day roi")
  //          axios({
  //           url: `${HTTP_API}/api/v/project/resources/person`,
  //           params: {
  //             project_id: data_import[0].project_id
  //           },
  //           method: 'GET'
  //         })
  //           .then(resp2 => {
  //             var desserts = [...resp2.data.data];
  //             commit('get_all_people_success', desserts)

  //             // resolve(resp)
  //           })
  //           .catch(err2 => {
  //             console.log(err2)
  //           })
  //         resolve(resp)
          
  //       })
  //       .catch(err => {
  //         console.log(err)
  //       })
  //   })
  // }
  
}
const getters = {
  // PersonStatus: state => state.status,
  // ListGroup: state => state.group,
  ListCamera: state => state.listCamera,
  GroupOfCamera: state => state.group_of_camera
}
export default {
  state,
  getters,
  actions,
  mutations
}
