import axios from 'axios'
import HTTP_API from '../../api/config';
const state = {
    status: '',
}
const mutations = {
    add_camera_success(state) {
        state.status = 'add_person_success'
    }

}
const actions = {
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
            .then( resp => {
              //cập nhât danh sach person mới
            //   await axios({
            //     url: `${HTTP_API}/api/v/project/resources/person`,
            //     params: {
            //       project_id: person.project_id
            //     },
            //     method: 'GET'
            //   })
            //     .then(resp2 => {
            //       var desserts = [...resp2.data.data]
            //       commit('add_person_success', desserts)
            //       // resolve(resp)
            //     })
            //     .catch(err => {
            //       console.log(err)
            //     })
    
              //console.log("sau khi gui axios: ", resp)
              commit('add_camera_success')
              resolve(resp)
            })
            .catch(err => {
              console.log(err)
            })
        })
      },
}
const getters = {

}
export default {
    state,
    getters,
    actions,
    mutations
}
